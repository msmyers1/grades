from enum import Enum
from pathlib import Path
import pickle
from typing import Optional


class Difficulty(Enum):
    NORMAL = 1
    HONORS = 2
    AP = 3


class Grade:
    def __init__(self, score: float, difficulty: Difficulty):
        self.score = score
        self.difficulty = difficulty

    def adj_score(self) -> float:
        if self.difficulty == Difficulty.NORMAL:
            return self.score
        elif self.difficulty == Difficulty.HONORS:
            return self.score * 1.05
        elif self.difficulty == Difficulty.AP:
            return self.score * 1.10
        else:
            raise Exception("Invalid Difficulty")


class Course:
    def __init__(self, name: str, grade: Optional[Grade]):
        self.name = name
        self.grade = grade

    def adj_score(self) -> Optional[float]:
        if not self.grade:
            return None
        return self.grade.adj_score()

    def difficulty(self) -> Optional[Difficulty]:
        if not self.grade:
            return None
        return self.grade.difficulty

    def score(self) -> Optional[float]:
        if not self.grade:
            return None
        return self.grade.score


class Grades:
    def __init__(
        self,
        *,
        cs: Optional[Grade] = None,
        ela: Optional[Grade] = None,
        lote: Optional[Grade] = None,
        math: Optional[Grade] = None,
        science: Optional[Grade] = None,
        ss: Optional[Grade] = None,
        tech: Optional[Grade] = None,
    ):
        self.data = [
            Course("Computer Science", cs),
            Course("ELA", ela),
            Course("LOTE", lote),
            Course("Math", math),
            Course("Science", science),
            Course("Social Studies", ss),
            Course("Technology", tech),
        ]

    def gpa(self) -> Optional[float]:
        if not self.is_complete():
            return None
        count = 0
        total = 0
        for course in self.data:
            count = count + 1
            total = total + course.adj_score()
        return total / count

    def is_complete(self) -> bool:
        for course in self.data:
            if course.grade is None:
                return False
        return True

    def power_index(self) -> Optional[float]:
        if not self.is_complete():
            return None
        return self.gpa() + self.data[3].adj_score() + self.data[0].adj_score() + self.data[1].adj_score()

    def update(self, course_number: int, new_score: float, new_difficulty: Difficulty):
        if course_number < 0 or course_number >= len(self):
            raise Exception("Invalid course number")
        self.data[course_number].grade = Grade(new_score, new_difficulty)

    def __len__(self) -> int:
        return len(self.data)

    def __repr__(self) -> str:
        s = ""
        s = s + "# | course              | score | difficulty | adj. score\n"
        s = s + "----------------------------------------------------------\n"

        for (i, course) in enumerate(self.data):
            if course.grade is None:
                s = s + "{:<1} | {:<19}\n".format(i, course.name)
            else:
                s = s + "{:<1} | {:<19} | {:<5.1f} | {:<10} | {:.1f}\n".format(
                    i, course.name, course.grade.score, course.grade.difficulty.name, course.grade.adj_score()
                )
        s = s + "\n"

        gpa = self.gpa()
        if gpa:
            s = s + "GPA: {:.1f}\n".format(gpa)
        else:
            s = s + "GPA: N/A\n"

        power_index = self.power_index()
        if power_index:
            s = s + "Power Index: {:.1f}\n".format(power_index)
        else:
            s = s + "Power Index: N/A\n"

        return s


def mainloop(db_path: Path, grades: Grades):
    print("Here are your grades:\n")
    print(grades)
    while True:
        choice = input("Enter the number of the course you would like to update or 'q' to quit: ").strip().lower()
        if choice == "q" or choice == "quit" or choice == "exit":
            serialized = pickle.dumps(grades)
            with open(db_path, "wb") as f:
                f.write(serialized)
            return
        try:
            course_number = int(choice)
        except Exception:
            print("Invalid option")
            continue
        if course_number >= 0 and course_number < len(grades):
            break
        else:
            print("Invalid option")
            continue
    while True:
        choice = input("New score: ").strip()
        try:
            new_score = float(choice)
        except Exception:
            print("Invalid input")
            continue
        if new_score >= 0 and new_score <= 100:
            break
        else:
            print("Invalid input")
            continue
    while True:
        choice = input("New difficulty (1=Normal, 2=Honors, 3=AP): ").strip()
        try:
            new_difficulty = int(choice)
        except Exception:
            print("Invalid input")
            continue
        if new_difficulty >= 1 and new_difficulty <= 3:
            break
        else:
            print("Invalid input")
            continue
    print()
    grades.update(course_number, new_score, Difficulty(new_difficulty))
    mainloop(db_path, grades)


def main():
    db_path = Path("grades.db")

    if db_path.exists():
        with open(db_path, "rb") as f:
            contents = f.read()
            grades = pickle.loads(contents)
    else:
        grades = Grades()

    mainloop(db_path, grades)


if __name__ == "__main__":
    main()
