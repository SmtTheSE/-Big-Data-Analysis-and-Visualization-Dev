# Egypt Real Estate Dashboard

A comprehensive dashboard for analyzing the Egypt real estate market.

## Features

- Property type distribution analysis
- Price analysis with visualizations
- Bedroom and bathroom distribution
- Location-based analysis
- Correlation analysis between variables

## Deployment to Render

1. Push this repository to GitHub or GitLab
2. Create a new Web Service on Render
3. Connect your repository
4. Configure the following settings:
   - Build Command: `./build.sh`
   - Start Command: `streamlit run real_estate_dashboard_app.py --server.port $PORT`
   - Environment Variables:
     - `PYTHON_VERSION`: `3.10.8`

## Local Development

1. Clone the repository
2. Install requirements:
   ```
   pip install -r requirements.txt
   ```
3. Run the app:
   ```
   streamlit run real_estate_dashboard_app.py
   ```

## Files Required

Make sure the following files are in your repository:
- `real_estate_dashboard_app.py` (main application)
- `detailed_cleaned_egypt_real_estate.csv` (data file)
- `eda_output/` directory with EDA results (optional but recommended)

## Troubleshooting

If you encounter issues during deployment:
1. Check that all data files are included in the repository
2. Ensure file paths in the code match your repository structure
3. Verify that all dependencies are listed in requirements.txt
4. Make sure the build.sh script has execute permissions