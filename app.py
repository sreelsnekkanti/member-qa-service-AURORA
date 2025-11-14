from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from pathlib import Path
import json
import re
# importing framework to write rest apis and Intialize
app = FastAPI(
    title="Member QA Service",
    description="Simple question-answering API over member messages",
    version="1.0.0",
)

# Global state

messages_raw: List[Dict[str, Any]] = []
index_built: bool = False

class AskResponse(BaseModel):
    answer: str

# Data Loading

def fetch_messages_local() -> List[Dict[str, Any]]:

    fixture_path = Path(__file__).with_name("sample_messages.json")
    if not fixture_path.exists():
        raise RuntimeError(
            "sample_messages.json not found. Please create it in the same folder as app.py."
        )


    with fixture_path.open("r", encoding="utf-8-sig") as f:
        data = json.load(f)

    if not isinstance(data, dict) or "messages" not in data or not isinstance(data["messages"], list):
        raise RuntimeError("sample_messages.json must contain a top-level 'messages' list")

    return data["messages"]

def ensure_index_built() -> None:
    
    global index_built, messages_raw
    if index_built:
        return

    print("Loading messages from local sample_messages.json")
    messages_raw = fetch_messages_local()
    index_built = True
    print(f"Loaded {len(messages_raw)} messages.")

# Message retrieval

def tokenize(text: str) -> List[str]:
    
    text = text.lower()
    tokens = re.findall(r"[a-z0-9]+", text)
    return tokens

def score_message(question: str, message: Dict[str, Any]) -> int:
    
    q_tokens = set(tokenize(question))
    m_text = str(
        message.get("text")
        or message.get("body")
        or message.get("content")
        or ""
    )
    m_tokens = set(tokenize(m_text))
    overlap = q_tokens.intersection(m_tokens)
    return len(overlap)

def get_best_message_for_question(question: str) -> Dict[str, Any]:
   
    if not question.strip():
        raise ValueError("Question is empty")

    if not messages_raw:
        raise RuntimeError("No messages loaded")

    best_msg = None
    best_score = -1

    for m in messages_raw:
        s = score_message(question, m)
        if s > best_score:
            best_score = s
            best_msg = m

    # If there are no overlaps at all, it falls back to the first message
    if best_msg is None:
        best_msg = messages_raw[0]

    return best_msg

# Answer extraction

_number_pattern = re.compile(r"\b\d+\b")

def extract_answer_from_message(message: Dict[str, Any], question: str) -> str:
    
    raw_text = (
        message.get("text")
        or message.get("body")
        or message.get("content")
        or ""
    )
    text = str(raw_text).strip()
    if not text:
        return "I could not find an answer in the member data."

    q_lower = question.lower()

    # If the question contains “how many”, it looks for a number in the text and returns the first one it finds
    if "how many" in q_lower:
        numbers = _number_pattern.findall(text)
        if numbers:
            return numbers[0]

    # For everything else, it will return the message text or most relevant text directly
    return text

# API endpoint 
# Rest APIs
@app.get("/ask", response_model=AskResponse)
def ask(q: str = Query(..., description="Natural-language question about member data")) -> AskResponse:
    
    try:
        ensure_index_built()
        best_message = get_best_message_for_question(q)
        answer = extract_answer_from_message(best_message, q)

        # Returns answer when a question is asked
        return AskResponse(answer=answer)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{type(e)._name_}: {e}")
