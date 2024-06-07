import streamlit as st
import requests
import pandas as pd
import altair as alt
from datetime import datetime

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
    st.title("EIA Electricity Data Viewer for PJM Grid")
    
    # Date input widgets
    start_date = st.date_input("Start date", pd.to_datetime("2024-06-01"))
    end_date = st.date_input("End date", datetime.today())
    
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
        df.rename(columns={'value': 'MWH'}, inplace=True)
        
        # Get unique sources of energy generation
        sources = df['fueltype'].unique()
        
        # Allow users to select sources to display
        selected_sources = st.multiselect("Select energy sources to display", sources, default=sources)
        
        # Filter data based on selected sources
        filtered_df = df[df['fueltype'].isin(selected_sources)]
        
        # Pivot the data to have 'period' as index and 'fueltype' as columns
        pivot_df = filtered_df.pivot(index='period', columns='fueltype', values='MWH')
        
        # Allow users to select sorting order
        sort_order = st.radio("Sort by total energy generation", ("Ascending", "Descending"))
        
        # Sort the columns based on total energy generation
        if sort_order == "Ascending":
            pivot_df = pivot_df[pivot_df.sum().sort_values().index]
        else:
            pivot_df = pivot_df[pivot_df.sum().sort_values(ascending=False).index]
        
        # Reset index to use 'period' as a column for Altair
        pivot_df.reset_index(inplace=True)
        
        # Melt the DataFrame for Altair
        melted_df = pivot_df.melt(id_vars=['period'], var_name='fueltype', value_name='MWH')
        
        # Create the Altair bar chart
        chart = alt.Chart(melted_df).mark_bar().encode(
            x='period:T',
            y='MWH:Q',
            color='fueltype:N',
            tooltip=['period:T', 'fueltype:N', 'MWH:Q']
        ).properties(
            title='Energy Generation (Megawatts)',
            width=800,
            height=400
        ).interactive()
        
        # Display the chart
        st.altair_chart(chart, use_container_width=True)
        
        # Display the data table
        st.dataframe(pivot_df)
        
        # Export to CSV
        csv = pivot_df.to_csv().encode('utf-8')
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='energy_data.csv',
            mime='text/csv',
        )
    else:
        st.write("No data available.")

if __name__ == "__main__":
    main()
