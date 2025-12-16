import zipfile
import os

# Files to include in the zip archive
files_to_zip = [
    'Medical_Insurance_Cost_Prediction_Report.docx',
    'Medical_Insurance_Cost_Prediction_Report.txt',
    'README.md',
    '[Final Project]medical_insurance.csv',
    'cost_relationships.png',
    'dashboard.py',
    'data_analysis_script.py',
    'data_distribution.png',
    'feature_importance.png',
    'project_summary.md',
    'requirements.txt',
    'generate_report.py',
    'create_zip.py'
]

# Create a zip file
with zipfile.ZipFile('project.zip', 'w') as zipf:
    for file in files_to_zip:
        if os.path.exists(file):
            zipf.write(file)

print("Project files have been archived into project.zip")