#!/usr/bin/env python3
"""
Audit d'Intégrité & Exploration Statistique Initiale
GCI World 2026 September - Final Assignment (Company A)
"""
import duckdb
import json
import pandas as pd
import numpy as np

DATA_DIR = "/Users/baptistebedeaux/gci_final_assignment/data"

def run_audit():
    con = duckdb.connect(database=':memory:')
    con.execute("PRAGMA threads=2;")
    con.execute("PRAGMA max_memory='1GB';")
    
    print("="*60)
    print("AUDIT DE QUALITÉ & INTÉGRITÉ - COMPANY A TELECOM")
    print("="*60)
    
    # 1. Vérification Client.csv
    client_count = con.execute(f"SELECT count(*), count(distinct Customer_ID) FROM '{DATA_DIR}/Client.csv'").fetchone()
    print(f"Client.csv: {client_count[0]} lignes | {client_count[1]} Customer_ID uniques")
    assert client_count[0] == client_count[1], "Duplication détectée dans Client.csv!"

    # 2. Vérification Record.csv
    record_count = con.execute(f"SELECT count(*), count(distinct Customer_ID) FROM '{DATA_DIR}/Record.csv'").fetchone()
    print(f"Record.csv: {record_count[0]} lignes | {record_count[1]} Customer_ID uniques")
    assert record_count[0] == record_count[1], "Duplication détectée dans Record.csv!"

    # 3. Vérification de l'intégrité du JOIN
    join_count = con.execute(f"""
        SELECT count(*) 
        FROM '{DATA_DIR}/Client.csv' c
        INNER JOIN '{DATA_DIR}/Record.csv' r ON c.Customer_ID = r.Customer_ID
    """).fetchone()[0]
    print(f"Jointure 1:1 exacte : {join_count} clients parfaitement réconciliés.")
    assert join_count == 100000, f"Erreur de jointure : {join_count} au lieu de 100000"

    # 4. Statistiques clés sur le Churn et la Valeur Client
    stats = con.execute(f"""
        SELECT 
            avg(churn) as churn_rate,
            avg(rev_Mean) as avg_monthly_rev,
            median(rev_Mean) as median_monthly_rev,
            avg(totrev) as avg_total_rev,
            avg(eqpdays) as avg_eqp_days,
            median(eqpdays) as median_eqp_days,
            avg(totcalls) as avg_totcalls,
            sum(CASE WHEN churn = 1 THEN rev_Mean ELSE 0 END) as monthly_rev_lost_to_churn
        FROM '{DATA_DIR}/Client.csv' c
        JOIN '{DATA_DIR}/Record.csv' r ON c.Customer_ID = r.Customer_ID
    """).df().to_dict(orient='records')[0]

    print("\n--- Indicateurs Macroéconomiques de Company A ---")
    print(f"Taux d'attrition (Churn rate) : {stats['churn_rate']*100:.2f}% (quasi 50/50)")
    print(f"Revenu mensuel moyen (ARPU)  : ${stats['avg_monthly_rev']:.2f} / mois (Médiane: ${stats['median_monthly_rev']:.2f})")
    print(f"Revenu total moyen cumulé    : ${stats['avg_total_rev']:.2f}")
    print(f"Âge moyen équipement mobile  : {stats['avg_eqp_days']:.1f} jours (~{stats['avg_eqp_days']/365:.1f} ans)")
    print(f"Revenu mensuel perdu (Churn) : ${stats['monthly_rev_lost_to_churn']:,.2f} / mois !")
    print(f"Perte annuelle estimée (ARR) : ${stats['monthly_rev_lost_to_churn']*12:,.2f} / an !")

    # 5. Croisement Valeur Client × Ancienneté Équipement × Churn
    segments = con.execute(f"""
        SELECT 
            CASE 
                WHEN eqpdays < 365 THEN '1. Récent (< 1 an)'
                WHEN eqpdays < 730 THEN '2. Moyen (1-2 ans)'
                ELSE '3. Ancien (> 2 ans)'
            END as equipment_age_group,
            count(*) as customer_count,
            round(avg(churn)*100, 2) as churn_rate_pct,
            round(avg(rev_Mean), 2) as avg_arpu,
            round(sum(CASE WHEN churn = 1 THEN rev_Mean * 12 ELSE 0 END), 0) as annual_churn_cost
        FROM '{DATA_DIR}/Client.csv' c
        JOIN '{DATA_DIR}/Record.csv' r ON c.Customer_ID = r.Customer_ID
        WHERE eqpdays IS NOT NULL
        GROUP BY 1
        ORDER BY 1
    """).df()
    print("\n--- Impact de l'Ancienneté Équipement sur le Churn et le Chiffre d'Affaires ---")
    print(segments.to_string(index=False))

    # Sauvegarde du rapport d'audit
    audit_results = {
        "status": "VALIDATED",
        "dataset_rows": join_count,
        "macro_stats": stats,
        "equipment_segments": segments.to_dict(orient='records')
    }
    with open('/Users/baptistebedeaux/gci_final_assignment/src/audit_results.json', 'w') as f:
        json.dump(audit_results, f, indent=2)
    print("\nRapport d'audit sauvegardé dans /Users/baptistebedeaux/gci_final_assignment/src/audit_results.json")

if __name__ == "__main__":
    run_audit()
