from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load .env file for API key
load_dotenv()

# Initialize FastAPI
app = FastAPI()

# Enable CORS (for frontend communication)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Set up OpenAI client
client = OpenAI(api_key=os.getenv("API_KEY"))

# Request schema
class Prompt(BaseModel):
    prompt: str

# Function to call OpenAI API
def generate_response(prompt: str, model: str = "gpt-4o"):
    print("Generating response from OpenAI...")

    try:
        response = client.chat.completions.create(model="gpt-4o",messages=[
        {"role": "system", "content": "You are a CP expert."},
        {"role": "user", "content": "Prompt here"}
        ])
        reply = response.choices[0].message.content
        print("OpenAI response:", reply)
        return reply
    except Exception as e:
        print("Error:", e)
        return f"Error: {e}"
@app.get("/")
def test():
    return {"success" : "Test Success"}

@app.post("/explain")
def explain(data: Prompt):
    print("Received prompt:\n", data.prompt)
    result = generate_response(data.prompt)
    return {"response": result}

# Run development server (optional)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend:app", host="0.0.0.0", port=8000, reload=True)
