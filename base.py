from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from database import Base, engine, SessionLocal, UserScore
import json
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Load quiz questions
with open("data/quiz.json") as f:
    quiz_data = json.load(f)

# Routes
@app.get("/", response_class=HTMLResponse)
async def landing_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/", response_class=HTMLResponse)
async def quiz_page(request: Request):
    return templates.TemplateResponse("quiz.html", {"request": request, "questions": quiz_data})

@app.get("/", response_class=HTMLResponse)
async def learning_page(request: Request):
    return templates.TemplateResponse("learning.html", {"request": request})

@app.get("/", response_class=HTMLResponse)
async def chatbot_page(request: Request):
    return templates.TemplateResponse("chatbot.html", {"request": request})

#@app.post("/api/chat")
#async def chat_response(user_input: str = Form(...)):
  #  azure_api_key = os.getenv("AZURE_API_KEY")
   # azure_endpoint = os.getenv("AZURE_API_ENDPOINT")

    #async with httpx.AsyncClient() as client:
      #  response = await client.post(
          #  azure_endpoint,
          #  headers={"Authorization": f"Bearer {azure_api_key}"},
            #json={"messages": [{"role": "user", "content": user_input}]}
       # )
        #result = response.json()
        #return {"reply": result.get("choices", [{}])[0].get("message", {}).get("content", "No response")}  

@app.post("/submit-score")
async def submit_score(username: str = Form(...), score: int = Form(...)):
    db = SessionLocal()
    new_score = UserScore(username=username, score=score)
    db.add(new_score)
    db.commit()
    db.refresh(new_score)
    db.close()
    return {"message": f"Score saved for {username}"}

Base.metadata.create_all(bind=engine)