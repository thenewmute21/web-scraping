from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, EmailStr, AnyHttpUrl

import requests
from scrape import run_scrape

app = FastAPI()
resonse_webhook_url = "https://hook.integrator.boost.space/k80rinp9fgzwhlysiohlvy12x8r0qa36"
# resonse_webhook_url = "http://localhost:5000/"

class UserCredential(BaseModel):
    email: EmailStr
    password: str
    url : str
    

@app.post("/")
async def main(user_credential: UserCredential, background_tasks: BackgroundTasks):
    background_tasks.add_task(
        run_scrape_and_send_webhook, 
        user_credential.email,
        user_credential.password,
        user_credential.url
    )
    return {'message': f'Scraping in progress. Check webhook for results. 👉 {resonse_webhook_url}'}
    

async def run_scrape_and_send_webhook(email: EmailStr, password: str, url: str):
    try:
        copied_text = run_scrape(email, password, url)
        send_webhook({"copied_text": copied_text})
    except Exception as error:
        print("An error occurred:", type(error).__name__, "–", error)


def send_webhook(response):
    print('sending weebhook response')
    print(response)
    res = requests.post(resonse_webhook_url, json=response)
    
    if res.ok:
        print('webhook was successful')
    else:
        print('Webhook failed with status code:', res.status_code)
        print('Response from webhook:', res.text)