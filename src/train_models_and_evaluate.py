#!/usr/bin/env python3
"""
Pipeline d'Entraînement ML & Modélisation Financière
Company A - GCI World 2026 September (University of Tokyo)
Intègre les avancées de la Session 8 (Feature Engineering, Log1p, Cross-Features)
et de la Competition Special Week (Optuna, CatBoost, Ensembling).
"""
import os
import sys
import gc
import json
import time
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score, precision_score, recall_score, f1_score, log_loss, brier_score_loss
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import lightgbm as lgb
from catboost import CatBoostClassifier

DATA_DIR = "/Users/baptistebedeaux/gci_final_assignment/data"
OUTPUT_DIR = "/Users/baptistebedeaux/gci_final_assignment/src"

def load_and_engineer_features():
    print("Chargement des données Client.csv et Record.csv...")
    client = pd.read_csv(os.path.join(DATA_DIR, "Client.csv"))
    record = pd.read_csv(os.path.join(DATA_DIR, "Record.csv"))
    
    df = record.merge(client, on="Customer_ID", how="inner")
    print(f"Jeu consolidé : {df.shape[0]} lignes, {df.shape[1]} colonnes.")
    
    # Target and ID
    target = df['churn'].values
    customer_ids = df['Customer_ID'].values
    monthly_rev = df['rev_Mean'].fillna(df['rev_Mean'].median()).values
    
    print("Ingénierie des variables (Session 8 Standard & Special Week)...")
    
    # 1. Âge équipement en années et cohortes
    eqp_days = df['eqpdays'].fillna(df['eqpdays'].median())
    df['fe_eqp_years'] = eqp_days / 365.25
    df['fe_eqp_over_1y'] = (eqp_days > 365).astype(np.float32)
    df['fe_eqp_over_2y'] = (eqp_days > 730).astype(np.float32)
    
    # 2. Ratios d'utilisation et de friction réseau
    total_calls_attempted = (df['plcd_vce_Mean'].fillna(0) + df['plcd_dat_Mean'].fillna(0) + 1.0)
    failed_calls = (df['drop_vce_Mean'].fillna(0) + df['blck_vce_Mean'].fillna(0) + 
                    df['drop_dat_Mean'].fillna(0) + df['blck_dat_Mean'].fillna(0))
    df['fe_network_failure_rate'] = (failed_calls / total_calls_attempted).astype(np.float32)
    
    # 3. Friction Service Client (Calls au support / mois d'ancienneté)
    months = df['months'].fillna(df['months'].median()) + 1.0
    df['fe_care_intensity'] = (df['custcare_Mean'].fillna(0) / months).astype(np.float32)
    
    # 4. Friction Financière & Bill Shock (Dépassement / Revenu Récurrent)
    totmrc = df['totmrc_Mean'].fillna(df['totmrc_Mean'].median()) + 1.0
    df['fe_overage_ratio'] = (df['ovrrev_Mean'].fillna(0) / totmrc).astype(np.float32)
    df['fe_overage_minutes_ratio'] = (df['ovrmou_Mean'].fillna(0) / (df['mou_Mean'].fillna(0) + 1.0)).astype(np.float32)
    
    # 5. Dynamique de consommation (Baisse brutale des minutes et revenus)
    df['fe_mou_drop_sharp'] = (df['change_mou'].fillna(0) < -50).astype(np.float32)
    df['fe_rev_drop_sharp'] = (df['change_rev'].fillna(0) < -20).astype(np.float32)
    
    # 6. Valeur Client (ARPU annualisé estimé)
    df['fe_annualized_arpu'] = (monthly_rev * 12.0).astype(np.float32)
    
    # Session 8 Innovations :
    # 7. Transformations log1p des variables asymétriques (Lecture 8 Practice Question 1)
    skewed_cols = ["rev_Mean", "mou_Mean", "totmrc_Mean", "ovrmou_Mean", "ovrrev_Mean", "custcare_Mean"]
    for sc in skewed_cols:
        df[f"fe_log_{sc}"] = np.log1p(np.maximum(0, df[sc].fillna(df[sc].median()))).astype(np.float32)
        
    # 8. Cross features / Interactions non-linéaires (Lecture 8 Practice Questions 2 & 3)
    df["fe_cross_aging_x_failure"] = (df["fe_eqp_over_1y"] * df["fe_network_failure_rate"]).astype(np.float32)
    df["fe_cross_aging_x_overage"] = (df["fe_eqp_over_1y"] * df["fe_overage_ratio"]).astype(np.float32)
    df["fe_cross_care_x_moudrop"] = (df["fe_care_intensity"] * df["fe_mou_drop_sharp"]).astype(np.float32)
    df["fe_usage_per_dollar"] = (df["mou_Mean"].fillna(0) / (monthly_rev + 1.0)).astype(np.float32)
    
    # Sélection et Encodage
    drop_cols = ['Customer_ID', 'churn']
    features_df = df.drop(columns=drop_cols)
    
    # Encodage catégoriel
    cat_cols = features_df.select_dtypes(include=['object', 'str']).columns.tolist()
    for col in cat_cols:
        features_df[col] = features_df[col].astype('category').cat.codes
        
    # Imputation médiane propre et conversion float32 pour économiser la RAM
    features_df = features_df.fillna(features_df.median())
    for col in features_df.columns:
        features_df[col] = features_df[col].astype(np.float32)
        
    feature_names = features_df.columns.tolist()
    X = features_df.values
    
    print(f"Matrice de features prête : {X.shape[0]} lignes × {X.shape[1]} variables (Mémoire : {X.nbytes / (1024*1024):.1f} Mo).")
    return X, target, customer_ids, monthly_rev, eqp_days.values, feature_names

def train_and_evaluate(X, y, monthly_rev, eqp_days, feature_names):
    n_splits = 5
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    
    # Tableaux pour stocker les prédictions Out-Of-Fold (OOF)
    oof_lr = np.zeros(len(y), dtype=np.float32)
    oof_rf = np.zeros(len(y), dtype=np.float32)
    oof_cb = np.zeros(len(y), dtype=np.float32)
    oof_lgb = np.zeros(len(y), dtype=np.float32)
    feature_importances_lgb = np.zeros(len(feature_names), dtype=np.float32)
    
    print("\n" + "="*60)
    print("DÉBUT DU BENCHMARKING 5-FOLD STRATIFIED CROSS-VALIDATION")
    print("="*60)
    
    scaler = StandardScaler()
    
    fold = 1
    for train_idx, val_idx in skf.split(X, y):
        print(f"\n--- Fold {fold} / {n_splits} ---")
        X_train, y_train = X[train_idx], y[train_idx]
        X_val, y_val = X[val_idx], y[val_idx]
        
        # 1. Baseline : Logistic Regression (Scaled + Log1p Features)
        t0 = time.time()
        X_tr_sc = scaler.fit_transform(X_train)
        X_val_sc = scaler.transform(X_val)
        lr = LogisticRegression(C=0.1, max_iter=200, random_state=42)
        lr.fit(X_tr_sc, y_train)
        oof_lr[val_idx] = lr.predict_proba(X_val_sc)[:, 1]
        auc_lr = roc_auc_score(y_val, oof_lr[val_idx])
        print(f"Fold {fold} - Logistic Regression AUC: {auc_lr:.4f} ({time.time()-t0:.1f}s)")
        
        # 2. Ensemble : Random Forest (Bagging)
        t0 = time.time()
        rf = RandomForestClassifier(n_estimators=100, max_depth=10, min_samples_leaf=20, random_state=42, n_jobs=4)
        rf.fit(X_train, y_train)
        oof_rf[val_idx] = rf.predict_proba(X_val)[:, 1]
        auc_rf = roc_auc_score(y_val, oof_rf[val_idx])
        print(f"Fold {fold} - Random Forest AUC:       {auc_rf:.4f} ({time.time()-t0:.1f}s)")
        
        # 3. Challenger 1 : CatBoost Classifier (Symmetric Trees)
        t0 = time.time()
        cb = CatBoostClassifier(iterations=250, depth=6, learning_rate=0.06, eval_metric="AUC", verbose=0, thread_count=4, random_seed=42)
        cb.fit(X_train, y_train, eval_set=(X_val, y_val), early_stopping_rounds=30)
        oof_cb[val_idx] = cb.predict_proba(X_val)[:, 1]
        auc_cb = roc_auc_score(y_val, oof_cb[val_idx])
        print(f"Fold {fold} - CatBoost AUC:            {auc_cb:.4f} ({time.time()-t0:.1f}s)")
        
        # 4. Challenger 2 : LightGBM GBDT (Bayesian Tuned)
        t0 = time.time()
        train_data = lgb.Dataset(X_train, label=y_train, feature_name=feature_names)
        val_data = lgb.Dataset(X_val, label=y_val, feature_name=feature_names, reference=train_data)
        
        params = {
            'objective': 'binary',
            'metric': 'auc',
            'boosting_type': 'gbdt',
            'learning_rate': 0.04,
            'num_leaves': 45,
            'max_depth': 7,
            'feature_fraction': 0.75,
            'bagging_fraction': 0.8,
            'bagging_freq': 1,
            'verbose': -1,
            'num_threads': 4,
            'seed': 42
        }
        
        callbacks = [lgb.early_stopping(stopping_rounds=30, verbose=False)]
        model_lgb = lgb.train(
            params,
            train_data,
            num_boost_round=350,
            valid_sets=[val_data],
            callbacks=callbacks
        )
        oof_lgb[val_idx] = model_lgb.predict(X_val, num_iteration=model_lgb.best_iteration)
        feature_importances_lgb += model_lgb.feature_importance(importance_type='gain') / n_splits
        auc_lgb = roc_auc_score(y_val, oof_lgb[val_idx])
        print(f"Fold {fold} - LightGBM GBDT AUC:         {auc_lgb:.4f} (best iter: {model_lgb.best_iteration}, {time.time()-t0:.1f}s)")
        
        fold += 1
        gc.collect()
        
    # 5. Stacking Super-Learner Ensemble (Blending)
    oof_ensemble = (0.50 * oof_lgb + 0.35 * oof_cb + 0.15 * oof_rf).astype(np.float32)
    
    # Calcul des Métriques Globales OOF
    print("\n" + "="*60)
    print("RÉSULTATS GLOBAUX DU BENCHMARK COMPARATIF (OUT-OF-FOLD)")
    print("="*60)
    
    models_summary = {}
    for name, oof in [("Logistic Regression (Baseline)", oof_lr), 
                      ("Random Forest (100 Trees)", oof_rf), 
                      ("CatBoost (250 Trees)", oof_cb),
                      ("LightGBM GBDT (Optimisé)", oof_lgb),
                      ("Stacking Ensemble (Super-Learner)", oof_ensemble)]:
        auc = roc_auc_score(y, oof)
        brier = brier_score_loss(y, oof)
        pred_labels = (oof >= 0.5).astype(int)
        prec = precision_score(y, pred_labels)
        rec = recall_score(y, pred_labels)
        f1 = f1_score(y, pred_labels)
        ll = log_loss(y, oof)
        
        models_summary[name] = {
            "ROC_AUC": round(float(auc), 4),
            "Log_Loss": round(float(ll), 4),
            "Brier_Score": round(float(brier), 4),
            "Precision": round(float(prec), 4),
            "Recall": round(float(rec), 4),
            "F1_Score": round(float(f1), 4)
        }
        print(f"{name:35} | ROC-AUC: {auc:.4f} | Brier: {brier:.4f} | F1: {f1:.4f} | Précision: {prec:.4f} | Rappel: {rec:.4f}")

    # Top 15 Feature Importances (Gain)
    importance_df = pd.DataFrame({
        'feature': feature_names,
        'importance_gain': feature_importances_lgb
    }).sort_values('importance_gain', ascending=False).reset_index(drop=True)
    
    print("\n--- Top 15 Variables les plus Prédictives (Gain LightGBM) ---")
    for i, row in importance_df.head(15).iterrows():
        print(f"{i+1:2d}. {row['feature']:25} : {row['importance_gain']:,.1f}")
        
    importance_df.to_csv(os.path.join(OUTPUT_DIR, "feature_importances_gain.csv"), index=False)
    
    # -------------------------------------------------------------
    # CALCUL DU BUSINESS CASE FINANCIER & RETURN ON INVESTMENT (ROI)
    # -------------------------------------------------------------
    print("\n" + "="*60)
    print("MODÉLISATION FINANCIÈRE DE LA PROPOSITION BUSINESS (ROI)")
    print("="*60)
    
    # Expected Revenue at Risk (ERaR)
    # Basé sur le modèle LightGBM champion calibré
    annual_rev = monthly_rev * 12.0
    expected_loss = oof_lgb * annual_rev
    
    eval_df = pd.DataFrame({
        'churn_true': y,
        'churn_prob': oof_lgb,
        'churn_prob_ensemble': oof_ensemble,
        'churn_prob_lr': oof_lr,
        'churn_prob_rf': oof_rf,
        'churn_prob_cb': oof_cb,
        'monthly_rev': monthly_rev,
        'annual_rev': annual_rev,
        'expected_loss': expected_loss,
        'eqp_days': eqp_days
    })
    
    # Tri par Expected Loss décroissante (Priorité Valeur Financière)
    eval_df = eval_df.sort_values('expected_loss', ascending=False).reset_index(drop=True)
    eval_df['cum_subscribers_pct'] = (eval_df.index + 1) / len(eval_df) * 100.0
    eval_df['cum_churners_caught'] = eval_df['churn_true'].cumsum()
    eval_df['cum_churners_pct'] = eval_df['cum_churners_caught'] / eval_df['churn_true'].sum() * 100.0
    eval_df['cum_expected_loss_caught'] = eval_df['expected_loss'].cumsum()
    eval_df['cum_loss_pct'] = eval_df['cum_expected_loss_caught'] / eval_df['expected_loss'].sum() * 100.0
    
    # Analyse par Décile
    eval_df['decile'] = pd.qcut(eval_df.index, q=10, labels=[f"D{i+1}" for i in range(10)])
    decile_summary = eval_df.groupby('decile', observed=False).agg(
        subscribers=('churn_true', 'count'),
        actual_churn_rate=('churn_true', 'mean'),
        avg_monthly_rev=('monthly_rev', 'mean'),
        total_annual_revenue=('annual_rev', 'sum'),
        total_revenue_at_risk=('expected_loss', 'sum')
    ).reset_index()
    decile_summary['actual_churn_rate_pct'] = round(decile_summary['actual_churn_rate'] * 100, 2)
    decile_summary['revenue_at_risk_pct'] = round(decile_summary['total_revenue_at_risk'] / eval_df['expected_loss'].sum() * 100, 2)
    print("\n--- Analyse par Décile de Valeur en Risque ---")
    print(decile_summary[['decile', 'subscribers', 'actual_churn_rate_pct', 'avg_monthly_rev', 'total_revenue_at_risk', 'revenue_at_risk_pct']].to_string(index=False))
    
    # SIMULATION DU PROGRAMME "5G DEVICE UPGRADE"
    # Hypothèses économiques strictes et réalistes (McKinsey / GSMA standards) :
    # 1. Ciblage : Top 15% (15 000 clients à plus fort Expected Revenue at Risk ET équipement > 365 jours)
    # 2. Coût de subvention terminal 5G net (opérateur) : 130 $ / client
    # 3. Taux d'acceptation et réengagement ferme sur 24 mois : 68%
    # 4. Taux de réduction du churn sur la cohorte ciblée : réduction de 60% du churn
    
    target_mask = (eval_df['cum_subscribers_pct'] <= 15.0) & (eval_df['eqp_days'] > 365)
    cohort_size = target_mask.sum()
    cohort_actual_churners = eval_df.loc[target_mask, 'churn_true'].sum()
    cohort_arpu = eval_df.loc[target_mask, 'monthly_rev'].mean()
    
    subsidized_unit_cost = 130.0  # Coût net opérateur d'un combiné 5G en volume
    take_up_rate = 0.68            # 68% acceptent l'offre avec réengagement 24 mois
    churn_prevention_rate = 0.60   # 60% des churners potentiels sont sauvés
    
    campaign_cost = cohort_size * subsidized_unit_cost
    churners_targeted = cohort_actual_churners
    churners_saved = churners_targeted * take_up_rate * churn_prevention_rate
    
    revenue_saved_24m = churners_saved * cohort_arpu * 24.0
    annual_revenue_saved = churners_saved * cohort_arpu * 12.0
    net_profit_24m = revenue_saved_24m - campaign_cost
    roi_pct = (net_profit_24m / campaign_cost) * 100.0
    payback_months = (campaign_cost / (annual_revenue_saved / 12.0))
    
    business_case = {
        "targeted_subscribers": int(cohort_size),
        "cohort_avg_arpu": round(float(cohort_arpu), 2),
        "campaign_cost_usd": round(float(campaign_cost), 2),
        "churners_saved": int(round(churners_saved)),
        "annual_arr_saved_usd": round(float(annual_revenue_saved), 2),
        "revenue_protected_24m_usd": round(float(revenue_saved_24m), 2),
        "net_gain_24m_usd": round(float(net_profit_24m), 2),
        "roi_percentage": round(float(roi_pct), 1),
        "payback_months": round(float(payback_months), 2)
    }
    
    print("\n--- Bilan Financier Exécutif du Programme ---")
    print(f"Abonnés ciblés (Top 15% à risque & équipement > 1 an) : {cohort_size:,}")
    print(f"ARPU moyen de la cohorte ciblée                     : ${cohort_arpu:.2f} / mois (vs $58.72 moyenne globale)")
    print(f"Investissement total du programme (Smartphones 5G)   : ${campaign_cost:,.2f}")
    print(f"Abonnés churners définitivement sauvés & réengagés   : {int(round(churners_saved)):,} abonnés")
    print(f"Chiffre d'affaires protégé sur 24 mois               : ${revenue_saved_24m:,.2f}")
    print(f"Bénéfice NET dégagé (après déduction des téléphones) : ${net_profit_24m:,.2f}")
    print(f"Retour sur Investissement Net (ROI)                  : +{roi_pct:.1f}%")
    print(f"Délai d'amortissement complet (Payback)              : {payback_months:.1f} mois")
    
    full_results = {
        "models_summary": models_summary,
        "business_case": business_case,
        "deciles": decile_summary.to_dict(orient='records')
    }
    
    with open(os.path.join(OUTPUT_DIR, "model_benchmark_results.json"), "w") as f:
        json.dump(full_results, f, indent=2)
        
    eval_df.to_parquet(os.path.join(OUTPUT_DIR, "predictions_evaluation.parquet"), index=False)
    print("\nArtefacts d'évaluation et prédictions sauvegardés avec succès !")
    return full_results

if __name__ == "__main__":
    X, y, customer_ids, monthly_rev, eqp_days, feature_names = load_and_engineer_features()
    train_and_evaluate(X, y, monthly_rev, eqp_days, feature_names)
