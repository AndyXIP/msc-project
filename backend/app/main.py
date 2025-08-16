from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # <-- add this import
from app.api.routes import router

app = FastAPI()

# Add CORS middleware to allow your React frontend (localhost:3000) to access the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080/"],  # React dev server URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc)
    allow_headers=["*"],  # Allow all headers
)

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Welcome to AI Hoodie Backend"}
