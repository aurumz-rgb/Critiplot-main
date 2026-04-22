![Preview](assets/preview1.png)

[![Python Version](https://img.shields.io/badge/python-3.11+-blue)](https://www.python.org/)
[![Streamlit Demo](https://img.shields.io/badge/Streamlit-Demo-orange)](https://critiplot.streamlit.app)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17236600.svg)](https://doi.org/10.5281/zenodo.17236600)

**Critiplot** is an open-source Python tool and **interactive web app** for **visualizing risk-of-bias (RoB) assessments** across multiple evidence synthesis tools:

* **Newcastle-Ottawa Scale (NOS)**
* **JBI Critical Appraisal Checklists** (Case Report / Case Series)
* **GRADE certainty of evidence**
* **ROBIS for systematic reviews**
* **Mixed Methods Appraisal Tool (MMAT)**

It produces **publication-ready traffic-light plots** and **stacked bar charts**, allowing researchers to summarize study quality clearly in systematic reviews and meta-analyses.

---


🔗 **Interactive web app:** [critiplot.vercel.app](https://critiplot.vercel.app)

- If you want to skip the Vercel user-interface, you can directly access Streamlit: [critiplot.streamlit.app](https://critiplot.streamlit.app)


![Example Result11](example/Screenshot3.png)
Vercel User-Inferface


![Example Result22](example/Screenshot1.png)

![Example Result33](example/Screenshot2.png)
Streamlit User-Inferface



📂 **Code & archive (Zenodo DOI):** [10.5281/zenodo.17236600](https://doi.org/10.5281/zenodo.17236600)

---

## ✨ Key Features

* Converts risk-of-bias ratings into **traffic-light plots**.
* Generates **publication-quality figures** in multiple formats: `.png`, `.pdf`, `.svg`, `.eps`.
* Supports **NOS, JBI (Case Report / Case Series), GRADE, ROBIS and MMAT**.
* Open-source, fully reproducible, usable via **Python scripts** or **Streamlit web app**.
* Adjustable **themes, figure sizes, line thickness, and legends**.

---


## Data & Template

* Please strictly follow the **Data & Template** _(available as .csv & excel format)_ as mentioned in the main Critiplot Web: [critiplot.vercel.app](https://critiplot.vercel.app)

---


## 📥 Installation

```bash
git clone https://github.com/aurumz-rgb/Critiplot-main.git
cd Critiplot
pip install -r requirements.txt
```

> Tested with **Python 3.11+**, **Matplotlib**, **Seaborn**, and **Pandas**.

---

## ⚡ Usage

### 1️⃣ Python Scripts

Separate scripts are available for each assessment tool:

| Script                    | Input                    | Output          | Notes                                             |
| ------------------------- | ------------------------ | --------------- | ------------------------------------------------- |
| `nos_plot.py`             | NOS CSV/XLSX             | PNG/PDF/SVG/EPS | Traffic-light & stacked bar plots for NOS studies |
| `jbi_case_report_plot.py` | JBI Case Report CSV/XLSX | PNG/PDF/SVG/EPS | For individual case reports                       |
| `jbi_case_series_plot.py` | JBI Case Series CSV/XLSX | PNG/PDF/SVG/EPS | For case series studies                           |
| `grade_plot.py`           | GRADE CSV/XLSX           | PNG/PDF/SVG/EPS | Summarizes certainty of evidence                  |
| `robis_plot.py`           | ROBIS CSV/XLSX           | PNG/PDF/SVG/EPS | Summarizes systematic review risk-of-bias         |
| `mmat_plot.py`            | MMAT CSV/XLSX            | PNG/PDF/SVG/EPS | Used for Mixed Methods Appraisal Tool studies     |

#### Example Commands

```bash
# NOS
python3 nos_plot.py nos_data.csv nos_plot.png
python3 nos_plot.py nos_data.xlsx nos_plot.png

# JBI Case Report
python3 jbi_case_report_plot.py case_report.csv report_plot.png
python3 jbi_case_report_plot.py case_report.xlsx report_plot.png

# JBI Case Series
python3 jbi_case_series_plot.py case_series.csv series_plot.png
python3 jbi_case_series_plot.py case_series.xlsx series_plot.png

# GRADE
python3 grade_plot.py grade_data.csv grade_plot.png
python3 grade_plot.py grade_data.xlsx grade_plot.png

# ROBIS
python3 robis_plot.py robis_data.csv robis_plot.png
python3 robis_plot.py robis_data.xlsx robis_plot.png

# MMAT
python3 mmat_plot.py mmat_data.csv mmat_plot.png
python3 mmat_plot.py mmats_data.xlsx mmat_plot.png
```

---

> Optional `[theme]` argument for **NOS, JBI Case Report / Case Series, MMAT and ROBIS**:
> `"default"`, `"blue"`, `"gray"`, `"smiley"`, `"smiley_blue"`
>
> ⚠️ **Note:** For **GRADE**, these themes are not available. Instead, GRADE supports:
> `"default"`, `"green"`, `"blue"`

**Example Usage:**

```bash
# NOS
python3 nos_plot.py nos_data.csv nos_plot.png smiley_blue

# ROBIS
python3 robis_plot.py robis_data.xlsx robis_plot.png blue

# GRADE (only default/green/blue)
python3 grade_plot.py grade_data.csv grade_plot.png green
```

> If the theme argument is omitted, the **default** theme will be used.

---

### Sample

![Sample Result](example/sample.png)

---

### 2️⃣ Streamlit Web App

```bash
streamlit run app.py
```

* Upload your CSV/XLSX file to visualize **traffic-light plots**.
* Select the **risk-of-bias tool**: NOS, JBI, GRADE, or ROBIS.
* Choose your **plot theme** for a publication-ready figure.
* Download plots in **PNG, PDF, SVG, or EPS formats** directly.

> The web provides **example CSV/XLSX templates** for each tool to guide formatting.

---

## 📖 Methods Notes

* **RoB assessment:** Follows the original scoring/checklists of each tool.
* **Visualisation:** Traffic-light and weighted bar plots generated with **Matplotlib / Seaborn**.
* **Transparency:** Raw scores should be included in supplementary tables.
* **Reproducibility:** Code and sample datasets archived via **Zenodo DOI**.
* **Scope:** Critiplot is a **visualisation tool only**; it does **not compute risk-of-bias**.

---

## 🔹 How Scores Are Converted to Risk-of-Bias (RoB)

### NOS

* **Selection domain (0–4 stars):** 3–4 → Low, 2 → Moderate, 0–1 → High
* **Comparability domain (0–2 stars):** 2 → Low, 1 → Moderate, 0 → High
* **Outcome/Exposure domain (0–3 stars):** 3 → Low, 2 → Moderate, 0–1 → High

### JBI

* Each domain is binary: `1 = low risk`, `0 = high risk` (case reports & series).

### GRADE

* High / Moderate / Low / Very Low certainty mapped to traffic-light colors.

### ROBIS

* Domains evaluated as Low / High / Unclear risk and visualized similarly.

---

## 📄 Citation

If you use **Critiplot** in your work, please cite:

**APA:**

> Sahu, V. (2025). *Critiplot: A Critical Appraisal Plot Visualiser for Risk of Bias in Systematic Reviews and Meta-Analyses (v2.1.1)*. (https://doi.org/10.5281/zenodo.17236600)

**Other formats:**

Harvard, MLA, Chicago, IEEE, Vancouver (see full web for options).

> Download RIS/BibTeX citation files directly from the web.

---

## 📜 License

<a href="https://opensource.org/licenses/Apache-2.0">
  <img src="https://upload.wikimedia.org/wikipedia/commons/7/7e/Apache_Feather_Logo.svg" alt="Apache 2.0 License" height="120">
</a>

Apache 2.0 © 2025 Vihaan Sahu

---

## Example / Result

Here’s an example traffic-light plot generated using Critiplot with different themes:

![Example Result](example/result.png)
![Example Result22](example/result2.png)
**NOS**


![Example Result1](example/grade_result2.png)
![Example Result13](example/grade_result3.png)
**GRADE**


![Example Result21](example/robis_result4.png)
![Example Result23](example/robis_result3.png)
**ROBIS**



![Example Result34](example/case_report.png)
![Example Result37](example/case_report2.png)
**JBI Case Report**


![Example Result4](example/series_plot1.png)
![Example Result43](example/series_plot4.png)
**JBI Case Series**


![Example Result990](example/MMAT2.png)
**MMAT Descriptive Plot**


![Example Result9909](example/MMAT7.png)
**MMAT Non-Randomized Plot**


![Example Result99099](example/MMAT8.png)
**MMAT Mixed-Methods Plot**


![Example Result990999](example/MMAT9.png)
**MMAT Randomized Plot**


![Example Result9909990](example/MMAT6.png)
**MMAT Qualitative Plot**