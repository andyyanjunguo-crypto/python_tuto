# ========================================
# Step 2: 第一个 FastAPI 服务器
# 运行: uvicorn step2_hello_fastapi:app --reload
# 打开: http://127.0.0.1:8000/docs
# ========================================

from fastapi import FastAPI, HTTPException

app = FastAPI(title="Hello FastAPI")


# ----------------------------------------
# 1. 最简单的接口: GET /
#    返回 dict, FastAPI 自动转成 JSON
# ----------------------------------------

@app.get("/")
def home():
    return {"message": "Hello, API!"}


# ----------------------------------------
# 2. 路径参数 (Path Parameter)
#    GET /hello/Ash  ->  name = "Ash"
#    times 不在路径里, 所以是 Query 参数: /hello/Ash?times=3
# ----------------------------------------

@app.get("/hello/{name}")
def say_hello(name: str, times: int = 1):
    return {"message": f"Hello, {name}! " * times}


# ----------------------------------------
# 3. 类型提示 = 自动校验
#    /add?a=1&b=2    -> 200 {"result": 3}
#    /add?a=1&b=abc  -> 422 (b 不是 int)
# ----------------------------------------

@app.get("/add")
def add(a: int, b: int):
    return {"a": a, "b": b, "result": a + b}


# ----------------------------------------
# 4. 假数据 (像 Day14 一样写死在代码里)
#    下一步 main.py 会把它换成真正的 PokeAPI
# ----------------------------------------

pokedex = {
    "pikachu": {"id": 25, "type": "electric", "hp": 35},
    "bulbasaur": {"id": 1, "type": "grass", "hp": 45},
    "charmander": {"id": 4, "type": "fire", "hp": 39},
}


@app.get("/pokemon/{name}")
def get_pokemon(name: str):
    name = name.lower()
    if name not in pokedex:
        # 抛出 HTTPException, 客户端会收到 404
        raise HTTPException(status_code=404, detail=f"Pokemon '{name}' not found")
    return pokedex[name]
