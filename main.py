from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, EmailStr

import requests
from scrape import run_scrape

app = FastAPI()
resonse_webhook_url = "https://hook.integrator.boost.space/k80rinp9fgzwhlysiohlvy12x8r0qa36"

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
async def main(user_credential: UserCredential, background_tasks: BackgroundTasks):
    background_tasks.add_task(
        run_scrape_and_send_webhook, 
        user_credential.email,
        user_credential.password,
    )
    return {'message': f'Scraping in progress. Check webhook for results. 👉 {resonse_webhook_url}'}
    

async def run_scrape_and_send_webhook(email: EmailStr, password: str):
    try:
        copied_text = run_scrape(email, password)
        send_webhook({"copied_text": copied_text})
    except Exception as error:
        print("An error occurred:", type(error).__name__, "–", error)
    
def send_webhook(response):
    print('sending weebhook response')
    requests.post(resonse_webhook_url, url=response)