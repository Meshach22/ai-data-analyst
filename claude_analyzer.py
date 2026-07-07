from dotenv import load_dotenv
load_dotenv()

from groq import Groq
import json
import pandas as pd
import os

def analyze_with_claude(df, question, conversation_history):
    """
    Uses Groq to analyze CSV data based on user question.
    Returns analysis and updated conversation history.
    """
    
    dataset_info = {
        "shape": df.shape,
        "columns": df.columns.tolist(),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "first_rows": df.head(3).to_dict('records'),
        "summary_stats": df.describe().to_dict()
    }
    
    system_prompt = f"""You are an expert data analyst. You have access to this dataset:

DATASET STRUCTURE:
{json.dumps(dataset_info, indent=2, default=str)}

YOUR TASK:
When the user asks a question about this data:
1. Analyze the data carefully
2. Provide specific insights with numbers
3. Suggest the best visualization
4. Explain any patterns or anomalies

FORMAT YOUR RESPONSE AS:
ANALYSIS: [Your detailed analysis with specific numbers]
KEY INSIGHTS: [2-3 bullet points with concrete findings]
VISUALIZATION: [Suggest: histogram/scatter/line/bar and what to plot]"""

    conversation_history.append({
        "role": "user",
        "content": question
    })
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in .env file")
    
    client = Groq(api_key=api_key)
    
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            *[
                {
                    "role": msg["role"],
                    "content": msg["content"]
                }
                for msg in conversation_history
            ]
        ],
        max_tokens=1024,
        temperature=0.7
    )
    
    analysis_text = response.choices[0].message.content
    
    conversation_history.append({
        "role": "assistant",
        "content": analysis_text
    })
    
    return analysis_text, conversation_history