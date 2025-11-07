import streamlit as st
import pandas as pd
import datetime
import calendar
import os
import altair as alt
import time

CSV_FILE = 'expenses.csv'
EXPENSE_CATEGORIES = [
    "🍔 Food", 
    "🎬 Entertainment", 
    "🚗 Transportation", 
    "💵 Savings", 
    "📚 Miscellaneous"
]
hide_input_instructions_style = """
<style>
[data-testid="InputInstructions"] {
    display: none;
}
</style>
"""

def load_data(csv_file):
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        df['Cost ($)'] = pd.to_numeric(df['Cost ($)'], errors='coerce')
        return df
    else:
        return pd.DataFrame(columns = ['Expense', 'Cost ($)', 'Category'])
    
def save_data(csv_file, new_expense):
    try:
        df = load_data(CSV_FILE)

        df_update = pd.concat([df, new_expense], ignore_index=True)

        df_update.to_csv(csv_file, index=False)
        st.success("Expense saved successfully!")
    except Exception as e:
        st.error(f"Error saving data: {e}")

st.set_page_config(page_title="FinanceTracker", layout="wide")
st.title("📊 FinanceTracker")
st.markdown("Track your spending, visualize your habits, and take control of your finances.")

st.markdown(hide_input_instructions_style, unsafe_allow_html=True)

st.sidebar.header("Add a New Expense")
with st.sidebar.form(key="expense_form", clear_on_submit=True):
    expense_name = st.text_input("Expense Name", placeholder="Ex: Coffee")
    expense_cost = st.number_input("Amount ($)", min_value=0.00, format="%.2f")
    expense_category = st.selectbox("Category", EXPENSE_CATEGORIES, index=None, placeholder="Select your category below:")
    
    submitted = st.form_submit_button("Add Expense")

monthly_budget = st.sidebar.number_input(
    "Set Your Monthly Budget:",
    min_value=0,
    step=100
)

st.sidebar.divider()
st.sidebar.header("Danger Zone")
st.sidebar.error("WARNING: This will permanently delete all expenses.")

if st.sidebar.button("Clear All Expenses"):
    if os.path.exists(CSV_FILE):
        try:
            os.remove(CSV_FILE)
            st.sidebar.success("All expenses has successfully been deleted!")
            time.sleep(1)
            st.rerun()
        except Exception as e:
            st.sidebar.error(f"Error clearing data: {e}")
    else:
        st.sidebar.info("No expenses to delete.")

if submitted:
    if not expense_name:
        st.sidebar.error("Please enter an expense name.")
    else:
        new_expense = pd.DataFrame({
            "Expense": [expense_name],
            "Cost ($)": [expense_cost],
            "Category": [expense_category]
        })
        save_data(CSV_FILE, new_expense)

df_expenses = load_data(CSV_FILE)

st.header("Expense Dashboard")

total_spent = df_expenses['Cost ($)'].sum()
remaining_budget = monthly_budget - total_spent

now = datetime.datetime.now()
days_in_month = calendar.monthrange(now.year, now.month)[1]
remaining_days = days_in_month - now.day

if remaining_days > 0:
    daily_budget = remaining_budget / remaining_days
else:
    daily_budget = remaining_budget

col1, col2, col3 = st.columns(3)
col1.metric(
    label="Total Spent",
    value=f"${total_spent:,.2f}",
    delta=f"{remaining_budget:,.2f} Remaining",
    delta_color="normal"
)
col2.metric("Monthly Budget", f"${monthly_budget:,.2f}")
col3.metric("Daily Budget", f"${daily_budget:,.2f}")

st.divider()

col_chart, col_data = st.columns(2)

with col_chart:
    st.subheader("Expenses by Category")
    amount_by_category = df_expenses.groupby('Category')['Cost ($)'].sum()

    if not amount_by_category.empty:
        df_chart = amount_by_category.reset_index()

        chart = (
            alt.Chart(df_chart)
            .mark_bar()
            .encode(
                x=alt.X('Category', title='Category', axis=alt.Axis(labelAngle=0)),
                y=alt.Y('Cost ($)', title='Cost ($)'),
                color=alt.Color('Category', title='Category'),
                tooltip=['Category', 'Cost ($)']
            )
            .interactive()
        )

        st.altair_chart(chart,width='stretch')
    else:
        st.info("No expenses logged yet to display a chart.")

with col_data:
    st.subheader("Full Expense Log")
    if not df_expenses.empty:
        df_display = df_expenses.copy()

        df_display['Cost ($)'] = df_display['Cost ($)'].apply(lambda x: f"${x:,.2f}")
        
        df_display.reset_index(drop=True, inplace=True)
        df_display.index += 1
        df_display.index.name = "Entry"
        
        st.dataframe(
            df_display,
            width='stretch'
        )
    else:
        st.info("No expenses in the log.")