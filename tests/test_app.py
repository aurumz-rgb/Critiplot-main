import pytest
from streamlit.testing.v1 import AppTest
import io

APP_FILE = "app.py"


class DummyFile(io.BytesIO):
    def __init__(self, content, name):
  
        super().__init__(content)
        self.name = name

        self.type = "text/csv" if name.endswith('.csv') else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        self.size = len(content)


test_data = [
    (
        "NOS (Newcastle-Ottawa Scale)", 
        "Study,Representativeness,Non-exposed Selection,Exposure Ascertainment,Outcome Absent at Start,Comparability (Age/Gender),Comparability (Other),Outcome Assessment,Follow-up Length,Follow-up Adequacy,Total Score,Overall RoB\nTestStudy,1,1,1,1,1,1,1,1,1,9,Low"
    ),
    (
        "GRADE", 
        "Outcome,Study,Risk of Bias,Inconsistency,Indirectness,Imprecision,Publication Bias,Overall Certainty\nOutcome1,Study1,High,Moderate,Low,Very Low,None,Moderate"
    ),
    (
        "ROBIS", 
        "Review,Study Eligibility,Identification & Selection,Data Collection,Synthesis & Findings,Overall Risk\nReview1,Low,Unclear,High,Low,Low"
    ),
    (
        "JBI Case Report", 
        "Author,Year,Demographics,History,ClinicalCondition,Diagnostics,Intervention,PostCondition,AdverseEvents,Lessons,Total,Overall RoB\nAuthor1,2020,1,1,1,1,1,1,1,1,8,Low"
    ),
    (
        "JBI Case Series", 
        "Author,Year,InclusionCriteria,StandardMeasurement,ValidIdentification,ConsecutiveInclusion,CompleteInclusion,Demographics,ClinicalInfo,Outcomes,SiteDescription,Statistics,Total,Overall RoB\nAuthor1,2021,1,1,1,1,1,1,1,1,1,1,10,Low"
    ),
    (
        "MMAT (Mixed Methods Appraisal Tool)", 
        "Author_Year,Study_Category,Criterion_1,Criterion_2,Overall_Rating\nStudy1,Qualitative,Yes,No,Moderate"
    ),
]

@pytest.mark.parametrize("tool_name, csv_content_str", test_data)
def test_tool_processing(tool_name, csv_content_str):
    """Test file upload and processing for all assessment tools."""
    
    
    at = AppTest.from_file(APP_FILE)
    at.run()
    assert not at.exception, "App failed on initial load"


    at.selectbox[0].select(tool_name).run()
    assert not at.exception, f"App crashed selecting tool: {tool_name}"


    csv_content = csv_content_str.encode('utf-8')
    uploader_key = f"file_uploader_{tool_name}"
    

    dummy_file = DummyFile(csv_content, "test.csv")


    at.session_state[uploader_key] = dummy_file
    

    at.run(timeout=30)


    assert not at.exception, f"App crashed processing file for: {tool_name}"
    
    # Debugging: If success is missing, check if an error was displayed
    if not at.success:
        if at.error:
            pytest.fail(f"Tool '{tool_name}' failed with error: {at.error[0].value}")
        else:
            pytest.fail(f"Success message not found for: {tool_name} (No error message displayed)")

    assert "Plot generated successfully!" in at.success[0].value

def test_app_loads():
    """Simple test to ensure app initializes."""
    at = AppTest.from_file(APP_FILE)
    at.run()
    assert not at.exception