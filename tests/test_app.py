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
  
        "\"Author, Year\",Representativeness,Non-exposed Selection,Exposure Ascertainment,Outcome Absent at Start,Comparability (Age/Gender),Comparability (Other),Outcome Assessment,Follow-up Length,Follow-up Adequacy,Total Score,Overall RoB\n\"Study 1, 2019\",1,1,1,1,1,0,1,1,1,8,Low\n\"Study 2, 2024\",1,1,1,1,1,0,1,1,0,7,Moderate\n\"Study 3, 2019\",1,0,1,1,0,1,1,0,1,6,Moderate\n\"Study 4, 2025\",1,0,1,0,0,1,0,0,1,4,High\n\"Study 5, 2025\",1,0,0,0,0,1,1,0,0,3,High\n\"Study 6, 2019\",1,1,1,1,1,0,1,1,1,8,Low"
    ),
    (
        "GRADE", 
     
        "Outcome,Risk_of_Bias,Inconsistency,Indirectness,Imprecision,Publication_Bias,Overall_Certainty\nMortality,Serious,Not Serious,Not Serious,Serious,Not Serious,Low\nInfection,Serious,Very Serious,Not Serious,Not Serious,Not Serious,High\nHospitalization,Not Serious,Not Serious,Serious,Not Serious,Moderate\nAdverse Events,Serious,Serious,Not Serious,Serious,Not Serious,Low\nQuality of Life,Not Serious,Not Serious,Very Serious,Serious,Not Reported,Very Low"
    ),
    (
        "ROBIS", 
        
        "Review,Study Eligibility Criteria,Identification & Selection of Studies,Data Collection & Study Appraisal,Synthesis & Findings,Overall RoB\nStudy 1 2021,Low,High,Unclear,Low,High\nStudy 2 2020,Low,Low,Low,Low,Low\nStudy 3 2019,Low,High,Unclear,Low,High\nStudy 4 2016,Low,Low,Low,Low,Low"
    ),
    (
        "JBI Case Report", 
        "Author,Year,Demographics,History,ClinicalCondition,Diagnostics,Intervention,PostCondition,AdverseEvents,Lessons,Total,Overall RoB\nStudy 1,2022,1,1,0,1,1,1,1,1,7,Low\nStudy 2,2021,1,Not Applicable,0,1,0,Unclear,0,1,3,High\nStudy 3,2022,1,1,0,1,1,1,1,1,7,Low\nStudy 4,2022,1,1,1,1,1,0,1,1,7,Low"
    ),
    (
        "JBI Case Series", 
        "Author,Year,InclusionCriteria,StandardMeasurement,ValidIdentification,ConsecutiveInclusion,CompleteInclusion,Demographics,ClinicalInfo,Outcomes,SiteDescription,Statistics,Total,Overall RoB\nStudy 1,2022,1,1,1,1,1,1,1,1,1,1,10,Low\nStudy 2,2021,1,0,1,1,0,1,0,1,0,0,5,High\nStudy 3,2018,1,1,1,1,1,1,1,1,1,1,10,Low\nStudy 4,2021,Unclear,Not Applicable,1,1,0,1,0,1,0,1,5,High"
    ),
    (
        "MMAT (Mixed Methods Appraisal Tool)", 
        "Author_Year,Study_Category,Appropriate randomization,Groups comparable at baseline,Complete outcome data,Outcome assessors blinded,Adherence to intervention,Overall_Rating\n\"Smith, 2019\",Qualitative,Yes,Yes,Yes,Yes,Yes,High\n\"Johnson, 2024\",Qualitative,Yes,No,Yes,\"Can't tell\",Yes,Moderate\n\"Garcia, 2020\",Qualitative,Yes,Yes,\"Can't tell\",Yes,Yes,Moderate\n\"Patel, 2021\",Qualitative,No,Yes,Yes,No,Yes,Low\n\"Lopez, 2022\",Qualitative,Yes,Yes,Yes,No,Yes,Moderate"
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
    
    if not at.success:
        if at.error:
            pytest.fail(f"Tool '{tool_name}' failed with error: {at.error[0].value}")
        else:
            pytest.fail(f"Success message not found for: {tool_name}")

    assert "Plot generated successfully!" in at.success[0].value

def test_app_loads():
    at = AppTest.from_file(APP_FILE)
    at.run()
    assert not at.exception