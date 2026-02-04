# 🌶️ Chile Index Explorer

**A Data Engineering & Visualization Dashboard**

The **Chili Index Explorer** is a Streamlit-based web application designed to catalog, filter, and visualize botanical and Scoville heat data for chili peppers. Built as a tool for both software engineering portfolio display and culinary education, it transforms raw, unstructured Excel/CSV data into an interactive, sanitized dashboard.

## 🚀 Live Demo

[https://chileheads.streamlit.app/](https://chileheads.streamlit.app/)

---

## 🛠️ The Data Pipeline (Engineering Highlights)

The core of this project is a robust **Data Sanitization Pipeline** designed to solve common "real-world" data integrity issues encountered when migrating from spreadsheet software (Excel/Google Sheets) to a Python environment.

### Key Engineering Challenges Solved:

* **The Excel Date Bug:** Automatically identified and corrected rows where heat scores (e.g., `2/10`) were misinterpreted as dates (e.g., `2026-02-10`).
* **Mixed-Type Type Safety:** Implemented a regex-based sanitization layer to handle mixed strings (e.g., `10+/10`) and convert them into sortable floats, preventing runtime comparison errors.
* **Botanical Mapping:** Built a mapping logic to standardize shorthand cultivar categories into full scientific names (*Capsicum annuum*, *Capsicum chinense*, etc.).
* **Responsive UI:** Utilized Streamlit's latest 2026 `width="stretch"` parameters to ensure the dashboard scales across mobile and desktop devices.

---

## 💻 Tech Stack

* **Language:** Python 3.13
* **Framework:** [Streamlit](https://streamlit.io/)
* **Data Science:** [Pandas](https://pandas.pydata.org/)
* **Styling:** Custom CSS & Streamlit Containers

---

## 📂 Project Structure

```text
├── app.py                # Main Streamlit application logic
├── chile_data.csv        # The sanitized "Source of Truth" dataset
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation

```

---

## 📖 How to Run Locally

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/ChiliIndex.git
cd ChiliIndex

```


2. **Set up a virtual environment:**
```bash
python3 -m venv .venv
source .venv/bin/activate

```


3. **Install dependencies:**
```bash
pip install -r requirements.txt

```


4. **Run the app:**
```bash
streamlit run app.py

```



---

## 🌟 About the Author

**Alena Davis** is a Software Engineer and Technical Educator based in Sacramento, CA. She is the founder of **Pixel & Whisk**, where she bridges the gap between technology and culinary arts through hands-on instruction and interactive software tools.


