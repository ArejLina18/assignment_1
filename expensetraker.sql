#1 Total Expenditure
SHOW TABLES FROM expensetracker;
USE expensetracker;
#1 Total amount spent in each category
Select Category, SUM(Amount_Paid) AS total_spent
from all_months_expenses
GROUP BY Category;
#2 total amount spent using each payment mode
SELECT Payment_Mode, SUM(Amount_Paid) AS total_spent
from all_months_expenses
GROUP BY Payment_Mode;
#3 TOTAL CASHBACK RECIEVED ACROSS ALL TRANSACTIONS
SELECT SUM(Cashback) AS total_cashback
from all_months_expenses;
#4 top 5 most expensive categories in terms of spending
SELECT Category, SUM(Amount_Paid) AS total_spent
from all_months_expenses
GROUP BY Category
Order by total_spent DESC
LIMIT 5;
#5 TOTAL AMOUNT SPENT ON TRANSPORTATION USING DIFFERENT PAYMENT MODE
SELECT Payment_Mode, SUM(Amount_Paid) AS total_spent
from all_months_expenses
WHERE Category='Transportation'
GROUP BY Payment_Mode;
#6 which transaction resulted in cashback?
select *
from all_months_expenses
where cashback > 0;
#7total spending in each month of the year
select month(date) AS month, SUM(Amount_Paid) AS total_spent
from all_months_expenses
GROUP BY month
order by month;
#8 Days with highest spending
SELECT Date, SUM(AmountPaid) AS Total_Spent 
FROM all_months_expenses
 GROUP BY Date
 ORDER BY Total_Spent DESC
 LIMIT 5;
#9 Total amount spent on 'Groceries
SELECT SUM(AmountPaid) AS Total_Spent 
FROM all_months_expenses
WHERE Category = 'Groceries';
#10 cahback earned each month
select month(date) AS month, SUM(Cashback) AS total_cashback
from all_months_expenses
GROUP BY month
order by month;
#11 how has overall spendind changed over time
select month(date) AS month, SUM(Amount_Paid) AS total_spent
from all_months_expenses
GROUP BY month
order by month;
#12 Transactions exceeding amount 490
Select *
From all_months_expenses
where Amount_Paid > 490;
#13 Average transaction amount by category
Select 
	Category,
    Avg(Amount_Paid) as Avg_Transaction_Amount
From all_months_expenses
group by Category;
#14 Maximum and Minimum Transaction amounts
Select
	max(Amount_Paid) as Max_Transaction,
    min(Amount_Paid) as Min_Transaction
From all_months_expenses;
#15 Daily Spending Trends
Select 
	day(date) as day,
    sum(Amount_Paid) as Total_Spent
From all_months_expenses
group by day(date)
order by day







