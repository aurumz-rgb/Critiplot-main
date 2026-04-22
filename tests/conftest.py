import pytest
import pandas as pd
import os
import sys
from unittest.mock import MagicMock


mock_critiplot = MagicMock()

def mock_plot_func(input_path, output_path, theme=None):
    """
    Simulates the external library function.
    It writes a dummy image file to the app's expected temp location.
    The app will automatically delete this temp folder, so no artifacts remain.
    """

    png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\x0d\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
    

    with open(output_path, 'wb') as f:
        f.write(png_data)

mock_critiplot.plot_nos = mock_plot_func
mock_critiplot.plot_grade = mock_plot_func
mock_critiplot.plot_robis = mock_plot_func
mock_critiplot.plot_jbi_case_report = mock_plot_func
mock_critiplot.plot_jbi_case_series = mock_plot_func
mock_critiplot.plot_mmat = mock_plot_func

sys.modules['critiplot'] = mock_critiplot

@pytest.fixture(scope="session", autouse=True)
def create_sample_data_files():
    files = [
        "nos_data", "grade_data", "robis_data", 
        "case_report", "case_series", "mmat_data"
    ]
    for name in files:
        if not os.path.exists(f"{name}.csv"):
            pd.DataFrame({'Dummy': [1]}).to_csv(f"{name}.csv", index=False)
        if not os.path.exists(f"{name}.xlsx"):
            pd.DataFrame({'Dummy': [1]}).to_excel(f"{name}.xlsx", index=False)