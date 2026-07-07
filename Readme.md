# AI Data Analyst

An AI-powered data analysis tool that lets users upload a CSV file and ask questions about it in natural language. The app analyzes the data and returns structured insights along with visualization suggestions.

## Features
- Upload any CSV file
- Ask questions in plain English
- Get structured analysis: key insights + visualization suggestions
- Multi-turn conversation memory (follow-up questions work)

## Tech Stack
- **Streamlit** — web interface
- **Pandas** — data processing
- **Groq API** (Llama 3.1) — natural language analysis

## How It Works
1. User uploads a CSV
2. Pandas extracts a summary (shape, columns, dtypes, sample rows, stats)
3. The summary + user's question is sent to Groq's Llama 3.1 model via a structured system prompt
4. The model returns a formatted analysis, which is displayed in a chat interface
5. Conversation history is stored in Streamlit's session_state, so follow-up questions maintain context

## Setup
1. Clone this repo
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file with: `GROQ_API_KEY=your_key_here`
4. Run: `streamlit run app.py`

## Screenshots
(Add a screenshot of the app here)