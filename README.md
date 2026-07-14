# ⚡ TrustCharge

TrustCharge is an intelligent dashboard for EV charging station trust and analytics.

## Project Structure

```
TrustCharge/
├── app.py              # Streamlit entry point
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
├── .gitignore
├── modules/
│   └── fake_pipeline.py  # Synthetic data pipeline
├── data/               # Data files
├── assets/             # Static assets (images, icons)
├── docs/               # Documentation
└── venv/               # Virtual environment (not tracked)
```

## Setup

```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```
