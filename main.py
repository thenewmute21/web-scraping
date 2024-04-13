from typing import Optional

from fastapi import FastAPI, HTTPException

from scrape import run_scrape

app = FastAPI()


@app.get("/")
async def root():
    try:
        copied_text = run_scrape()
        return {"copied_text": copied_text}
    except:
        raise HTTPException(status_code=400, detail='something went wrong')