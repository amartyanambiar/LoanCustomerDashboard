import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt

portfolio_data = pd.read_csv('data/Portfolio_data.csv')
communication_history = pd.read_csv('data/CommunicationHistory.csv')
merged_df = pd.merge(portfolio_data, communication_history, on="Loan Number")


st.title('Additional Insights')

st.subheader('1. States with highest "completed" calls')
completed_calls = merged_df[merged_df['Status'] == 'completed']
completed_calls = completed_calls.groupby(
    'State')['Loan Number'].count().sort_values(ascending=False)
completed_calls = completed_calls.to_frame()
completed_calls.columns = ['Number of completed calls']
col1, col2 = st.columns(2)
with col1:
    st.write(completed_calls)
with col2:
    st.bar_chart(completed_calls.head(10))
st.write('- **Maharashtra** has the highest number of completed calls')
st.write('- **Madhya Pradesh** has the least number of completed calls')
st.write("")

st.subheader('2. States with highest "failed" calls')
failed_calls = merged_df[merged_df['Status'] == 'FAILED']
failed_calls = failed_calls.groupby(
    'State')['Loan Number'].count().sort_values(ascending=False)
failed_calls = failed_calls.to_frame()
failed_calls.columns = ['Number of failed calls']
col1, col2 = st.columns(2)
with col1:
    st.write(failed_calls)
with col2:
    st.bar_chart(failed_calls.head(10))
st.write('- Only **9 States** have failed calls')
st.write('- **Maharashtra** has the highest number (5) of failed calls. Considering the high number of loans in Maharashtra, this is not a significant number')
st.write('- **West Bengal** has the least number of failed calls')
st.write('- Focus on Delhi. It has very high number of failed calls in comparison to the total loans')
st.write("")

st.subheader('3. Select Campaign ID to see the "Age" of customers targeted')
campaign_id = st.selectbox(
    'Select Campaign ID', merged_df['Campaign ID'].unique())
campaign_id_df = merged_df[merged_df['Campaign ID'] == campaign_id]
campaign_id_df['Age'] = pd.to_datetime(
    campaign_id_df['DOB'], errors='coerce').dt.year
campaign_id_df['Age'] = 2023 - campaign_id_df['Age']
fig = px.histogram(campaign_id_df, x="Age", nbins=100,
                   title=f"Distribution of customers by age for Campaign ID {campaign_id}")
fig.update_xaxes(title_text='Age')
fig.update_yaxes(title_text='Count')
st.plotly_chart(fig)
st.write('- Campaigns like **166790104** and **167104482** have a high number of customers in the age group of **20-24**')
st.write('- Campaigns like **167104481** have targeted customers in the ages of **24, 32**')
st.write("")


st.subheader('4. Select Campaign ID to see the "State" of customers targeted')
campaign_id1 = st.selectbox(
    'Select Campaign ID', merged_df['Campaign ID'].unique(), key=f"state")
campaign_id_df = merged_df[merged_df['Campaign ID'] == campaign_id1]
state_counts = campaign_id_df["State"].value_counts()
fig = px.bar(x=state_counts.index, y=state_counts.values, color=state_counts.index,
             labels={'x': 'State', 'y': 'Number of Customers'},
             title=f'State Distribution for Campaign ID {campaign_id1}')
st.plotly_chart(fig)
st.write('- Campaigns like **166790104** have targeted many states. Prioiritised states like **Maharashtra, Karnataka* & *Tamil Nadu**')
st.write('- Campaigns **167104481** has not been very successful in targeting customers in states with high number of loans like **Maharashtra, Karnataka & Tamil Nadu**')
st.write("")


st.subheader("5. Loan Amount vs Age Analysis")
merged_df['Age'] = pd.to_datetime(
    merged_df['DOB'], errors='coerce').dt.year
merged_df['Age'] = 2023 - merged_df['Age']
fig = px.scatter(merged_df, x="Age", y="Loan Amount",
                 title="Loan Amount vs Age Analysis")
fig.update_xaxes(title_text='Age')
fig.update_yaxes(title_text='Loan Amount')
st.plotly_chart(fig)
st.write('- **Age** does seem to have a significant impact on the **Loan Amount**')
st.write('- In the age group of **16-25**, we can see a consistent increase in the **Loan Amount**')
st.write('- And then the plot flattens out, then the Loan Amount drops significantly after the approximate age of **38-40** in most cases')
