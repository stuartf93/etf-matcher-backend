from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, List, Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class State(BaseModel):
    full_counterparties: Dict[str, Dict[str, List[str]]] = {}
    last_cp: Optional[str] = None

state = State()
version = 0  # monotonically increasing version number

@app.get("/state")
def get_state():
    return {
        "version": version,
        "full_counterparties": state.full_counterparties,
        "last_cp": state.last_cp,
    }

@app.post("/state")
def update_state(new_state: State):
    global state, version
    state = new_state
    version += 1
    return {"version": version}
