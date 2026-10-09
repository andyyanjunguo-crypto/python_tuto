# ========================================
# Step 3: 宝可梦 API (连接真实的 PokeAPI)
# 运行: uvicorn main:app --reload
# 文档: http://127.0.0.1:8000/docs
# 卡片: http://127.0.0.1:8000/card/
# ========================================

import asyncio
from pathlib import Path

import httpx
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

POKEAPI_BASE = "https://pokeapi.co/api/v2"

app = FastAPI(
    title="Pokémon Trainer API",
    description="Day15: 用 FastAPI 包装公开的 PokeAPI",
    version="1.0.0",
)

# CORS: 允许其它网页 (比如用 Live Server 打开的 Day14 卡片) 调用我们的 API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 课堂演示用; 正式项目要写具体的域名
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----------------------------------------
# 1. 数据模型 (Pydantic)
#    定义 "数据长什么样", FastAPI 用它来校验和生成文档
# ----------------------------------------

class Stats(BaseModel):
    hp: int
    attack: int
    defense: int
    special_attack: int
    special_defense: int
    speed: int


class Pokemon(BaseModel):
    id: int
    name: str
    height_m: float
    weight_kg: float
    types: list[str]
    abilities: list[str]
    stats: Stats
    total: int
    image: str | None


class TeamCreate(BaseModel):
    """POST /teams 时, 客户端要发送的 JSON"""
    trainer: str = Field(min_length=1, max_length=20, examples=["Ash"])
    members: list[str] = Field(min_length=1, max_length=6, examples=[["pikachu", "charmander"]])


class Team(BaseModel):
    trainer: str
    members: list[Pokemon]
    total_power: int


# ----------------------------------------
# 2. 工具函数: 调用 PokeAPI
# ----------------------------------------

cache: dict[str, dict] = {}  # 简单缓存: 同一个地址只向 PokeAPI 请求一次


async def fetch_from_pokeapi(path: str) -> dict:
    if path in cache:
        return cache[path]

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(f"{POKEAPI_BASE}{path}")
    except httpx.RequestError:
        # 断网 / 超时 -> 503 Service Unavailable
        raise HTTPException(status_code=503, detail="Cannot reach PokeAPI, try again later")

    if response.status_code == 404:
        raise HTTPException(status_code=404, detail=f"Not found on PokeAPI: {path}")
    if response.status_code != 200:
        # PokeAPI 自己出错了 -> 502 Bad Gateway
        raise HTTPException(status_code=502, detail=f"PokeAPI error: {response.status_code}")

    data = response.json()
    cache[path] = data
    return data


def clean_name(text: str) -> str:
    """'  Pikachu ' -> 'pikachu'; 只允许字母、数字和 '-' (例如 mr-mime)"""
    name = text.strip().lower()
    if not name.replace("-", "").isalnum():
        raise HTTPException(status_code=400, detail=f"Invalid name: '{text}'")
    return name


def to_pokemon(data: dict) -> Pokemon:
    """把 PokeAPI 又大又乱的原始数据, 整理成我们自己的简洁格式"""
    stats = {s["stat"]["name"].replace("-", "_"): s["base_stat"] for s in data["stats"]}
    return Pokemon(
        id=data["id"],
        name=data["name"],
        height_m=data["height"] / 10,   # PokeAPI 的单位是分米
        weight_kg=data["weight"] / 10,  # PokeAPI 的单位是百克
        types=[t["type"]["name"] for t in data["types"]],
        abilities=[a["ability"]["name"] for a in data["abilities"]],
        stats=Stats(**stats),
        total=sum(stats.values()),
        image=data["sprites"]["other"]["official-artwork"]["front_default"],
    )


async def get_pokemon_data(name_or_id: str) -> Pokemon:
    data = await fetch_from_pokeapi(f"/pokemon/{clean_name(name_or_id)}")
    return to_pokemon(data)


# ----------------------------------------
# 3. 接口 (Endpoints)
# ----------------------------------------

# https://yanjunapi.com/api/v1/
@app.get("/")
def home():
    return {
        "message": "Welcome to the Pokémon Trainer API!",
        "docs": "/docs",
        "card": "/card/",
    }

# https://yanjunapi.com/api/v1/pokemon
@app.get("/pokemon")
async def list_pokemon(
    limit: int = Query(20, ge=1, le=100, description="How many to return"),
    offset: int = Query(0, ge=0, description="How many to skip"),
):
    data = await fetch_from_pokeapi(f"/pokemon?limit={limit}&offset={offset}")
    return {
        "count": data["count"],
        "limit": limit,
        "offset": offset,
        "results": [p["name"] for p in data["results"]],
    }


# https://yanjunapi.com/api/v1/pokemon/123
@app.get("/pokemon/{name_or_id}")
async def get_pokemon(name_or_id: str) -> Pokemon:
    return await get_pokemon_data(name_or_id)


@app.get("/type/{type_name}")
async def pokemon_by_type(type_name: str, limit: int = Query(20, ge=1, le=100)):
    data = await fetch_from_pokeapi(f"/type/{clean_name(type_name)}")
    names = [p["pokemon"]["name"] for p in data["pokemon"]]
    return {"type": data["name"], "count": len(names), "results": names[:limit]}


@app.get("/compare")
async def compare(first: str, second: str):
    # asyncio.gather: 两个请求同时发出, 不用排队一个一个等
    a, b = await asyncio.gather(get_pokemon_data(first), get_pokemon_data(second))

    if a.total == b.total:
        winner = "draw"
    else:
        winner = a.name if a.total > b.total else b.name

    return {
        "first": {"name": a.name, "total": a.total},
        "second": {"name": b.name, "total": b.total},
        "winner": winner,
    }


# ----------------------------------------
# 4. POST: 创建训练家队伍
#    teams 存在内存里, 服务器重启后会清空 (以后可以换成数据库)
# ----------------------------------------

teams: dict[str, Team] = {}


@app.post("/teams", status_code=201)
async def create_team(team: TeamCreate) -> Team:
    if team.trainer in teams:
        raise HTTPException(status_code=409, detail=f"Team '{team.trainer}' already exists")

    members = await asyncio.gather(*(get_pokemon_data(name) for name in team.members))

    new_team = Team(
        trainer=team.trainer,
        members=list(members),
        total_power=sum(p.total for p in members),
    )
    teams[team.trainer] = new_team
    return new_team


@app.get("/teams")
def list_teams() -> list[Team]:
    return list(teams.values())


# ----------------------------------------
# 5. 网页: 把 static/ 文件夹挂到 /card
#    浏览器打开 http://127.0.0.1:8000/card/
# ----------------------------------------

app.mount("/card", StaticFiles(directory=Path(__file__).parent / "static", html=True), name="card")
