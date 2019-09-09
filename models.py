from collections import namedtuple
import pickle

file_name = "data.pickle"

Class = namedtuple("Class", ["location", "time"])


class Data:
    def __init__(self):
        self.all_courses = []

    def save(self):
        with open(file_name, "wb") as f:
            pickle.dump(self.all_courses, f)

    def load(self):
        with open(file_name, "rb") as f:
            self.all_courses = pickle.load(f)


class Course:
    def __init__(
        self, cno, name, teacher, week, classes, selected, limit, students, list_params
    ):
        self.cno = cno
        self.name = name
        self.teacher = teacher
        self.week = week
        self.classes = classes
        self.selected = selected
        self.limit = limit
        self.students = students
        self.list_params = list_params

    def __repr__(self):
        return "Course(%s, %s, %s, %s, %s, %s, %s, %s)" % (
            repr(self.cno),
            repr(self.name),
            repr(self.teacher),
            repr(self.week),
            repr(self.classes),
            repr(self.selected),
            repr(self.limit),
            repr(self.students),
        )


class Student:
    def __init__(self, sno, name):
        self.sno = sno
        self.name = name

    def __repr__(self):
        return "Student(%s, %s)" % (repr(self.sno), repr(self.name))

    def __eq__(self, other):
        return self.sno == other.sno

    def __hash__(self):
        return hash((self.sno, self.name))
