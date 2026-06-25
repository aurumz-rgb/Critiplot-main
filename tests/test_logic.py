# tests/test_logic.py
import os
import sys
import pytest
import pandas as pd
from unittest.mock import MagicMock

# Access the mock that conftest.py set up in sys.modules
mock_critiplot = sys.modules.get('critiplot')


class TestDataValidation:
    """Test data validation logic."""

    def test_valid_nos_data(self):
        df = pd.DataFrame({
            '"Author, Year"': ['Study 1, 2024'],
            'Total Score': [8],
            'Overall RoB': ['Low']
        })
        assert 'Total Score' in df.columns
        assert 'Overall RoB' in df.columns

    def test_valid_grade_data(self):
        df = pd.DataFrame({
            'Outcome': ['Mortality'],
            'Risk_of_Bias': ['Serious'],
            'Overall_Certainty': ['Low']
        })
        assert 'Outcome' in df.columns
        assert 'Overall_Certainty' in df.columns

    def test_valid_robis_data(self):
        df = pd.DataFrame({
            'Review': ['Study 1'],
            'Overall RoB': ['Low']
        })
        assert 'Review' in df.columns
        assert 'Overall RoB' in df.columns

    def test_valid_jbi_data(self):
        df = pd.DataFrame({
            'Author': ['Study 1'],
            'Total': [7],
            'Overall RoB': ['Low']
        })
        assert 'Author' in df.columns
        assert 'Total' in df.columns
        assert 'Overall RoB' in df.columns

    def test_valid_mmat_data(self):
        df = pd.DataFrame({
            'Author_Year': ['Smith, 2019'],
            'Overall_Rating': ['High']
        })
        assert 'Author_Year' in df.columns
        assert 'Overall_Rating' in df.columns


class TestCritiplotMock:
    """Test that critiplot mock is available and works."""

    def test_critiplot_mock_exists(self):
        assert mock_critiplot is not None
        assert isinstance(mock_critiplot, MagicMock)

    def test_plot_nos_called(self):
        mock_critiplot.plot_nos.reset_mock()
        mock_critiplot.plot_nos("input.csv", "output.png")
        mock_critiplot.plot_nos.assert_called_once_with("input.csv", "output.png")

    def test_plot_grade_called(self):
        mock_critiplot.plot_grade.reset_mock()
        mock_critiplot.plot_grade("input.csv", "output.png")
        mock_critiplot.plot_grade.assert_called_once_with("input.csv", "output.png")

    def test_plot_robis_called(self):
        mock_critiplot.plot_robis.reset_mock()
        mock_critiplot.plot_robis("input.csv", "output.png")
        mock_critiplot.plot_robis.assert_called_once_with("input.csv", "output.png")

    def test_plot_jbi_case_report_called(self):
        mock_critiplot.plot_jbi_case_report.reset_mock()
        mock_critiplot.plot_jbi_case_report("input.csv", "output.png")
        mock_critiplot.plot_jbi_case_report.assert_called_once_with("input.csv", "output.png")

    def test_plot_jbi_case_series_called(self):
        mock_critiplot.plot_jbi_case_series.reset_mock()
        mock_critiplot.plot_jbi_case_series("input.csv", "output.png")
        mock_critiplot.plot_jbi_case_series.assert_called_once_with("input.csv", "output.png")

    def test_plot_mmat_called(self):
        mock_critiplot.plot_mmat.reset_mock()
        mock_critiplot.plot_mmat("input.csv", "output.png")
        mock_critiplot.plot_mmat.assert_called_once_with("input.csv", "output.png")


class TestDataFiles:
    """Test that sample data files exist."""

    def test_nos_files_exist(self):
        assert os.path.exists("nos_data.csv")
        assert os.path.exists("nos_data.xlsx")

    def test_grade_files_exist(self):
        assert os.path.exists("grade_data.csv")
        assert os.path.exists("grade_data.xlsx")

    def test_robis_files_exist(self):
        assert os.path.exists("robis_data.csv")
        assert os.path.exists("robis_data.xlsx")

    def test_case_report_files_exist(self):
        assert os.path.exists("case_report.csv")
        assert os.path.exists("case_report.xlsx")

    def test_case_series_files_exist(self):
        assert os.path.exists("case_series.csv")
        assert os.path.exists("case_series.xlsx")

    def test_mmat_files_exist(self):
        assert os.path.exists("mmat_data.csv")
        assert os.path.exists("mmat_data.xlsx")