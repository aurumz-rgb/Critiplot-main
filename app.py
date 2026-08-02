import streamlit as st
import pandas as pd
import os
import shutil
import tempfile
from io import BytesIO
import base64
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import glob

import critiplot

st.set_page_config(
    page_title="Critiplot",
    layout="wide",
    page_icon="./assets/icon.png"  
)

hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;}
    button[title="Toggle sidebar"] {display: none;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.markdown("""
<style>
    .stApp { background-color: #111111; }
    h1, h2, h3 { color: #2c3e50; font-weight: 600; }
    .main-content { margin-top: 2vh; }
    .citation-box { border-left: 4px solid #3498db; background-color: #e9ecef; padding: 1rem; margin: 1rem 0; color: #000 !important; }
    .centered-title { 
        text-align: center; 
        font-size: 3.5rem !important;
        font-weight: 800 !important; 
        margin-top: -40px; 
        margin-bottom: 10px; 
        color: #ffffff !important;
    }
    .centered-subtitle { 
        text-align: center; 
        font-size: 1.5rem !important;
        font-weight: 500 !important; 
        margin-bottom: 30px; 
        color: #ffffff !important;
    }
    .quickstart { font-size: 1.4rem; line-height: 1.6; }
    .scrollable-table { overflow-x: auto; }
    .lowered-section { margin-top: 30px; }
    .custom-button {
        background-color: #3498db !important;
        color: white !important;
        text-decoration: none !important;
        padding: 0.5rem 1rem !important;
        font-size: 1rem !important;
        border-radius: 5px !important;
        display: inline-block !important;
        margin: 0 !important;
        transition: background-color 0.3s ease !important;
        border: none !important;
        cursor: pointer !important;
    }
    .custom-button:hover {
        background-color: #2980b9 !important;
    }
    .top-padding-container { margin-top: 100px; }
    .plot-container {
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
        justify-content: center;
        margin-bottom: 20px;
    }
    .plot-item {
        flex: 1;
        min-width: 300px;
        max-width: 45%;
    }
    .plot-title {
        text-align: center;
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 10px;
        color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

def add_background_png(png_file):
    if os.path.exists(png_file):
        with open(png_file, "rb") as f:
            b64_img = base64.b64encode(f.read()).decode()
        st.markdown(f"""
            <style>
            .stApp {{
                background-image: url("data:image/png;base64,{b64_img}");
                background-size: cover;
                background-attachment: fixed;
                padding-top: 0px;
            }}
            </style>
        """, unsafe_allow_html=True)

def display_logo_png_top_touch(png_file, height=180):
    if os.path.exists(png_file):
        with open(png_file, "rb") as f:
            b64_img = base64.b64encode(f.read()).decode()
        st.markdown(f'''
            <div style="text-align:center; margin-top:0px; padding-top:0px;">
                <img src="data:image/png;base64,{b64_img}" height="{height}px" style="display:block; margin:0 auto; padding:0;">
            </div>
        ''', unsafe_allow_html=True)

add_background_png("./assets/background.png")

st.markdown('<div class="top-padding-container">', unsafe_allow_html=True)
display_logo_png_top_touch("./assets/logo.png", height=180)
st.markdown('<div class="main-content">', unsafe_allow_html=True)
st.markdown('<h1 class="centered-title">Critiplot.</h1>', unsafe_allow_html=True)
st.markdown('<p class="centered-subtitle">A Critical Appraisal Plot Visualiser for Risk of Bias Assessments</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="lowered-section">', unsafe_allow_html=True)


tool = st.selectbox(
    "Select Assessment Tool",
    ["NOS (Newcastle-Ottawa Scale)", "GRADE", "ROBIS", "JBI Case Report", "JBI Case Series", "MMAT (Mixed Methods Appraisal Tool)"],
    key="tool"
)


st.markdown('<div style="font-size: 1.6rem; font-weight: bold; margin-bottom: 10px;"> Quick Start & Data Instructions</div>', unsafe_allow_html=True)
with st.expander("**Setting Up Your Data**", expanded=False):  
    st.markdown('<div class="quickstart" style="margin-top:-1rem;">', unsafe_allow_html=True)
    
    if tool.startswith("NOS"):
        st.write("""
✨  **Critiplot** is a web app for visualizing Newcastle–Ottawa Scale (NOS) risk-of-bias assessments.
It generates:

* **Traffic light plots** showing domain-level judgements for each study.
* **Weighted bar plots** summarizing the distribution of judgements across domains.

All figures are **publication-ready** and formatted to match NOS assessment standards.

---        
             
To work correctly with **Critiplot**, your uploaded table should follow this structure:
    
- **First column:** Study details (Author, Year)
    - **Domain columns:** Each additional column corresponds to a specific NOS domain:
        - Representativeness
        - Non-exposed Selection
        - Exposure Ascertainment
        - Outcome Absent at Start
        - Comparability (Age/Gender)
        - Comparability (Other)
        - Outcome Assessment
        - Follow-up Length
        - Follow-up Adequacy
    - **Total Score:** Sum of the domain scores
    - **Overall RoB:** Overall risk-of-bias judgement for each study (Low, Moderate, High)
    """)
        
        sample_csv_path = "nos_data.csv"
        if os.path.exists(sample_csv_path):
            st.markdown('<div class="scrollable-table">', unsafe_allow_html=True)
            st.dataframe(pd.read_csv(sample_csv_path), width='stretch')
            st.markdown('</div>', unsafe_allow_html=True)

        excel_file_path = "nos_data.xlsx"
        csv_file_path = "nos_data.csv"
        def file_to_b64(path):
            if os.path.exists(path):
                with open(path, "rb") as f:
                    return base64.b64encode(f.read()).decode()
            return ""
        st.markdown(f"""
        <div style="display:flex; gap:10px; margin-bottom:10px;">
            <a download="nos_data.xlsx" href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{file_to_b64(excel_file_path)}" class="custom-button">
                Excel Template
            </a>
            <a download="nos_data.csv" href="data:text/csv;base64,{file_to_b64(csv_file_path)}" class="custom-button">
                CSV Template
            </a>
        </div>
        """, unsafe_allow_html=True)
    
    elif tool == "GRADE":
        st.write("""
✨  **Critiplot** is a web app for visualizing GRADE assessments.
It generates:

* **Traffic light plots** showing domain-level judgements for each outcome.
* **Weighted bar plots** summarizing the distribution of judgements across domains.

All figures are **publication-ready** and formatted to match GRADE assessment standards.

---        
             
To work correctly with **Critiplot**, your uploaded table should follow this structure:
    
- **Outcome:** Name of the outcome
- **Study:** Study identifier
- **Risk of Bias:** Risk of bias judgement (High, Moderate, Low, Very Low, None)
- **Inconsistency:** Inconsistency judgement (High, Moderate, Low, Very Low, None)
- **Indirectness:** Indirectness judgement (High, Moderate, Low, Very Low, None)
- **Imprecision:** Imprecision judgement (High, Moderate, Low, Very Low, None)
- **Publication Bias:** Publication bias judgement (High, Moderate, Low, Very Low, None)
- **Overall Certainty:** Overall certainty judgement (High, Moderate, Low, Very Low)
    """)
        
        sample_csv_path = "grade_data.csv"
        if os.path.exists(sample_csv_path):
            st.markdown('<div class="scrollable-table">', unsafe_allow_html=True)
            st.dataframe(pd.read_csv(sample_csv_path), width='stretch')
            st.markdown('</div>', unsafe_allow_html=True)

        excel_file_path = "grade_data.xlsx"
        csv_file_path = "grade_data.csv"
        def file_to_b64(path):
            if os.path.exists(path):
                with open(path, "rb") as f:
                    return base64.b64encode(f.read()).decode()
            return ""
        st.markdown(f"""
        <div style="display:flex; gap:10px; margin-bottom:10px;">
            <a download="grade_data.xlsx" href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{file_to_b64(excel_file_path)}" class="custom-button">
                Excel Template
            </a>
            <a download="grade_data.csv" href="data:text/csv;base64,{file_to_b64(csv_file_path)}" class="custom-button">
                CSV Template
            </a>
        </div>
        """, unsafe_allow_html=True)
    
    elif tool == "ROBIS":
        st.write("""
✨  **Critiplot** is a web app for visualizing ROBIS assessments.
It generates:

* **Traffic light plots** showing domain-level judgements for each review.
* **Weighted bar plots** summarizing the distribution of judgements across domains.

All figures are **publication-ready** and formatted to match ROBIS assessment standards.

---        
             
To work correctly with **Critiplot**, your uploaded table should follow this structure:
    
- **Review:** Review identifier
- **Study Eligibility:** Risk of bias judgement (Low, Unclear, High)
- **Identification & Selection:** Risk of bias judgement (Low, Unclear, High)
- **Data Collection:** Risk of bias judgement (Low, Unclear, High)
- **Synthesis & Findings:** Risk of bias judgement (Low, Unclear, High)
- **Overall Risk:** Overall risk of bias judgement (Low, Unclear, High)
    """)
        
        sample_csv_path = "robis_data.csv"
        if os.path.exists(sample_csv_path):
            st.markdown('<div class="scrollable-table">', unsafe_allow_html=True)
            st.dataframe(pd.read_csv(sample_csv_path), width='stretch')
            st.markdown('</div>', unsafe_allow_html=True)

        excel_file_path = "robis_data.xlsx"
        csv_file_path = "robis_data.csv"
        def file_to_b64(path):
            if os.path.exists(path):
                with open(path, "rb") as f:
                    return base64.b64encode(f.read()).decode()
            return ""
        st.markdown(f"""
        <div style="display:flex; gap:10px; margin-bottom:10px;">
            <a download="robis_data.xlsx" href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{file_to_b64(excel_file_path)}" class="custom-button">
                Excel Template
            </a>
            <a download="robis_data.csv" href="data:text/csv;base64,{file_to_b64(csv_file_path)}" class="custom-button">
                CSV Template
            </a>
        </div>
        """, unsafe_allow_html=True)
    
    elif tool == "JBI Case Report":
        st.write("""
✨  **Critiplot** is a web app for visualizing JBI Case Report assessments.
It generates:

* **Traffic light plots** showing domain-level judgements for each study.
* **Weighted bar plots** summarizing the distribution of judgements across domains.

All figures are **publication-ready** and formatted to match JBI assessment standards.

---        
             
To work correctly with **Critiplot**, your uploaded table should follow this structure:
    
- **Author,Year:** Study identifier (e.g., "Smith, 2020")
- **Demographics:** Score (0 or 1)
- **History:** Score (0 or 1)
- **ClinicalCondition:** Score (0 or 1)
- **Diagnostics:** Score (0 or 1)
- **Intervention:** Score (0 or 1)
- **PostCondition:** Score (0 or 1)
- **AdverseEvents:** Score (0 or 1)
- **Lessons:** Score (0 or 1)
- **Total:** Sum of the domain scores
- **Overall RoB:** Overall risk of bias judgement (Low, High)
    """)
        
        sample_csv_path = "case_report.csv"
        if os.path.exists(sample_csv_path):
            st.markdown('<div class="scrollable-table">', unsafe_allow_html=True)
            st.dataframe(pd.read_csv(sample_csv_path), width='stretch')
            st.markdown('</div>', unsafe_allow_html=True)

        excel_file_path = "case_report.xlsx"
        csv_file_path = "case_report.csv"
        def file_to_b64(path):
            if os.path.exists(path):
                with open(path, "rb") as f:
                    return base64.b64encode(f.read()).decode()
            return ""
        st.markdown(f"""
        <div style="display:flex; gap:10px; margin-bottom:10px;">
            <a download="case_report.xlsx" href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{file_to_b64(excel_file_path)}" class="custom-button">
                Excel Template
            </a>
            <a download="case_report.csv" href="data:text/csv;base64,{file_to_b64(csv_file_path)}" class="custom-button">
                CSV Template
            </a>
        </div>
        """, unsafe_allow_html=True)
    
    elif tool == "JBI Case Series":
        st.write("""
✨  **Critiplot** is a web app for visualizing JBI Case Series assessments.
It generates:

* **Traffic light plots** showing domain-level judgements for each study.
* **Weighted bar plots** summarizing the distribution of judgements across domains.

All figures are **publication-ready** and formatted to match JBI assessment standards.

---        
             
To work correctly with **Critiplot**, your uploaded table should follow this structure:
    
- **Author,Year:** Study identifier (e.g., "Smith, 2020")
- **InclusionCriteria:** Score (0 or 1)
- **StandardMeasurement:** Score (0 or 1)
- **ValidIdentification:** Score (0 or 1)
- **ConsecutiveInclusion:** Score (0 or 1)
- **CompleteInclusion:** Score (0 or 1)
- **Demographics:** Score (0 or 1)
- **ClinicalInfo:** Score (0 or 1)
- **Outcomes:** Score (0 or 1)
- **SiteDescription:** Score (0 or 1)
- **Statistics:** Score (0 or 1)
- **Total:** Sum of the domain scores
- **Overall RoB:** Overall risk of bias judgement (Low, High)
    """)
        
        sample_csv_path = "case_series.csv"
        if os.path.exists(sample_csv_path):
            st.markdown('<div class="scrollable-table">', unsafe_allow_html=True)
            st.dataframe(pd.read_csv(sample_csv_path), width='stretch')
            st.markdown('</div>', unsafe_allow_html=True)

        excel_file_path = "case_series.xlsx"
        csv_file_path = "case_series.csv"
        def file_to_b64(path):
            if os.path.exists(path):
                with open(path, "rb") as f:
                    return base64.b64encode(f.read()).decode()
            return ""
        st.markdown(f"""
        <div style="display:flex; gap:10px; margin-bottom:10px;">
            <a download="case_series.xlsx" href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{file_to_b64(excel_file_path)}" class="custom-button">
                Excel Template
            </a>
            <a download="case_series.csv" href="data:text/csv;base64,{file_to_b64(csv_file_path)}" class="custom-button">
                CSV Template
            </a>
        </div>
        """, unsafe_allow_html=True)
    
    elif tool == "MMAT (Mixed Methods Appraisal Tool)":
        st.write("""
✨  **Critiplot** is a web app for visualizing Mixed Methods Appraisal Tool (MMAT) assessments.
It generates:

* **Traffic light plots** showing domain-level judgements for each study.
* **Weighted bar plots** summarizing the distribution of judgements across domains.

All figures are **publication-ready** and formatted to match MMAT assessment standards.

---        
             
To work correctly with **Critiplot**, your uploaded table should follow this structure:
    
- **Author_Year:** Study identifier (e.g., "Smith, 2019")
- **Study_Category:** Type of study (Qualitative, Randomized, Non-randomized, Descriptive, Mixed Methods)
- **Criterion columns:** Each additional column corresponds to a specific MMAT criterion (Yes, No, Can't tell)
- **Overall_Rating:** Overall rating (High, Moderate, Low)
    """)
        
        sample_csv_path = "mmat_data.csv"
        if os.path.exists(sample_csv_path):
            st.markdown('<div class="scrollable-table">', unsafe_allow_html=True)
            st.dataframe(pd.read_csv(sample_csv_path), width='stretch')
            st.markdown('</div>', unsafe_allow_html=True)

        excel_file_path = "mmat_data.xlsx"
        csv_file_path = "mmat_data.csv"
        def file_to_b64(path):
            if os.path.exists(path):
                with open(path, "rb") as f:
                    return base64.b64encode(f.read()).decode()
            return ""
        st.markdown(f"""
        <div style="display:flex; gap:10px; margin-bottom:10px;">
            <a download="mmat_data.xlsx" href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{file_to_b64(excel_file_path)}" class="custom-button">
                Excel Template
            </a>
            <a download="mmat_data.csv" href="data:text/csv;base64,{file_to_b64(csv_file_path)}" class="custom-button">
                CSV Template
            </a>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


st.markdown("### Upload Your Data")
st.markdown('<p style="color: #ffff; font-size: 1.1rem;">Please upload your file in <b>CSV</b> or <b>Excel (.xlsx)</b> format. <b>Maximum file size: 20MB per file.</b></p>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=["csv","xls","xlsx"], key=f"file_uploader_{tool}")

if tool.startswith("NOS"):
    theme_options = ["default", "blue", "gray", "smiley", "smiley_blue"]
elif tool == "GRADE":
    theme_options = ["default", "green", "blue"]
elif tool == "ROBIS":
    theme_options = ["default", "blue", "gray", "smiley", "smiley_blue"]
elif tool == "JBI Case Report":
    theme_options = ["default", "blue", "gray", "smiley", "smiley_blue"]
elif tool == "JBI Case Series":
    theme_options = ["default", "blue", "gray", "smiley", "smiley_blue"]
elif tool == "MMAT (Mixed Methods Appraisal Tool)":
    theme_options = ["default", "blue", "gray", "smiley", "smiley_blue"]

theme = st.selectbox(
    "Select Plot Theme",
    theme_options,
    key=f"theme_{tool}"
)

tmp_file_path = None
temp_dir = None

if uploaded_file is not None:
    try:
        if uploaded_file.size > 20 * 1024 * 1024:  
            st.error("❌ File size exceeds the 20MB limit per file. Please upload a smaller file.")
            st.stop()
            
        file_ext = os.path.splitext(uploaded_file.name)[1].lower()
        if file_ext not in ['.csv', '.xlsx', '.xls']:
            st.error(f"❌ Invalid file format: '{file_ext}'. Please upload a CSV or Excel file.")
            st.stop()
            
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name
        

        if tool.startswith("NOS"):
            plot_function = critiplot.plot_nos
            plot_name = "NOS"
        elif tool == "GRADE":
            plot_function = critiplot.plot_grade
            plot_name = "GRADE"
        elif tool == "ROBIS":
            plot_function = critiplot.plot_robis
            plot_name = "ROBIS"
        elif tool == "JBI Case Report":
            plot_function = critiplot.plot_jbi_case_report
            plot_name = "JBI_Case_Report"
        elif tool == "JBI Case Series":
            plot_function = critiplot.plot_jbi_case_series
            plot_name = "JBI_Case_Series"
        elif tool == "MMAT (Mixed Methods Appraisal Tool)":
            plot_function = critiplot.plot_mmat
            plot_name = "MMAT"

        temp_dir = tempfile.mkdtemp()
        

        if tool == "MMAT (Mixed Methods Appraisal Tool)":
            output_files = {}
            for ext in [".png", ".pdf", ".svg", ".eps"]:
                temp_file_path_ext = os.path.join(temp_dir, f"{plot_name}_TrafficLight{ext}")
            
                plot_function(tmp_file_path, temp_file_path_ext, theme=theme)
                plt.close('all')
                
                pattern = os.path.join(temp_dir, f"{plot_name}_TrafficLight_*{ext}")
                files = glob.glob(pattern)
                output_files[ext] = files
        else:
            output_files = {ext: os.path.join(temp_dir, f"{plot_name}_TrafficLight{ext}") for ext in [".png",".pdf",".svg",".eps"]}
            for out_ext, path in output_files.items():
               
                plot_function(tmp_file_path, path, theme=theme)
                plt.close('all') 
        
        st.success(" Plot generated successfully!")
        st.markdown("### Visualization Preview")
        if tool == "MMAT (Mixed Methods Appraisal Tool)":
            if output_files.get(".png") and len(output_files[".png"]) > 0:
                st.markdown('<div class="plot-container">', unsafe_allow_html=True)
                for file_path in output_files[".png"]:
                    filename = os.path.basename(file_path)
                    category = filename.replace(f"{plot_name}_TrafficLight_", "").replace(".png", "")
                    
                    st.markdown(f'<div class="plot-item">', unsafe_allow_html=True)
                    st.markdown(f'<div class="plot-title">{category}</div>', unsafe_allow_html=True)
                    st.image(file_path, width='stretch')
                    st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning("No PNG files were generated.")
        else:
            st.image(output_files[".png"], width='stretch')

        st.markdown("###  Download Visualization")
        st.markdown('<p style="color: #ffff; font-size: 1.1rem;">Download your Critiplot visualisation in formats like:</p>', unsafe_allow_html=True)

        if tool == "MMAT (Mixed Methods Appraisal Tool)":
            for ext in [".png", ".pdf", ".svg", ".eps"]:
                if ext in output_files and output_files[ext]:
                    st.markdown(f"#### {ext[1:].upper()} Files")
                    download_buttons = []
                    for file_path in output_files[ext]:
                        filename = os.path.basename(file_path)
                        category = filename.replace(f"{plot_name}_TrafficLight_", "").replace(ext, "")
                        
                        with open(file_path, "rb") as f:
                            b64 = base64.b64encode(f.read()).decode()
                        
                        mime = {
                            ".png": "image/png",
                            ".pdf": "application/pdf",
                            ".svg": "image/svg+xml",
                            ".eps": "application/postscript"
                        }[ext]
                        
                        download_buttons.append(
                            f'<a download="{filename}" href="data:{mime};base64,{b64}" class="custom-button">{category}</a>'
                        )
                    
                    if download_buttons:
                        st.markdown('<div style="display:flex; gap:10px; margin-bottom:10px; flex-wrap: wrap;">' + ''.join(download_buttons) + '</div>', unsafe_allow_html=True)
        else:
            download_html = '<div style="display:flex; gap:10px; margin-bottom:10px;">'
            for out_ext, path in output_files.items():
                with open(path, "rb") as f:
                    b64 = base64.b64encode(f.read()).decode()
                mime = {".png":"image/png",".pdf":"application/pdf",".svg":"image/svg+xml",".eps":"application/postscript"}[out_ext]
                download_html += f'<a download="{plot_name}_TrafficLight{out_ext}" href="data:{mime};base64,{b64}" class="custom-button">{out_ext[1:].upper()}</a>'
            download_html += "</div>"
            st.markdown(download_html, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")
        st.markdown("""
**Please ensure your data meets these requirements:**

* **First, always verify you've selected the correct Risk of Bias (RoB) assessment tool** that matches your data format. The tool you select must correspond to the type of RoB assessment you're uploading.

* Your file must strictly follow the template structure shown above.

* Ensure there are no AI-generated invisible marks or spaces in your data that might cause processing errors.

* **Important:** Use the exact capitalization shown in the templates. For example, if the template specifies "Very Low" or "Low Risk" for a domain, you must use that exact formatting. Variations like "very low" or "low risk" will not be recognized by the tool and will result in that domain being ignored in the generated plot.
""")
    finally:
        if tmp_file_path and os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        import gc
        gc.collect()

st.markdown("---")
st.markdown("## Citation")

apa_citation = (
    "Sahu, V. (2025). Critiplot: A Critical Appraisal Plot Visualiser for Risk of Bias in Systematic Reviews and Meta-Analyses (v2.1.1). "
    "Zenodo. https://doi.org/10.5281/zenodo.17236600"
)

harvard_citation = (
    "Sahu, V., 2025. Critiplot: A Critical Appraisal Plot Visualiser for Risk of Bias in Systematic Reviews and Meta-Analyses (v2.1.1). "
    "Zenodo. Available at: https://doi.org/10.5281/zenodo.17236600"
)

mla_citation = (
    "Sahu, Vihaan. \"Critiplot: A Critical Appraisal Plot Visualiser for Risk of Bias in Systematic Reviews and Meta-Analyses (v2.1.1).\" "
    "2025, Zenodo, https://doi.org/10.5281/zenodo.17236600."
)

chicago_citation = (
    "Sahu, Vihaan. 2025. \"Critiplot: A Critical Appraisal Plot Visualiser for Risk of Bias in Systematic Reviews and Meta-Analyses (v2.1.1).\" "
    "Zenodo. https://doi.org/10.5281/zenodo.17236600."
)

ieee_citation = (
    "V. Sahu, \"Critiplot: A Critical Appraisal Plot Visualiser for Risk of Bias in Systematic Reviews and Meta-Analyses (v2.1.1),\" "
    "Zenodo, 2025. doi: 10.5281/zenodo.17236600."
)

vancouver_citation = (
    "Sahu V. Critiplot: A Critical Appraisal Plot Visualiser for Risk of Bias in Systematic Reviews and Meta-Analyses (v2.1.1). "
    "Zenodo. 2025. doi:10.5281/zenodo.17236600"
)

ris_data = """TY  - JOUR
AU  - Sahu, V
TI  - Critiplot: A Critical Appraisal Plot Visualiser for Risk of Bias in Systematic Reviews and Meta-Analyses (v2.1.1)
PY  - 2025
DO  - 10.5281/zenodo.17236600
ER  -"""

bib_data = """@misc{Sahu2025,
  author={Sahu, V.},
  title={Critiplot: A Critical Appraisal Plot Visualiser for Risk of Bias in Systematic Reviews and Meta-Analyses (v2.1.1)},
  year={2025},
  doi={10.5281/zenodo.17236600}
}"""

citation_style = st.selectbox(
    "Select citation style",
    ["APA", "Harvard", "MLA", "Chicago", "IEEE", "Vancouver"]
)

if citation_style == "APA":
    citation_text = apa_citation
elif citation_style == "Harvard":
    citation_text = harvard_citation
elif citation_style == "MLA":
    citation_text = mla_citation
elif citation_style == "Chicago":
    citation_text = chicago_citation
elif citation_style == "IEEE":
    citation_text = ieee_citation
elif citation_style == "Vancouver":
    citation_text = vancouver_citation

st.markdown(f'<p style="margin:0; color:#ffff; font-size:1.1rem;"><i>If you use Critiplot to create risk-of-bias plots for your study, please remember to cite the tool.</i></p>', unsafe_allow_html=True)
st.markdown(f'<div class="citation-box"><p style="margin:0; color: #000;">{citation_text}</p></div>', unsafe_allow_html=True)

copy_button_html = f"""
<style>
.custom-button {{
    background-color: #3498db !important;
    color: white !important;
    text-decoration: none !important;
    padding: 0.5rem 1rem !important;
    font-size: 1rem !important;
    border-radius: 5px !important;
    display: inline-block !important;
    margin: 0 !important;
    transition: background-color 0.3s ease !important;
    border: none !important;
    cursor: pointer !important;
}}
.custom-button:hover {{
    background-color: #2980b9 !important;
}}
</style>

<div style="display:flex; gap:10px; margin-top:10px; margin-bottom:10px; position:relative;" id="button-container">
    <a id="copy-btn" class="custom-button">Copy Citation</a>
    <a download="Critiplot_citation.ris" href="data:application/x-research-info-systems;base64,{base64.b64encode(ris_data.encode()).decode()}" class="custom-button">RIS Format</a>
    <a download="Critiplot_citation.bib" href="data:application/x-bibtex;base64,{base64.b64encode(bib_data.encode()).decode()}" class="custom-button">BibTeX Format</a>
</div>

<script>
document.getElementById("copy-btn").onclick = function() {{
    const text = `{citation_text}`;
    const btn = document.getElementById("copy-btn");
    navigator.clipboard.writeText(text).then(() => {{
        const originalText = btn.innerText;
        btn.innerText = "Copied!";
        setTimeout(() => {{ btn.innerText = originalText; }}, 2000);
    }});
}};
</script>
"""
components.html(copy_button_html, height=100)

st.markdown("---")
st.markdown("""
<style>
.footer-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: #fff;
    padding: 1rem;
    font-size: 1.05rem;
}
.footer-left { text-align:left; }
.footer-center { display:flex; gap:40px; justify-content:center; align-items:center; }
.footer-link { color:#3498db; text-decoration:none; transition:color 0.3s ease; }
.footer-link:hover { color:#5682B1; }
</style>

<div class="footer-container">
    <div class="footer-left">
        <div>© 2025-26 Vihaan Sahu</div>
        <div>Licensed under the Apache License, Version 2.0</div>
    </div>
    <div class="footer-center">
        <span>Critiplot</span>
        <span>Professional Risk of Bias Visualization Tool</span>
        <a href='https://github.com/aurumz-rgb/Critiplot-main' target='_blank' class='footer-link'>GitHub Repository</a>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)