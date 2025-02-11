from fastapi import FastAPI

app = FastAPI()

print("\nI'm the server\n")

# @app.get("/")
# async def get_():
#     print("\nget_data\n")
#     return {"message": "Hello from Service B!"}

@app.get("/data")
async def get_data():
    print("\nget_data\n")
    return {"message": "Hello from Service B!"}