
import dotenv
import uvicorn
dotenv.load_dotenv()
from fastapi import FastAPI
from routers import status, users
from app.database.engine import create_db_and_tables


app = FastAPI()
app.include_router(status.router)
app.include_router(users.router)

if __name__ == "__main__":
    create_db_and_tables()
    uvicorn.run(app, host="127.0.0.1", port=8002)



