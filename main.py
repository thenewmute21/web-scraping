from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

from scrape import run_scrape

app = FastAPI()


class UserCredential(BaseModel):
    email: EmailStr
    password: str


@app.get("/")
async def root():
    email = "thenewmute21@gmail.com"
    password = "Ylopo*12"
    try:
        copied_text = run_scrape(email, password)
        return {"copied_text": copied_text}
    except Exception as error:
        print("An error occurred:", type(error).__name__, "–", error)
        raise HTTPException(status_code=400, detail='something went wrong')
    

@app.post("/")
async def main(user_credential: UserCredential):
    try:
        copied_text = run_scrape(
                        user_credential.email,
                        user_credential.password,
                    )
        return {"copied_text": copied_text}
    except Exception as error:
        print("An error occurred:", type(error).__name__, "–", error)
        raise HTTPException(status_code=400, detail='something went wrong')