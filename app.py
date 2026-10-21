import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load the saved model
model = joblib.load('pricing_model.pkl')

st.title("🏷️ Dynamic Pricing Optimizer")
st.write("Adjust the market conditions below to simulate and find the optimal product price.")

# Sidebar Controls for User Inputs
st.sidebar.header("Current Market Conditions")
inventory = st.sidebar.slider("Inventory Level", min_value=10, max_value=200, value=80)
competitor_price = st.sidebar.number_input("Competitor Price ($)", min_value=10.0, max_value=200.0, value=45.99)
day_of_week = st.sidebar.selectbox("Day of Week", options=[0, 1, 2, 3, 4, 5, 6], format_func=lambda x: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][x])
month = st.sidebar.slider("Month", min_value=1, max_value=12, value=11)

is_weekend = 1 if day_of_week in [5, 6] else 0

# Button to run optimization
if st.button("Calculate Optimal Price"):
    test_prices = np.arange(20, 100, 1)
    
    best_price = 0
    max_revenue = 0
    best_sales = 0

    for price in test_prices:
        scenario = pd.DataFrame({
            'base_price': [price],
            'competitor_price': [competitor_price],
            'inventory_level': [inventory],
            'price_ratio': [price / competitor_price],
            'day_of_week': [day_of_week],
            'is_weekend': [is_weekend],
            'month': [month]
        })
        
        predicted_sales = model.predict(scenario)[0]
        expected_revenue = price * predicted_sales
        
        if expected_revenue > max_revenue:
            max_revenue = expected_revenue
            best_price = price
            best_sales = predicted_sales

    # Display Results in Metric Cards
    col1, col2, col3 = st.columns(3)
    col1.metric("Optimal Price", f"${best_price:.2f}")
    col2.metric("Predicted Units Sold", f"{best_sales:.1f}")
    col3.metric("Maximized Revenue", f"${max_revenue:.2f}")
