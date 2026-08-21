import io

class People:
    # 构造函数
    def __init__(self, name: str, age: int):
        self.name = name
        self._age = age
    
    @property
    def age(self) -> int:
        return self._age
    
    @age.setter
    def age(self, value: int):
        self._age = value 
    
    def talk(self):
        print(f"hello {self.name}")
        
class Student(People):
    def __init__(self, name: str, age: int, score: int):
        super().__init__(name, age)
        self._score = score
    
    @property
    def score(self) -> int:
        return self._score + 100
    
stu1 = Student("lucase", 19, 240)
stu1.age = 100
print(stu1.talk())
