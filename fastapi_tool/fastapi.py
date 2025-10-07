from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

# uv run fastapi dev fastapi_tool/fastapi.py