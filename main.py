import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import expense_tracker as et
import datetime

CSV_FILE = 'expenses.csv'
CATEGORIES = [
    "",
    "🍔 Food", 
    "🎬 Entertainment", 
    "🚗 Transportation", 
    "💵 Savings", 
    "📚 Miscellaneous"
]
st.title("💰 Finance Tracker")
st.markdown("Track your spending, visualize your habits, and take control of your finances.")


st.sidebar.header("Add a New Expense")
with st.sidebar.form("expense_form", clear_on_submit=True):
    name = st.text_input("Expense Name", placeholder="e.g., Coffee")
    amount = st.number_input("Amount ($)", min_value=0.01, step=0.01, format="%.2f")
    category = st.selectbox("Category", CATEGORIES)
    
    submitted = st.form_submit_button("Add Expense")