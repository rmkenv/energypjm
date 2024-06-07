import streamlit as st
import requests
import pandas as pd

# Read API key from Streamlit secrets
API_KEY = st.secrets["EIA_API_KEY"]

# EIA API URL and Parameters
EIA_API_URL = "https://api.eia.gov/v2/electricity/rto/fuel-type-data/data/"

PARAMS = {
    "api_key": API_KEY,
    "frequency": "hourly",
    "data[0]": "value",
    "facets[respondent][]": "PJM",
    "start": "2024-06-01T00",
    "sort[0][column]": "period",
    "sort[0][direction]": "desc",
    "offset": 0,
    "length": 5000
}

# Function to fetch data from EIA API
def fetch_data():
    response = requests.get(EIA_API_URL, params=PARAMS)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch data: {response.status_code}")
        return None

# Streamlit app
def main():
    st.title("EIA Electricity Data Viewer")
    
    st.write("Fetching data from EIA API...")
    data = fetch_data()
    
    if data:
        df = pd.DataFrame(data['response']['data'])
        st.write("Data fetched successfully!")
        
        # Convert 'period' to datetime
        df['period'] = pd.to_datetime(df['period'])
        
        # Rename 'value' column to avoid conflicts
        df.rename(columns={'value': 'energy_value'}, inplace=True)
        
        # Plot the data
        st.line_chart(df.set_index('period')['energy_value'])
    else:
        st.write("No data available.")

if __name__ == "__main__":
    main()
