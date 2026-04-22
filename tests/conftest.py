import pytest
import pandas as pd
import os
import matplotlib


matplotlib.use('Agg')


@pytest.fixture(scope="session", autouse=True)
def create_sample_data_files():
    """
    Your app.py tries to read these files on startup.
    We create dummy versions so the app loads without crashing.
    """
    files = [
        "nos_data", "grade_data", "robis_data", 
        "case_report", "case_series", "mmat_data"
    ]
    
    for name in files:
        csv_path = f"{name}.csv"
        xlsx_path = f"{name}.xlsx"
        
        if not os.path.exists(csv_path):
            pd.DataFrame({'Study': ['Sample']}).to_csv(csv_path, index=False)
            
        if not os.path.exists(xlsx_path):
            pd.DataFrame({'Study': ['Sample']}).to_excel(xlsx_path, index=False)