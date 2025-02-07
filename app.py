import streamlit as st
import pandas as pd
from datetime import datetime

# GitHub raw file URL (Replace with your actual GitHub username & repo)
csv_url = "https://raw.githubusercontent.com/YOUR_GITHUB_USERNAME/GovCon-Dashboard/main/ContractOpportunities-20250203-100221.csv"

# Load the dataset from GitHub
@st.cache_data
def load_data():
    return pd.read_csv(csv_url, encoding='latin1')

data = load_data()

# Convert 'Current Response Date' to datetime
data["Current Response Date"] = pd.to_datetime(data["Current Response Date"], errors='coerce')

# Filter for contract opportunity types
valid_opportunity_types = ["Sources Sought", "Presolicitation", "Solicitation", "Combined Synopsis/Solicitation"]
data = data[data["Contract Opportunity Type"].isin(valid_opportunity_types)]

# Filter for only future or today’s response dates
today_date = pd.to_datetime(datetime.today().strftime("%Y-%m-%d"))
data = data[data["Current Response Date"] >= today_date]

# Streamlit App
st.title("Contract Opportunities Dashboard")

# Sidebar Filters
st.sidebar.header("Filter Options")

# Contract Status Filter
status_options = data["Active/Inactive"].dropna().unique()
selected_status = st.sidebar.multiselect("Select Status:", status_options, default=status_options)

# NAICS Filter
naics_options = data["NAICS"].dropna().unique()
selected_naics = st.sidebar.multiselect("Select NAICS Code:", naics_options, default=naics_options)

# Set-Aside Filter
set_aside_options = data["Set Aside"].dropna().unique()
selected_set_aside = st.sidebar.multiselect("Select Set-Aside Type:", set_aside_options, default=set_aside_options)

# Apply filters
filtered_df = data[
    (data["Active/Inactive"].isin(selected_status)) &
    (data["NAICS"].isin(selected_naics)) &
    (data["Set Aside"].isin(selected_set_aside))
]

# Display results
st.subheader(f"Filtered Contract Opportunities ({len(filtered_df)} results)")
st.dataframe(filtered_df)

# Download Button for Filtered Data
st.download_button(
    label="Download Filtered Data as CSV",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_contract_opportunities.csv",
    mime="text/csv"
)