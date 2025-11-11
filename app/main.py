from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.convert import router as convert_router

app = FastAPI()

# ✅ CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://fomago-convertor.vercel.app/", "http://localhost:5173",],  # or ["*"] for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)

# ✅ Register your router
app.include_router(convert_router)

# Optional test route
@app.get("/")
def home():
    return {"message": "Backend is running 🚀"}
