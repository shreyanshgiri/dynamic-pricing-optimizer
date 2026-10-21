import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Set page config for a wider layout
st.set_page_config(page_title="Dynamic Pricing Optimizer", layout="wide")

# Load the saved model
@st.cache_resource # This tells Streamlit to only load the model once, making the app faster
def load_model():
    return joblib.load('pricing_model.pkl')

model = load_model()

st.title("🏷️ Dynamic Pricing Optimizer")
st.write("Adjust the market conditions below to simulate and find the optimal product price.")

# Sidebar Controls for User Inputs
st.sidebar.header("Current Market Conditions")
inventory = st.sidebar.slider("Inventory Level", min_value=10, max_value=200, value=80)
competitor_price = st.sidebar.number_input("Competitor Price ($)", min_value=10.0, max_value=200.0, value=45.99)
day_of_week = st.sidebar.selectbox("Day of Week", options=[0, 1, 2, 3, 4, 5, 6], format_func=lambda x: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][x])
month = st.sidebar.slider("Month", min_value=1, max_value=12, value=11)

is_weekend = 1 if day_of_week in [5, 6] else 0

# Main logic runs when the button is clicked, or automatically on load
st.markdown("---")
st.subheader("Optimization Results")

# Define the range of prices to test
test_prices = np.arange(20, 100, 1)

best_price = 0
max_revenue = 0
best_sales = 0

# Lists to store data for our chart
prices_list = []
revenues_list = []
sales_list = []

# Optimization Loop
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
    
    # Save data for the chart
    prices_list.append(price)
    revenues_list.append(expected_revenue)
    sales_list.append(predicted_sales)
    
    if expected_revenue > max_revenue:
        max_revenue = expected_revenue
        best_price = price
        best_sales = predicted_sales

# Display Top-Level Results in Metric Cards
col1, col2, col3 = st.columns(3)
col1.metric(label="Optimal Price", value=f"${best_price:.2f}")
col2.metric(label="Predicted Units Sold", value=f"{best_sales:.1f}")
col3.metric(label="Maximized Revenue", value=f"${max_revenue:.2f}")

st.markdown("---")
st.subheader("Revenue Curve")
st.write("This chart maps out every simulated price point. The peak of the curve represents the absolute highest revenue possible under current market conditions.")

# Create a DataFrame for the chart data
chart_data = pd.DataFrame({
    'Simulated Price ($)': prices_list,
    'Expected Revenue ($)': revenues_list
})

# Use Streamlit's native line_chart
st.line_chart(
    data=chart_data,
    x='Simulated Price ($)',
    y='Expected Revenue ($)',
    color="#00ff00" # Bright green for revenue
)
