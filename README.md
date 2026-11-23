# GCI World 2026 September — Final Assignment (Report 125)
**Candidate:** Baptiste Bedeaux (`BaptisteBdx`)  
**Institution:** The University of Tokyo — Matsuo-Iwasawa Laboratory  
**Official Portal:** [Omnicampus Course 170 / Report 125](https://edu.omnicamp.us/courses/170/reports/125/)  
**Submission Deadline:** November 28, 2026, 11:30 UTC  
**Target Distinction:** Outstanding Student Award (Top 1–2% global)

---

## 📁 Project Quick Directory Index

```
/Users/baptistebedeaux/gci_final_assignment/
├── slides/
│   ├── BaptisteBdx.pdf              # FINAL DELIVERABLE 1 (15 slides, 2.56 MB, Apple Keynote vector design)
│   ├── BaptisteBdx.html             # Source HTML for Playwright vector rendering
│   ├── figures/                     # 6 High-resolution (350 DPI) Apple Keynote figures
│   └── previews/                    # PNG snapshots of all 15 slides for rapid inspection
├── notebooks/
│   └── BaptisteBdx.ipynb            # FINAL DELIVERABLE 2 (18 cells, 8/8 executed, 100% reproducible)
├── data/
│   ├── Client.csv                   # Raw customer table (100k rows × 50 cols)
│   └── Record.csv                   # Raw usage table (100k rows × 50 cols)
├── src/
│   ├── train_models_and_evaluate.py # 5-Fold Stratified Cross-Validation benchmark (LogReg, RF, LightGBM)
│   ├── generate_executive_charts.py # Matplotlib 350 DPI Apple Keynote chart generator
│   ├── generate_slides_pdf.py       # Playwright PDF builder & vector blueprint compiler
│   └── model_benchmark_results.json # Full cross-validation metrics, decile breakdown & ROI model
└── OMNICAMPUS_SUBMISSION_GUIDE.md   # Exact answers to AI survey (Q1-Q4) and submission checklist
```

---

## 🏆 Core Strategic & Academic Highlights

1. **Strategic Thesis:**
   - Instead of generic binary churn modeling, this work introduces the **Value-at-Risk Framework**: ranking subscribers by `Expected Loss = P(churn) × ARPU × 12`.
   - **Empirical Discovery:** Equipment age (`eqpdays`) is the #1 predictive driver across 100 variables (Split Gain: 17,186). Churn surges from 41.8% (<6m) to 59.7% (>30m).
   - **Executive Solution:** *"Predictive 5G Device Upgrade"* program subsidizing a $130 modern 5G smartphone for the Top 15% VIP cohort in exchange for a mandatory 24-month contract extension.
   - **Business Impact:** **+$3,168,404 Net Profit**, **+433.8% Net ROI**, **4.5 Months Payback**.

2. **Machine Learning Rigor:**
   - 5-Fold Stratified Out-of-Fold Cross-Validation.
   - Baseline Logistic Regression: `ROC-AUC = 0.6262`, `Brier = 0.2382`
   - Random Forest (100 Trees): `ROC-AUC = 0.6676`, `Brier = 0.2294`
   - **LightGBM GBDT (Optimized):** **`ROC-AUC = 0.6968`**, **`Brier = 0.2203`**, **`F1 = 0.6423`**
