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
async def register(req: Register):
    if req.email in map(lambda x: x["email"], db):
        return {"message": "Already applied"}

    data = {"email": req.email, "password": req.password}
    res = requests.post(url=SIGNIN_URL, json=data, headers=header)

    if res.status_code != 200:
        return {"message": "Invalid email or password"}

    db.append(
        {
            "email": req.email,
            "access_token": res.json()["data"]["token"]["accessToken"],
        }
    )
    return {"message": "Success"}


@app.get("/list/applicant")
async def get_user_list():
    return list(map(lambda x: x["email"], db))


@app.on_event("startup")
async def startup():
    t = BackgroundApply(db=db, hour=20, minute=00)
    t.start()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
