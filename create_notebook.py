import nbformat as nbf

nb = nbf.v4.new_notebook()

text = """\
# Sea Buckthorn Market Analytics & EDA

This notebook performs Exploratory Data Analysis (EDA) on the Sea buckthorn market dataset. It analyzes pricing, origins, health claims, and bioactives across various competitors.
"""

code_imports = """\
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Set plot style
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)
"""

code_load = """\
# Load the dataset
df = pd.read_csv('data/seabuckthorn_market_data.csv')
print(f"Dataset Shape: {df.shape}")
df.head()
"""

text_eda1 = """\
## 1. Market Overview by Origin and Brand
Let's see the distribution of products based on their origin (e.g., Himalayas vs China) and by Brand.
"""

code_eda1 = """\
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

sns.countplot(y='Origin', data=df, order=df['Origin'].value_counts().index, ax=axes[0], palette='viridis')
axes[0].set_title('Product Distribution by Origin')
axes[0].set_xlabel('Count')

sns.countplot(y='Brand', data=df, order=df['Brand'].value_counts().index, ax=axes[1], palette='magma')
axes[1].set_title('Product Distribution by Competitor Brand')
axes[1].set_xlabel('Count')

plt.tight_layout()
plt.savefig('data/market_overview.png')
plt.show()
"""

text_eda2 = """\
## 2. Pricing Analysis
Analyzing the price distribution across different brands.
"""

code_eda2 = """\
plt.figure(figsize=(12, 8))
sns.boxplot(x='Price ($)', y='Brand', data=df, palette='Set2')
plt.title('Price Distribution by Brand')
plt.savefig('data/pricing_analysis.png')
plt.show()
"""

text_eda3 = """\
## 3. Health Claims & Bioactives Analysis
Sea buckthorn is known for its "180+ bioactives" and being an "Omega powerhouse". Let's analyze the frequency of these claims.
"""

code_eda3 = """\
# Explode the comma-separated claims and bioactives
claims_series = df['Health Claims'].str.split(', ').explode()
bioactives_series = df['Bioactives'].str.split(', ').explode()

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Plot Claims
sns.countplot(y=claims_series, order=claims_series.value_counts().index, ax=axes[0], palette='coolwarm')
axes[0].set_title('Frequency of Health Claims')
axes[0].set_xlabel('Count')

# Plot Bioactives
sns.countplot(y=bioactives_series, order=bioactives_series.value_counts().index, ax=axes[1], palette='crest')
axes[1].set_title('Frequency of Marketed Bioactives')
axes[1].set_xlabel('Count')

plt.tight_layout()
plt.savefig('data/claims_analysis.png')
plt.show()
"""

nb['cells'] = [
    nbf.v4.new_markdown_cell(text),
    nbf.v4.new_code_cell(code_imports),
    nbf.v4.new_code_cell(code_load),
    nbf.v4.new_markdown_cell(text_eda1),
    nbf.v4.new_code_cell(code_eda1),
    nbf.v4.new_markdown_cell(text_eda2),
    nbf.v4.new_code_cell(code_eda2),
    nbf.v4.new_markdown_cell(text_eda3),
    nbf.v4.new_code_cell(code_eda3)
]

with open('eda.ipynb', 'w') as f:
    nbf.write(nb, f)
    
print("Successfully generated eda.ipynb")
