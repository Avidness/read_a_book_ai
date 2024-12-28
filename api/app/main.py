from app.db import PineconeAdapter
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

@app.post("/init_pinecone")
async def init_pc():
    
    # WIP add some basic data to Pinecone
    adapter = PineconeAdapter()
    adapter.create_index()
    data = [
        {'id': 'vec1', 'text': 'Apple is a popular fruit known for its sweetness and crisp texture.'},
        {'id': 'vec2', 'text': 'The tech company Apple is known for its innovative products like the iPhone.'},
        {'id': 'vec3', 'text': 'Many people enjoy eating apples as a healthy snack.'},
        {'id': 'vec4', 'text': 'Apple Inc. has revolutionized the tech industry with its sleek designs and user-friendly interfaces.'},
        {'id': 'vec5', 'text': 'An apple a day keeps the doctor away, as the saying goes.'},
        {'id': 'vec6', 'text': 'Apple Computer Company was founded on April 1, 1976, by Steve Jobs, Steve Wozniak, and Ronald Wayne as a partnership.'}
    ]
    adapter.upsert_data(data)
    return

@app.post("/send_input")
async def ai_request(input_data: UserInput):
    return StreamingResponse(pipeline_core(input_data.user_input), media_type="application/json")