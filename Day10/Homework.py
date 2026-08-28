class Student:
    def __init__(self, name, age, score):
        self.name = name
        self.age = age
        self.score = score


class StudentManager:
    def __init__(self):
        # The list now lives inside the manager instead of being a global.
        self.students = [
            Student("Tom", 20, 85),
            Student("Alice", 21, 92),
        ]

    def find_student(self, name):
        """Return the Student matching name (case-insensitive), or None if not found."""
        for student in self.students:
            if student.name.lower() == name.lower():
                return student
        return None

    def add_student(self):
        name = input("Enter student name: ").strip()
        if self.find_student(name):
            print(f"Error: a student named '{name}' already exists.")
            return
        try:
            age = int(input("Enter age: "))
            score = float(input("Enter score: "))
        except ValueError:
            print("Error: age must be a whole number and score must be a number.")
            return
        self.students.append(Student(name, age, score))
        print(f"Student '{name}' added successfully.")

    def remove_student(self):
        name = input("Enter the name of the student to remove: ").strip()
        student = self.find_student(name)
        if student is None:
            print("Error: student cannot be found.")
            return
        self.students.remove(student)
        print(f"Student '{name}' removed successfully.")

    def show_all_students(self):
        if not self.students:
            print("No students in the system.")
            return
        print("\nName - Age - Score")
        for student in self.students:
            print(f"{student.name} - {student.age} - {student.score}")
        print()

    def show_average_score(self):
        if not self.students:
            print("No students in the system.")
            return
        total = sum(student.score for student in self.students)
        average = total / len(self.students)
        print(f"Average score: {average:.2f}")

    def find_highest_score(self):
        if not self.students:
            print("No students in the system.")
            return
        top_student = self.students[0]
        for student in self.students:
            if student.score > top_student.score:
                top_student = student
        print(f"Highest score: {top_student.name} ({top_student.score})")


def show_menu():
    print("\n=== Student Management System ===")
    print("1. Add student")
    print("2. Remove student")
    print("3. Show all students")
    print("4. Show average score")
    print("5. Find highest score")
    print("6. Exit")


def main():
    manager = StudentManager()
    while True:
        show_menu()
        choice = input("Please choose an option (1-6): ").strip()
        if choice == "1":
            manager.add_student()
        elif choice == "2":
            manager.remove_student()
        elif choice == "3":
            manager.show_all_students()
        elif choice == "4":
            manager.show_average_score()
        elif choice == "5":
            manager.find_highest_score()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose a number between 1 and 6.")


if __name__ == "__main__":
    main()
    