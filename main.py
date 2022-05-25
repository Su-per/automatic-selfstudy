from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from background_apply import BackgroundApply
from config import header, SIGNIN_URL
import requests


app = FastAPI(title="Automatic selfstudy")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
db = []


class Register(BaseModel):
    email: str
    password: str


@app.post("/register")
async def register(apply_type: str, req: Register):
    if not apply_type in ["selfstudy", "massage"]:
        return {"message": "Invalid apply type"}
    if req.email in [i["email"] for i in db if i["apply_type"] == apply_type]:
        return {"message": "Already applied"}

    data = {"email": req.email, "password": req.password}
    res = requests.post(url=SIGNIN_URL, json=data, headers=header)

    if res.status_code != 200:
        return {"message": "Invalid email or password"}

    db.append(
        {
            "email": req.email,
            "access_token": res.json()["data"]["token"]["accessToken"],
            "pw": req.password,
            "apply_type": apply_type,
        }
    )
    return {"message": "Success"}


@app.get("/list")
async def get_user_list(apply_type: str):
    if apply_type == "selfstudy":
        return [i["email"] for i in db if i["apply_type"] == "selfstudy"]
    elif apply_type == "massage":
        return [i["email"] for i in db if i["apply_type"] == "massage"]


@app.on_event("startup")
async def startup():
    t = BackgroundApply(db=db, selfstudy_time=(20, 0), massage_time=(20, 20))
    t.start()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
