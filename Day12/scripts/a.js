// console.log("aaa")

let firstName = "tom";
firstName = null;

const LIMIT_COUNT = 5.0; // float, double

let price = 232;

let isTrue = true; // false

let emptyWord = null;

// + - * / %

// > < >= <=, === (不用 ==）， ！==

// AND: && 
// OR: ||

// Python
// if price > 5:
//      print(">5")
// elif price < 10:
//      print("< 10")
// else:
//      print("hi")

if (price > 5 && price < 10) { // AND &&
    console.log(">5");
} else {
    console.log(">5");
}

if (price < 5 || price > 10) { // OR || 
    console.log("true");
} else {
    console.log("false");    
}

if (price !== 5) {

} else {

}

// for i in range(1, 6):
//      print(i)
//      if i === 3:
//          break

for (let i = 0; i < 6; i++) { // i += 1, i = i + 1
    console.log(i);

    if (i === 3) {
        break;
    }
}

// i = 0
// while i < 6:
//      print(i)
//      i +=1

let i = 0;
while (i < 6) {
    if (i === 3) {
        i++;
        continue;
    }
    console.log(i);
    i++;
}

// def printName(name: str):
//      print(name)

function printName(name) {
    return `hello ${name}`;

}

const greet = printName(500);
console.log(greet)

// Array

let students = ["Tom", "Lili", "Lucas"];

// count = len(students)
const count = students.length;
const lastItem = students[students.length - 1] 

// last item
// studends.append("New")
students.push("Lucy");
// students = students.pop();

// for student in students:
//      print(student)
for (const student of students) {
    console.log(student);
}