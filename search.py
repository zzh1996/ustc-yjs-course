#!/usr/bin/env python3
import sys
from models import Data


def search(keywords):
    for keyword in keywords:
        students = set()
        for course in data.all_courses:
            for student in course.students:
                if student.name == keyword or student.sno == keyword:
                    students.add(student)

        for s in students:
            print("----------", s.sno, s.name, "----------")
            print()
            for course in data.all_courses:
                for student in course.students:
                    if student == s:
                        print(
                            course.cno,
                            "%s/%s" % (course.selected, course.limit),
                            course.name,
                            course.teacher,
                            course.week,
                        )
                        for c in course.classes:
                            print(c.location, c.time)
                        print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 search.py [ Student NO. | Name ]")
        print("eg. python3 search.py SA18011001")
        print("eg. python3 search.py 张三")
    else:
        data = Data()
        data.load()
        search(sys.argv[1:])
