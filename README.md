# Morocco Housing Price Prediction 🏠

End-to-end ML project predicting apartment prices in Rabat, Morocco — from web scraping to deployment.

**🔗 Live Demo:** [Add Streamlit link after deployment]

## Overview

This project covers the full data science pipeline:
**Scraping (Selenium) → Cleaning (regex/Pandas) → Modeling (Random Forest) → Deployment (Streamlit).**

Unlike most student projects that rely on curated Kaggle datasets, the data here was self-collected from Avito.ma — making this as much a data engineering project as a machine learning one.

## Problem Statement

Real estate pricing in Morocco lacks transparent, data-driven benchmarks. This project builds a baseline price estimator for Rabat apartments using surface area and neighborhood as primary signals — designed to be expandable to other Moroccan cities (V2).

## Data Pipeline

### 1. Web Scraping (`src/scraper.py`)
- **Tool:** Selenium with WebDriverManager
- **Source:** avito.ma — apartment sales listings in Rabat
- **Robustness:** Explicit waits (`WebDriverWait`), per-ad error handling, randomized delays (2–5s) to mimic human browsing
- **Output:** Raw CSV with listing text, extracted price, and source URL

### 2. Data Cleaning (`src/cleaning.py`)
- Regex-based extraction of price, surface area, and location from unstructured listing text
- Filters applied:
  - Price ≥ 10,000 DH (removes rentals and noise)
  - Surface > 20 m² (removes obvious errors)
  - Drops rows with missing price or surface
- Custom neighborhood parser with fallback logic for non-standard formats

### 3. Modeling (`src/model.py`)
- **Algorithm:** Random Forest Regressor (`n_estimators=100`)
- **Pipeline:** `ColumnTransformer` with `OneHotEncoder` for categorical features (`quartier`, `ville`), passthrough for numerical (`surface_final`)
- **Evaluation:** Mean Absolute Error on a held-out 20% test set
- **Artifact:** Serialized model (`models/price_predictor.pkl`) for the Streamlit app

## Dataset (V1)

| Property | Value |
|---|---|
| Source | Self-scraped from Avito.ma |
| City | Rabat (V1 — `ville` feature kept for V2 expansion) |
| Listings (raw) | ~200 (from 5 pages) |
| Listings (after cleaning) | 160 |
| Features | Surface (m²), Neighborhood, City |
| Target | Sale price (MAD) |

## Results (V1 Baseline)

| Metric | Value |
|---|---|
| MAE | 542,506 MAD |
| Relative error | 25.39% |

**Honest assessment:** This is a baseline. The 25% error reflects two real limitations: (1) only 160 training rows, and (2) a feature set restricted to surface and neighborhood. The value of V1 lies in the *pipeline*, not the model accuracy — the infrastructure is in place to retrain quickly as more features and listings are added.

## Limitations & Next Steps

**Known limitations (V1):**
- Small sample size (only 5 pages scraped)
- No deduplication of listings appearing across multiple pages
- Some listings fall into the "Autre" neighborhood bucket when regex parsing fails
- CSS selectors are tied to Avito's current DOM — would need updating if the site redesigns

**Planned for V2:**
- Scrape additional features: property condition (new/old), floor, number of rooms, amenities
- Expand to Casablanca, Marrakech, Tanger (the `ville` feature is already in place)
- Increase sample size by scraping more pages
- Try gradient boosting (XGBoost, LightGBM) and compare against Random Forest baseline
- Add cross-validation for more robust evaluation
- Implement outlier handling for high-end villa listings

## Project Structure

```
├── app/                    # Streamlit web app
├── data/
│   ├── raw/                # Raw scraped listings
│   └── processed/          # Cleaned dataset
├── models/                 # Trained model artifact (.pkl)
├── src/
│   ├── scraper.py          # Selenium scraper
│   ├── cleaning.py         # Regex-based data cleaning
│   └── model.py            # Training pipeline
└── requirements.txt
```

## How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# 1. Scrape listings (takes ~2-3 minutes)
python src/scraper.py

# 2. Clean the data
python src/cleaning.py

# 3. Train the model
python src/model.py

# 4. Launch the Streamlit app
streamlit run app/app.py
```

## Tech Stack

**Scraping:** Selenium · WebDriverManager
**Data:** Pandas · Regex
**ML:** Scikit-learn (Random Forest, ColumnTransformer, Pipeline)
**Deployment:** Streamlit · Joblib
**Language:** Python 3

## What I Learned

- **Building a data pipeline from scratch** is harder than working with curated Kaggle datasets — but far more representative of real-world data science work
- **Sample size dominates feature engineering** at small scales — the limiting factor on this project wasn't the algorithm choice, it was the volume of clean data
- **MAE in the target unit (MAD)** is more interpretable to non-technical stakeholders than RMSE or R²
- **Web scraping is brittle** — regex patterns and CSS selectors are tied to a specific snapshot of a website and need ongoing maintenance
