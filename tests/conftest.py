
import pytest
import pandas as pd
import os
import sys
from unittest.mock import MagicMock



mock_critiplot = MagicMock()


mock_critiplot.plot_nos = MagicMock()
mock_critiplot.plot_grade = MagicMock()
mock_critiplot.plot_robis = MagicMock()
mock_critiplot.plot_jbi_case_report = MagicMock()
mock_critiplot.plot_jbi_case_series = MagicMock()
mock_critiplot.plot_mmat = MagicMock()

sys.modules['critiplot'] = mock_critiplot


@pytest.fixture(scope="session", autouse=True)
def create_sample_data_files():
    """Create sample CSV/XLSX files for unit tests."""
    files = [
        "nos_data", "grade_data", "robis_data", 
        "case_report", "case_series", "mmat_data"
    ]
    for name in files:
        if not os.path.exists(f"{name}.csv"):
            pd.DataFrame({'Dummy': [1]}).to_csv(f"{name}.csv", index=False)
        if not os.path.exists(f"{name}.xlsx"):
            pd.DataFrame({'Dummy': [1]}).to_excel(f"{name}.xlsx", index=False)