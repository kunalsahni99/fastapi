from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def index() -> dict[str, str]:
    return {'hello': 'world'}

@app.get('/about')
async def about() -> str:
    return "About page of the company ABC"