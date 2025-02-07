import streamlit as st
import pandas as pd
from datetime import datetime

# File Path (Update if needed)
file_path = r"C:\Users\RyanHasty\Desktop\GovCon Python Model\GovCon Data\ContractOpportunities-20250203-100221.csv"

# Generate today's date for filtering
today_date = datetime.today().strftime("%Y-%m-%d")

# Read the dataset
try:
    data = pd.read_csv(file_path, encoding='latin1')
except UnicodeDecodeError:
    st.error("Encoding error. Try another encoding like 'cp1252'.")
    st.stop()

# Columns to extract
columns_to_extract = [
    "Notice ID", "Title", "Current Response Date",
    "Contract Opportunity Type", "Active/Inactive", "NAICS", "Set Aside"
]

# Check for missing columns
missing_columns = [col for col in columns_to_extract if col not in data.columns]
if missing_columns:
    st.error(f"Missing columns: {missing_columns}")
    st.stop()
else:
    extracted_data = data[columns_to_extract]

# Convert 'Current Response Date' to datetime format
extracted_data["Current Response Date"] = pd.to_datetime(
    extracted_data["Current Response Date"], errors='coerce'
)

# Filter for valid contract opportunity types
valid_opportunity_types = ["Sources Sought", "Presolicitation", "Solicitation", "Combined Synopsis/Solicitation"]
filtered_data = extracted_data[extracted_data["Contract Opportunity Type"].isin(valid_opportunity_types)]

# Filter for only future or today’s response dates
filtered_data = filtered_data[filtered_data["Current Response Date"] >= pd.to_datetime(today_date)]

# NAICS categories to filter
naics_filter = [
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

# Apply NAICS filter
filtered_data = filtered_data[filtered_data["NAICS"].isin(naics_filter)]

# Streamlit App
st.title("Contract Opportunities Dashboard")

# Sidebar Filters
st.sidebar.header("Filter Options")

# Contract Status Filter
status_options = filtered_data["Active/Inactive"].dropna().unique()
selected_status = st.sidebar.multiselect("Select Status:", status_options, default=status_options)

# NAICS Filter
naics_options = filtered_data["NAICS"].dropna().unique()
selected_naics = st.sidebar.multiselect("Select NAICS Code:", naics_options, default=naics_options)

# Set-Aside Filter
set_aside_options = filtered_data["Set Aside"].dropna().unique()
selected_set_aside = st.sidebar.multiselect("Select Set-Aside Type:", set_aside_options, default=set_aside_options)

# Apply filters
filtered_df = filtered_data[
    (filtered_data["Active/Inactive"].isin(selected_status)) &
    (filtered_data["NAICS"].isin(selected_naics)) &
    (filtered_data["Set Aside"].isin(selected_set_aside))
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

# Show a preview of the raw dataset
st.write("Preview of the dataset:")
st.dataframe(extracted_data.head())