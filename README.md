# Analisis Segmentasi Konten Hoaks di Indonesia

This project aims to analyze and segment hoax content in Indonesia using a Streamlit dashboard. The dashboard provides various insights into the nature of hoax content, its trends, and segmentation analysis.

## Project Structure

- **app.py**: Main entry point for the Streamlit application.
- **pages/**: Contains different pages of the dashboard:
  - **1_Overview.py**: Overview of the analysis.
  - **2_Segmentation.py**: Segmentation analysis insights.
  - **3_Trends.py**: Trend analysis of hoax content.
  - **4_Admin.py**: Administrative functions for data management.
  
- **data/**: Contains raw and processed data.
  - **raw/**: Documentation about the raw data.
  - **processed/**: Information about the processed data structure.
  
- **db/**: Database related files.
  - **schema.sql**: SQL schema defining the database structure.
  - **connection.py**: Handles database connection logic.
  
- **services/**: Contains functions for analysis and data processing.
  - **segmentation.py**: Functions for content segmentation analysis.
  - **preprocessing.py**: Functions for data preprocessing.
  - **analytics.py**: Analytical functions for deriving insights.
  
- **utils/**: Utility functions and constants.
  - **constants.py**: Defines constants used throughout the project.
  - **helpers.py**: Contains helper functions for various tasks.
  
- **tests/**: Unit tests for the project functionalities.
  - **test_segmentation.py**: Tests for segmentation functionality.
  - **test_preprocessing.py**: Tests for preprocessing functions.
  
- **requirements.txt**: Lists dependencies required for the project.
- **.streamlit/**: Configuration files for the Streamlit application.
  - **config.toml**: Configuration settings for the app.
  - **secrets.toml**: Stores sensitive information securely.

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd analisis-segmentasi-konten-hoaks-indonesia
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up the database using the schema provided in `db/schema.sql`.

4. Run the Streamlit application:
   ```
   streamlit run app.py
   ```

## Usage

Navigate through the dashboard to explore the different analyses related to hoax content in Indonesia. Each page provides specific insights and functionalities to understand the segmentation and trends of hoax content effectively.