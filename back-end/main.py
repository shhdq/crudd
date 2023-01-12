
from fastapi import FastAPI
from db import Db
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

db = Db()


origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/add")
async def create_note(request_data: dict):
    note = request_data["note"]

    if len(note) == 0:
        return "error"
    else:
        connection = db.connection_pool

        try:
            with connection.cursor() as cursor:
                insert = "INSERT INTO notes (note) VALUES %s"

                cursor.execute(insert, (note))
        finally:
            connection.commit()
