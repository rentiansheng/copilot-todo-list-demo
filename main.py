from fastapi import FastAPI
from app.api.routes import tree, model
from app.core.config import settings

app = FastAPI(
    title="CMDB Tree API",
    description="API for CMDB tree hierarchy management with Elasticsearch backend",
    version="1.0.0"
)

# Include routers
app.include_router(tree.router, prefix="/api/tree", tags=["tree"])
app.include_router(model.router, prefix="/api/model", tags=["model"])

@app.get("/")
async def root():
    return {"message": "CMDB Tree API is running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
