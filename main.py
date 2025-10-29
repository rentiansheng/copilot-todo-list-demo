from fastapi import FastAPI
from app.api import tree, model

app = FastAPI(title="Tree Management API", version="1.0.0")

# Include routers
app.include_router(tree.router, prefix="/api/tree", tags=["tree"])
app.include_router(model.router, prefix="/api/model", tags=["model"])

@app.get("/")
async def root():
    return {"message": "Tree Management API is running"}
