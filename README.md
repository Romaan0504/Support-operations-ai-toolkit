# Support Operations AI Toolkit

A portfolio project built during AI learning journey.

This project demonstrates how Large Language Models can support a customer-support team by answering policy questions, triaging customer tickets, storing results, and visualizing support trends.

## Features

- **RAG Policy Assistant:** Answers customer-policy questions using semantic search with ChromaDB.
- **Grounded answers:** Retrieves relevant policy text before asking the LLM to answer.
- **Ticket Triage:** Classifies support tickets by category, priority, sentiment, and summary.
- **Structured AI output:** Uses JSON responses so ticket data can be saved and analyzed reliably.
- **SQLite storage:** Saves policy-question history and ticket-triage results locally.
- **Analytics Dashboard:** Shows total tickets, high-priority tickets, negative tickets, and charts.
- **Dockerized dashboard:** Runs the Streamlit dashboard inside a Docker container.

## Tech Stack

- Python
- Groq API and `openai/gpt-oss-20b`
- Streamlit
- ChromaDB
- SQLite
- Docker
- python-dotenv

## Project Structure

```text
genai-15-days/
├── rag_practice/
│   ├── app.py                 # RAG policy-question assistant
│   ├── triage_ticket.py       # LLM support-ticket classifier
│   ├── dashboard.py           # Streamlit analytics dashboard
│   ├── database.py            # SQLite database functions
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile             # Docker instructions
│   └── .dockerignore          # Files excluded from Docker image
└── README.md
```

## How It Works

```text
Customer policy question
        ↓
ChromaDB finds relevant policy text
        ↓
Groq LLM answers only from that context
        ↓
Question and answer are saved in SQLite
```

```text
Customer support ticket
        ↓
Groq LLM returns structured JSON
        ↓
Category + priority + sentiment + summary
        ↓
SQLite saves ticket data
        ↓
Streamlit dashboard shows analytics
```

## Local Setup

1. Clone the repository.

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

2. Enter the RAG project folder.

```bash
cd genai-15-days/rag_practice
```

3. Create and activate a virtual environment.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

4. Install dependencies.

```powershell
python -m pip install -r requirements.txt
```

5. Create a `.env` file.

```text
GROQ_API_KEY=your_groq_api_key
```

6. Run the applications.

```powershell
python triage_ticket.py
streamlit run app.py
streamlit run dashboard.py
```

## Run With Docker

From the `rag_practice` folder:

```powershell
docker build -t support-dashboard .
docker run --rm -p 8501:8501 -v "${PWD}:/app" support-dashboard
```

Open `http://localhost:8501` in your browser.

## What I Learned

- Calling LLM APIs safely with environment variables
- Prompt engineering and structured JSON output
- Retrieval-Augmented Generation (RAG)
- Embeddings and semantic search with ChromaDB
- Building browser apps with Streamlit
- Saving application data using SQLite
- Containerizing a Python app with Docker
- Documenting and sharing a project on GitHub

## Future Improvements

- Combine Policy Assistant, Ticket Triage, and Dashboard into one Streamlit application
- Add user login and role-based access
- Add automated evaluation tests for RAG answers
- Deploy the dashboard online
