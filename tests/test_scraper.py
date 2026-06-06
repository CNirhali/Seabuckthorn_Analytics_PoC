"""
Unit tests for scraper.py
"""
import pytest
import pandas as pd
import sys
import os

# Add parent directory to path to import scraper
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scraper import clean_price, generate_synthetic_data


class TestCleanPrice:
    """Test the clean_price function"""
    
    def test_clean_price_with_float(self):
        """Test cleaning a float price"""
        assert clean_price(25.99) == 25.99
    
    def test_clean_price_with_int(self):
        """Test cleaning an integer price"""
        assert clean_price(25) == 25
    
    def test_clean_price_with_string(self):
        """Test cleaning a string price"""
        assert clean_price("$29.99") == 29.99
    
    def test_clean_price_with_complex_string(self):
        """Test cleaning a string with currency symbols"""
        assert clean_price("USD 49.50") == 49.50
    
    def test_clean_price_with_nan(self):
        """Test cleaning NaN values"""
        assert clean_price(pd.NA) is None
    
    def test_clean_price_invalid(self):
        """Test cleaning invalid price strings"""
        assert clean_price("no price") is None


class TestGenerateSyntheticData:
    """Test the synthetic data generation"""
    
    def test_generate_synthetic_data_structure(self):
        """Test that synthetic data has correct structure"""
        data = generate_synthetic_data(num_records=10)
        
        assert len(data) == 10
        
        # Check required fields in each record
        required_fields = ['Brand', 'Product Name', 'Price ($)', 'Origin', 
                          'Health Claims', 'Bioactives', 'Source']
        for record in data:
            for field in required_fields:
                assert field in record
    
    def test_generate_synthetic_data_price_range(self):
        """Test that prices are in expected range"""
        data = generate_synthetic_data(num_records=50)
        
        for record in data:
            price = record['Price ($)']
            assert 15.0 <= price <= 65.0
    
    def test_generate_synthetic_data_brand_validity(self):
        """Test that brands are from valid competitor list"""
        data = generate_synthetic_data(num_records=30)
        
        valid_brands = ['SeabuckWonders', 'Wellsash/Biosash', 'Leh Berry', 'Sibu', 
                       'Terezia company', 'Natures Aid Ltd', 'Weleda', 'Erbology', 
                       'WellWith', 'Pahari haat', 'Maven & bloom']
        
        for record in data:
            assert record['Brand'] in valid_brands
    
    def test_generate_synthetic_data_origin_logic(self):
        """Test origin assignment logic"""
        data = generate_synthetic_data(num_records=100)
        
        valid_origins = ['Himalayas (India)', 'Nubra Valley, Ladakh', 'China', 'Unknown']
        
        for record in data:
            assert record['Origin'] in valid_origins
            
            # Verify origin logic
            brand = record['Brand']
            origin = record['Origin']
            
            if brand in ['WellWith', 'Pahari haat', 'Maven & bloom', 'Leh Berry', 'Wellsash/Biosash']:
                assert origin in ['Himalayas (India)', 'Nubra Valley, Ladakh']
