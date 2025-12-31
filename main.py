from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
import json
from typing import Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # sau này siết domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_FILE = "data/content.json"

# mật khẩu đơn giản – đủ dùng giai đoạn đầu
ADMIN_PASSWORD = "888888"
EDITOR_PASSWORD = "111111"

def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.get("/content")
def get_content():
    return load_data()

@app.post("/content")
def update_content(
    payload: dict,
    x_password: Optional[str] = Header(None)
):
    if x_password not in [ADMIN_PASSWORD, EDITOR_PASSWORD]:
        raise HTTPException(status_code=401, detail="Unauthorized")

    save_data(payload)
    return {"status": "saved"}

