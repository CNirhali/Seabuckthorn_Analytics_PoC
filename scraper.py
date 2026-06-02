import asyncio
from playwright.async_api import async_playwright
import pandas as pd
import random
import os
import time

# User-provided context for fallback/synthetic generation
COMPETITORS = ['SeabuckWonders', 'Wellsash/Biosash', 'Leh Berry', 'Sibu', 'Terezia company', 
               'Natures Aid Ltd', 'Weleda', 'Erbology', 'WellWith', 'Pahari haat', 'Maven & bloom']
PRODUCT_TYPES = ['Sea buckthorn Tea', 'Sea buckthorn Oil', 'Sea buckthorn Juice', 'Wonder Berry Capsules', 'GI TAG Berry Powder']
ORIGINS = ['Himalayas (India)', 'Nubra Valley, Ladakh', 'China']
CLAIMS = ['Immunity', 'Anti Ageing', 'Gut Friendly', 'Cellular Hydration', 'Promotes skin health', 
          'Heart & Metabolic health', 'Menopause support', 'Skin hydration', 'Stress Relief']
BIOACTIVES = ['Omega 3', 'Omega 6', 'Omega 7', 'Omega 9', 'Vitamin A', 'Vitamin C', 'Vitamin E', 'Vitamin K', '180+ Bioactives']

async def scrape_site(page, brand, url, product_selector, name_selector, price_selector):
    print(f"Scraping {brand} at {url}...")
    products = []
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        # Give some time for JS to render
        await page.wait_for_timeout(3000) 
        
        items = await page.query_selector_all(product_selector)
        print(f"Found {len(items)} items for {brand}")
        
        for item in items:
            name_el = await item.query_selector(name_selector)
            price_el = await item.query_selector(price_selector)
            
            if name_el and price_el:
                name = await name_el.inner_text()
                price = await price_el.inner_text()
                products.append({
                    'Brand': brand,
                    'Product Name': name.strip().replace('\n', ' '),
                    'Price': price.strip(),
                    'Source': 'Scraped'
                })
    except Exception as e:
        print(f"Failed to scrape {brand}: {e}")
    return products

async def run_scrapers():
    scraped_data = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        # 1. Scrape SeabuckWonders
        sbw_data = await scrape_site(
            page, 
            brand="SeabuckWonders", 
            url="https://www.seabuckwonders.com/collections/all", 
            product_selector=".grid-product", 
            name_selector=".grid-product__title", 
            price_selector=".grid-product__price"
        )
        scraped_data.extend(sbw_data)
        
        # 2. Scrape Sibu (Using broad selectors as example)
        sibu_data = await scrape_site(
            page, 
            brand="Sibu", 
            url="https://sibu.com/collections/all-products", 
            product_selector=".product-item", 
            name_selector=".product-item__title", 
            price_selector=".price"
        )
        scraped_data.extend(sibu_data)
        
        await browser.close()
        
    return scraped_data

def generate_synthetic_data(num_records=100):
    print(f"Generating {num_records} records based on domain knowledge...")
    data = []
    for _ in range(num_records):
        brand = random.choice(COMPETITORS)
        
        # Origin logic: China is biggest competitor, others are Indian/European
        if brand in ['WellWith', 'Pahari haat', 'Maven & bloom', 'Leh Berry', 'Wellsash/Biosash']:
            origin = random.choice(['Himalayas (India)', 'Nubra Valley, Ladakh'])
        elif brand in ['SeabuckWonders', 'Sibu', 'Terezia company', 'Weleda']:
            origin = random.choice(['China', 'Unknown'])
        else:
            origin = random.choice(ORIGINS)
            
        product_type = random.choice(PRODUCT_TYPES)
        price = round(random.uniform(15.0, 65.0), 2)
        
        # Select 2-4 claims
        num_claims = random.randint(2, 4)
        product_claims = random.sample(CLAIMS, num_claims)
        
        # Select bioactives
        num_bioactives = random.randint(3, 6)
        product_bioactives = random.sample(BIOACTIVES, num_bioactives)
        
        data.append({
            'Brand': brand,
            'Product Name': f"{brand} {product_type}",
            'Price ($)': price,
            'Origin': origin,
            'Health Claims': ", ".join(product_claims),
            'Bioactives': ", ".join(product_bioactives),
            'Source': 'Generated based on prompt domain knowledge'
        })
    return data

def clean_price(price_str):
    if pd.isna(price_str): return None
    if isinstance(price_str, (int, float)): return price_str
    import re
    # Extract numbers and decimals
    match = re.search(r'[\d\.]+', str(price_str))
    if match:
        try:
            return float(match.group())
        except:
            pass
    return None

def main():
    os.makedirs('data', exist_ok=True)
    
    # 1. Attempt Scraping
    print("Attempting to scrape live data using Playwright...")
    try:
        scraped_data = asyncio.run(run_scrapers())
    except Exception as e:
        print(f"Scraping error: {e}")
        scraped_data = []
        
    if scraped_data:
        df_scraped = pd.DataFrame(scraped_data)
        df_scraped['Price ($)'] = df_scraped['Price'].apply(clean_price)
        print(f"Successfully scraped {len(df_scraped)} items.")
    else:
        print("Live scraping yielded no data (likely blocked by anti-bot systems like Cloudflare).")
        df_scraped = pd.DataFrame()

    # 2. Generate Domain-Specific Data based on User's parameters
    synthetic_data = generate_synthetic_data(150)
    df_synthetic = pd.DataFrame(synthetic_data)
    
    # Combine (if scraped data exists, append it. Otherwise just use synthetic)
    if not df_scraped.empty:
        # Align columns
        for col in df_synthetic.columns:
            if col not in df_scraped.columns:
                df_scraped[col] = "N/A"
        df_combined = pd.concat([df_scraped, df_synthetic], ignore_index=True)
    else:
        df_combined = df_synthetic
        
    # Save to CSV
    output_path = 'data/seabuckthorn_market_data.csv'
    df_combined.to_csv(output_path, index=False)
    print(f"\nFinal dataset saved to {output_path} with {len(df_combined)} rows.")
    print("This dataset includes live scraped data (if successful) and data populated based on the provided domain knowledge (Origins, Competitors, Bioactives, Claims) for EDA purposes.")

if __name__ == "__main__":
    main()
