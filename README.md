# 🐦 Twitter Sentiment Analysis — Power BI Dashboard

> A real-time Twitter sentiment analysis pipeline built with **Python**, **NLTK** & **VADER**, visualized through an interactive **Power BI** dashboard for trend monitoring.

---

## 📌 Overview

This project collects tweets, processes and classifies them as **Positive**, **Negative**, or **Neutral** using NLP techniques, and exports the results to a Power BI dashboard for real-time visualization of public sentiment trends.

---

## 🗂️ Project Structure

```
twitter-sentiment-powerbi/
│
├── 1_data_collection.py       # Fetches tweets using Twitter API
├── 2_preprocessing.py         # Cleans and tokenizes tweet text
├── 3_modeling.py              # Sentiment scoring using VADER
├── 4_powerbi_export.py        # Exports processed data to Excel for Power BI
├── 5_scheduler.py             # Automates pipeline at regular intervals
├── config.py                  # API keys and configuration settings
│
├── dashboard/
│   ├── Twitter_Sentiment_Dashboard.pbix   # Power BI dashboard file
│   └── twitter_sentiment_powerbi.xlsx     # Processed data source for Power BI
│
└── LICENSE                    # MIT License
```

---

## ⚙️ Tech Stack

| Layer | Tools |
|---|---|
| Data Collection | Twitter API v2 / Tweepy |
| NLP & Sentiment | Python, NLTK, VADER |
| Data Processing | Pandas |
| Visualization | Microsoft Power BI |
| Automation | Python Scheduler (`schedule`) |
| Export Format | Excel (`.xlsx`) |

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Technicaladvisor01/twitter-sentiment-powerbi.git
cd twitter-sentiment-powerbi
```

### 2. Install Dependencies

```bash
pip install tweepy nltk vaderSentiment pandas openpyxl schedule
```

### 3. Configure API Keys

Edit `config.py` with your Twitter Developer credentials:

```python
BEARER_TOKEN = "your_bearer_token"
API_KEY = "your_api_key"
API_SECRET = "your_api_secret"
ACCESS_TOKEN = "your_access_token"
ACCESS_TOKEN_SECRET = "your_access_token_secret"
```

### 4. Run the Pipeline

```bash
# Step-by-step
python 1_data_collection.py
python 2_preprocessing.py
python 3_modeling.py
python 4_powerbi_export.py

# OR run the automated scheduler
python 5_scheduler.py
```

### 5. Open the Dashboard

1. Open `dashboard/Twitter_Sentiment_Dashboard.pbix` in **Power BI Desktop**
2. Refresh the data source pointing to `dashboard/twitter_sentiment_powerbi.xlsx`
3. Explore real-time sentiment trends!

---

## 📊 Dashboard Features

- **KPI Cards** — Total Tweets, Positive %, Negative %, Neutral %, Avg VADER Score at a glance
- **Sentiment Distribution** — Donut chart breaking down Positive / Negative / Neutral tweet share
- **Sentiment Trend Over Time** — Line chart tracking sentiment changes from March to April
- **Topic-wise Sentiment Breakdown** — Stacked bar chart across 5 topics: AI, Climate, Crypto, Politics, Sports
- **Model Accuracy Comparison** — Bar chart comparing Logistic Regression, SVM (LinearSVC), Naive Bayes, and VADER-only
- **Topic Filter** — Slicer to filter all visuals by topic (AI, Climate, Crypto, Politics, Sports)

---

## 🖼️ Dashboard Screenshots

### Overall View (All Topics)
![Twitter Sentiment Dashboard - All Topics](dashboard/screenshots/image1.png)

> **10K** Total Tweets | **47.03%** Positive | **35.32%** Negative | **17.65%** Neutral | Avg VADER Score: **0.05**

---

### Filtered View (Sports Topic)
![Twitter Sentiment Dashboard - Sports Filter](dashboard/screenshots/image2.png)

> **2,189** Tweets | **63.23%** Positive | **21.24%** Negative | **15.53%** Neutral | Avg VADER Score: **0.21**

---

## 📈 Sample Sentiment Output

| Tweet | Sentiment | Score |
|---|---|---|
| "Loving the new update!" | Positive | 0.87 |
| "This is terrible service." | Negative | -0.72 |
| "Just saw the announcement." | Neutral | 0.00 |

---

## 📝 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Krishna Rawat**
GitHub: [@Technicaladvisor01](https://github.com/Technicaladvisor01)

---

> ⭐ If you found this project helpful, consider giving it a star!
