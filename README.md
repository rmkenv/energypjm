# EIA Electricity Data Viewer

This Streamlit app fetches and displays electricity data from the EIA (U.S. Energy Information Administration) API. Users can filter the data by the source of energy generation and date range, and view the data as a bar chart. The app also provides an option to export the data to a CSV file. (EIA Open data: https://www.eia.gov/opendata/) 

## Features

- Fetches electricity data from the EIA API.
- Allows users to filter data by the source of energy generation.
- Allows users to select a date range for the data.
- Displays the data as a bar chart with tooltips showing the time, fuel type, and MWH.
- Provides an option to export the data to a CSV file.
- Allows users to sort the y-axis based on total energy generation.

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/eia-electricity-data-viewer.git
    cd eia-electricity-data-viewer
    ```

2. Create a virtual environment and activate it:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required libraries:

    ```sh
    pip install -r requirements.txt
    ```

4. Create a `secrets.toml` file in the root directory of your project and add your EIA API key:

    ```toml
    # secrets.toml
    EIA_API_KEY = "YOUR_API_KEY_HERE"
    ```

## Usage

1. Run the Streamlit app:

    ```sh
    streamlit run app.py
    ```

2. Open your web browser and go to `http://localhost:8501` to view the app.

## File Structure
