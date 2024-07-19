from fastapi import FastAPI
import subprocess
import sys
import os
from pydantic import BaseModel

app = FastAPI()
python_path = os.path.abspath(".")

class Query(BaseModel):
    question: str

@app.post("/query")
async def run_query(query: Query):
    print(query.question)
    command = [
        sys.executable, "-m", "graphrag.query",
        "--root", "./ragtest",
        "--method", "global",
        "Who is Thomas Edison?"
    ]

    # Environment variables
    env = os.environ.copy()
    env["PYTHONPATH"] = python_path
    
    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode == 0:
        return {"result": result.stdout}
    else:
        return {"error": result.stderr}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)