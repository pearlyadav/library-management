from fastapi import FastAPI
from routers import books, students

app = FastAPI()
app.include_router(books.router)
app.include_router(students.router)

# Check the health of the API
@app.get("/health")
async def health():
    return {"status": "working"}
