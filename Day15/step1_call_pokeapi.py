# ========================================
# Step 1: Python 作为 API 客户端
# 用 httpx 调用公开的 PokeAPI
# 运行: python step1_call_pokeapi.py
# ========================================

import httpx

BASE_URL = "https://pokeapi.co/api/v2"


# ----------------------------------------
# 1. 最简单的 GET 请求
# ----------------------------------------

response = httpx.get(f"{BASE_URL}/pokemon/pikachu")

print("状态码:", response.status_code)                  # 200 = 成功
print("数据格式:", response.headers["content-type"])    # application/json

data = response.json()  # JSON 文本 -> Python dict

print("名字:", data["name"])
print("编号:", data["id"])


# ----------------------------------------
# 2. 读取嵌套的数据 (dict 里套 list 再套 dict)
# ----------------------------------------

types = [t["type"]["name"] for t in data["types"]]
print("属性:", types)

for s in data["stats"]:
    print(f"  {s['stat']['name']:>16}: {s['base_stat']}")

image = data["sprites"]["other"]["official-artwork"]["front_default"]
print("图片:", image)


# ----------------------------------------
# 3. Query 参数: 分页获取列表
#    等价于 /pokemon?limit=5&offset=0
# ----------------------------------------

response = httpx.get(f"{BASE_URL}/pokemon", params={"limit": 5, "offset": 0})
names = [p["name"] for p in response.json()["results"]]
print("\n前 5 只宝可梦:", names)


# ----------------------------------------
# 4. 错误处理 (复习 Day9 的 try / except)
# ----------------------------------------

def get_pokemon(name: str) -> dict | None:
    try:
        response = httpx.get(f"{BASE_URL}/pokemon/{name.lower()}", timeout=10)
        response.raise_for_status()  # 4xx / 5xx 会抛出 HTTPStatusError
        return response.json()
    except httpx.HTTPStatusError as e:
        print(f"服务器返回错误: {e.response.status_code}")
    except httpx.RequestError as e:
        print(f"网络连接失败: {e}")
    return None


print()
for name in ["Charmander", "agumon"]:  # agumon 是数码宝贝, 不是宝可梦 :)
    pokemon = get_pokemon(name)
    if pokemon:
        print(f"找到了 {pokemon['name']}! 体重 {pokemon['weight'] / 10} kg")
    else:
        print(f"找不到 {name}")
