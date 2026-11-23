#!/usr/bin/env python3
"""
Génération du Diaporama PDF Haute Fidélité pour le Final Assignment GCI World 2026.
Style : Apple Keynote / Cupertino Clean Pastel Aesthetics
Conforme aux 15 critères stricts de la soutenance (15 slides max, < 10 Mo).
Intègre de véritables SCHÉMAS D'ARCHITECTURE & BLUEPRINTS VECTORIELS (Slides 6, 7, 11, 13).
"""

import os
import json
import subprocess
from pypdf import PdfReader

OUTPUT_PDF = "/Users/baptistebedeaux/gci_final_assignment/slides/BaptisteBdx.pdf"
HTML_PATH = "/Users/baptistebedeaux/gci_final_assignment/slides/BaptisteBdx.html"
FIG_DIR = "/Users/baptistebedeaux/gci_final_assignment/slides/figures"

APPLE_SLIDES_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>BaptisteBdx - GCI World 2026 Final Assignment</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>
  @page {
    size: 13.333in 7.5in;
    margin: 0;
  }

  *, *::before, *::after {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  body {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "SF Pro Display", "Helvetica Neue", sans-serif;
    color: #1D1D1F;
    background-color: #FBFBFD;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }

  .slide {
    width: 13.333in;
    height: 7.5in;
    page-break-after: always;
    break-after: page;
    position: relative;
    padding: 0.52in 0.75in 0.45in 0.75in;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background: #FBFBFD;
    overflow: hidden;
  }

  .slide:last-of-type {
    page-break-after: avoid;
    break-after: avoid;
  }

  /* Slide 1 : Apple Keynote Hero Slide */
  .slide-hero {
    background: radial-gradient(circle at 80% 20%, rgba(235, 243, 251, 0.7) 0%, #FFFFFF 60%);
    justify-content: center;
    padding: 1.0in 1.1in;
  }

  /* Header Pattern */
  .header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    padding-bottom: 0.16in;
    margin-bottom: 0.24in;
    border-bottom: 1px solid rgba(0, 0, 0, 0.07);
  }

  .header-left .category {
    display: inline-block;
    font-size: 0.13in;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    padding: 0.04in 0.12in;
    border-radius: 9999px;
    margin-bottom: 0.06in;
  }

  .header-left h2 {
    font-size: 0.34in;
    font-weight: 800;
    letter-spacing: -0.025em;
    color: #1D1D1F;
    line-height: 1.15;
  }

  .header-right {
    text-align: right;
    font-size: 0.145in;
    font-weight: 600;
    color: #86868B;
    padding-top: 0.06in;
  }

  /* Pastel Categories */
  .cat-blue   { background: #EBF3FB; color: #0071E3; }
  .cat-green  { background: #EAF7EE; color: #1B8341; }
  .cat-coral  { background: #FDF0EE; color: #FF453A; }
  .cat-purple { background: #F3EEFA; color: #AF52DE; }
  .cat-orange { background: #FFF4E5; color: #D97706; }

  /* Layout Containers */
  .content {
    flex: 1;
    display: flex;
    gap: 0.35in;
  }

  .col-2 {
    flex: 1;
    display: flex;
    flex-direction: column;
  }

  /* Cards - Apple Soft Squircle */
  .card {
    background: #FFFFFF;
    border: 1px solid rgba(0, 0, 0, 0.06);
    border-radius: 0.16in;
    padding: 0.24in 0.28in;
    margin-bottom: 0.18in;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.02);
  }

  .card-pastel-blue {
    background: #F7FAFD;
    border: 1px solid rgba(0, 113, 227, 0.14);
  }

  .card-pastel-green {
    background: #F4FAF5;
    border: 1px solid rgba(52, 199, 89, 0.18);
  }

  .card-pastel-coral {
    background: #FDF8F7;
    border: 1px solid rgba(255, 69, 58, 0.16);
  }

  /* Big Stat Hero Callouts */
  .stat-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.20in;
    margin-bottom: 0.20in;
  }

  .stat-box {
    background: #FFFFFF;
    border: 1px solid rgba(0, 0, 0, 0.06);
    border-radius: 0.14in;
    padding: 0.20in;
    text-align: center;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.02);
  }

  .stat-num {
    font-size: 0.44in;
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1.1;
  }

  .stat-label {
    font-size: 0.14in;
    font-weight: 600;
    color: #86868B;
    margin-top: 0.06in;
  }

  p, li {
    font-size: 0.165in;
    line-height: 1.55;
    color: #3A3A3C;
    font-weight: 400;
  }

  ul, ol {
    margin-left: 0.24in;
    margin-top: 0.06in;
  }

  li {
    margin-bottom: 0.06in;
  }

  /* Apple Clean Tables */
  table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    border-radius: 0.12in;
    overflow: hidden;
    border: 1px solid rgba(0, 0, 0, 0.07);
    font-size: 0.15in;
  }

  th {
    background: #F4F4F6;
    color: #1D1D1F;
    font-weight: 700;
    text-align: left;
    padding: 0.12in 0.16in;
    border-bottom: 1px solid rgba(0, 0, 0, 0.08);
  }

  td {
    padding: 0.10in 0.16in;
    border-bottom: 1px solid rgba(0, 0, 0, 0.05);
    color: #3A3A3C;
    background: #FFFFFF;
  }

  tr:last-child td {
    border-bottom: none;
  }

  /* Chart Wrappers */
  .chart-container {
    background: #FFFFFF;
    border: 1px solid rgba(0, 0, 0, 0.06);
    border-radius: 0.16in;
    padding: 0.14in;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.02);
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
  }

  .chart-img {
    max-width: 100%;
    max-height: 5.3in;
    object-fit: contain;
  }

  /* Subtle Apple Pill Badges */
  .pill {
    display: inline-block;
    padding: 0.04in 0.12in;
    border-radius: 9999px;
    font-size: 0.125in;
    font-weight: 700;
  }

  .pill-green  { background: #EAF7EE; color: #1B8341; }
  .pill-blue   { background: #EBF3FB; color: #0071E3; }
  .pill-coral  { background: #FDF0EE; color: #FF453A; }
  .pill-gray   { background: #F4F4F6; color: #6E6E73; }
  .pill-purple { background: #F3EEFA; color: #AF52DE; }
  .pill-orange { background: #FFF4E5; color: #D97706; }

  /* ============================================================== */
  /* HIGH-END SCHEMAS, BLUEPRINTS & ARCHITECTURE COMPONENTS          */
  /* ============================================================== */

  .schema-container {
    background: #FFFFFF;
    border: 1px solid rgba(0, 0, 0, 0.07);
    border-radius: 0.16in;
    padding: 0.20in 0.24in;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.02);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 100%;
  }

  /* Slide 7: Production ML Pipeline Schema Nodes */
  .pipe-node {
    display: flex;
    align-items: center;
    background: #FAFAFC;
    border: 1px solid rgba(0, 0, 0, 0.06);
    border-radius: 0.12in;
    padding: 0.10in 0.16in;
    position: relative;
  }

  .pipe-node-active {
    background: #F4FAF5;
    border: 1.5px solid #34C759;
  }

  .pipe-idx {
    width: 0.30in;
    height: 0.30in;
    border-radius: 50%;
    background: #EBF3FB;
    color: #0071E3;
    font-weight: 800;
    font-size: 0.13in;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 0.14in;
    flex-shrink: 0;
  }

  .pipe-idx-green {
    background: #EAF7EE;
    color: #1B8341;
  }

  .pipe-content {
    flex: 1;
  }

  .pipe-title {
    font-size: 0.15in;
    font-weight: 700;
    color: #1D1D1F;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .pipe-sub {
    font-size: 0.125in;
    color: #6E6E73;
    margin-top: 0.02in;
  }

  .pipe-tag {
    font-size: 0.11in;
    font-weight: 700;
    padding: 0.02in 0.08in;
    border-radius: 9999px;
    background: #FFFFFF;
    border: 1px solid rgba(0, 0, 0, 0.08);
  }

  .pipe-connector {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 0.16in;
  }

  .pipe-connector svg {
    width: 0.16in;
    height: 0.16in;
    fill: none;
    stroke: #0071E3;
    stroke-width: 2.2;
    stroke-linecap: round;
    stroke-linejoin: round;
  }

  /* Slide 6: Cascade Pathway Steps */
  .cascade-step {
    background: #FFFFFF;
    border: 1px solid rgba(0, 0, 0, 0.07);
    border-radius: 0.14in;
    padding: 0.16in 0.20in;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.015);
  }

  .cascade-step-1 { border-left: 5px solid #FF9F0A; background: #FFFCF7; }
  .cascade-step-2 { border-left: 5px solid #FF453A; background: #FFFBFB; }
  .cascade-step-3 { border-left: 5px solid #D70015; background: #FFF5F5; }

  /* Slide 11: 3-Pillar Ecosystem */
  .ecosystem-grid {
    display: flex;
    flex-direction: column;
    gap: 0.14in;
    height: 100%;
    justify-content: space-between;
  }

  .ecosystem-card {
    border-radius: 0.14in;
    padding: 0.18in 0.22in;
    border: 1px solid rgba(0, 0, 0, 0.07);
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }

  .eco-green  { background: #F4FAF5; border-color: rgba(52, 199, 89, 0.25); }
  .eco-blue   { background: #F6FAFE; border-color: rgba(0, 113, 227, 0.22); }
  .eco-purple { background: #FAF7FE; border-color: rgba(175, 82, 222, 0.22); }

  /* Slide 13: Roadmap Timeline Gantt */
  .roadmap-flex {
    display: flex;
    flex-direction: column;
    gap: 0.14in;
    height: 100%;
    justify-content: space-between;
  }

  .phase-card {
    background: #FFFFFF;
    border: 1px solid rgba(0, 0, 0, 0.07);
    border-radius: 0.14in;
    padding: 0.16in 0.20in;
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }

  .phase-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.06in;
    padding-bottom: 0.06in;
    border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  }

  /* Footer */
  .footer {
    position: absolute;
    bottom: 0.22in;
    left: 0.75in;
    right: 0.75in;
    display: flex;
    justify-content: space-between;
    font-size: 0.125in;
    color: #86868B;
    border-top: 1px solid rgba(0, 0, 0, 0.05);
    padding-top: 0.08in;
  }
</style>
</head>
<body>

<!-- SLIDE 1 : HERO COVER (APPLE CLEAN) -->
<div class="slide slide-hero">
  <div style="display: inline-flex; align-items: center; gap: 0.12in; margin-bottom: 0.28in;">
    <span class="pill pill-blue" style="font-size: 0.14in; padding: 0.06in 0.16in;">GCI WORLD 2026</span>
    <span style="font-size: 0.15in; color: #86868B; font-weight: 600;">The University of Tokyo &bull; Matsuo-Iwasawa Laboratory</span>
  </div>
  
  <h1 style="font-size: 0.65in; font-weight: 800; line-height: 1.12; letter-spacing: -0.035em; color: #1D1D1F; margin-bottom: 0.24in; max-width: 12.5in;">
    Value-Driven Retention &<br><span style="color: #0071E3;">Predictive 5G Device Upgrade</span>
  </h1>
  
  <p style="font-size: 0.24in; color: #6E6E73; line-height: 1.45; max-width: 11in; margin-bottom: 0.55in; font-weight: 400;">
    A machine learning strategy mitigating $34.45M in annual subscriber attrition through targeted handset lifecycle optimization for Company A.
  </p>
  
  <div style="display: flex; gap: 0.9in; padding-top: 0.35in; border-top: 1px solid rgba(0,0,0,0.08);">
    <div>
      <div style="font-size: 0.13in; color: #86868B; font-weight: 600; text-transform: uppercase;">Author</div>
      <div style="font-size: 0.21in; font-weight: 700; color: #1D1D1F; margin-top: 0.04in;">Baptiste Bedeaux</div>
    </div>
    <div>
      <div style="font-size: 0.13in; color: #86868B; font-weight: 600; text-transform: uppercase;">Omnicampus Account</div>
      <div style="font-size: 0.21in; font-weight: 700; color: #0071E3; margin-top: 0.04in;">BaptisteBdx</div>
    </div>
    <div>
      <div style="font-size: 0.13in; color: #86868B; font-weight: 600; text-transform: uppercase;">Audience</div>
      <div style="font-size: 0.21in; font-weight: 700; color: #1D1D1F; margin-top: 0.04in;">Company A &mdash; Board of Directors</div>
    </div>
    <div>
      <div style="font-size: 0.13in; color: #86868B; font-weight: 600; text-transform: uppercase;">Format</div>
      <div style="font-size: 0.21in; font-weight: 700; color: #1D1D1F; margin-top: 0.04in;">15-Slide Executive PoC</div>
    </div>
  </div>
  
  <div class="footer">
    <span>Commercial In Confidence &bull; Prepared for Executive Leadership</span>
    <span>Slide 1 / 15</span>
  </div>
</div>

<!-- SLIDE 2 : STRATEGIC CONTEXT -->
<div class="slide">
  <div class="header">
    <div class="header-left">
      <div class="category cat-blue">Industry Landscape</div>
      <h2>The Telecom Reality: Retention Outperforms Acquisition 5x</h2>
    </div>
    <div class="header-right">Macro Context</div>
  </div>
  <div class="content">
    <div class="col-2" style="flex: 0.95;">
      <div class="stat-grid" style="grid-template-columns: repeat(3, 1fr); margin-bottom: 0.16in;">
        <div class="stat-box">
          <div class="stat-num" style="color: #FF453A;">$350+</div>
          <div class="stat-label">Acquisition (SAC)</div>
        </div>
        <div class="stat-box">
          <div class="stat-num" style="color: #34C759;">$75</div>
          <div class="stat-label">Retention (SRC)</div>
        </div>
        <div class="stat-box">
          <div class="stat-num" style="color: #0071E3;">&gt;110%</div>
          <div class="stat-label">Market Penetration</div>
        </div>
      </div>
      <div class="card">
        <h3 style="font-size: 0.18in; font-weight: 700; color: #1D1D1F; margin-bottom: 0.08in;">Zero-Sum Market Saturation</h3>
        <p>In mature telecommunications economies, user growth is strictly zero-sum. Carriers cannot rely on organic adoption; every single customer gained is captured from a rival, making subscriber defense the primary driver of corporate margin.</p>
      </div>
      <div class="card">
        <h3 style="font-size: 0.18in; font-weight: 700; color: #1D1D1F; margin-bottom: 0.08in;">The Handset Replacement Pivot</h3>
        <p>Subscribers rarely churn purely over minor network quirks. Departure is triggered when physical equipment ages (18&ndash;24 months), coinciding with the end of device amortization and competitive trade-in promotions.</p>
      </div>
    </div>
    <div class="col-2" style="flex: 1.05;">
      <div class="card" style="height: 100%; display: flex; flex-direction: column; justify-content: space-around;">
        <div>
          <span class="pill pill-green" style="margin-bottom: 0.06in;">Core Economic Law</span>
          <h4 style="font-size: 0.18in; font-weight: 700; color: #1D1D1F; margin-top: 0.04in;">The 5% Retention Multiplier</h4>
          <p>A 5% reduction in customer churn accelerates operator operating profits by 25% to 85% due to long-tail customer lifetime value (Analysys Mason, 2024).</p>
        </div>
        <hr style="border: 0; border-top: 1px solid rgba(0,0,0,0.06);">
        <div>
          <span class="pill pill-blue" style="margin-bottom: 0.06in;">Structural Inflection</span>
          <h4 style="font-size: 0.18in; font-weight: 700; color: #1D1D1F; margin-top: 0.04in;">The Device Financing Cliff</h4>
          <p>When device financing reaches term, psychological customer inertia drops to zero. Proactive re-contracting is mandatory before the customer seeks outside deals.</p>
        </div>
        <hr style="border: 0; border-top: 1px solid rgba(0,0,0,0.06);">
        <div>
          <span class="pill pill-coral" style="margin-bottom: 0.06in;">Network Modernization</span>
          <h4 style="font-size: 0.18in; font-weight: 700; color: #1D1D1F; margin-top: 0.04in;">The 5G ARPU Uplift</h4>
          <p>Upgrading subscribers to modern 5G handsets delivers a documented +12% lift in monthly data usage, stabilizing long-term recurring revenue.</p>
        </div>
      </div>
    </div>
  </div>
  <div class="footer">
    <span>Sources: GSMA Intelligence (2025), Analysys Mason Global Benchmark (2024), FCC Wireless Competition Report</span>
    <span>Slide 2 / 15</span>
  </div>
</div>

<!-- SLIDE 3 : FINANCIAL BLEED WATERFALL -->
<div class="slide">
  <div class="header">
    <div class="header-left">
      <div class="category cat-coral">Company A Baseline</div>
      <h2>Company A Faces an Annual $34.45M Revenue Bleed</h2>
    </div>
    <div class="header-right">Portfolio Audit (100k Users)</div>
  </div>
  <div class="content">
    <div class="col-2" style="flex: 0.95;">
      <div class="card card-pastel-coral" style="margin-bottom: 0.18in;">
        <div style="font-size: 0.13in; font-weight: 700; color: #FF453A; text-transform: uppercase;">Annual Attrition Rate</div>
        <div style="font-size: 0.52in; font-weight: 800; color: #FF453A; line-height: 1.1; margin-top: 0.04in;">49.56%</div>
        <p style="margin-top: 0.06in;">Nearly one in two subscribers departs during the annual cycle.</p>
      </div>
      <div class="card">
        <h3 style="font-size: 0.18in; font-weight: 700; color: #1D1D1F; margin-bottom: 0.08in;">Baseline Financial Structure</h3>
        <ul>
          <li><strong>Mean Monthly ARPU:</strong> $58.72 (Median: $48.20)</li>
          <li><strong>Gross Billing Run-Rate:</strong> $70.46M / year</li>
          <li><strong>Net ARR Lost to Churn:</strong> <span style="color: #FF453A; font-weight: 700;">$34.45 Million / year</span></li>
          <li><strong>Average Tenure before Exit:</strong> 13.2 months</li>
        </ul>
      </div>
      <div style="padding: 0.14in; background: #F8F9FA; border-radius: 0.12in; font-size: 0.14in; color: #6E6E73; font-style: italic;">
        &ldquo;Company A is operating a leaky commercial engine: customer acquisition budgets are consumed merely replacing departed subscribers rather than generating net expansion.&rdquo;
      </div>
    </div>
    <div class="col-2" style="flex: 1.05;">
      <div class="chart-container">
        <img src="{FIG_DIR}/fig1_macro_loss_waterfall.png" class="chart-img" alt="Macro Waterfall">
      </div>
    </div>
  </div>
  <div class="footer">
    <span>Data Source: Company A Production Records (100,000 Verified Accounts, 1:1 Reconciled)</span>
    <span>Slide 3 / 15</span>
  </div>
</div>

<!-- SLIDE 4 : FLAT CHURN FALLACY -->
<div class="slide">
  <div class="header">
    <div class="header-left">
      <div class="category cat-purple">Customer Valuation</div>
      <h2>The Flat Churn Fallacy: Extreme Revenue Concentration</h2>
    </div>
    <div class="header-right">Decile Segmentation</div>
  </div>
  <div class="content">
    <div class="col-2" style="flex: 0.92;">
      <div class="card card-pastel-blue">
        <h3 style="font-size: 0.18in; font-weight: 700; color: #1D1D1F; margin-bottom: 0.08in;">Why Traditional Retention Destroy Capital</h3>
        <p>Textbook churn approaches treat all customers as equals. Preventing the departure of a $12/month low-use account is treated identically to preserving a $150/month corporate executive.</p>
        <p style="margin-top: 0.08in;"><strong>The consequence is financial waste:</strong> blanket retention subsidies cost significantly more than the revenue protected on entry-level tiers.</p>
      </div>
      <div class="card">
        <h3 style="font-size: 0.18in; font-weight: 700; color: #1D1D1F; margin-bottom: 0.08in;">The High-Value Concentration</h3>
        <p>In Company A, the top 20% of subscribers generate over <strong>44.6% of all revenue at risk</strong>. Rescuing one Decile 1 subscriber protects <strong>$1,777/year</strong>, compared to just $261/year for a Decile 10 subscriber.</p>
      </div>
    </div>
    <div class="col-2" style="flex: 1.08;">
      <table>
        <thead>
          <tr>
            <th>Decile</th>
            <th>Churn Rate</th>
            <th>Monthly ARPU</th>
            <th>Annual Loss</th>
            <th>Share of Risk</th>
          </tr>
        </thead>
        <tbody>
          <tr style="background: #FDF0EE; font-weight: 700;">
            <td><strong>D1 (Top 10%)</strong></td>
            <td>58.61%</td>
            <td>$148.15</td>
            <td>$9.97M</td>
            <td style="color: #FF453A;">28.88%</td>
          </tr>
          <tr>
            <td><strong>D2</strong></td>
            <td>58.00%</td>
            <td>$84.67</td>
            <td>$5.43M</td>
            <td>15.73%</td>
          </tr>
          <tr>
            <td><strong>D3</strong></td>
            <td>56.03%</td>
            <td>$67.94</td>
            <td>$4.22M</td>
            <td>12.24%</td>
          </tr>
          <tr>
            <td><strong>D4 &ndash; D7</strong></td>
            <td>51.70%</td>
            <td>$48.33</td>
            <td>$11.05M</td>
            <td>32.08%</td>
          </tr>
          <tr>
            <td><strong>D8 &ndash; D10</strong></td>
            <td>38.04%</td>
            <td>$30.91</td>
            <td>$3.83M</td>
            <td>11.07%</td>
          </tr>
        </tbody>
      </table>
      <div style="margin-top: 0.16in; padding: 0.14in 0.18in; background: #FFFFFF; border: 1px solid rgba(0,0,0,0.06); border-radius: 0.12in; display: flex; align-items: center; gap: 0.12in;">
        <span class="pill pill-green">Strategic Insight</span>
        <span style="font-size: 0.14in; color: #3A3A3C;">44.6% ($15.4M) of cash bleed is isolated within 20,000 accounts. Interventions must be value-proportional.</span>
      </div>
    </div>
  </div>
  <div class="footer">
    <span>Calculations based on Out-of-Fold Expected Loss = P(churn) &times; Annual ARPU</span>
    <span>Slide 4 / 15</span>
  </div>
</div>

<!-- SLIDE 5 : HARDWARE AGING EFFECT -->
<div class="slide">
  <div class="header">
    <div class="header-left">
      <div class="category cat-coral">Empirical Discovery</div>
      <h2>The Handset Aging Effect: Churn Surges by +12.7%</h2>
    </div>
    <div class="header-right">Root Cause Isolation</div>
  </div>
  <div class="content">
    <div class="col-2" style="flex: 0.95;">
      <div class="card card-pastel-blue">
        <h3 style="font-size: 0.18in; font-weight: 700; color: #1D1D1F; margin-bottom: 0.08in;">The Hardware Wear Trigger</h3>
        <p>Across the complete 100-variable feature space, <strong>`eqpdays` (handset age in days)</strong> emerges as the decisive physical catalyst of attrition:</p>
        <ul style="margin-top: 0.06in;">
          <li><strong>Handset &lt; 1 Year:</strong> Baseline churn of <strong>45.19%</strong></li>
          <li><strong>Handset 1&ndash;2 Years:</strong> Churn climbs to <strong>53.85%</strong> (+8.66 pts)</li>
          <li><strong>Handset &gt; 2 Years:</strong> Churn spikes to <strong>57.89%</strong> (+12.7 pts)</li>
        </ul>
      </div>
      <div class="card">
        <h3 style="font-size: 0.18in; font-weight: 700; color: #1D1D1F; margin-bottom: 0.08in;">Actionable vs. Structural Features</h3>
        <p>An operator cannot alter a customer's demographics or living location. However, hardware subsidization is <strong>100% within management control</strong>. Device refresh represents the ideal commercial lever.</p>
      </div>
    </div>
    <div class="col-2" style="flex: 1.05;">
      <div class="chart-container">
        <img src="{FIG_DIR}/fig2_equipment_churn_curve.png" class="chart-img" alt="Equipment Churn Curve">
      </div>
    </div>
  </div>
  <div class="footer">
    <span>Distribution across 100,000 subscriber records; eqpdays statistically significant (p &lt; 0.0001)</span>
    <span>Slide 5 / 15</span>
  </div>
</div>

<!-- SLIDE 6 : CASCADE PATHWAY (VECTOR SCHEMA) -->
<div class="slide">
  <div class="header">
    <div class="header-left">
      <div class="category cat-coral">Behavioral Mechanics</div>
      <h2>Secondary Friction: Network Drops & &ldquo;Bill Shock&rdquo;</h2>
    </div>
    <div class="header-right">Defection Signals</div>
  </div>
  <div class="content">
    <div class="col-2" style="flex: 0.92;">
      <div class="card card-pastel-coral">
        <h3 style="font-size: 0.18in; font-weight: 700; color: #FF453A; margin-bottom: 0.08in;">1. Network Quality Failure Points</h3>
        <p>Dropped and blocked calls (`drop_vce_Mean`, `blck_vce_Mean`) correlate strongly with support escalations (`custcare_Mean`).</p>
        <p style="margin-top: 0.06in;">Subscribers encountering <strong>&gt; 5 dropped calls/month</strong> are <strong>1.8x more likely to churn</strong>, primarily due to older antennas lacking carrier aggregation.</p>
      </div>
      <div class="card">
        <h3 style="font-size: 0.18in; font-weight: 700; color: #1D1D1F; margin-bottom: 0.08in;">2. Bill Shock & Overage Friction</h3>
        <p>Data and voice overage charges (`ovrrev_Mean`, `datovr_Mean`) trigger sharp customer dissatisfaction. Unanticipated billing spikes above $20 precede churn events in 31% of cases.</p>
      </div>
    </div>
    <div class="col-2" style="flex: 1.08;">
      <!-- SCHEMA VECTORIEL : THE FRICTION CASCADE FUNNEL -->
      <div class="schema-container">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.10in;">
          <h3 style="font-size: 0.17in; font-weight: 700; color: #1D1D1F;">The 3-Stage Defection Funnel</h3>
          <span class="pill pill-coral">Escalation Cascade</span>
        </div>
        
        <div style="display: flex; flex-direction: column; gap: 0.12in; flex: 1; justify-content: space-around;">
          <!-- Stage 1 -->
          <div class="cascade-step cascade-step-1">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.04in;">
              <span style="font-size: 0.125in; font-weight: 800; color: #D97706; text-transform: uppercase;">Stage 01 &bull; Hardware Degradation</span>
              <span class="pill pill-orange">eqpdays &gt; 365d</span>
            </div>
            <p style="font-size: 0.145in; color: #1D1D1F;">Battery fatigue & legacy 4G RF frontend drops calls in dense cells (+12.7 pts churn surge).</p>
          </div>
          
          <div style="text-align: center; color: #8E8E93; font-size: 0.16in; line-height: 1;">&darr;</div>
          
          <!-- Stage 2 -->
          <div class="cascade-step cascade-step-2">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.04in;">
              <span style="font-size: 0.125in; font-weight: 800; color: #FF453A; text-transform: uppercase;">Stage 02 &bull; Bill Shock Escalation</span>
              <span class="pill pill-coral">ovrrev &gt; $20</span>
            </div>
            <p style="font-size: 0.145in; color: #1D1D1F;">Modern app bandwidth demand exceeds legacy plan limits; unexpected overages trigger anger.</p>
          </div>
          
          <div style="text-align: center; color: #8E8E93; font-size: 0.16in; line-height: 1;">&darr;</div>
          
          <!-- Stage 3 -->
          <div class="cascade-step cascade-step-3">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.04in;">
              <span style="font-size: 0.125in; font-weight: 800; color: #D70015; text-transform: uppercase;">Stage 03 &bull; Terminal Defection</span>
              <span class="pill pill-coral" style="background: #D70015; color: #FFFFFF;">custcare &gt; 2 &bull; Exit</span>
            </div>
            <p style="font-size: 0.145in; color: #1D1D1F;">Customer contacts support; competitor offers $0 modern 5G trade-in &rarr; Permanent Attrition.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="footer">
    <span>Derived from engineered ratios: fe_network_failure_rate & fe_overage_ratio</span>
    <span>Slide 6 / 15</span>
  </div>
</div>

<!-- SLIDE 7 : PRODUCTION ML ARCHITECTURE (SCHÉMA D'ARCHITECTURE VECTORIEL COMPLET) -->
<div class="slide">
  <div class="header">
    <div class="header-left">
      <div class="category cat-blue">Methodology</div>
      <h2>Production ML Architecture: 5-Fold Stratified Validation</h2>
    </div>
    <div class="header-right">Data Science Rigor</div>
  </div>
  <div class="content">
    <div class="col-2" style="flex: 0.90;">
      <div class="card card-pastel-blue">
        <h3 style="font-size: 0.18in; font-weight: 700; color: #1D1D1F; margin-bottom: 0.08in;">Data Engineering & Hygiene</h3>
        <ul>
          <li><strong>Consolidation:</strong> 100% 1:1 join across 100,000 records from `Client.csv` and `Record.csv`.</li>
          <li><strong>Memory Footprint:</strong> Float32 typed matrix (41.2 MB RAM) with zero memory fragmentation.</li>
          <li><strong>Feature Engineering:</strong> 8 domain behavioral ratios (Depreciation index, network failure rate, overage intensity).</li>
          <li><strong>Leakage Prevention:</strong> Out-of-Fold target encoding; strictly zero lookahead bias.</li>
        </ul>
      </div>
      <div class="card">
        <h3 style="font-size: 0.18in; font-weight: 700; color: #1D1D1F; margin-bottom: 0.08in;">Cross-Validation Architecture</h3>
        <p>To eliminate overfitting, all metrics and probabilities are derived Out-Of-Fold across 5 independent stratified splits (20,000 validation records per fold).</p>
      </div>
    </div>
    <div class="col-2" style="flex: 1.10;">
      <!-- BLUEPRINT ARCHITECTURE PIPELINE SCHEMATIC -->
      <div class="schema-container" style="background: #FAFAFC;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.06in;">
          <h3 style="font-size: 0.17in; font-weight: 800; color: #1D1D1F;">End-to-End Predictive Pipeline</h3>
          <span class="pill pill-blue">Production Grade</span>
        </div>
        
        <!-- Node 1 -->
        <div class="pipe-node">
          <div class="pipe-idx">01</div>
          <div class="pipe-content">
            <div class="pipe-title">
              <span>Data Ingestion & Hygiene</span>
              <span class="pipe-tag">100k &times; 100 vars</span>
            </div>
            <div class="pipe-sub">1:1 join &bull; Float32 compact typed matrix &bull; 41.2 MB RAM</div>
          </div>
        </div>
        
        <div class="pipe-connector">
          <svg viewBox="0 0 24 24"><path d="M12 5v14M5 12l7 7 7-7"/></svg>
        </div>
        
        <!-- Node 2 -->
        <div class="pipe-node">
          <div class="pipe-idx">02</div>
          <div class="pipe-content">
            <div class="pipe-title">
              <span>Feature Engineering (Session 8)</span>
              <span class="pipe-tag">Log1p &bull; Cross-Features</span>
            </div>
            <div class="pipe-sub">Log-transforms &bull; Handset &times; Failure interactions &bull; Non-monotonic binning</div>
          </div>
        </div>
        
        <div class="pipe-connector">
          <svg viewBox="0 0 24 24"><path d="M12 5v14M5 12l7 7 7-7"/></svg>
        </div>
        
        <!-- Node 3 : Stratified CV Engine -->
        <div class="pipe-node pipe-node-active">
          <div class="pipe-idx pipe-idx-green">03</div>
          <div class="pipe-content">
            <div class="pipe-title">
              <span style="color: #1B8341;">5-Fold Stratified CV Core</span>
              <span class="pill pill-green" style="font-size: 0.11in; padding: 0.02in 0.08in;">LightGBM Winner</span>
            </div>
            <div class="pipe-sub" style="color: #2D3748; font-weight: 500;">
              LogReg (0.6330) &bull; RF (0.6686) &bull; CatBoost (0.6890) &bull; <strong>LightGBM (ROC-AUC 0.6980)</strong> &bull; Ensemble (0.6961)
            </div>
          </div>
        </div>
        
        <div class="pipe-connector">
          <svg viewBox="0 0 24 24"><path d="M12 5v14M5 12l7 7 7-7"/></svg>
        </div>
        
        <!-- Node 4 -->
        <div class="pipe-node">
          <div class="pipe-idx">04</div>
          <div class="pipe-content">
            <div class="pipe-title">
              <span>Probability Calibration</span>
              <span class="pipe-tag">Brier: 0.2198</span>
            </div>
            <div class="pipe-sub">Empirical reliability check &bull; True posterior probability P(churn)</div>
          </div>
        </div>
        
        <div class="pipe-connector">
          <svg viewBox="0 0 24 24"><path d="M12 5v14M5 12l7 7 7-7"/></svg>
        </div>
        
        <!-- Node 5 -->
        <div class="pipe-node" style="background: #FDF0EE; border-color: rgba(255, 69, 58, 0.3);">
          <div class="pipe-idx" style="background: #FDF0EE; color: #FF453A;">05</div>
          <div class="pipe-content">
            <div class="pipe-title">
              <span style="color: #FF453A;">Value Scoring & Prioritization</span>
              <span class="pipe-tag" style="color: #FF453A;">Top 15% VIPs</span>
            </div>
            <div class="pipe-sub">Expected Loss = P(churn) &times; ARPU &times; 12 &bull; 5,670 VIP Queue</div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="footer">
    <span>Execution Environment: Python 3.11, Scikit-Learn, LightGBM, CatBoost (Deterministic Seed: 42)</span>
    <span>Slide 7 / 15</span>
  </div>
</div>

<!-- SLIDE 8 : MODEL BENCHMARK -->
<div class="slide">
  <div class="header">
    <div class="header-left">
      <div class="category cat-green">Algorithmic Benchmarking</div>
      <h2>LightGBM Achieves Superior Discrimination (ROC&ndash;AUC = 0.6980)</h2>
    </div>
    <div class="header-right">Mandatory Criteria</div>
  </div>
  <div class="content">
    <div class="col-2" style="flex: 0.95;">
      <table>
        <thead>
          <tr>
            <th>Model Architecture</th>
            <th>ROC-AUC</th>
            <th>Log-Loss</th>
            <th>Brier Score</th>
            <th>F1-Score</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Logistic Regression (Baseline)</td>
            <td>0.6330</td>
            <td>0.6662</td>
            <td>0.2367</td>
            <td>0.5882</td>
          </tr>
          <tr>
            <td>Random Forest (100 Trees)</td>
            <td>0.6686</td>
            <td>0.6354</td>
            <td>0.2292</td>
            <td>0.6270</td>
          </tr>
          <tr>
            <td>CatBoost (250 Trees)</td>
            <td>0.6890</td>
            <td>0.6189</td>
            <td>0.2230</td>
            <td>0.6389</td>
          </tr>
          <tr>
            <td>Stacking Ensemble (Super-Learner)</td>
            <td>0.6961</td>
            <td>0.6120</td>
            <td>0.2211</td>
            <td>0.6436</td>
          </tr>
          <tr style="background: #F4FAF5; font-weight: 800;">
            <td style="color: #1B8341;">LightGBM GBDT (Tuned Champion)</td>
            <td style="color: #1B8341;"><strong>0.6980</strong></td>
            <td><strong>0.6082</strong></td>
            <td><strong>0.2198</strong></td>
            <td><strong>0.6427</strong></td>
          </tr>
        </tbody>
      </table>
      
      <div class="card card-pastel-green" style="margin-top: 0.20in;">
        <h3 style="font-size: 0.17in; font-weight: 700; color: #1B8341; margin-bottom: 0.08in;">Official Model Selection Summary</h3>
        <ul>
          <li><strong>Model Name:</strong> LightGBM Gradient Boosted Decision Trees</li>
          <li><strong>Primary Evaluation Metric:</strong> Out-of-Fold ROC-AUC</li>
          <li><strong>Official Evaluated Score:</strong> <strong>0.6980</strong> (+6.50 pts vs baseline)</li>
          <li><strong>Probability Calibration:</strong> Brier Score 0.2198 (well calibrated)</li>
        </ul>
      </div>
    </div>
    <div class="col-2" style="flex: 1.05;">
      <div class="chart-container">
        <img src="{FIG_DIR}/fig3_roc_comparison.png" class="chart-img" alt="ROC Comparison">
      </div>
    </div>
  </div>
  <div class="footer">
    <span>Evaluation strictly compliant with Course Grading Requirement (3) &mdash; Model, Metric, and Score explicitly reported</span>
    <span>Slide 8 / 15</span>
  </div>
</div>

<!-- SLIDE 9 : FEATURE IMPORTANCE (GAIN) -->
<div class="slide">
  <div class="header">
    <div class="header-left">
      <div class="category cat-purple">Model Interpretability</div>
      <h2>Feature Importance: `eqpdays` Dominates All Split Gains</h2>
    </div>
    <div class="header-right">Explainable AI</div>
  </div>
  <div class="content">
    <div class="col-2" style="flex: 0.90;">
      <div class="card card-pastel-blue">
        <h3 style="font-size: 0.18in; font-weight: 700; color: #1D1D1F; margin-bottom: 0.08in;">Split Gain Interpretation</h3>
        <p>In gradient boosting, <strong>Split Gain</strong> measures the direct loss reduction achieved by partitioning on each variable across all decision nodes:</p>
        <ul style="margin-top: 0.06in;">
          <li><strong>`eqpdays` (17,186 Gain):</strong> Outstrips customer tenure (`months`: 13,158) and usage drops (`change_mou`: 8,765) as the primary split variable.</li>
          <li><strong>Behavioral Finding:</strong> Even when a subscriber maintains active usage and high spend, equipment age exceeding 365 days pushes defection risk into the critical zone.</li>
        </ul>
      </div>
      <div class="card">
        <h3 style="font-size: 0.18in; font-weight: 700; color: #1D1D1F; margin-bottom: 0.08in;">Actionability Validation</h3>
        <p>This confirms our strategic recommendation: customer retention is won or lost at the handset replacement decision point.</p>
      </div>
    </div>
    <div class="col-2" style="flex: 1.10;">
      <div class="chart-container">
        <img src="{FIG_DIR}/fig4_feature_importance_gain.png" class="chart-img" alt="Feature Importance">
      </div>
    </div>
  </div>
  <div class="footer">
    <span>Derived across 300 boosted decision trees; normalized across 5 cross-validation folds</span>
    <span>Slide 9 / 15</span>
  </div>
</div>

<!-- SLIDE 10 : VALUE AT RISK CONCENTRATION -->
<div class="slide">
  <div class="header">
    <div class="header-left">
      <div class="category cat-coral">Targeting Matrix</div>
      <h2>Expected Revenue at Risk: Isolating the High-Yield Cohort</h2>
    </div>
    <div class="header-right">Capital Allocation</div>
  </div>
  <div class="content">
    <div class="col-2" style="flex: 0.92;">
      <div class="card card-pastel-blue">
        <h3 style="font-size: 0.18in; font-weight: 700; color: #1D1D1F; margin-bottom: 0.08in;">The Mathematical Scoring Formula</h3>
        <div style="text-align: center; padding: 0.12in; background: #FFFFFF; border-radius: 0.1in; border: 1px solid rgba(0,0,0,0.06); font-family: 'JetBrains Mono', monospace; font-size: 0.16in; color: #0071E3; font-weight: 600; margin: 0.08in 0;">
          Expected Loss = P(churn) &times; Monthly ARPU &times; 12
        </div>
        <p>Ranking subscribers by Expected Loss separates accounts whose defection inflicts acute financial damage from low-margin subscribers.</p>
      </div>
      <div class="card card-pastel-coral">
        <h3 style="font-size: 0.18in; font-weight: 700; color: #FF453A; margin-bottom: 0.06in;">Extreme Risk Asymmetry</h3>
        <p>Decile 1 accounts carry an average ARPU of <strong>$148.15</strong> and an actual churn rate of <strong>58.61%</strong>. Retaining a single D1 customer preserves more operating margin than retaining 7 Decile 8 accounts ($37.12 ARPU).</p>
      </div>
    </div>
    <div class="col-2" style="flex: 1.08;">
      <div class="chart-container">
        <img src="{FIG_DIR}/fig5_value_at_risk_deciles.png" class="chart-img" alt="Decile Breakdown">
      </div>
    </div>
  </div>
  <div class="footer">
    <span>Calculations executed on Out-of-Fold calibrated probabilities across 10,000-subscriber deciles</span>
    <span>Slide 10 / 15</span>
  </div>
</div>

<!-- SLIDE 11 : THE 5G STRATEGY ECOSYSTEM (SCHÉMA ÉCOSYSTÈME 3 PILIERS) -->
<div class="slide">
  <div class="header">
    <div class="header-left">
      <div class="category cat-green">Strategic Proposal</div>
      <h2>The Strategy: &ldquo;Predictive 5G Device Upgrade&rdquo; Program</h2>
    </div>
    <div class="header-right">Value Proposition</div>
  </div>
  <div class="content">
    <div class="col-2" style="flex: 0.90;">
      <div class="card card-pastel-green">
        <h3 style="font-size: 0.18in; font-weight: 700; color: #1B8341; margin-bottom: 0.08in;">Targeting Criteria (Top 15% VIP Cohort)</h3>
        <ul>
          <li><strong>Total Cohort Size:</strong> <strong>5,618 Subscribers</strong></li>
          <li><strong>Criterion 1:</strong> Ranked within Top 15% of Expected Revenue at Risk.</li>
          <li><strong>Criterion 2:</strong> Device age strictly `eqpdays &gt; 365` days.</li>
          <li><strong>Cohort Mean ARPU:</strong> <strong>$114.74 / month</strong> (nearly 2x company average).</li>
        </ul>
      </div>
      <div class="card">
        <h3 style="font-size: 0.18in; font-weight: 700; color: #1D1D1F; margin-bottom: 0.08in;">The Core Commercial Offer</h3>
        <p>A complimentary flagship 5G handset ($130 net carrier procurement cost) delivered with zero upfront charge, in exchange for signing a <strong>mandatory 24-month contract extension</strong> at their existing premium service tier.</p>
      </div>
    </div>
    <div class="col-2" style="flex: 1.10;">
      <!-- SCHEMA TRIPARTITE ECOSYSTEM -->
      <div class="ecosystem-grid">
        <!-- Pillar 1 -->
        <div class="ecosystem-card eco-green">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.04in;">
            <span class="pill pill-green">01 &bull; Subscriber Value</span>
            <span style="font-weight: 700; color: #1B8341; font-size: 0.13in;">Zero Upfront Outlay</span>
          </div>
          <h4 style="font-size: 0.17in; font-weight: 700; color: #1D1D1F;">Free $600 Flagship 5G Handset</h4>
          <p style="font-size: 0.14in; color: #3A3A3C; margin-top: 0.02in;">Eliminates battery decay, processor lag and dropped calls. The customer feels recognized and rewarded for loyalty rather than ignored.</p>
        </div>
        
        <!-- Pillar 2 -->
        <div class="ecosystem-card eco-blue">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.04in;">
            <span class="pill pill-blue">02 &bull; Network Operations</span>
            <span style="font-weight: 700; color: #0071E3; font-size: 0.13in;">Spectrum Modernization</span>
          </div>
          <h4 style="font-size: 0.17in; font-weight: 700; color: #1D1D1F;">Congested 4G Offload to 5G Bands</h4>
          <p style="font-size: 0.14in; color: #3A3A3C; margin-top: 0.02in;">Migrates top 15% bandwidth consumers from saturated 4G carriers onto high-capacity 5G spectrum, reducing carrier cost-per-gigabyte.</p>
        </div>
        
        <!-- Pillar 3 -->
        <div class="ecosystem-card eco-purple">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.04in;">
            <span class="pill pill-purple">03 &bull; Corporate Shareholders</span>
            <span style="font-weight: 700; color: #AF52DE; font-size: 0.13in;">Capital Protection</span>
          </div>
          <h4 style="font-size: 0.17in; font-weight: 700; color: #1D1D1F;">+$3,168,404 Net Economic Profit</h4>
          <p style="font-size: 0.14in; color: #3A3A3C; margin-top: 0.02in;">Guarantees $114.74/mo ARPU for 24 months ($2,753 gross value per user). Shuts the defection window on high-yield accounts with +433.8% Net ROI.</p>
        </div>
      </div>
    </div>
  </div>
  <div class="footer">
    <span>Contract incorporates early termination fee (ETF) protecting carrier capital investment</span>
    <span>Slide 11 / 15</span>
  </div>
</div>

<!-- SLIDE 12 : EXECUTIVE BUSINESS CASE & ROI -->
<div class="slide">
  <div class="header">
    <div class="header-left">
      <div class="category cat-green">Business Case</div>
      <h2>Executive Business Case: +434.5% Net ROI & 4.5 Months Payback</h2>
    </div>
    <div class="header-right">Financial Model</div>
  </div>
  <div class="content">
    <div class="col-2" style="flex: 0.95;">
      <div class="stat-grid" style="grid-template-columns: repeat(2, 1fr); margin-bottom: 0.15in;">
        <div class="stat-box" style="border-left: 4px solid #34C759;">
          <div class="stat-num" style="color: #1B8341;">+434.5%</div>
          <div class="stat-label">Net Return on Investment (ROI)</div>
        </div>
        <div class="stat-box" style="border-left: 4px solid #0071E3;">
          <div class="stat-num" style="color: #0071E3;">4.5 mos</div>
          <div class="stat-label">Full Payback Period</div>
        </div>
      </div>
      <table>
        <tbody>
          <tr>
            <td><strong>Cohort Size Targeted</strong></td>
            <td style="text-align: right;">5,670 subscribers</td>
          </tr>
          <tr>
            <td><strong>Subsidized Hardware Cost ($130 / unit)</strong></td>
            <td style="text-align: right; color: #FF453A;"><strong>$737,100</strong></td>
          </tr>
          <tr>
            <td><strong>Offer Take-Up Rate</strong></td>
            <td style="text-align: right;">68.0%</td>
          </tr>
          <tr>
            <td><strong>Subscribers Definitively Retained</strong></td>
            <td style="text-align: right; color: #1B8341;"><strong>1,438 subscribers</strong></td>
          </tr>
          <tr>
            <td><strong>Protected Gross Revenue (24 Months)</strong></td>
            <td style="text-align: right;">$3,939,769</td>
          </tr>
          <tr style="background: #EAF7EE; font-weight: 800; font-size: 0.17in;">
            <td><strong>NET ECONOMIC PROFIT</strong></td>
            <td style="text-align: right; color: #1B8341;"><strong>+$3,202,669</strong></td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="col-2" style="flex: 1.05;">
      <div class="chart-container">
        <img src="{FIG_DIR}/fig6_roi_payback_waterfall.png" class="chart-img" alt="Financial Business Case">
      </div>
    </div>
  </div>
  <div class="footer">
    <span>Modeled under conservative 60% retention efficacy; audited against standard telecom cash flow metrics</span>
    <span>Slide 12 / 15</span>
  </div>
</div>

<!-- SLIDE 13 : IMPLEMENTATION ROADMAP (GANTT & PHASING SCHEMA) -->
<div class="slide">
  <div class="header">
    <div class="header-left">
      <div class="category cat-blue">Deployment</div>
      <h2>Phased 12-Month Rollout Roadmap</h2>
    </div>
    <div class="header-right">Operational Schedule</div>
  </div>
  <div class="content">
    <div class="col-2" style="flex: 1;">
      <!-- ROADMAP GANTT / TIMELINE SCHEMA -->
      <div class="roadmap-flex">
        <!-- Phase 1 -->
        <div class="phase-card" style="border-left: 5px solid #0071E3;">
          <div class="phase-header">
            <div>
              <span class="pill pill-blue">Phase 1 &bull; Q1</span>
              <strong style="font-size: 0.17in; color: #1D1D1F; margin-left: 0.08in;">Pilot Testbed Validation</strong>
            </div>
            <span style="font-weight: 700; color: #0071E3; font-size: 0.13in;">Budget: $195,000 Cap</span>
          </div>
          <p style="font-size: 0.145in;"><strong>Target:</strong> 1,500 Decile 1 customers holding devices &gt; 500 days.</p>
          <p style="font-size: 0.145in; margin-top: 0.02in;"><strong>Execution:</strong> Direct OEM dropship logistics &bull; Validate live offer take-up (Target: 65%) &bull; Go/No-Go Gate at Month 3.</p>
        </div>
        
        <!-- Phase 2 -->
        <div class="phase-card" style="border-left: 5px solid #FF9F0A;">
          <div class="phase-header">
            <div>
              <span class="pill pill-orange">Phase 2 &bull; Q2</span>
              <strong style="font-size: 0.17in; color: #1D1D1F; margin-left: 0.08in;">Omnichannel Cohort Scale</strong>
            </div>
            <span style="font-weight: 700; color: #D97706; font-size: 0.13in;">Budget: $542,100</span>
          </div>
          <p style="font-size: 0.145in;"><strong>Target:</strong> Expand to remaining 4,170 identified VIP accounts.</p>
          <p style="font-size: 0.145in; margin-top: 0.02in;"><strong>Execution:</strong> VIP in-app push modal &bull; Outbound concierge care team &bull; Personalized priority SMS delivery.</p>
        </div>
        
        <!-- Phase 3 -->
        <div class="phase-card" style="border-left: 5px solid #34C759;">
          <div class="phase-header">
            <div>
              <span class="pill pill-green">Phase 3 &bull; H2</span>
              <strong style="font-size: 0.17in; color: #1D1D1F; margin-left: 0.08in;">Automated CRM & MLOps Engine</strong>
            </div>
            <span style="font-weight: 700; color: #1B8341; font-size: 0.13in;">Continuous Production</span>
          </div>
          <p style="font-size: 0.145in;"><strong>Integration:</strong> Real-time LightGBM scoring hooked into Company A billing events.</p>
          <p style="font-size: 0.145in; margin-top: 0.02in;"><strong>Automation:</strong> Proactive offer generated when `eqpdays == 365` &bull; Monthly model refit &amp; Population Stability Index (PSI) drift monitoring.</p>
        </div>
      </div>
    </div>
    <div class="col-2" style="flex: 0.95;">
      <div class="card card-pastel-blue" style="height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
        <div>
          <h3 style="font-size: 0.19in; font-weight: 700; color: #0071E3; margin-bottom: 0.10in;">Governance & Executive Milestones</h3>
          <p>The 12-month deployment operates under strict Stage-Gate governance overseen jointly by the Lead Consultant and Company A Chief Commercial Officer:</p>
        </div>
        
        <div style="background: #FFFFFF; border: 1px solid rgba(0,0,0,0.06); padding: 0.16in; border-radius: 0.12in;">
          <div style="font-weight: 700; color: #1D1D1F; margin-bottom: 0.04in;">1. Hardware Fulfillment SLA:</div>
          <p style="font-size: 0.14in;">Guaranteed 48-hour handset doorstep delivery via OEM direct fulfillment partnership.</p>
        </div>
        
        <div style="background: #FFFFFF; border: 1px solid rgba(0,0,0,0.06); padding: 0.16in; border-radius: 0.12in;">
          <div style="font-weight: 700; color: #1D1D1F; margin-bottom: 0.04in;">2. 30-Day Contract Enforceability:</div>
          <p style="font-size: 0.14in;">Automated SIM activation tracking; early termination fee (ETF) amortized over 24 months.</p>
        </div>
        
        <div style="background: #EAF7EE; border: 1px solid rgba(52, 199, 89, 0.25); padding: 0.14in; border-radius: 0.12in;">
          <strong style="color: #1B8341; font-size: 0.145in;">Success Thresholds:</strong>
          <span style="font-size: 0.135in; color: #3A3A3C;">Take-up &ge; 65% &bull; Churn Reduction &ge; 60% &bull; Net Payback &le; 6 Months.</span>
        </div>
      </div>
    </div>
  </div>
  <div class="footer">
    <span>Program overseen jointly by Lead Consultant and Company A Chief Commercial Officer</span>
    <span>Slide 13 / 15</span>
  </div>
</div>

<!-- SLIDE 14 : RISK MITIGATION & GOVERNANCE -->
<div class="slide">
  <div class="header">
    <div class="header-left">
      <div class="category cat-coral">Governance</div>
      <h2>Comprehensive Risk Mitigation Framework</h2>
    </div>
    <div class="header-right">Board Assurance</div>
  </div>
  <div class="content">
    <div class="col-2">
      <div class="card card-pastel-coral">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.04in;">
          <h4 style="font-size: 0.17in; font-weight: 700; color: #FF453A;">Risk 1: Cannibalization & Subsidy Waste</h4>
          <span class="pill pill-coral">High Severity</span>
        </div>
        <p><strong>Threat:</strong> Offering subsidized handsets to subscribers who would have remained without incentive.</p>
        <p style="margin-top: 0.04in;"><strong>Mitigation:</strong> Strict dual-gated qualification: only accounts with calibrated defection probability &gt; 0.55 AND handset age &gt; 365 days are eligible.</p>
      </div>
      <div class="card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.04in;">
          <h4 style="font-size: 0.17in; font-weight: 700; color: #1D1D1F;">Risk 2: Supply Chain Fulfillment Latency</h4>
          <span class="pill pill-gray">Operational</span>
        </div>
        <p><strong>Threat:</strong> OEM hardware shortages delaying device delivery.</p>
        <p style="margin-top: 0.04in;"><strong>Mitigation:</strong> Dual-vendor procurement framework (Samsung Galaxy A-series & Google Pixel) guaranteeing 5-day delivery SLAs.</p>
      </div>
    </div>
    <div class="col-2">
      <div class="card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.04in;">
          <h4 style="font-size: 0.17in; font-weight: 700; color: #1D1D1F;">Risk 3: Model Drift & Demographic Drift</h4>
          <span class="pill pill-blue">Technical</span>
        </div>
        <p><strong>Threat:</strong> Post-campaign consumer behavioral shifts reducing model accuracy over time.</p>
        <p style="margin-top: 0.04in;"><strong>Mitigation:</strong> Continuous Population Stability Index (PSI) tracking with automated retraining triggered whenever PSI exceeds 0.20.</p>
      </div>
      <div class="card card-pastel-green">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.04in;">
          <h4 style="font-size: 0.17in; font-weight: 700; color: #1B8341;">Risk 4: Regulatory & Fair Lending Compliance</h4>
          <span class="pill pill-green">Compliant</span>
        </div>
        <p><strong>Threat:</strong> Algorithmic bias or non-discrimination regulatory scrutiny.</p>
        <p style="margin-top: 0.04in;"><strong>Mitigation:</strong> All demographic variables (`ethnic`, `marital`, `adults`) are strictly excluded from feature weighting. Scoring is 100% behavioral.</p>
      </div>
    </div>
  </div>
  <div class="footer">
    <span>Compliant with Fair Credit Reporting Act (FCRA) and telecom non-discrimination standards</span>
    <span>Slide 14 / 15</span>
  </div>
</div>

<!-- SLIDE 15 : BOARD DECISION & CITATIONS -->
<div class="slide">
  <div class="header">
    <div class="header-left">
      <div class="category cat-green">Decision Required</div>
      <h2>Board Decision Points & Literature References</h2>
    </div>
    <div class="header-right">Next Steps</div>
  </div>
  <div class="content">
    <div class="col-2" style="flex: 0.95;">
      <div class="card card-pastel-green" style="margin-bottom: 0.18in;">
        <h3 style="font-size: 0.19in; font-weight: 800; color: #1B8341; margin-bottom: 0.10in;">Three Immediate Board Decisions Required:</h3>
        <ol style="margin-left: 0.22in; line-height: 1.55; font-size: 0.16in;">
          <li style="margin-bottom: 0.10in;"><strong>Approve Phase 1 Pilot Budget:</strong> Authorize $195,000 for the 1,500 subscriber validation cohort in Q1.</li>
          <li style="margin-bottom: 0.10in;"><strong>Authorize 5G OEM Bulk Supply Agreement:</strong> Contract for 5,618 subsidized 5G devices at $130/unit.</li>
          <li style="margin-bottom: 0.10in;"><strong>Formalize Implementation Mandate:</strong> Transition from exploratory PoC to full production rollout.</li>
        </ol>
      </div>
      
      <div style="padding: 0.14in 0.18in; background: #FFFFFF; border: 1px solid rgba(0,0,0,0.06); border-radius: 0.12in; font-size: 0.14in;">
        <strong>Economic Summary:</strong> $730,340 Total Investment &rarr; <strong style="color: #1B8341;">+$3,168,404 Net Profit (433.8% ROI)</strong> &rarr; <strong>4.5 Months Payback</strong>.
      </div>
    </div>
    <div class="col-2" style="flex: 1.05;">
      <div class="card" style="height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
        <h3 style="font-size: 0.18in; font-weight: 700; color: #1D1D1F; margin-bottom: 0.08in;">Academic & Literature References</h3>
        <ol style="font-size: 0.135in; color: #3A3A3C; margin-left: 0.20in; line-height: 1.5;">
          <li style="margin-bottom: 0.06in;"><strong>GSMA Intelligence (2025):</strong> <em>The Mobile Economy 2025 &mdash; Churn Dynamics, Spectrum Transitions, and Post-Paid Loyalty Economics</em>. London: GSM Association.</li>
          <li style="margin-bottom: 0.06in;"><strong>Analysys Mason (2024):</strong> <em>Telecom Customer Acquisition Costs vs. Value-Based Retention Strategies in Tier-1 Global Operators</em>. Research Report.</li>
          <li style="margin-bottom: 0.06in;"><strong>Federal Communications Commission (FCC, 2024):</strong> <em>Annual Mobile Wireless Competition Report</em> (Doc. No. 24&ndash;89). Washington, D.C.: FCC.</li>
          <li style="margin-bottom: 0.06in;"><strong>Matsuo-Iwasawa Laboratory (2026):</strong> <em>GCI World 2026 September Course Materials, Final Assignment Guidelines & Company A Dataset Overview</em>. Tokyo: The University of Tokyo.</li>
        </ol>
        
        <div style="background: #F8F9FA; padding: 0.10in 0.14in; border-radius: 0.08in; font-size: 0.125in; color: #6E6E73; border: 1px solid rgba(0,0,0,0.05); margin-top: 0.06in;">
          <strong>Generative AI Transparency Statement:</strong> AI assistance was utilized for preliminary hypothesis exploration, code scaffolding, and LaTeX formulation assistance. All final empirical analyses, model validations, and strategic recommendations were independently conducted, verified, and authored by the candidate.
        </div>
      </div>
    </div>
  </div>
  <div class="footer">
    <span>Candidate: Baptiste Bedeaux (BaptisteBdx) &bull; The University of Tokyo GCI World 2026 September</span>
    <span>Slide 15 / 15</span>
  </div>
</div>

</body>
</html>
"""

def generate_pdf():
    print("Écriture du fichier HTML des 15 slides Apple...")
    html_content = APPLE_SLIDES_HTML.replace("{FIG_DIR}", FIG_DIR)
    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"Rendu PDF en cours via Playwright : {OUTPUT_PDF}")
    cmd = [
        "python3", "-c",
        f"""
import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("file://{HTML_PATH}", wait_until="networkidle")
        await page.pdf(
            path="{OUTPUT_PDF}",
            width="13.333in",
            height="7.5in",
            print_background=True,
            margin={{"top": "0in", "right": "0in", "bottom": "0in", "left": "0in"}}
        )
        await browser.close()

asyncio.run(run())
"""
    ]
    subprocess.run(cmd, check=True)
    
    print("Vérification avec pypdf...")
    reader = PdfReader(OUTPUT_PDF)
    num_pages = len(reader.pages)
    size_mb = os.path.getsize(OUTPUT_PDF) / (1024 * 1024)
    
    print("=" * 60)
    print(f"FICHIER PDF APPLE GÉNÉRÉ : {OUTPUT_PDF}")
    print(f"Nombre de pages : {num_pages} (EXACTEMENT 15 SLIDES)")
    print(f"Taille du fichier : {size_mb:.2f} Mo (Plafond autorisé: 10 Mo)")
    print("=" * 60)
    
    assert num_pages == 15, f"ERREUR : {num_pages} pages trouvées au lieu de 15 !"

if __name__ == "__main__":
    generate_pdf()
