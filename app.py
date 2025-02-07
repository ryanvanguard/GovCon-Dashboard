import streamlit as st
import pandas as pd
from datetime import datetime

# ✅ Use the correct GitHub raw URL
csv_url = "https://raw.githubusercontent.com/ryanvanguard/GovCon-Dashboard/main/ContractOpportunities-20250206-115602.csv"

# Load the dataset from GitHub
@st.cache_data
def load_data():
    try:
        return pd.read_csv(csv_url, encoding='latin1')
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on failure

data = load_data()

# Check if data is loaded
if data.empty:
    st.error("Failed to load data. Please check the file URL or format.")
    st.stop()

# Convert 'Current Response Date' to datetime
data["Current Response Date"] = pd.to_datetime(data["Current Response Date"], errors='coerce')

# ✅ Filter for only the following contract opportunity types
valid_opportunity_types = ["Sources Sought", "Presolicitation", "Solicitation", "Combined Synopsis/Solicitation"]
data = data[data["Contract Opportunity Type"].isin(valid_opportunity_types)]

# ✅ Filter for only future or today’s response dates
today_date = pd.to_datetime(datetime.today().strftime("%Y-%m-%d"))
data = data[data["Current Response Date"] >= today_date]

# ✅ Filter for only these specific NAICS codes
allowed_naics = [
    "Commercial and Institutional Building Construction",
    "Surgical and Medical Instrument Manufacturing",
    "Surgical Appliance and Supplies Manufacturing",
    "Hazardous Waste Treatment and Disposal",
    "Couriers and Express Delivery Services",
    "Testing Laboratories",
    "Analytical Laboratory Instrument Manufacturing",
    "Diagnostic Imaging Centers",
    "Medical Laboratories"
]

data = data[data["NAICS"].isin(allowed_naics)]  # ✅ Remove contracts that don't match these NAICS codes

# Streamlit App
st.title("Contract Opportunities Dashboard")

# Sidebar Filters
st.sidebar.header("Filter Options")

# Contract Status Filter
status_options = data["Active/Inactive"].dropna().unique()
selected_status = st.sidebar.multiselect("Select Status:", status_options, default=status_options)

# NAICS Filter (Only shows allowed NAICS codes)
naics_options = sorted(data["NAICS"].dropna().unique())
selected_naics = st.sidebar.multiselect("Select NAICS Code:", naics_options, default=naics_options)

# Set-Aside Filter
set_aside_options = data["Set Aside"].dropna().unique()
selected_set_aside = st.sidebar.multiselect("Select Set-Aside Type:", set_aside_options, default=set_aside_options)

# Apply sidebar filters
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