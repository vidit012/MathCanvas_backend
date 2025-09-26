from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from constants import SERVER_URL,PORT,ENV
from apps.calculator.route import router as calculator_router
from apps.calculator.image import router as image_router

@asynccontextmanager
async def lifespan(app:FastAPI):
    yield
    

app=FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*","https://math-canvas-frontend-khaki.vercel.app/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"server is running good"}

app.include_router(calculator_router,prefix="/calculate",tags=["calculate"])
app.include_router(image_router,prefix="/generate",tags=["generate"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=SERVER_URL, port=int(PORT),reload=(ENV=="dev"))