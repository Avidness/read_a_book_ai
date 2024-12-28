from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from app.pipeline.core import pipeline_core
from app.models.UserInput import UserInput

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/")
async def main():
    return 'hello world'

@app.post("/send_input")
async def main2(input_data: UserInput):
    return StreamingResponse(pipeline_core(input_data.user_input), media_type="application/json")