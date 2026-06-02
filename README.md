# Seabuckthorn Analytics Pipeline 🫐

This repository contains a comprehensive data scraping and Exploratory Data Analysis (EDA) pipeline designed to extract and analyze market data for Sea buckthorn products. 

Sea buckthorn (also known as Ladakh berry or Wonder berry) is renowned for being an Omega powerhouse (Omega 3, 6, 7, 9) and containing 180+ bioactives. This project aims to analyze the competitor landscape, pricing, origins, and marketed health claims across the industry.

---

## 🛠️ Project Structure

- `scraper.py` - The core web scraping script. It utilizes **Playwright** to interact with Javascript-heavy e-commerce pages (e.g., SeabuckWonders, Sibu). It also includes a synthetic data generator as a fallback mechanism to populate the dataset with domain-specific knowledge if live scraping is blocked by anti-bot protections.
- `create_notebook.py` - A utility script that programmatically generates the Jupyter Notebook for data analysis.
- `eda.ipynb` - The primary Jupyter Notebook where the Exploratory Data Analysis is performed. It reads the CSV data and generates visual insights.
- `data/` - The directory where the scraped datasets (CSV) and generated visualization plots (PNG) are saved.
- `venv/` - (Ignored in Git) The Python virtual environment for managing dependencies.

---

## 📊 Analytics Highlights

The EDA notebook (`eda.ipynb`) focuses on the following analytical questions:

1. **Market Overview by Origin**: Analyzes product distribution comparing major origins like the Himalayas (India), Nubra Valley (Ladakh), and China.
2. **Competitor Pricing Analysis**: Evaluates the price distribution (in USD) across major brands (e.g., Weleda, Erbology, Leh Berry, WellWith).
3. **Health Claims & Bioactives**: Quantifies the frequency of marketed benefits such as *Immunity*, *Anti Ageing*, *Cellular Hydration*, and *Stress Relief*.

---

## 🚀 How to Run Locally

### 1. Prerequisites
Make sure you have Python 3.9+ installed.

### 2. Setup the Environment
Clone the repository and install the required dependencies:
```bash
git clone git@github.com:CNirhali/Seabuckthorn_Analytics_PoC.git
cd Seabuckthorn_Analytics_PoC

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install pandas beautifulsoup4 requests matplotlib seaborn jupyter notebook playwright
playwright install chromium
```

### 3. Run the Data Scraper
To collect the latest market data (or generate the fallback dataset based on domain parameters), run:
```bash
python3 scraper.py
```
*This will output `data/seabuckthorn_market_data.csv`.*

### 4. Run the EDA Notebook
Generate the notebook (if not already present) and execute it:
```bash
python3 create_notebook.py
jupyter nbconvert --to notebook --execute --inplace eda.ipynb
```
Alternatively, launch Jupyter Notebook and explore it interactively:
```bash
jupyter notebook eda.ipynb
```

---

## 📝 Technologies Used
- **Data Scraping**: Playwright, Requests, BeautifulSoup
- **Data Science/EDA**: Pandas, Matplotlib, Seaborn
- **Notebooks**: Jupyter Lab, nbformat

## 🔗 Competitors Analyzed
SeabuckWonders (USA), Wellsash/Biosash (India), Leh Berry (India), Sibu (USA), Terezia company (Czech Republic), Natures Aid Ltd, Weleda, Erbology, WellWith (India), Pahari haat (India), Maven & bloom (India).
