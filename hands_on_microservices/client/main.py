from fastapi import FastAPI
import httpx

app = FastAPI()

print("\nI'm the client\n")


@app.get("/")
async def call_basic():
    print("\ncall_basic\n")
    # Define the path to the Unix Domain Socket
    return "hello"

@app.get("/call-serveur")
async def call_service_b():
    print("\ncall_service_b\n")
    # Define the path to the Unix Domain Socket
    uds_path = "/tmp/serveur.sock"
    # Use a custom transport to make requests via the UDS
    transport = httpx.AsyncHTTPTransport(uds=uds_path)
    # Standard URL format without http+unix://
    url = "http://serveur/data"
    async with httpx.AsyncClient(transport=transport) as client:
        response = await client.get(url)
    return response.json()




