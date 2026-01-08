# ==============================
# Imports
# ==============================
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import string, os, nltk, time
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sentence_transformers import SentenceTransformer, util
import torch
import mysql.connector
from mysql.connector import Error

# ==============================
# NLP setup
# ==============================
for resource in ["punkt", "stopwords", "wordnet"]:
    try:
        nltk.data.find(resource)
    except LookupError:
        nltk.download(resource, quiet=True)

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def preprocess(text: str) -> str:
    tokens = word_tokenize(text.lower())
    tokens = [t for t in tokens if t not in stop_words and t not in string.punctuation]
    tokens = [lemmatizer.lemmatize(t) for t in tokens]
    return " ".join(tokens)

print("NLTK punkt OK")

# ==============================
# wait_for_db function
# ==============================
def wait_for_db(host, user, password, database, retries=10, delay=3):
    for i in range(retries):
        try:
            conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                port=3306
            )
            print("✅ Connected to MySQL!")
            return conn
        except Error as e:
            print(f"⏳ Waiting for MySQL ({i+1}/{retries})... {e}")
            time.sleep(delay)
    raise Exception("❌ Could not connect to MySQL after several retries")

# ==============================
# Database connection
# ==============================
db = wait_for_db(
    host=os.getenv("DB_HOST", "mysql"),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD", "root"),
    database=os.getenv("DB_NAME", "chatbot"),
    retries=20,
    delay=3
)
cursor = db.cursor(dictionary=True)

# Créer la table si elle n'existe pas
cursor.execute("""
    CREATE TABLE IF NOT EXISTS faqs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        question TEXT NOT NULL,
        answer TEXT NOT NULL
    )
""")
db.commit()

# ==============================
# Load FAQs from DB
# ==============================
cursor.execute("SELECT question, answer FROM faqs")
rows = cursor.fetchall()
questions = [preprocess(r["question"]) for r in rows]
answers = [r["answer"] for r in rows]

# ==============================
# Sentence-BERT
# ==============================
model = SentenceTransformer("all-MiniLM-L6-v2")
question_embeddings = model.encode(questions, convert_to_tensor=True)

# ==============================
# FastAPI setup
# ==============================
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

# ==============================
# Chat logic
# ==============================
@app.post("/chat")
def chat(request: ChatRequest):
    user_message = preprocess(request.message)
    message_embedding = model.encode(user_message, convert_to_tensor=True)
    similarity_scores = util.cos_sim(message_embedding, question_embeddings)[0]
    max_score_idx = torch.argmax(similarity_scores).item()
    score = similarity_scores[max_score_idx].item()
    if score > 0.6:
        return {"reply": answers[max_score_idx]}
    else:
        return {"reply": "I'm sorry, I don't have an answer for that."}
