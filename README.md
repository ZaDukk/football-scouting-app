# Football Scouting App

Simple Streamlit app to explore player datasets, rank players with weighted metrics, and visualize top performers.

## Project Structure

```
football-scouting-app/
├── data/               # For CSVs or datasets
├── notebooks/          # Jupyter notebooks for exploration
├── src/                # Source code
│   ├── data_loader.py  # Load & clean data
│   ├── model.py        # Ranking/scouting models
│   └── viz.py          # Visualization functions
├── app.py              # Streamlit app entry point
├── requirements.txt    
└── README.md
```

## Setup

1) Create and activate virtual environment (already present in this repo as `venv/`):

Windows PowerShell:
```bash
./venv/Scripts/Activate.ps1
```

2) Install dependencies:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run the app

```bash
streamlit run app.py
```

Open the URL shown in the terminal.

## Usage

- Upload a CSV, or place a file under `data/` and enter its filename.
- Choose name column, select metrics, and assign weights to rank players.
- View table and bar chart of top players.
