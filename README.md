# 🌶️ Chile Index Explorer
**A Data Engineering & Visualization Dashboard**

The **Chile Index Explorer** is a Streamlit-based web application designed to catalog, filter, and visualize botanical and Scoville heat data for chiles. Built for both software engineering portfolio display and culinary education, it transforms raw, unstructured data into an interactive, sanitized dashboard.



## 🚀 Live Demo
[chileheads.streamlit.app](https://chileheads.streamlit.app/)

---

## 🛠️ The Data Pipeline (Engineering Highlights)
The core of this project is a robust **Data Sanitization Pipeline** designed to solve common "real-world" integrity issues encountered when migrating from spreadsheet software to Python.

### Key Engineering Challenges Solved:
* **The Excel Date Bug:** Automatically identified and corrected rows where heat scores (e.g., `2/10`) were misinterpreted as dates (e.g., `2026-02-10`).
* **Mixed-Type Type Safety:** Implemented a regex-based sanitization layer to handle mixed strings (e.g., `10+/10`) and convert them into sortable floats.
* **Botanical Mapping:** Standardized shorthand cultivar categories into proper italicized scientific names (e.g., *Capsicum annuum*, *Capsicum chinense*).
* **Responsive UI:** Utilized Streamlit's latest `width="stretch"` parameters for cross-device scaling.

---

## 📜 Credits & Data Sources
This project relies on the extensive research and data curation of [u/BennyTheAstronaut](https://www.reddit.com/user/BennyTheAstronaut/), who compiled the primary dataset.

### Technical & Culinary References:
* **SHU Calculations:** Based on High-Performance Liquid Chromatography (HPLC) methods defined by **Collins et al. (1995)** and **ASTA** standards.
* **Botanical Data:** Compiled from sources including *Cayenne Diane*, *PepperScale*, *The Chilli Workshop*, and the *Auguste Escoffier School of Culinary Arts*.
* **Seed & Cultivar Info:** Reference data provided by *Sandia Seed Company* and *Pepper Joe's*.

---

## 💻 Tech Stack
* **Language:** Python 3.13
* **Framework:** Streamlit
* **Data Science:** Pandas
* **Styling:** Custom CSS & Streamlit Containers

---

## 📖 How to Run Locally

1. **Clone the repository:**
```bash
git clone https://github.com/joan0fsnark/chile-index.git
cd chile-index
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

---

## ⚖️ License
This project is licensed under the [CC BY-NC 4.0](LICENSE) - see the LICENSE file for details. 
It is free for personal and educational use; commercial use is prohibited.