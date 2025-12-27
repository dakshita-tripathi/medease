from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import user
from api.routes import auth
from api.routes import patient

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend
    allow_credentials=True,
    allow_methods=["*"],   # allows OPTIONS
    allow_headers=["*"],
)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(patient.router)

@app.get("/health")
def health():
    return {"status": "ok"}



