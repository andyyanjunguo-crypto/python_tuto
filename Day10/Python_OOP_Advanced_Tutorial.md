# Python 面向对象编程（OOP）进阶与实战教程

面向对象编程（Object-Oriented Programming, OOP）是一种以**数据（属性）**和**行为（方法）**为核心的编程范式。在 Python 中，“一切皆对象”（包括数字、函数、类本身）。深入理解并熟练运用 Python 的 OOP 特性，是编写高质量、高可扩展性代码的关键。

---

## 一、 核心基础回顾与类架构

### 1.1 类的基本定义与实例化

类是对象的模板，对象是类的实例。

* **类属性（Class Attribute）**：被所有实例共享，位于类的作用域内、方法体之外。
* **实例属性（Instance Attribute）**：属于具体实例，通常在 `__init__` 中初始化。
* **`self` 的本质**：`self` 是对当前实例对象的引用。当调用 `obj.method()` 时，Python 会自动将 `obj` 作为第一个参数传递给 `self`。

```python
class BankAccount:
    # 类属性：银行名称（所有账户共享）
    bank_name: str = "Global Digital Bank"
    total_accounts: int = 0

    def __init__(self, account_holder: str, initial_balance: float = 0.0):
        # 实例属性：每个账户独立
        self.account_holder: str = account_holder
        self.__balance: float = initial_balance  # 私有属性
        
        # 更新类状态
        BankAccount.total_accounts += 1

    def deposit(self, amount: float) -> None:
        if amount > 0:
            self.__balance += amount
            print(f"[{self.account_holder}] 存入: ${amount:.2f} | 余额: ${self.__balance:.2f}")
        else:
            raise ValueError("存款金额必须大于零")

    def get_balance(self) -> float:
        return self.__balance
```

---

## 二、 OOP 四大核心特性深入解析

### 2.1 封装（Encapsulation）与 `@property`

封装旨在隐藏内部实现细节，仅对外暴露安全受控的接口。

#### Python 中的名称改编（Name Mangling）
Python 通过前缀下划线约束访问权限：
* `_attr`（单下划线）：**约定**上的受保护属性（Protected），提示外部不要直接修改，但机制上仍可访问。
* `__attr`（双下划线）：**私有属性（Private）**，触发名称改编机制，实际在内部重命名为 `_ClassName__attr`。

#### 使用 `@property` 实现优雅的 Getter/Setter

```python
class Temperature:
    def __init__(self, celsius: float = 0.0):
        self._celsius = celsius

    @property
    def celsius(self) -> float:
        '''Getter: 读取摄氏度'''
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        '''Setter: 校验并设置摄氏度'''
        if value < -273.15:
            raise ValueError("温度不能低于绝对零度 (-273.15°C)")
        self._celsius = value

    @property
    def fahrenheit(self) -> float:
        '''动态计算属性：华氏度'''
        return (self._celsius * 9/5) + 32

# 使用示例
temp = Temperature(25)
print(f"摄氏度: {temp.celsius}°C, 华氏度: {temp.fahrenheit}°F")
temp.celsius = 30  # 自动触发 @celsius.setter
```

---

### 2.2 继承（Inheritance）与 `super()`

继承允许子类复用父类的逻辑并进行扩展。使用 `super()` 可以安全地调用父类的方法，特别是父类的 `__init__` 初始化逻辑。

```python
class Vehicle:
    def __init__(self, brand: str, model: str):
        self.brand = brand
        self.model = model

    def get_specs(self) -> str:
        return f"{self.brand} {self.model}"

class ElectricCar(Vehicle):
    def __init__(self, brand: str, model: str, battery_capacity: int):
        # 显式调用父类构造函数
        super().__init__(brand, model)
        self.battery_capacity = battery_capacity  # kWh

    # 方法重写 (Override)
    def get_specs(self) -> str:
        base_specs = super().get_specs()
        return f"{base_specs} (纯电动, 电池容量: {self.battery_capacity}kWh)"

tesla = ElectricCar("Tesla", "Model 3", 75)
print(tesla.get_specs())
```

---

### 2.3 多态（Polymorphism）与鸭子类型（Duck Typing）

在 Python 中，多态不仅体现在继承树上，更核心的哲学是**鸭子类型（Duck Typing）**：“如果它走起来像鸭子，叫起来像鸭子，那它就是鸭子。” 

代码关心的是**对象具有什么能力（支持什么方法）**，而非对象的具体类型。

```python
class PDFExporter:
    def export(self, data: str) -> None:
        print(f"导出 PDF 报表: {data}")

class ExcelExporter:
    def export(self, data: str) -> None:
        print(f"导出 Excel 工作表: {data}")

class HTMLExporter:
    def export(self, data: str) -> None:
        print(f"生成 HTML 页面: {data}")

# 多态处理函数：无需关心具体 Exporter 类型，只要实现 export 接口即可
def generate_report(exporter, content: str):
    exporter.export(content)

generate_report(PDFExporter(), "月度财务数据")
generate_report(ExcelExporter(), "月度财务数据")
```

---

### 2.4 抽象类（Abstraction）与 `abc` 模块

当需要定义一套严格的子类规范、禁止直接实例化基类时，使用 `abc`（Abstract Base Classes）模块。

```python
from abc import ABC, abstractmethod

class PaymentGateway(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        '''抽象方法：必须在子类中实现'''
        pass

    @abstractmethod
    def refund(self, transaction_id: str) -> bool:
        pass

class StripePayment(PaymentGateway):
    def process_payment(self, amount: float) -> bool:
        print(f"通过 Stripe 支付 ${amount}")
        return True

    def refund(self, transaction_id: str) -> bool:
        print(f"通过 Stripe 针对交易 {transaction_id} 退款")
        return True

# gateway = PaymentGateway()  # 报错: TypeError (无法实例化抽象类)
stripe = StripePayment()
stripe.process_payment(99.9)
```

---

## 三、 方法分类：实例方法、类方法与静态方法

| 类型 | 装饰器 | 首个形参 | 使用场景 |
| :--- | :--- | :--- | :--- |
| **实例方法** | 无 | `self` | 操作实例状态、访问 `self.attr` |
| **类方法** | `@classmethod` | `cls` | 工厂模式（从不同数据源创建实例）、操作类状态 |
| **静态方法** | `@staticmethod` | 无 | 独立工具函数（逻辑关联但不需要访问实例/类状态）|

```python
class User:
    def __init__(self, username: str, email: str):
        self.username = username
        self.email = email

    # 1. 实例方法
    def send_email(self, message: str):
        print(f"发送至 {self.email}: {message}")

    # 2. 类方法：作为替代构造函数（Factory Method）
    @classmethod
    def from_dict(cls, data: dict):
        return cls(username=data["username"], email=data["email"])

    # 3. 静态方法：工具函数
    @staticmethod
    def is_valid_email(email: str) -> bool:
        return "@" in email and "." in email

# 使用类方法创建对象
user_data = {"username": "alex", "email": "alex@example.com"}
user = User.from_dict(user_data)

# 使用静态方法校验
print(User.is_valid_email("invalid-email"))  # False
```

---

## 四、 特殊方法（魔术方法 Magic Methods）

魔术方法以双下划线开头和结尾，允许自定义类的运算符重载和内置行为。

```python
class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    # 1. 对象的可读文本表示（用于开发者调试与 print）
    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y})"

    # 2. 运算符重载: +
    def __add__(self, other: "Vector") -> "Vector":
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self.x + other.x, self.y + other.y)

    # 3. 运算符重载: ==
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector):
            return False
        return self.x == other.x and self.y == other.y

    # 4. 向量模长 len()
    def __len__(self) -> int:
        return int((self.x ** 2 + self.y ** 2) ** 0.5)

v1 = Vector(3, 4)
v2 = Vector(1, 2)
v3 = v1 + v2  # 触发 __add__

print(v3)        # Vector(4.0, 6.0)
print(len(v1))   # 5
print(v1 == Vector(3, 4)) # True
```

---

## 五、 多重继承与 MRO（方法解析顺序）

Python 支持多重继承。当多个父类包含同名方法时，Python 使用 **C3 线性化算法** 计算 **MRO (Method Resolution Order)** 决定方法的调用顺序。

```python
class A:
    def process(self):
        print("A.process")

class B(A):
    def process(self):
        print("B.process")
        super().process()

class C(A):
    def process(self):
        print("C.process")
        super().process()

class D(B, C):
    def process(self):
        print("D.process")
        super().process()

d = D()
d.process()

# 查看 MRO 顺序
print("\nMRO 继承链:")
for cls in D.__mro__:
    print(cls.__name__)
```

**输出的 MRO 顺序：** `D -> B -> C -> A -> object`（菱形继承问题通过 MRO 得到了平滑解决）。

---

## 六、 现代高级特性：Data Class (`dataclasses`)

在 Python 3.7+ 中，若创建类主要是为了存储数据，推荐使用 `@dataclass`。它会自动生成 `__init__`、`__repr__`、`__eq__` 等方法，大幅简化代码。

```python
from dataclasses import dataclass, field
from typing import List

@dataclass
class Product:
    name: str
    price: float
    tags: List[str] = field(default_factory=list)

    def apply_discount(self, percent: float):
        self.price *= (1 - percent / 100)

p1 = Product(name="MacBook Pro", price=1999.0, tags=["Electronics", "Apple"])
p2 = Product(name="MacBook Pro", price=1999.0, tags=["Electronics", "Apple"])

print(p1)          # Product(name='MacBook Pro', price=1999.0, tags=['Electronics', 'Apple'])
print(p1 == p2)    # True (自动实现了属性值比较)
```

---

## 七、 面向对象设计原则（SOLID 简介）

1. **单一职责原则 (SRP)**：一个类应该只有一个引起它变化的原因。
2. **开闭原则 (OCP)**：对扩展开放，对修改关闭。
3. **里氏替换原则 (LSP)**：子类必须能够替换其基类。
4. **接口隔离原则 (ISP)**：不应强迫客户端依赖它们不使用的方法。
5. **依赖倒置原则 (DIP)**：高层模块不应依赖低层模块，二者都应依赖抽象。
