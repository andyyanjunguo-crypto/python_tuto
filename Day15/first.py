import asyncio
from pathlib import Path

import httpx
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

async def fetch_name(id: int):
    async with httpx.AsyncClient(timeout=10) as client: 
        response = await client.get("https://pokeapi.co/api/v2/pokemon/pikachu")
        data = response.json()        # JSON 文本 → Python dict
        
        return data["name"]
    
    
@app.get("/name/{id}")
async def name(id: int):
    name = await fetch_name(id)
    return {"name": name}