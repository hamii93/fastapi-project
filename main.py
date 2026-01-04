from fastapi import FastAPI


app = FastAPI()

@app.get("/")
async def root():
    return {"status": "ok"}

@app.get("/user/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id}

@app.get("/items")
def get_items(limit : int=10, offset: int = 0 ):
    return{
        "limit":limit,
        "offset":offset
    }
