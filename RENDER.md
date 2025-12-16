# Deploying to Render

## Prerequisites

1. A GitHub account
2. A Render account (free tier available at https://render.com)

## Steps to Deploy

1. Push your code to a GitHub repository
   - Make sure all files are included, especially:
     - `heroku_ready_dashboard.py`
     - `requirements.txt`
     - `render.yaml`
     - `[Final Project]medical_insurance.csv`
     - `runtime.txt`

2. Sign up or log in to Render (https://render.com)

3. Click "New" and select "Web Service"

4. Connect your GitHub account and select your repository

5. Configure your web service:
   - Name: Choose a name for your service
   - Region: Choose the region closest to you
   - Branch: Usually main or master
   - Root Directory: Leave empty if the files are in the root directory
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn --bind 0.0.0.0:$PORT heroku_ready_dashboard:server`

6. Click "Create Web Service"

7. Render will automatically build and deploy your application

8. Once deployment is complete, you'll receive a URL where your dashboard is accessible

## Notes

- Render automatically reads the `render.yaml` file for configuration
- The application will be available at a public URL provided by Render
- Render automatically sets the PORT environment variable
- Initial deployment may take a few minutes as Render installs dependencies

## Troubleshooting

- If deployment fails, check the logs in the Render dashboard
- Ensure all required files are in your repository
- Make sure the data file `[Final Project]medical_insurance.csv` is included
- Check that all dependencies in `requirements.txt` are correctly specified