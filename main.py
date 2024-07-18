from fastapi import FastAPI
import subprocess
from pydantic import BaseModel

app = FastAPI()

class Query(BaseModel):
    question: str

@app.post("/query")
async def run_query(query: Query):
    command = [
        "python", "-m", "graphrag.query",
        "--root", "./ragtest",
        "--method", "global",
        query.question
    ]
    
    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode == 0:
        return {"result": result.stdout}
    else:
        return {"error": result.stderr}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)