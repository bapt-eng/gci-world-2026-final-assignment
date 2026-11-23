#!/usr/bin/env python3
"""
Génération des Graphiques Apple Keynote Épurés (350 DPI)
Suppression des titres redondants intra-graphiques pour maximiser l'espace visuel des données.
Style : Apple Human Interface Guidelines / Keynote Clean Vector Aesthetics
"""
import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from sklearn.metrics import roc_curve, auc

OUTPUT_DIR = "/Users/baptistebedeaux/gci_final_assignment/slides/figures"
SRC_DIR = "/Users/baptistebedeaux/gci_final_assignment/src"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Palette Apple Keynote Pure & Pastel
APPLE_BLUE = "#0071E3"
APPLE_BLUE_MID = "#5AC8FA"
APPLE_GREEN = "#34C759"
APPLE_CORAL = "#FF453A"
APPLE_ORANGE = "#FF9F0A"
APPLE_MUTED = "#8E8E93"
APPLE_LIGHT_BAR = "#E5E5EA"
APPLE_GRID = "#F2F2F7"
APPLE_TEXT = "#1D1D1F"
APPLE_SUBTEXT = "#6E6E73"

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['SF Pro Display', 'Helvetica Neue', 'Arial', 'DejaVu Sans'],
    'font.size': 11,
    'axes.labelsize': 12,
    'xtick.labelsize': 11,
    'ytick.labelsize': 10.5,
    'legend.fontsize': 11,
    'figure.dpi': 350,
    'axes.edgecolor': '#E5E5EA',
    'axes.linewidth': 0.8,
    'text.color': APPLE_TEXT,
    'axes.labelcolor': APPLE_SUBTEXT,
    'xtick.color': APPLE_SUBTEXT,
    'ytick.color': APPLE_SUBTEXT,
    'figure.facecolor': '#FFFFFF',
    'axes.facecolor': '#FFFFFF'
})

def format_spines_and_grid(ax):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('#E5E5EA')
    ax.spines['bottom'].set_linewidth(1.0)
    ax.yaxis.grid(True, linestyle='-', linewidth=0.8, color=APPLE_GRID, zorder=1)
    ax.xaxis.grid(False)
    ax.tick_params(axis='y', length=0)
    ax.tick_params(axis='x', length=4, color='#E5E5EA')

def draw_rounded_vbars(ax, x_positions, heights, width=0.48, colors=None, corner_radius=0.03):
    for x, h, col in zip(x_positions, heights, colors):
        box = FancyBboxPatch(
            (x - width/2, 0), width, h,
            boxstyle=f"round,pad=0,rounding_size={corner_radius}",
            facecolor=col, edgecolor='none', zorder=3
        )
        ax.add_patch(box)

def draw_rounded_hbars(ax, y_positions, widths, height=0.55, colors=None, corner_radius=0.02):
    for y, w, col in zip(y_positions, widths, colors):
        box = FancyBboxPatch(
            (0, y - height/2), w, height,
            boxstyle=f"round,pad=0,rounding_size={corner_radius}",
            facecolor=col, edgecolor='none', zorder=3
        )
        ax.add_patch(box)

def generate_charts():
    print("Régénération des figures Apple sans titres redondants...")
    eval_df = pd.read_parquet(os.path.join(SRC_DIR, "predictions_evaluation.parquet"))
    with open(os.path.join(SRC_DIR, "model_benchmark_results.json")) as f:
        bench_data = json.load(f)
    feat_df = pd.read_csv(os.path.join(SRC_DIR, "feature_importances_gain.csv"))

    # -------------------------------------------------------------
    # FIGURE 1 : Macro Waterfall / Churn Impact ($34.45M ARR)
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    x_pos = np.arange(3)
    categories = ['Total Annual\nGross Run-Rate', 'Annual Churn\nRevenue Bleed', 'Net Retained\nAnnual ARR']
    values = [70.46, -34.45, 36.01]
    bar_heights = [70.46, 34.45, 36.01]
    colors = [APPLE_BLUE, APPLE_CORAL, APPLE_GREEN]
    
    draw_rounded_vbars(ax, x_pos, bar_heights, width=0.46, colors=colors, corner_radius=0.04)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(categories, fontweight='700')
    ax.set_ylabel('Annual Revenue ($ Millions USD)', fontweight='600', labelpad=12)
    ax.set_ylim(0, 85)
    
    ax.annotate('$70.46M\n(100%)', xy=(0, 70.46), xytext=(0, 9), textcoords="offset points",
                ha='center', va='bottom', fontweight='700', fontsize=12, color=APPLE_BLUE)
    ax.annotate('-$34.45M\n(-48.9%)', xy=(1, 34.45), xytext=(0, 9), textcoords="offset points",
                ha='center', va='bottom', fontweight='700', fontsize=12, color=APPLE_CORAL)
    ax.annotate('$36.01M\n(+51.1%)', xy=(2, 36.01), xytext=(0, 9), textcoords="offset points",
                ha='center', va='bottom', fontweight='700', fontsize=12, color=APPLE_GREEN)
                
    ax.plot([0.25, 0.75], [70.46, 70.46], color='#D1D1D6', linestyle=':', linewidth=1.2, zorder=2)
    ax.plot([1.25, 1.75], [36.01, 36.01], color='#D1D1D6', linestyle=':', linewidth=1.2, zorder=2)
                    
    format_spines_and_grid(ax)
    ax.set_xlim(-0.55, 2.55)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "fig1_macro_loss_waterfall.png"), dpi=350, facecolor='#FFFFFF')
    plt.close()
    print("Fig 1 épurée.")

    # -------------------------------------------------------------
    # FIGURE 2 : Impact Massif de l'Âge de l'Équipement (eqpdays)
    # -------------------------------------------------------------
    fig, ax1 = plt.subplots(figsize=(8.5, 5.2))
    
    bins = [0, 180, 365, 545, 730, 910, 1200]
    labels = ['< 6m', '6-12m', '12-18m', '18-24m', '24-30m', '> 30m']
    eval_df['age_bracket'] = pd.cut(eval_df['eqp_days'], bins=bins, labels=labels)
    grouped = eval_df.groupby('age_bracket', observed=False).agg(
        subscribers=('churn_true', 'count'),
        churn_rate=('churn_true', 'mean')
    ).reset_index()
    
    x_pos = np.arange(len(labels))
    draw_rounded_vbars(ax1, x_pos, grouped['subscribers'], width=0.48, 
                      colors=[APPLE_LIGHT_BAR]*len(labels), corner_radius=0.03)
                      
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(labels, fontweight='700')
    ax1.set_ylabel('Subscribers Count (Volume in Cohort)', color=APPLE_SUBTEXT, fontweight='600', labelpad=12)
    ax1.tick_params(axis='y', labelcolor=APPLE_SUBTEXT, length=0)
    ax1.set_ylim(0, 42000)
    format_spines_and_grid(ax1)
    
    ax2 = ax1.twinx()
    ax2.plot(x_pos, grouped['churn_rate']*100, color=APPLE_CORAL, 
             marker='o', linewidth=3.2, markersize=9, markerfacecolor='#FFFFFF', 
             markeredgewidth=2.6, zorder=5)
    ax2.set_ylabel('Actual Churn Rate (%)', color=APPLE_CORAL, fontweight='700', labelpad=12)
    ax2.tick_params(axis='y', labelcolor=APPLE_CORAL, length=0)
    ax2.set_ylim(38, 66)
    ax2.spines['top'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['bottom'].set_color('#E5E5EA')
    ax2.grid(False)
    
    # Seuil critique mis en valeur
    ax1.axvline(1.5, color=APPLE_CORAL, linestyle='--', linewidth=1.4, alpha=0.5, zorder=2)
    ax1.text(1.55, 38000, 'Threshold: Device > 1 Year (Warranty Expiry)', 
             color=APPLE_CORAL, fontsize=10, fontweight='700')
    
    for i, row in grouped.iterrows():
        ax2.annotate(f"{row['churn_rate']*100:.1f}%",
                     xy=(i, row['churn_rate']*100),
                     xytext=(0, 9), textcoords="offset points",
                     ha='center', va='bottom', fontweight='700', color=APPLE_CORAL, fontsize=11.5)
                     
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "fig2_equipment_churn_curve.png"), dpi=350, facecolor='#FFFFFF')
    plt.close()
    print("Fig 2 épurée.")

    # -------------------------------------------------------------
    # FIGURE 3 : Comparatif des Courbes ROC (Multi-Modèles & Ensembling)
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(7.8, 5.2))
    
    # 1. LightGBM Champion
    fpr_lgb, tpr_lgb, _ = roc_curve(eval_df['churn_true'], eval_df['churn_prob'])
    roc_lgb = auc(fpr_lgb, tpr_lgb)
    
    # 2. Stacking Ensemble
    fpr_ens, tpr_ens, _ = roc_curve(eval_df['churn_true'], eval_df['churn_prob_ensemble'])
    roc_ens = auc(fpr_ens, tpr_ens)
    
    # 3. CatBoost
    fpr_cb, tpr_cb, _ = roc_curve(eval_df['churn_true'], eval_df['churn_prob_cb'])
    roc_cb = auc(fpr_cb, tpr_cb)
    
    # 4. Random Forest
    fpr_rf, tpr_rf, _ = roc_curve(eval_df['churn_true'], eval_df['churn_prob_rf'])
    roc_rf = auc(fpr_rf, tpr_rf)
    
    # 5. Logistic Regression
    fpr_lr, tpr_lr, _ = roc_curve(eval_df['churn_true'], eval_df['churn_prob_lr'])
    roc_lr = auc(fpr_lr, tpr_lr)
    
    ax.fill_between(fpr_lgb, tpr_lgb, color=APPLE_BLUE, alpha=0.08, zorder=2)
    ax.plot(fpr_lgb, tpr_lgb, color=APPLE_BLUE, linewidth=3.2, label=f'LightGBM GBDT (Tuned) — AUC {roc_lgb:.4f}', zorder=6)
    ax.plot(fpr_ens, tpr_ens, color=APPLE_GREEN, linewidth=2.4, linestyle='-', label=f'Stacking Ensemble — AUC {roc_ens:.4f}', zorder=5)
    ax.plot(fpr_cb, tpr_cb, color="#AF52DE", linewidth=2.0, linestyle='--', label=f'CatBoost (250 Trees) — AUC {roc_cb:.4f}', zorder=4)
    ax.plot(fpr_rf, tpr_rf, color=APPLE_ORANGE, linewidth=1.8, linestyle='--', label=f'Random Forest — AUC {roc_rf:.4f}', zorder=3)
    ax.plot(fpr_lr, tpr_lr, color=APPLE_MUTED, linewidth=1.5, linestyle=':', label=f'Logistic Regression — AUC {roc_lr:.4f}', zorder=2)
    ax.plot([0, 1], [0, 1], color=APPLE_LIGHT_BAR, linestyle='--', linewidth=1.2, label='Random Baseline — AUC 0.5000', zorder=1)
    
    ax.set_xlabel('False Positive Rate (1 - Specificity)', fontweight='600', labelpad=10)
    ax.set_ylabel('True Positive Rate (Sensitivity / Recall)', fontweight='600', labelpad=10)
    
    legend = ax.legend(loc='lower right', frameon=True, facecolor='#FFFFFF', edgecolor='#E5E5EA', framealpha=0.98)
    legend.get_frame().set_boxstyle("square,pad=0.5")
    
    format_spines_and_grid(ax)
    ax.xaxis.grid(True, linestyle='-', linewidth=0.8, color=APPLE_GRID, zorder=0)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "fig3_roc_comparison.png"), dpi=350, facecolor='#FFFFFF')
    plt.close()
    print("Fig 3 épurée.")

    # -------------------------------------------------------------
    # FIGURE 4 : Top 12 Feature Importances (Gain)
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8.8, 5.2))
    top12 = feat_df.head(12).sort_values('importance_gain', ascending=True)
    
    y_pos = np.arange(len(top12))
    colors = [APPLE_BLUE if f == 'eqpdays' else APPLE_BLUE_MID if 'eqp' in f else APPLE_LIGHT_BAR for f in top12['feature']]
    text_colors = [APPLE_BLUE if f == 'eqpdays' else APPLE_TEXT for f in top12['feature']]
    
    draw_rounded_hbars(ax, y_pos, top12['importance_gain'], height=0.62, colors=colors, corner_radius=0.03)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(top12['feature'], fontweight='700')
    ax.set_xlabel('Total Split Gain (Relative Predictive Contribution)', fontweight='600', labelpad=10)
    
    for y, w, tc, f in zip(y_pos, top12['importance_gain'], text_colors, top12['feature']):
        label = f"{w:,.0f}" + ("  [#1 PREDICTIVE SIGNAL]" if f == 'eqpdays' else "")
        ax.annotate(label,
                    xy=(w, y), xytext=(8, 0), textcoords="offset points",
                    ha='left', va='center', fontsize=10, fontweight='700' if f == 'eqpdays' else '600', color=tc)
                    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#E5E5EA')
    ax.spines['bottom'].set_visible(False)
    ax.xaxis.grid(True, linestyle='-', linewidth=0.8, color=APPLE_GRID, zorder=1)
    ax.yaxis.grid(False)
    ax.tick_params(axis='y', length=0)
    ax.tick_params(axis='x', length=0)
    ax.set_xlim(0, 28000)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "fig4_feature_importance_gain.png"), dpi=350, facecolor='#FFFFFF')
    plt.close()
    print("Fig 4 épurée.")

    # -------------------------------------------------------------
    # FIGURE 5 : Expected Revenue at Risk par Décile (Concentration)
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8.8, 5.2))
    deciles = [f"D{i+1}" for i in range(10)]
    losses_m = [d['total_revenue_at_risk'] / 1e6 for d in bench_data['deciles']]
    pcts = [d['revenue_at_risk_pct'] for d in bench_data['deciles']]
    
    x_pos = np.arange(10)
    colors = [APPLE_CORAL if i == 0 else APPLE_ORANGE if i == 1 else APPLE_LIGHT_BAR for i in range(10)]
    draw_rounded_vbars(ax, x_pos, losses_m, width=0.52, colors=colors, corner_radius=0.03)
    
    ax.set_xticks(x_pos)
    ax.set_xticklabels(deciles, fontweight='700')
    ax.set_ylabel('Annual Revenue at Risk ($ Millions)', fontweight='600', labelpad=12)
    ax.set_xlabel('Customer Deciles (Ranked by Expected Loss = P(churn) × ARPU)', fontweight='600', labelpad=10)
    
    for x, pct, loss, i in zip(x_pos, pcts, losses_m, range(10)):
        tc = APPLE_CORAL if i == 0 else APPLE_ORANGE if i == 1 else APPLE_SUBTEXT
        ax.annotate(f'${loss:.1f}M\n({pct:.1f}%)',
                    xy=(x, loss), xytext=(0, 6), textcoords="offset points",
                    ha='center', va='bottom', fontsize=9, fontweight='700' if i < 2 else '600', color=tc)
                    
    ax.annotate('D1 + D2 = $15.5M (44.8% of Total)', xy=(0.5, 10.5), xytext=(2.2, 11.2),
                arrowprops=dict(arrowstyle="->", color=APPLE_CORAL, lw=1.2),
                bbox=dict(boxstyle="round,pad=0.5,rounding_size=0.3", fc="#FDF0EE", ec=APPLE_CORAL, lw=1.0),
                fontsize=10, fontweight='700', color=APPLE_CORAL)
                
    ax.set_ylim(0, 13.0)
    format_spines_and_grid(ax)
    ax.set_xlim(-0.6, 9.6)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "fig5_value_at_risk_deciles.png"), dpi=350, facecolor='#FFFFFF')
    plt.close()
    print("Fig 5 épurée.")

    # -------------------------------------------------------------
    # FIGURE 6 : ROI & Business Case Financier ($3.20M Bénéfice Net)
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8.4, 5.2))
    fin_cats = ['Campaign Cost\n(5G Subsidies)', 'Protected Gross ARR\n(24-Month Plan)', 'Net Economic Profit\n(Net Return)']
    fin_vals = [0.737, 3.940, 3.203]
    fin_colors = [APPLE_CORAL, APPLE_BLUE, APPLE_GREEN]
    
    x_pos = np.arange(3)
    draw_rounded_vbars(ax, x_pos, fin_vals, width=0.46, colors=fin_colors, corner_radius=0.04)
    
    ax.set_xticks(x_pos)
    ax.set_xticklabels(fin_cats, fontweight='700')
    ax.set_ylabel('Value ($ Millions USD)', fontweight='600', labelpad=12)
    ax.set_ylim(0, 5.0)
    
    for x, val, col in zip(x_pos, fin_vals, fin_colors):
        ax.annotate(f'${val:.2f}M',
                    xy=(x, val), xytext=(0, 8), textcoords="offset points",
                    ha='center', va='bottom', fontweight='700', fontsize=13, color=col)
                    
    ax.text(1.95, 4.35, 'NET ROI: +434.5%  •  PAYBACK: 4.5 MOS',
            bbox=dict(boxstyle="round,pad=0.6,rounding_size=0.3", fc="#EAF7EE", ec="#34C759", lw=1.2),
            fontsize=11, fontweight='700', color="#1B7339", ha='center', va='center')
                
    format_spines_and_grid(ax)
    ax.set_xlim(-0.55, 2.55)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "fig6_roi_payback_waterfall.png"), dpi=350, facecolor='#FFFFFF')
    plt.close()
    print("Fig 6 épurée.")

if __name__ == "__main__":
    generate_charts()
