# World Happiness Dashboard (Week 9 – Streamlit)

An interactive Streamlit dashboard built for the Data Visualization course (Lecture 9).
It explores the **World Happiness Report 2023** with sidebar filters, KPI cards and two Plotly charts.

## Features
- **Sidebar filters:** choose a region and how many top countries to show (5–25)
- **KPI row:** number of countries, average happiness score (vs. global average), happiest country
- **Chart 1:** horizontal bar chart of the happiest countries
- **Chart 2:** GDP per capita vs. happiness score, coloured with a **diverging continuous scale** (`RdBu`) whose midpoint is the global average score, with the midpoint labelled directly on the chart

## Project structure
```
week09/
├── app.py
├── requirements.txt
├── README.md
└── data/
    └── world_happiness_2023.csv
```

## Dataset
World Happiness Report 2023 (Helliwell et al., 2023), as distributed on Kaggle and used in class.
The app expects a CSV with these 9 columns, in this order:
`Country, Region, Score, GDP, Social_Support, Life_Expectancy, Freedom, Generosity, Corruption`

Save it as `data/world_happiness_2023.csv`.

## Run locally
```bash
# from inside the week09 folder
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```
The app opens at http://localhost:8501. Press `Ctrl + C` in the terminal to stop it.

## Deploy (Streamlit Community Cloud)
1. Push this folder to a public GitHub repository.
2. Sign in at Streamlit Community Cloud with GitHub and click **New app**.
3. Select the repository, branch `main`, and main file path `week09/app.py`.
4. Click **Deploy**.

Live app: http://localhost:8501/

## Author
Mohammad Shariq Ali
