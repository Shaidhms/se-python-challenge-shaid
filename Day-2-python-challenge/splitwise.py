import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import math
import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

logo_base64 = get_base64_image("se.png")

st.markdown(
    f"""
    <h1 class="main-header">
         <img src="data:image/png;base64,{logo_base64}" width="40" style="vertical-align: middle; margin-left:5px;">
        Social Eagle Python Challenge Day 2 - Smart Expense Splitter
    </h1>
    """,
    unsafe_allow_html=True
)
# Page configuration
st.set_page_config(
  page_title="Social Eagle Python Challenge Day 1", page_icon="🦅", layout="centered"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #2E8B57;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #4A90E2;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }

    .positive-amount {
        color: #28a745;
        font-weight: bold;
    }
    .negative-amount {
        color: #dc3545;
        font-weight: bold;
    }
    .neutral-amount {
        color: #6c757d;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

#checking here 

st.markdown("""
<style>
div[data-testid="stMetricValue"] {
  overflow: visible !important;
  text-overflow: clip !important;
  white-space: nowrap !important;
  font-size: 1.3rem !important;
}
div[data-testid="stMetricLabel"] {
  white-space: nowrap !important;
  overflow: visible !important;
  text-overflow: clip !important;
  font-size: 0.9rem !important;
}
</style>
""", unsafe_allow_html=True)

def main():
    # Header

    

    #st.markdown('<h1 class="main-header">Social Eagle 🦅 Python Challenge Day 2 - Smart Expense Splitter</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar for app info and settings
    with st.sidebar:
        st.header("🎯 App Features")
        st.info("✅ Equal & Custom Split\n✅ Visual Dashboard\n✅ Export Results\n✅ Multiple Scenarios")
        
        st.header("📊 Quick Stats")
        if 'total_amount' in st.session_state:
            st.metric("Total Amount", f"₹{st.session_state.total_amount:,.2f}")
            st.metric("Number of People", st.session_state.get('num_people', 0))
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["💸 Split Calculator", "📊 Dashboard", "📋 Summary", "📤 Export"])
    
    with tab1:
        split_calculator()
    
    with tab2:
        dashboard()
    
    with tab3:
        summary_view()
    
    with tab4:
        export_data()

def split_calculator():
    st.markdown('<h2 class="sub-header">Calculate Expense Split</h2>', unsafe_allow_html=True)
    
    # Initialize session state
    if 'expenses' not in st.session_state:
        st.session_state.expenses = []
    
    # Two columns for input
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🧮 Basic Information")
        total_amount = st.number_input("Total Amount (₹)", min_value=0.01, value=1000.0, step=0.01)
        num_people = st.number_input("Number of People", min_value=2, max_value=20, value=2)
        
        # Store in session state
        st.session_state.total_amount = total_amount
        st.session_state.num_people = num_people
        
        split_type = st.selectbox("Split Type", ["Equal Split", "Custom Contributions", "Percentage Split"])
    
    with col2:
        st.subheader("📝 Expense Details")
        expense_name = st.text_input("Expense Name (Optional)", placeholder="Dinner at Restaurant XYZ")
        expense_date = st.date_input("Date", date.today())
        expense_category = st.selectbox(
            "Category", 
            ["Restaurant", "Travel", "Entertainment", "Groceries", "Utilities", "Other"]
        )
    
    # People input section
    st.markdown("---")
    st.subheader("👥 People & Contributions")
    
    # Initialize people data
    if 'people_data' not in st.session_state:
        st.session_state.people_data = []
    
    # Adjust people_data based on num_people
    while len(st.session_state.people_data) < num_people:
        st.session_state.people_data.append({
            'name': f'Person {len(st.session_state.people_data) + 1}',
            'contribution': 0.0,
            'percentage': 100/num_people
        })
    
    while len(st.session_state.people_data) > num_people:
        st.session_state.people_data.pop()
    
    # Create input fields for each person
    people_cols = st.columns(min(num_people, 3))
    
    for i in range(num_people):
        col_idx = i % 3
        with people_cols[col_idx]:
            st.markdown(f'<div class="person-card">', unsafe_allow_html=True)
            
            name = st.text_input(
                "Name", 
                value=st.session_state.people_data[i]['name'],
                key=f"name_{i}"
            )
            st.session_state.people_data[i]['name'] = name
            
            if split_type == "Custom Contributions":
                contribution = st.number_input(
                    "Paid Amount (₹)", 
                    min_value=0.0, 
                    value=st.session_state.people_data[i]['contribution'],
                    step=0.01,
                    key=f"contrib_{i}"
                )
                st.session_state.people_data[i]['contribution'] = contribution
            
            elif split_type == "Percentage Split":
                percentage = st.number_input(
                    "Share (%)", 
                    min_value=0.0, 
                    max_value=100.0,
                    value=st.session_state.people_data[i]['percentage'],
                    step=0.1,
                    key=f"percent_{i}"
                )
                st.session_state.people_data[i]['percentage'] = percentage
            
            st.markdown('</div>', unsafe_allow_html=True)
    


    # Calculate button
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🧮 Calculate Split", type="primary", use_container_width=True):
            calculate_and_display_results(total_amount, split_type, expense_name, expense_date, expense_category)


def calculate_and_display_results(total_amount, split_type, expense_name, expense_date, expense_category):
    """Calculate the split and display results"""
    results = []
        
    if split_type == "Equal Split":
        equal_share = total_amount / st.session_state.num_people
        for person in st.session_state.people_data:
            balance = equal_share - person['contribution']
            results.append({
                'name': person['name'],
                'should_pay': equal_share,
                'paid': person['contribution'],
                'balance': balance,
                'status': 'owes' if balance > 0 else 'gets back' if balance < 0 else 'settled'
            })
    
    elif split_type == "Custom Contributions":
        total_paid = sum(person['contribution'] for person in st.session_state.people_data)
        equal_share = total_amount / st.session_state.num_people
        # Optionally warn if total_paid != total_amount
        # if abs(total_paid - total_amount) > 0.01:
        #     st.warning(f"Total paid (₹{total_paid:.2f}) differs from total amount (₹{total_amount:.2f}).")
        
        for person in st.session_state.people_data:
            balance = equal_share - person['contribution']
            results.append({
                'name': person['name'],
                'should_pay': equal_share,
                'paid': person['contribution'],
                'balance': balance,
                'status': 'owes' if balance > 0 else 'gets back' if balance < 0 else 'settled'
            })
    
    elif split_type == "Percentage Split":
        total_percentage = sum(person['percentage'] for person in st.session_state.people_data)
        if abs(total_percentage - 100) > 0.01:
            st.error(f"⚠️ Percentages must add up to 100%. Current total: {total_percentage:.1f}%")
            return
        
        for person in st.session_state.people_data:
            should_pay = (person['percentage'] / 100) * total_amount
            balance = should_pay - person['contribution']
            results.append({
                'name': person['name'],
                'should_pay': should_pay,
                'paid': person['contribution'],
                'balance': balance,
                'status': 'owes' if balance > 0 else 'gets back' if balance < 0 else 'settled'
            })
    
    # Store results in session state
    st.session_state.results = results
    st.session_state.expense_details = {
        'name': expense_name or "Unnamed Expense",
        'date': expense_date,
        'category': expense_category,
        'total_amount': total_amount,
        'split_type': split_type
    }
    
    # Display results
    display_results(results)

def display_results(results):
    """Display the calculated results"""
    st.markdown("---")
    st.markdown('<h2 class="sub-header">💡 Split Results</h2>', unsafe_allow_html=True)
    
    # Summary metrics
   # col1, col2, col3, col4 = st.columns(4)
    col1, col2, col3, col4 = st.columns([1.7, 1.7, 1.7, 1.0])
    
    total_owes = sum(abs(r['balance']) for r in results if r['balance'] > 0)
    total_gets_back = sum(abs(r['balance']) for r in results if r['balance'] < 0)
    settled_count = sum(1 for r in results if r['balance'] == 0)
    
    with col1:
        st.metric("Total Amount", f"₹{st.session_state.total_amount:,.2f}")
    with col2:
        st.metric("Total Owed", f"₹{total_owes:,.2f}")
    with col3:
        st.metric("Total to Return", f"₹{total_gets_back:,.2f}")
    with col4:
        st.metric("Settled People", settled_count)
        
    
    # Individual results
    st.subheader("👤 Individual Breakdown")
    
    for result in results:
        with st.container():
            col1, col2, col3, col4 = st.columns([2, 1.5, 1.5, 2])
            
            with col1:
                st.write(f"**{result['name']}**")
            
            with col2:
                st.write(f"Should pay: ₹{result['should_pay']:.2f}")
            
            with col3:
                st.write(f"Paid: ₹{result['paid']:.2f}")
            
            with col4:
                balance = result['balance']
                if balance > 0.01:
                    st.markdown(f'<span class="negative-amount">Owes: ₹{balance:.2f}</span>', unsafe_allow_html=True)
                elif balance < -0.01:
                    st.markdown(f'<span class="positive-amount">Gets back: ₹{abs(balance):.2f}</span>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<span class="neutral-amount">Settled ✅</span>', unsafe_allow_html=True)
    
    # Settlement suggestions
    st.subheader("💸 Settlement Suggestions")
    generate_settlement_suggestions(results)

def generate_settlement_suggestions(results):
    """Generate optimal settlement suggestions"""
    debtors = [(r['name'], r['balance']) for r in results if r['balance'] > 0.01]
    creditors = [(r['name'], -r['balance']) for r in results if r['balance'] < -0.01]
    
    if not debtors and not creditors:
        st.success("🎉 Everyone is settled! No transactions needed.")
        return
    
    debtors.sort(key=lambda x: x[1], reverse=True)
    creditors.sort(key=lambda x: x[1], reverse=True)
    
    transactions = []
    i, j = 0, 0
    while i < len(debtors) and j < len(creditors):
        debtor_name, debt_amount = debtors[i]
        creditor_name, credit_amount = creditors[j]
        settlement_amount = min(debt_amount, credit_amount)
        
        transactions.append({'from': debtor_name, 'to': creditor_name, 'amount': settlement_amount})
        
        debtors[i] = (debtor_name, debt_amount - settlement_amount)
        creditors[j] = (creditor_name, credit_amount - settlement_amount)
        
        if debtors[i][1] < 0.01:
            i += 1
        if creditors[j][1] < 0.01:
            j += 1
    
    if transactions:
        st.write("**Optimal Settlement Plan:**")
        for idx, transaction in enumerate(transactions, 1):
            st.info(f"{idx}. **{transaction['from']}** pays **₹{transaction['amount']:.2f}** to **{transaction['to']}**")
    else:
        st.success("No settlements needed!")

def dashboard():
    """Dashboard with visual representations"""
    st.markdown('<h2 class="sub-header">📊 Visual Dashboard</h2>', unsafe_allow_html=True)
    
    if 'results' not in st.session_state:
        st.info("👆 Please calculate a split first in the Split Calculator tab!")
        return
    
    results = st.session_state.results
    
    # Create visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        # Balance chart
        names = [r['name'] for r in results]
        balances = [r['balance'] for r in results]
        colors = ['red' if b > 0 else 'green' if b < 0 else 'gray' for b in balances]
        
        fig_balance = go.Figure(data=[
            go.Bar(x=names, y=balances, marker_color=colors,
                  text=[f"₹{abs(b):.1f}" for b in balances],
                  textposition='auto')
        ])
        fig_balance.update_layout(
            title="Balance Overview (Red=Owes, Green=Gets Back)",
            yaxis_title="Amount (₹)",
            xaxis_title="People"
        )
        st.plotly_chart(fig_balance, use_container_width=True)
    
    with col2:
        # Contribution pie chart
        contributions = [r['paid'] for r in results if r['paid'] > 0]
        contributors = [r['name'] for r in results if r['paid'] > 0]
        
        if contributions:
            fig_pie = px.pie(values=contributions, names=contributors, title="Contribution Distribution")
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No contributions recorded for pie chart")
    
    # Status overview
    st.subheader("📈 Split Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    owes_count = sum(1 for r in results if r['balance'] > 0.01)
    gets_back_count = sum(1 for r in results if r['balance'] < -0.01)
    settled_count = sum(1 for r in results if abs(r['balance']) <= 0.01)
    
    with col1:
        st.metric("People Who Owe", owes_count, delta=None)
    with col2:
        st.metric("People Getting Back", gets_back_count, delta=None)
    with col3:
        st.metric("Already Settled", settled_count, delta=None)

def summary_view():
    """Summary view of the expense split"""
    st.markdown('<h2 class="sub-header">📋 Expense Summary</h2>', unsafe_allow_html=True)
    
    if 'results' not in st.session_state:
        st.info("👆 Please calculate a split first in the Split Calculator tab!")
        return
    
    # Expense details
    expense_details = st.session_state.expense_details
    results = st.session_state.results
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📝 Expense Information")
        st.write(f"**Name:** {expense_details['name']}")
        st.write(f"**Date:** {expense_details['date']}")
        st.write(f"**Category:** {expense_details['category']}")
        st.write(f"**Total Amount:** ₹{expense_details['total_amount']:,.2f}")
        st.write(f"**Split Type:** {expense_details['split_type']}")
    
    with col2:
        st.subheader("🧮 Quick Stats")
        avg_should_pay = sum(r['should_pay'] for r in results) / len(results)
        total_paid = sum(r['paid'] for r in results)
        
        st.write(f"**Average Share:** ₹{avg_should_pay:.2f}")
        st.write(f"**Total Paid:** ₹{total_paid:.2f}")
        st.write(f"**Difference:** ₹{abs(expense_details['total_amount'] - total_paid):.2f}")
        
        if abs(expense_details['total_amount'] - total_paid) > 0.01:
            st.warning("⚠️ Total paid doesn't match expense amount!")
    
    # Detailed table
    st.subheader("📊 Detailed Breakdown")
    
    df = pd.DataFrame([
        {
            'Name': r['name'],
            'Should Pay (₹)': f"{r['should_pay']:.2f}",
            'Actually Paid (₹)': f"{r['paid']:.2f}",
            'Balance (₹)': f"{r['balance']:.2f}",
            'Status': r['status'].title()
        } for r in results
    ])
    
    st.dataframe(df, use_container_width=True, hide_index=True)

def export_data():
    """Export functionality"""
    st.markdown('<h2 class="sub-header">📤 Export Results</h2>', unsafe_allow_html=True)
    
    if 'results' not in st.session_state:
        st.info("👆 Please calculate a split first in the Split Calculator tab!")
        return
    
    results = st.session_state.results
    expense_details = st.session_state.expense_details
    
    # Export options
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📄 Export Formats")
        
        # CSV Export
        df = pd.DataFrame([
            {
                'Expense_Name': expense_details['name'],
                'Date': expense_details['date'],
                'Category': expense_details['category'],
                'Total_Amount': expense_details['total_amount'],
                'Person_Name': r['name'],
                'Should_Pay': r['should_pay'],
                'Actually_Paid': r['paid'],
                'Balance': r['balance'],
                'Status': r['status']
            } for r in results
        ])
        
        csv_data = df.to_csv(index=False)
        st.download_button(
            label="📊 Download CSV",
            data=csv_data,
            file_name=f"expense_split_{expense_details['date']}.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        # Summary text
        summary_text = generate_summary_text(expense_details, results)
        st.download_button(
            label="📝 Download Summary (TXT)",
            data=summary_text,
            file_name=f"expense_summary_{expense_details['date']}.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    with col2:
        st.subheader("📱 Share Options")
        
        # WhatsApp message
        whatsapp_text = generate_whatsapp_message(expense_details, results)
        st.text_area("WhatsApp Message", whatsapp_text, height=200, help="Copy this text to share via WhatsApp")
        
        # Quick copy preview
        st.code(whatsapp_text, language="text")

def generate_summary_text(expense_details, results):
    """Generate a text summary"""
    summary = f"""
EXPENSE SPLIT SUMMARY
====================

Expense: {expense_details['name']}
Date: {expense_details['date']}
Category: {expense_details['category']}
Total Amount: ₹{expense_details['total_amount']:,.2f}
Split Type: {expense_details['split_type']}

INDIVIDUAL BREAKDOWN:
"""
    for result in results:
        summary += f"""
{result['name']}:
  Should Pay: ₹{result['should_pay']:.2f}
  Actually Paid: ₹{result['paid']:.2f}
  Balance: ₹{result['balance']:.2f} ({result['status']})
"""
    return summary

def generate_whatsapp_message(expense_details, results):
    """Generate WhatsApp-friendly message"""
    message = f"💰 *{expense_details['name']}*\n"
    message += f"📅 {expense_details['date']} | {expense_details['category']}\n"
    message += f"💵 Total: ₹{expense_details['total_amount']:,.2f}\n\n"
    message += "*Settlement Required:*\n"
    
    for result in results:
        if result['balance'] > 0.01:
            message += f"• {result['name']}: Owes ₹{result['balance']:.2f}\n"
        elif result['balance'] < -0.01:
            message += f"• {result['name']}: Gets ₹{abs(result['balance']):.2f}\n"
        else:
            message += f"• {result['name']}: Settled ✅\n"
    
    message += f"\nGenerated by Shaid's Expense Splitter📱"
    return message

if __name__ == "__main__":
    main()

    # ----- Footer -----
st.markdown("---")
st.markdown(
    '<p class="footer">🎓 Keep coding, keep learning! Made with ❤️ by Shaid using Streamlit '
    "</p>",
    unsafe_allow_html=True,
)