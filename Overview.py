import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

portfolio_data = pd.read_csv('data/Portfolio_data.csv')
communication_history = pd.read_csv('data/CommunicationHistory.csv')
merged_df = pd.merge(portfolio_data, communication_history, on="Loan Number")

st.title('Loan Customer Dashboard')
st.subheader('The Data')

st.write("*Portfolio_data.csv* -> Contains the loan portfolio of the customers. Columns include Loan Number, Due Date, State, DOB and Loan Amount.")
st.write(portfolio_data.head(10))
st.write("*CommunicationHistory.csv* -> Contains the communication history of the customers. Columns include Loan Number, Campaign ID, Status, Date and Time.")
st.write(communication_history.head(10))

st.subheader('Tech Used')
st.write("- Streamlit \n- Pandas  \n- Plotly \n- Matplotlib")
