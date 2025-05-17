from fastapi import FastAPI
from app.translation import router as translation_router
from app.text_generation import router as text_gen_router
from app.summarization import router as summarization_router

app = FastAPI(title="Unified AI & FAST API App")

app.include_router(translation_router, prefix="/api")
app.include_router(text_gen_router, prefix="/api")
app.include_router(summarization_router, prefix="/api")

@app.get("/health")
def health_check():
    return {"status": "ok"}
