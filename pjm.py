import streamlit as st
import requests
import pandas as pd

# Read API key from Streamlit secrets
API_KEY = st.secrets["EIA_API_KEY"]

# EIA API URL and Parameters
EIA_API_URL = "https://api.eia.gov/v2/electricity/rto/fuel-type-data/data/"

# Function to fetch data from EIA API
def fetch_data(start_date, end_date):
    params = {
        "api_key": API_KEY,
        "frequency": "hourly",
        "data[0]": "value",
        "facets[respondent][]": "PJM",
        "start": start_date,
        "end": end_date,
        "sort[0][column]": "period",
        "sort[0][direction]": "desc",
        "offset": 0,
        "length": 5000
    }
    response = requests.get(EIA_API_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch data: {response.status_code}")
        return None

# Streamlit app
def main():
    st.title("EIA Electricity Data Viewer")
    
    # Date input widgets
    start_date = st.date_input("Start date", pd.to_datetime("2024-06-01"))
    end_date = st.date_input("End date", pd.to_datetime("2024-06-02"))
    
    if start_date > end_date:
        st.error("Error: End date must fall after start date.")
        return
    
    st.write("Fetching data from EIA API...")
    data = fetch_data(start_date.strftime("%Y-%m-%dT%H"), end_date.strftime("%Y-%m-%dT%H"))
    
    if data:
        df = pd.DataFrame(data['response']['data'])
        st.write("Data fetched successfully!")
        
        # Convert 'period' to datetime
        df['period'] = pd.to_datetime(df['period'])
        
        # Rename 'value' column to avoid conflicts
        df.rename(columns={'value': 'energy_value'}, inplace=True)
        
        # Get unique sources of energy generation
        sources = df['fueltype'].unique()
        
        # Allow users to select sources to display
        selected_sources = st.multiselect("Select energy sources to display", sources, default=sources)
        
        # Filter data based on selected sources
        filtered_df = df[df['fueltype'].isin(selected_sources)]
        
        # Pivot the data to have 'period' as index and 'fueltype' as columns
        pivot_df = filtered_df.pivot(index='period', columns='fueltype', values='energy_value')
        
        # Plot the data
        st.line_chart(pivot_df)
    else:
        st.write("No data available.")

if __name__ == "__main__":
    main()
