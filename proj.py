import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector



st.set_page_config(page_title="Expense Tracker", layout="wide")

st.title("Analyzing Personal Expenses")

tab_home,tab1, tab2, tab3 = st.tabs(["Home","Data", "SQL Queries", "Visualizations"])
with tab_home:
    st.header("Welcome to the Expense Analyzer")
    st.write("This is a simple expense tracker application that allows users to track their expenses and analyze their spending habits.")
    st.write("Contents of the page:")
    st.write("1. **All Data**- This tab will show all the expenses.")
    st.write("2. **SQL Queries**- This tab will show the SQL queries run by the user to analyze the data.")
    st.write("3. **Visualizations**- This tab will show the visualizations made by the user.")
    
#ALL_Data Tab
with tab1:
    data=pd.read_csv(r"C:\Users\Hp\Desktop\analyzing personal expense\all_months_expenses.csv")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Dataset")
        st.write(data)
    with col2:
        
        st.subheader("This is a personal expenses data for the year 2023 generated using Faker library for this project. This data is used to perform sql queries and matplotlib visualizations.")
        st.subheader(" Descriptions of the Dataset")
        st.write("**Date**: The transaction date.")
        st.write("**Category**: Type of expense (Food, Transportation, Bills, etc.).")
        st.write("**Payment Mode**: Specifies whether it was a Cash or Online transaction.")
        st.write("**Description**: Details about the expense.")
        st.write("**Amount Paid**: Total amount paid for the transaction.")
        st.write("**Cashback**: Cashback received (if any) during the transaction.")



#SQL Queries Tab
with tab2:
    queries = [
    {"title": "Total amount spent per category", 
     "query": "Select Category, SUM(Amount_Paid) AS total_spent from all_months_expenses GROUP BY Category;"},
     
    {"title": "total amount spent using each payment mode", 
     "query": "SELECT Payment_Mode, SUM(Amount_Paid) AS total_spent from all_months_expenses GROUP BY Payment_Mode;"},
     
    {"title": "TOTAL CASHBACK RECIEVED ACROSS ALL TRANSACTIONS", 
     "query": "SELECT SUM(Cashback) AS total_cashback from all_months_expenses;"},
     
    {"title": "top 5 most expensive categories in terms of spending", 
     "query": "SELECT Category, SUM(Amount_Paid) AS total_spent from all_months_expenses GROUP BY Category Order by total_spent DESC LIMIT 5;"},
     
    {"title": "TOTAL AMOUNT SPENT ON TRANSPORTATION USING DIFFERENT PAYMENT MODE", 
     "query": "SELECT Payment_Mode, SUM(Amount_Paid) AS total_spent from all_months_expenses WHERE Category='Transportation' GROUP BY Payment_Mode;"},
     
    {"title": "which transaction resulted in cashback?", 
     "query": "select * from all_months_expenses where cashback > 0;"},
     
    {"title": "total spending in each month of the year", 
     "query": "select month(date) AS month, SUM(Amount_Paid) AS total_spent from all_months_expenses GROUP BY month order by month;"},
     
    {"title": "Days with highest spending", 
     "query": "SELECT Date, SUM(AmountPaid) AS Total_Spent FROM expenses GROUP BY Date ORDER BY Total_Spent DESC LIMIT 5;"},
     
    {"title": "Total amount spent on 'Groceries", 
     "query": "SELECT SUM(AmountPaid) AS Total_Spent FROM expenses WHERE Category = 'Groceries';"},
     
    {"title": "cahback earned each month", 
     "query": "select month(date) AS month, SUM(Cashback) AS total_cashback from all_months_expenses GROUP BY month order by month;"},
     
    {"title": "how has overall spendind changed over time", 
     "query": "select month(date) AS month, SUM(Amount_Paid) AS total_spent from all_months_expenses GROUP BY month order by month;"},
     
    {"title": "Transactions exceeding amount 490", 
     "query": "Select * From all_months_expenses where Amount_Paid > 490;"},
     
    {"title": "Average transaction amount by category", 
     "query": """Select 
	                Category,
                    Avg(Amount_Paid) as Avg_Transaction_Amount
                From all_months_expenses
                group by Category;"""},
     
    {"title": "Maximum and Minimum Transaction amounts", 
     "query": "Select max(Amount_Paid) as Max_Transaction, min(Amount_Paid) as Min_Transaction From all_months_expenses;"},
     
    {"title": "Daily Spending Trends", 
     "query": "Select day(date) as day, sum(Amount_Paid) as Total_Spent From all_months_expenses group by day(date) order by day"},
   
    ]
    st.title("Select Query to Execute")
    query_titles = [q["title"] for q in queries]
    selected_title = st.selectbox("Choose a query:", query_titles)
    
    selected_query = next(q["query"] for q in queries if q["title"] == selected_title)


    # Button to execute the query
    if st.button("Execute Query"):
        try:
            # Connect to the database
            connection = mysql.connector.connect(
                host=localhost,
                user=root,
                password=12345678,
                database=expensetracker
            )
            cursor = connection.cursor(dictionary=True)
            
            # Execute the selected query
            cursor.execute(selected_query)
            results = cursor.fetchall()

            # Convert results to Pandas DataFrame
            df = pd.DataFrame(results)
            st.write("### Query")

            st.write(selected_query)
            # Display the results
            if df.empty:
                st.warning("The query returned no results.")
            else:
                st.write("### Query Results")
                st.dataframe(df)

        except mysql.connector.Error as e:
            st.error(f"Error: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

#Visualizations Tab
with tab3:
    st.header("Visualizations")
    
    # Creating two columns
    col1, col2 = st.columns(2)

    # 1. Bar Chart: Total expenses by category
    with col1:
        category_expenses = data.groupby('Category')['Amount_Paid'].sum()
        fig1, ax1 = plt.subplots(figsize=(12, 6))
        category_expenses.plot(kind='bar', color='skyblue', edgecolor='black', ax=ax1)
        ax1.set_title('Total Expenses by Category', fontsize=16)
        ax1.set_xlabel('Category', fontsize=12)
        ax1.set_ylabel('Total Amount Paid', fontsize=12)
        ax1.tick_params(axis='x', rotation=45)
        st.pyplot(fig1)
        st.caption("Bar Chart: Total expenses by category")
    
    # 2. Pie Chart: Distribution of payment modes
    with col2:
        payment_mode_distribution = data['Payment_Mode'].value_counts()
        fig2, ax2 = plt.subplots(figsize=(12,6))
        payment_mode_distribution.plot(
            kind='pie',
            autopct='%1.1f%%',
            startangle=140,
            colors=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99'],
            ax=ax2
        )
        ax2.set_title('Distribution', fontsize=16)
        ax2.set_ylabel('')  # Hide y-label for pie chart
        st.pyplot(fig2)
        st.caption("Pie Chart: Distribution of payment modes")
    
    # 3. Stacked Bar Chart: Expenses by category and payment mode
    with col1:
        expenses_by_category_and_payment = data.pivot_table(
            index='Category', 
            columns='Payment_Mode', 
            values='Amount_Paid', 
            aggfunc='sum', 
            fill_value=0
        )
        fig3, ax3 = plt.subplots(figsize=(12, 6))
        expenses_by_category_and_payment.plot(
            kind='bar', 
            stacked=True, 
            color=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99'], 
            edgecolor='black',
            ax=ax3
        )
        ax3.set_title('Expenses by Category and Payment Mode', fontsize=16)
        ax3.set_xlabel('Category', fontsize=12)
        ax3.set_ylabel('Total Amount Paid', fontsize=12)
        ax3.tick_params(axis='x', rotation=45)
        ax3.legend(title='Payment Mode', fontsize=10)
        st.pyplot(fig3)
        st.caption("Stacked Bar Chart: Expenses by category and payment mode")
    
    
    # 4. Line Graph: Distribution of cashback amounts visualization for stramlit
    with col2:
        fig4, ax4 = plt.subplots(figsize=(12, 6))
        data['Cashback'].plot(kind='line', ax=ax4)
        ax4.set_title('Distribution of Cashback Amounts', fontsize=16)
        ax4.set_xlabel('Cashback Amount', fontsize=12)
        ax4.set_ylabel('Frequency', fontsize=12)
        st.pyplot(fig4)
        st.caption("Histogram: Distribution of cashback amounts")
