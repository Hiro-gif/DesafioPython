from fastapi import APIRouter, HTTPException
from app.task import send_scrape_task
from config import reddis_config
from pydantic import BaseModel
import aioredis

app_router = APIRouter()



@app_router.post("/scrape")
async def scrape_data(cnpj: str):
    print(f"Cnpj: {cnpj}")
    task_id = await send_scrape_task(cnpj)
    return {"task_id": task_id}

@app_router.get("/results/{task_id}")
async def get_results(task_id: str):
    redis = await aioredis.create_redis_pool('redis://redis:6379')
    result = await redis.get(task_id)
    if not result:
        raise HTTPException(status_code=404, detail="Task not found or still processing")
    return {"task_id": task_id, "data": result}