# Day 15：Python API 入门 —— 用 FastAPI 做一个宝可梦 API

> 昨天（Day14）我们用 JavaScript 做了一张宝可梦卡片，但数据是**写死**在代码里的。
> 今天我们用 Python 写一个**自己的 API 服务器**，从全世界开发者都在用的 [PokeAPI](https://pokeapi.co) 拿到**真实数据**，再让卡片从我们的 API 读取数据。

---

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 时长 | 45 分钟 |
| 前置知识 | 函数、dict / list、try / except（Day9）、类（Day10）、宝可梦卡片（Day14） |
| 用到的库 | `fastapi`（写 API）、`uvicorn`（运行服务器）、`httpx`（发请求）、`pydantic`（数据模型） |

**学完这节课，你能：**

1. 说清楚 API、请求 / 响应、HTTP 方法、状态码、JSON 是什么
2. 用 Python（httpx）调用别人的 API
3. 用 FastAPI 写出自己的 API，并在 `/docs` 页面里测试它
4. 理解 “网页 → 我们的 API → PokeAPI” 这条完整的数据链路

### 课堂时间表

| 时间 | 环节 | 用到的文件 |
| --- | --- | --- |
| 0 – 5 分钟 | 一、什么是 API | 浏览器 |
| 5 – 12 分钟 | 二、HTTP 基础知识 | 浏览器 |
| 12 – 20 分钟 | 三、Python 调用 API | `step1_call_pokeapi.py` |
| 20 – 28 分钟 | 四、第一个 FastAPI 服务器 | `step2_hello_fastapi.py` |
| 28 – 38 分钟 | 五、宝可梦 API：连接 PokeAPI | `main.py` |
| 38 – 42 分钟 | 六、前后端连起来 | `static/` |
| 42 – 45 分钟 | 七、总结 + 布置作业 | — |

### 文件结构

```text
Day15/
├── README.md                 ← 本教程
├── requirements.txt          ← 需要安装的库
├── step1_call_pokeapi.py     ← 第三部分：Python 调用 API
├── step2_hello_fastapi.py    ← 第四部分：第一个 FastAPI
├── main.py                   ← 第五部分：宝可梦 API（完整版）
└── static/                   ← 第六部分：宝可梦卡片网页（Day14 升级版）
    ├── index.html
    ├── style.css
    └── script.js
```

---

## 课前准备（老师提前 10 分钟完成）

```bash
cd Day15
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip3 install -r requirements.txt
```

检查环境：运行 `python step1_call_pokeapi.py`，能打印出 pikachu 的信息，说明 Python 环境和网络都正常。

> 💡 **venv（虚拟环境）是什么？** 每个项目一个独立的 “工具箱”。在里面安装的库不会影响其它项目。
> 命令行前面出现 `(.venv)` 字样，就说明已经进入虚拟环境。

---

## 一、什么是 API？（5 分钟）

**API** = Application Programming Interface，应用程序编程接口。

一句话：**API 是程序和程序之间 “对话” 的约定。**

### 餐厅比喻

```text
   你（客户端）  ── ① 点菜（请求）──▶  服务员（API）  ──▶  厨房（服务器 / 数据库）
        ▲                                 │
        └──────── ② 上菜（响应）───────────┘
```

| 餐厅 | API 世界 |
| --- | --- |
| 菜单 | API 文档：告诉你能点什么、怎么点 |
| 点菜 | 请求（Request） |
| 上菜 | 响应（Response） |
| 你不需要知道厨房怎么做菜 | 你不需要知道服务器内部怎么实现 |

**生活中的 API：** 天气 App 获取天气、地图导航、用微信登录其它 App、AI 聊天机器人……背后都是 API。

### 回顾 Day14

```javascript
// Day14: 数据写死在代码里
let pokemon = { name: "Pikachu", number: 25, hp: 35, attack: 55, ... };
```

> 🙋 **课堂提问：** 如果要做 1000 多只宝可梦的卡片，用 Day14 的方法要写多少代码？宝可梦公司出了新宝可梦怎么办？
>
> 答案：把数据交给 **专门提供数据的服务器**，我们的程序需要时用 API 去 “要”。

---

## 二、HTTP 基础知识（7 分钟）

### 2.1 动手试一试

在浏览器里打开：<https://pokeapi.co/api/v2/pokemon/pikachu>

看到一大段文字？这就是 **JSON 数据**。刚才浏览器发出了一个 **HTTP GET 请求**，PokeAPI 服务器返回了一个 **响应**。

### 2.2 URL 的组成

```text
https://pokeapi.co/api/v2/pokemon?limit=5&offset=10
└─┬─┘   └───┬────┘└──────┬──────┘└───────┬────────┘
 协议       域名         路径 Path      查询参数 Query
```

- **路径 Path**：要 “哪个资源” → `/pokemon/pikachu`
- **查询参数 Query**：“怎么要”（筛选、分页），写在 `?` 后面，多个参数用 `&` 连接 → `?limit=5&offset=10`
- **本地地址** `http://127.0.0.1:8000`：`127.0.0.1`（也叫 `localhost`）就是 “自己这台电脑”；`8000` 是 **端口**，像门牌号，一台电脑可以同时运行很多服务

### 2.3 请求（Request）与响应（Response）

```text
请求 Request（客户端 → 服务器）         响应 Response（服务器 → 客户端）
───────────────────────────────        ──────────────────────────────────
GET /api/v2/pokemon/pikachu             200 OK
Host: pokeapi.co                        Content-Type: application/json

                                        {"name": "pikachu", "id": 25, ...}
```

| 请求包含 | 响应包含 |
| --- | --- |
| 方法（GET / POST …） | 状态码（200 / 404 …） |
| 地址（URL） | 响应头 Headers（例如数据格式） |
| 请求头 Headers | 响应体 Body（真正的数据） |
| 请求体 Body（POST 时才有） | |

### 2.4 HTTP 方法：对资源做什么

| 方法 | 含义 | 宝可梦例子 |
| --- | --- | --- |
| **GET** | 获取 | `GET /pokemon/pikachu` 查看皮卡丘 |
| **POST** | 创建 | `POST /teams` 创建一支队伍 |
| **PUT / PATCH** | 修改 | `PUT /teams/Ash` 修改队伍 |
| **DELETE** | 删除 | `DELETE /teams/Ash` 解散队伍 |

**REST 风格：** URL 用 **名词** 表示资源，用 **HTTP 方法** 表示动作。

- ❌ `/getPokemon?name=pikachu`
- ✅ `GET /pokemon/pikachu`

### 2.5 状态码

口诀：**2 开头成功，4 开头是你（客户端）的错，5 开头是我（服务器）的错。**

| 状态码 | 含义 | 今天在哪里会见到 |
| --- | --- | --- |
| **200** OK | 成功 | 查到皮卡丘 |
| **201** Created | 创建成功 | `POST /teams` |
| **400** Bad Request | 请求有问题 | `/pokemon/a.b`（名字里有奇怪字符） |
| **404** Not Found | 找不到 | `/pokemon/agumon`（亚古兽是数码宝贝！） |
| **409** Conflict | 冲突 | 同名队伍已经存在 |
| **422** Unprocessable Content | 参数格式不对 | `/add?a=1&b=abc`（`abc` 不是数字） |
| **500** Internal Server Error | 服务器代码有 bug | 希望别见到 😅 |
| **502** Bad Gateway | 上游服务出错 | PokeAPI 返回了错误 |
| **503** Service Unavailable | 服务暂时不可用 | 连不上 PokeAPI（断网） |

> 🐱 课后可以看看 <https://http.cat> ，每个状态码都配了一张猫猫图。

### 2.6 JSON ↔ Python

| JSON | Python |
| --- | --- |
| `{"key": "value"}`（对象） | `dict` |
| `[1, 2, 3]`（数组） | `list` |
| `"text"` | `str` |
| `42` / `3.14` | `int` / `float` |
| `true` / `false` | `True` / `False` |
| `null` | `None` |

JSON 看起来几乎就是 Python 的 dict + list！所以在 Python 里处理 API 数据非常顺手。

---

## 三、Python 作为客户端：调用 PokeAPI（8 分钟）

📄 文件：`step1_call_pokeapi.py`　▶️ 运行：`python step1_call_pokeapi.py`

**httpx** 就是 Python 里的 “浏览器”：用代码发 HTTP 请求。（另一个常用的库 `requests` 用法几乎一样。）

### 3.1 发请求 → 拿 JSON

```python
import httpx

response = httpx.get("https://pokeapi.co/api/v2/pokemon/pikachu?param1=value1&param2=value2&param3=value3")

print(response.status_code)   # 200
data = response.json()        # JSON 文本 → Python dict
print(data["name"])           # pikachu
```

### 3.2 读取嵌套数据：一层一层 “剥洋葱”

PokeAPI 返回的数据结构（节选）：

```json
{
  "name": "pikachu",
  "types": [
    { "slot": 1, "type": { "name": "electric", "url": "..." } },
    { "slot": 2, "type": { "name": "electric2", "url": "..." } }
  ],
  "stats": [
    { "base_stat": 35, "stat": { "name": "hp" } },
    { "base_stat": 55, "stat": { "name": "attack" } }
  ]
}
```

```python
data["types"]                     # list
data["types"][0]                  # dict: {"slot": 1, "type": {...}}
data["types"][0]["type"]["name"]  # "electric"

# 列表推导式：取出所有属性
types = [t["type"]["name"] for t in data["types"]]   # ['electric']
```

### 3.3 Query 参数

```python
# 等价于 GET /pokemon?limit=5&offset=0
response = httpx.get(f"{BASE_URL}/pokemon", params={"limit": 5, "offset": 0})
```

用 `params=` 让 httpx 帮我们拼接 `?` 和 `&`，不用手写。

### 3.4 错误处理（复习 Day9）

网络请求 **一定会** 遇到失败：名字打错、断网、服务器太慢……

```python
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
```

| 异常 | 什么时候发生 | 例子 |
| --- | --- | --- |
| `httpx.HTTPStatusError` | 服务器回复了，但状态码是 4xx / 5xx | 查 `agumon` → 404 |
| `httpx.RequestError` | 根本没收到回复 | 断网、超时 |

💡 `timeout=10`：最多等 10 秒。**永远给网络请求设置超时**，否则程序可能一直卡住。

> ✍️ **课堂小练习（2 分钟）：** 修改代码，打印你最喜欢的宝可梦的身高和体重。
> 提示：PokeAPI 里 `height` 的单位是 **分米**，`weight` 的单位是 **百克**，都要除以 10 才是米和千克。

---

## 四、第一个 FastAPI 服务器（8 分钟）

刚才我们是 **点菜的客人**（客户端），现在我们要 **开餐厅**（服务器），自己提供 API！

**为什么选 FastAPI？**

- 代码少：几行就能写出一个 API
- 用 Python **类型提示** 自动校验参数
- 自动生成 **交互式文档**（`/docs`），不用写一行前端代码就能测试
- 速度快，支持 `async`（异步）

### 4.1 运行服务器

📄 文件：`step2_hello_fastapi.py`

```bash
python3 -m uvicorn step2_hello_fastapi:app --reload
```

| 部分 | 含义 |
| --- | --- |
| `uvicorn` | 服务器程序，负责监听 8000 端口、接收请求 |
| `step2_hello_fastapi` | Python 文件名（不带 `.py`） |
| `app` | 文件里的变量 `app = FastAPI()` |
| `--reload` | 修改代码后自动重启（开发时用） |

看到 `Uvicorn running on http://127.0.0.1:8000` 就成功了。停止服务器：**Ctrl + C**。

### 4.2 Hello World

```python
from fastapi import FastAPI

app = FastAPI(title="Hello FastAPI")

@app.get("/")
def home():
    return {"message": "Hello, API!"}
```

- `@app.get("/")` 是 **装饰器**：意思是 “当有人用 GET 方法访问 `/` 时，调用下面这个函数”
- 函数返回 `dict`，FastAPI **自动转换成 JSON**

浏览器打开 <http://127.0.0.1:8000> → 看到 `{"message":"Hello, API!"}`

### 4.3 路径参数 vs Query 参数

```python
@app.get("/hello/{name}")
def say_hello(name: str, times: int = 1):
    return {"message": f"Hello, {name}! " * times}
```

| 参数 | 怎么判断 | 访问例子 |
| --- | --- | --- |
| `name` | 出现在路径 `{name}` 里 → **路径参数** | `/hello/Ash` |
| `times` | 不在路径里 → **Query 参数**；有默认值 → 可以不传 | `/hello/Ash?times=3` |

### 4.4 类型提示 = 自动校验

```python
@app.get("/add")
def add(a: int, b: int):
    return {"a": a, "b": b, "result": a + b}
```

- <http://127.0.0.1:8000/add?a=1&b=2> → `{"a":1,"b":2,"result":3}`
- <http://127.0.0.1:8000/add?a=1&b=abc> → **422**：

```json
{"detail": [{"type": "int_parsing", "loc": ["query", "b"],
             "msg": "Input should be a valid integer, unable to parse string as an integer"}]}
```

> 🎉 我们 **一行校验代码都没写**！FastAPI 看到 `b: int`，就自动检查了。`loc` 告诉你哪个参数出错。

### 4.5 自动文档 `/docs`

打开 <http://127.0.0.1:8000/docs>：

1. 点开任意一个接口
2. 点 **Try it out**
3. 填参数 → 点 **Execute**
4. 下面会显示：请求 URL、状态码、响应 JSON

> 这个页面叫 **Swagger UI**，是 FastAPI 根据代码自动生成的。以后写 API，`/docs` 就是你最好的测试工具。

### 4.6 返回错误：HTTPException

```python
pokedex = {
    "pikachu": {"id": 25, "type": "electric", "hp": 35},
    "bulbasaur": {"id": 1, "type": "grass", "hp": 45},
    "charmander": {"id": 4, "type": "fire", "hp": 39},
}

@app.get("/pokemon/{name}")
def get_pokemon(name: str):
    name = name.lower()
    if name not in pokedex:
        raise HTTPException(status_code=404, detail=f"Pokemon '{name}' not found")
    return pokedex[name]
```

`raise HTTPException(...)` 会立刻结束函数，客户端收到 404 和 `detail` 里的错误信息。

> 🙋 **课堂提问：** 这个 `pokedex` 只有 3 只宝可梦，和 Day14 一样是写死的。怎么才能查到 **所有** 宝可梦？
> → 让我们的服务器去调用 PokeAPI！这就是 `main.py`。

---

## 五、宝可梦 API：连接真正的 PokeAPI（10 分钟）

先 **Ctrl + C** 停掉 step2，然后运行：

```bash
uvicorn main:app --reload
```

### 5.1 架构：我们是 “中间人”

```text
  浏览器 / 卡片网页              我们的 FastAPI（main.py）               PokeAPI
 ┌───────────────┐  GET /pokemon/pikachu  ┌───────────────┐  GET /api/v2/pokemon/pikachu  ┌────────────┐
 │    客户端      │ ────────────────────▶ │ 127.0.0.1:8000 │ ────────────────────────────▶ │ pokeapi.co │
 │               │ ◀──────────────────── │                │ ◀──────────────────────────── │            │
 └───────────────┘   简洁 JSON（< 0.5 KB） └───────────────┘     原始 JSON（约 300 KB！）     └────────────┘
```

`main.py` 同时扮演两个角色：对 PokeAPI 来说它是 **客户端**，对浏览器来说它是 **服务器**。

**为什么不让网页直接调用 PokeAPI，要自己再包一层？**

1. **整理数据**：皮卡丘的原始数据约 300 KB（大部分是招式列表），我们只返回需要的字段，还顺便把单位换算好
2. **组合新功能**：`/compare`（比较两只宝可梦）、`/teams`（组队）—— PokeAPI 本身没有这些功能
3. **缓存**：同样的数据只请求一次，更快，也遵守 PokeAPI 的 [公平使用政策](https://pokeapi.co/docs/v2#fairuse)
4. **以后还能加**：登录、数据库、隐藏 API 密钥（很多 API 需要密钥，密钥绝对不能放在前端网页里）

### 5.2 接口一览

| 方法 | 路径 | 作用 | 试一试 |
| --- | --- | --- | --- |
| GET | `/` | 欢迎信息 | <http://127.0.0.1:8000/> |
| GET | `/pokemon` | 宝可梦列表（分页） | <http://127.0.0.1:8000/pokemon?limit=5&offset=0> |
| GET | `/pokemon/{name_or_id}` | 单只宝可梦详情 | <http://127.0.0.1:8000/pokemon/pikachu> 或 `/pokemon/25` |
| GET | `/type/{type_name}` | 某个属性的宝可梦 | <http://127.0.0.1:8000/type/fire?limit=5> |
| GET | `/compare` | 比较两只的总能力值 | <http://127.0.0.1:8000/compare?first=pikachu&second=charizard> |
| POST | `/teams` | 创建训练家队伍 | 在 `/docs` 里试 |
| GET | `/teams` | 查看所有队伍 | <http://127.0.0.1:8000/teams> |
| GET | `/card/` | 宝可梦卡片网页 | <http://127.0.0.1:8000/card/> |

### 5.3 核心函数：调用 PokeAPI

```python
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
```

这个函数做了 3 件事：**查缓存 → 发请求 → 把 PokeAPI 的错误翻译成我们自己的状态码**。

### 5.4 async / await：等网络的时候别闲着

和 step1 相比，这里多了 `async` 和 `await`。

**奶茶店比喻：**

- **同步（sync）**：你点了奶茶，站在柜台前一直等，店员也陪你等 → 后面的人全都要排队
- **异步（async）**：你点了奶茶拿个号，店员马上去招呼下一位，奶茶做好了再叫你 → 一个店员能同时服务很多人

```python
async def fetch_from_pokeapi(path: str) -> dict:     # async def：这是一个 “可以等待” 的函数
    ...
    response = await client.get(url)                  # await：这里要等网络，先去处理别人的请求吧
```

**规则：**

- `await` 只能写在 `async def` 里面
- 调用一个 `async` 函数时，前面要加 `await`
- 在 `async` 函数里发请求，要用 `httpx.AsyncClient`，不用 `httpx.get`

> 服务器的大部分时间都在 **等网络**（等 PokeAPI 回复）。用了 async，等待期间服务器可以处理其他同学的请求。

### 5.5 Pydantic 模型：定义数据的 “形状”

```python
from pydantic import BaseModel

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
    stats: Stats          # 模型里可以嵌套另一个模型
    total: int
    image: str | None     # 可能没有图片 → None
```

还记得 Day10 的类吗？Pydantic 模型就是一个 **带自动校验的类**。

```python
@app.get("/pokemon/{name_or_id}")
async def get_pokemon(name_or_id: str) -> Pokemon:    # 返回类型 = 响应的格式
    return await get_pokemon_data(name_or_id)
```

`-> Pokemon` 告诉 FastAPI：这个接口一定返回 `Pokemon` 格式的数据。FastAPI 会校验输出，还会把格式显示在 `/docs` 最下面的 **Schemas** 里。

**数据整理：** `to_pokemon()` 函数把 PokeAPI 又大又乱的原始数据，变成我们干净的 `Pokemon`：

```python
def to_pokemon(data: dict) -> Pokemon:
    stats = {s["stat"]["name"].replace("-", "_"): s["base_stat"] for s in data["stats"]}
    return Pokemon(
        id=data["id"],
        name=data["name"],
        height_m=data["height"] / 10,   # PokeAPI 的单位是分米
        weight_kg=data["weight"] / 10,  # PokeAPI 的单位是百克
        types=[t["type"]["name"] for t in data["types"]],
        ...
    )
```

### 5.6 Query 参数校验

```python
@app.get("/pokemon")
async def list_pokemon(
    limit: int = Query(20, ge=1, le=100, description="How many to return"),
    offset: int = Query(0, ge=0, description="How many to skip"),
):
```

- `Query(20, ...)`：默认值是 20
- `ge=1`：**g**reater than or **e**qual，大于等于 1
- `le=100`：**l**ess than or **e**qual，小于等于 100

试试 <http://127.0.0.1:8000/pokemon?limit=500> → 422：`Input should be less than or equal to 100`

> 为什么要限制？防止有人一次要 100 万条数据，把服务器拖垮。

### 5.7 asyncio.gather：同时发出多个请求

```python
@app.get("/compare")
async def compare(first: str, second: str):
    # asyncio.gather: 两个请求同时发出, 不用排队一个一个等
    a, b = await asyncio.gather(get_pokemon_data(first), get_pokemon_data(second))
    ...
```

```text
一个一个等:   [── pikachu 150ms ──][── charizard 150ms ──]    共约 300ms
gather 同时:  [── pikachu 150ms ──]
              [── charizard 150ms ──]                         共约 150ms
```

这就是 async 的威力：**等待的时间可以重叠**。

### 5.8 POST 请求与请求体（Request Body）

GET 的参数放在 URL 里；POST 要发送的数据放在 **请求体** 里（JSON 格式）。

```python
class TeamCreate(BaseModel):
    """POST /teams 时, 客户端要发送的 JSON"""
    trainer: str = Field(min_length=1, max_length=20, examples=["Ash"])
    members: list[str] = Field(min_length=1, max_length=6, examples=[["pikachu", "charmander"]])


@app.post("/teams", status_code=201)
async def create_team(team: TeamCreate) -> Team:
    if team.trainer in teams:
        raise HTTPException(status_code=409, detail=f"Team '{team.trainer}' already exists")
    ...
```

FastAPI 看到参数类型是 Pydantic 模型 → 自动从 **请求体** 读取 JSON 并校验。

**在 `/docs` 里演示（Try it out）：**

| 请求体 | 结果 |
| --- | --- |
| `{"trainer": "Ash", "members": ["pikachu", "charmander"]}` | ✅ 201 Created |
| 同样的再发一次 | ❌ 409 Conflict（队伍已存在） |
| `{"trainer": "Misty", "members": []}` | ❌ 422（至少要 1 只） |
| `members` 里放 7 只 | ❌ 422（最多 6 只，和游戏规则一样！） |
| `{"trainer": "Brock", "members": ["onix", "agumon"]}` | ❌ 404（亚古兽不是宝可梦） |

然后打开 <http://127.0.0.1:8000/teams> 查看刚创建的队伍。

> ⚠️ `teams` 存在 **内存** 里，服务器一重启就没了（`--reload` 模式下改代码也会重启！）。真正的项目会把数据存进 **数据库**。

### 5.9 错误处理汇总

| 发生了什么 | 返回 | 谁负责 |
| --- | --- | --- |
| 参数类型 / 范围不对 | 422 | FastAPI 自动（类型提示、`Query`、`Field`） |
| 名字里有奇怪字符 | 400 | `clean_name()` |
| PokeAPI 找不到 | 404 | `fetch_from_pokeapi()` |
| 队伍重名 | 409 | `create_team()` |
| PokeAPI 自己出错 | 502 | `fetch_from_pokeapi()` |
| 连不上 PokeAPI | 503 | `fetch_from_pokeapi()` |

> 🧑‍🏫 **老师提示：** 如果时间紧张，5.7 和 5.8 可以只在 `/docs` 里演示效果，代码留给学生课后阅读。

---

## 六、前后端连起来（4 分钟）

保持 `uvicorn main:app --reload` 运行，浏览器打开：<http://127.0.0.1:8000/card/>

这是 Day14 卡片的升级版：输入名字或编号 → 点 **Search**（或者点 **Random** 随机抽一只）。

### 6.1 完整的数据链路

```text
点击 Search
   → script.js 调用 fetch()
      → main.py 的 GET /pokemon/{name_or_id}
         → PokeAPI
         ← 原始 JSON（约 300 KB）
      ← main.py 整理后的 JSON（< 0.5 KB）
   ← script.js 调用 displayPokemon()
卡片更新！
```

### 6.2 JavaScript 的 fetch() 和 Python 很像

```javascript
async function loadPokemon(nameOrId) {
    const url = API_BASE + "/pokemon/" + encodeURIComponent(nameOrId);
    const response = await fetch(url);
    const data = await response.json();

    if (!response.ok) {
        showMessage("😵 " + formatDetail(data.detail), true);
        return;
    }
    displayPokemon(data);
}
```

| Python（httpx） | JavaScript（fetch） |
| --- | --- |
| `response = await client.get(url)` | `const response = await fetch(url)` |
| `data = response.json()` | `const data = await response.json()` |
| `response.status_code` | `response.status` |
| `response.is_success` | `response.ok` |

> 👀 **看页面最下面的灰色小字：** 它显示每次调用的 API 地址、状态码和耗时。
> 同一只宝可梦查两次，第二次明显更快 —— 这就是 **缓存** 的效果！

### 6.3 CORS（跨域）

如果网页和 API **不在同一个 “源”**（协议 + 域名 + 端口 有一个不同），浏览器默认会 **拦截** 请求。

例如：用 VS Code 的 Live Server 打开 Day14 卡片（`http://127.0.0.1:5500`），去调用我们的 API（`http://127.0.0.1:8000`）→ 端口不同 → 跨域。

服务器需要明确说 “我允许”：

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 课堂演示用; 正式项目要写具体的域名
    allow_methods=["*"],
    allow_headers=["*"],
)
```

> CORS 是 **浏览器** 的安全规则。用 Python、curl 调用 API 不受影响。

### 🎯 课堂挑战（有时间就做）：改造 Day14

在 Day14 的 `script.js` 最后加上这段，让卡片的数据来自我们的 API：

```javascript
async function loadFromAPI(name) {
    const response = await fetch("http://127.0.0.1:8000/pokemon/" + name);
    const data = await response.json();

    pokemon.name = data.name;
    pokemon.number = data.id;
    pokemon.hp = data.stats.hp;
    pokemon.attack = data.stats.attack;
    pokemon.defense = data.stats.defense;
    pokemon.type = data.types.join(", ");
    pokemon.image = data.image;

    displayPokemon();
}

loadFromAPI("pikachu");
```

---

## 七、总结（3 分钟）

今天我们 **当了客人**（用 httpx 调用 PokeAPI），**开了餐厅**（用 FastAPI 提供自己的 API），还 **把前端卡片接了上来**。

### 知识地图

```text
API
├── HTTP 基础
│   ├── URL = 域名 + 路径 Path + 查询参数 Query
│   ├── 方法: GET 获取 / POST 创建 / PUT 修改 / DELETE 删除
│   ├── 状态码: 2xx 成功 / 4xx 客户端错 / 5xx 服务器错
│   └── JSON ↔ Python dict / list
├── 客户端（调用别人的 API）
│   ├── Python: httpx.get() → .status_code → .json()
│   ├── JavaScript: fetch() → .status → .json()
│   └── 错误处理: timeout、raise_for_status、try / except
└── 服务器（FastAPI）
    ├── @app.get / @app.post → 路由
    ├── 路径参数 / Query 参数 / 请求体（Pydantic 模型）
    ├── 类型提示 → 自动校验（422）+ 自动文档（/docs）
    ├── HTTPException → 返回错误状态码
    ├── async / await → 等网络时不阻塞
    └── CORS → 允许其他网页调用
```

### 常见错误排查

| 报错 | 原因 | 解决办法 |
| --- | --- | --- |
| `ModuleNotFoundError: No module named 'fastapi'` | 没进入虚拟环境，或没安装库 | `source .venv/bin/activate`，再 `pip install -r requirements.txt` |
| `Could not import module "main"` | 没在 `Day15` 文件夹里运行 | 先 `cd Day15` |
| `[Errno 48] ... address already in use` | 8000 端口被占用（另一个 uvicorn 还在运行） | 找到那个终端按 Ctrl + C，或者换端口 `--port 8001` |
| 422 Unprocessable Content | 参数类型或格式不对 | 看 `detail` 里的 `loc`（哪个参数）和 `msg`（为什么） |
| 503 Cannot reach PokeAPI | 断网，或 PokeAPI 暂时不可用 | 检查网络 |
| 卡片显示 `Cannot reach the API` | uvicorn 没有运行 | 运行 `uvicorn main:app --reload` |
| 浏览器控制台出现 CORS error | 跨域请求被拦截 | 确认 `main.py` 里有 `CORSMiddleware` |

---

## 八、课后作业

### ⭐ 基础

1. 在 `step2_hello_fastapi.py` 里加一个接口 `GET /multiply?a=3&b=4`，返回两个数的乘积。
2. 给 `main.py` 的 `Pokemon` 模型加一个字段 `shiny_image`（闪光版图片）。
   提示：`data["sprites"]["other"]["official-artwork"]["front_shiny"]`

### ⭐⭐ 进阶

3. 添加 `GET /teams/{trainer}`：查看某个训练家的队伍，找不到时返回 404。
4. 添加 `DELETE /teams/{trainer}`：解散队伍。（提示：`@app.delete(...)`、`del teams[trainer]`）

### ⭐⭐⭐ 挑战

5. **中文名！** 添加 `GET /pokemon/{name}/chinese`：
   - 调用 PokeAPI 的 `/pokemon-species/{name}`
   - 在 `names` 列表里找到 `language.name == "zh-hans"` 的那一项 → `皮卡丘`
   - 在 `flavor_text_entries` 里找到中文介绍
   - 返回 `{"name": "pikachu", "chinese_name": "皮卡丘", "description": "..."}`
6. 让卡片网页（`static/script.js`）同时显示中文名。

---

## 附录

### A. 常用命令速查

```bash
# 创建并进入虚拟环境
python3 -m venv .venv
source .venv/bin/activate              # Windows: .venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 运行
python step1_call_pokeapi.py
uvicorn step2_hello_fastapi:app --reload
uvicorn main:app --reload
uvicorn main:app --reload --port 8001  # 换个端口

# 用命令行测试 API
curl http://127.0.0.1:8000/pokemon/pikachu
curl -X POST http://127.0.0.1:8000/teams \
     -H "Content-Type: application/json" \
     -d '{"trainer": "Ash", "members": ["pikachu", "charmander"]}'
```

### B. 名词表（中英对照）

| English | 中文 | 一句话解释 |
| --- | --- | --- |
| API | 应用程序编程接口 | 程序之间对话的约定 |
| Client / Server | 客户端 / 服务器 | 发请求的一方 / 回应请求的一方 |
| Request / Response | 请求 / 响应 | 一问一答 |
| Endpoint | 接口 / 端点 | 一个具体的 “方法 + 路径”，如 `GET /pokemon` |
| HTTP Method | HTTP 方法 | GET、POST、PUT、DELETE |
| Status Code | 状态码 | 200、404、500…… |
| JSON | — | 最常用的数据交换格式 |
| Path / Query Parameter | 路径参数 / 查询参数 | `/pokemon/{name}` / `?limit=5` |
| Request Body | 请求体 | POST 时发送的 JSON 数据 |
| Header | 请求头 / 响应头 | 附加信息，如数据格式 |
| Schema / Model | 数据模型 | 规定数据长什么样 |
| Validation | 校验 | 检查数据格式是否正确 |
| async / await | 异步 / 等待 | 等网络时不阻塞程序 |
| Cache | 缓存 | 把结果存起来，下次直接用 |
| Middleware | 中间件 | 每个请求都会经过的处理层，如 CORS |
| CORS | 跨域资源共享 | 浏览器允许网页调用其它源的规则 |
| localhost / 127.0.0.1 | 本机 | 自己这台电脑 |
| Port | 端口 | 同一台电脑上不同服务的 “门牌号” |

### C. 扩展阅读

- FastAPI 官方教程（中文）：<https://fastapi.tiangolo.com/zh/>
- PokeAPI 文档：<https://pokeapi.co/docs/v2>
- httpx 文档：<https://www.python-httpx.org/>
- MDN：HTTP 概述（中文）：<https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Guides/Overview>
- HTTP 状态码猫猫图：<https://http.cat>
