import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
portfolio_data = pd.read_csv('data/Portfolio_data.csv')

portfolio_data["State"] = portfolio_data["State"].str.lower().str.capitalize()
communication_history = pd.read_csv('data/CommunicationHistory.csv')
merged_df = pd.merge(portfolio_data, communication_history, on="Loan Number")


titles = ['1. Distribution of loans across different states', "2. Distribution of loans across different amounts", "3. Distribution of customers by age",
          "4. Distribution of loans by due dates", "5. Unique number of customers contacted on daily basis", "6. Number of customers not contacted on daily basis", "7. Who are the customers who have been contacted the most", "8. Who are the customers who have been contacted the least", "9. How many customers have never been reached out?", "10. Distribution of calls by states.", "11. Distribution of calls by campaign ids", "12. Unique number of customers by campaign ID"]
st.title('Loan Customer Dashboard')


st.sidebar.title('12 Findings')
page = st.sidebar.multiselect(
    'Select/Deselect the findings you want to see/unsee', titles, default=titles)


if titles[0] in page:
    st.subheader(titles[0])
    loans_by_state = portfolio_data.groupby(
        'State')['Loan Number'].count().sort_values(ascending=False)
    col1, col2 = st.columns(2)
    with col1:
        st.write(loans_by_state)
    with col2:
        fig = px.bar(loans_by_state.head(10),
                     labels={'x': 'State', 'y': 'Number of Loans'},
                     title=f'State Distribution')
        st.plotly_chart(fig)
    st.write('- **Maharashtra** has the highest number of loans. Other states topping the list are **Tamil Nadu, Karnataka & Telangana**')
    st.write('- **Pondicherry, Mizoram, Madhya Pradesh, Chattisgarh, Haryana** has the least number of loans')
    st.write('- States in the South have the highest number of loans.')
    st.write('')

if titles[1] in page:
    st.subheader(titles[1])

    fig = px.histogram(portfolio_data, x="Loan Amount", nbins=50,
                       title="Distribution of loans across different amounts")
    fig.update_xaxes(title_text='Loan Amount')
    fig.update_yaxes(title_text='Count')
    st.plotly_chart(fig)
    st.write(
        '- Most of the loans can be approximated to be in the range of **2500 to 7500**')
    st.write('')

if titles[2] in page:
    st.subheader(titles[2])
    portfolio_data['Age'] = pd.to_datetime(
        portfolio_data['DOB'], errors='coerce').dt.year
    portfolio_data['Age'] = 2023 - portfolio_data['Age']

    fig = px.histogram(portfolio_data, x="Age", nbins=100,
                       title="Distribution of customers by age")
    fig.update_xaxes(title_text='Age')
    fig.update_yaxes(title_text='Count')
    st.plotly_chart(fig)
    st.write(
        '- Age group of **20 - 26** have the highest number of loans - **1000+**')
    st.write('- Loans are provided to teens as well of age **16 +**')
    st.write('')

if titles[3] in page:
    st.subheader(titles[3])
    portfolio_data['Due Date'] = pd.to_datetime(
        portfolio_data['Due Date'], errors='coerce').dt.date
    portfolio_data['Due Date'] = pd.to_datetime(
        portfolio_data['Due Date'], errors='coerce').dt.day
    fig = px.histogram(portfolio_data, x="Due Date", nbins=100,
                       title="Distribution of loans by due dates")
    fig.update_xaxes(title_text='Due Date')
    fig.update_yaxes(title_text='Count')
    st.plotly_chart(fig)
    st.write(
        "- A huge number of the loans are due on the **first 5 days** of the month")
    st.write("- Many Loans are due on the **19 - 25 of the month** as well")
    st.write('')

if titles[4] in page:
    st.subheader(titles[4])
    completed_calls = communication_history[communication_history['Status'] == 'completed']
    completed_calls['Date'] = pd.to_datetime(
        completed_calls['Call time'], errors='coerce').dt.date
    unique_customers_contacted = completed_calls.groupby(
        'Date')['Loan Number'].nunique()
    unique_customers_contacted = unique_customers_contacted.to_frame()
    unique_customers_contacted.columns = ['Number of customers contacted']
    st.write(unique_customers_contacted)
    st.write("")

if titles[5] in page:
    st.subheader(titles[5])
    completed_calls = communication_history[communication_history["Status"] == "completed"]
    completed_calls["Call time"] = pd.to_datetime(completed_calls["Call time"])
    completed_calls["Call Date"] = completed_calls["Call time"].dt.date
    unique_customers_contacted = completed_calls.groupby([completed_calls["Call Date"], "Loan Number"])[
        "Loan Number"].count().reset_index(name="Count")

    total_customers = len(communication_history["Loan Number"].unique())

    customers_not_contacted = {}
    for date in unique_customers_contacted["Call Date"].unique():
        customers_contacted = unique_customers_contacted[unique_customers_contacted["Call Date"] == date]
        customers_not_contacted[str(
            date)] = total_customers - len(customers_contacted)
    NotContactedFrame = pd.DataFrame.from_dict(
        customers_not_contacted, orient='index', columns=['Number of customers not contacted'])
    st.write(NotContactedFrame)
    st.write("")


if titles[6] in page:
    st.subheader(titles[6])
    most_contacted_customers = communication_history.groupby(
        'Loan Number')['Loan Number'].count().sort_values(ascending=False)
    most_contacted_customers = most_contacted_customers.to_frame()
    most_contacted_customers.columns = ['Number of times contacted']
    most_contacted_customers = most_contacted_customers.head(10)
    st.write(most_contacted_customers)
    st.write('- These are the top 10 customers who were contacted the most')
    st.write('- **Loan No. 1,659,081** applicant was contacted **38 times**')
    st.write("")

if titles[7] in page:
    st.subheader(titles[7])
    least_contacted_customers = communication_history.groupby(
        'Loan Number')['Loan Number'].count().sort_values(ascending=True)
    least_contacted_customers = least_contacted_customers[least_contacted_customers == 1]
    least_contacted_customers = least_contacted_customers.to_frame()
    least_contacted_customers.columns = ['Number of times contacted']
    st.write("Around **"+str(len(least_contacted_customers)) +
             "** customers were contacted only once")
    st.write(least_contacted_customers)

if titles[8] in page:
    st.subheader(titles[8])
    loan_numbers = communication_history['Loan Number'].unique()
    customers_never_contacted = portfolio_data[portfolio_data['Loan Number'].isin(
        loan_numbers) == False]['Loan Number'].count()
    st.write("**"+str(customers_never_contacted) +
             '** Customers were never contacted')
    st.write('')

if titles[9] in page:
    st.subheader(titles[9])
    calls_by_state = merged_df['State'].value_counts(
    ).sort_values(ascending=False)
    st.plotly_chart(px.bar(calls_by_state))

    st.write('- The highest number of calls are from the state of **Maharashtra**')
    st.write('')


if titles[10] in page:
    st.subheader(titles[10])
    calls_by_campaign = communication_history.groupby('Campaign ID')[
        'Loan Number'].count().sort_values(ascending=False)
    calls_by_campaign = calls_by_campaign.to_frame()
    calls_by_campaign.columns = ['Number of calls']
    st.write(calls_by_campaign)
    st.write('- Most of the calls are from **Campaign 164,168,595**')
    st.write('- Least number of calls are from **Campaign 135,474,249**')
    st.write('')


if titles[11] in page:
    st.subheader(titles[11])
    unique_customers_by_campaign = communication_history.groupby('Campaign ID')[
        'Loan Number'].nunique().sort_values(ascending=False)
    st.write(unique_customers_by_campaign)
    st.write(
        '- Most of the customers have been targeted in the **Campaign 164,168,595**')
    st.write('- Least number of customers have been targeted in **Campaign 161,307,935** and **Campaign 135,474,249**')
