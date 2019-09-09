#!/usr/bin/env python3
from models import Data, Course, Student, Class
import requests
import sys
from bs4 import BeautifulSoup


def debug(a):
    import IPython

    IPython.embed(using=False)
    exit()


def get_students(code, term, classno):
    r = s.get(
        "http://yjs.ustc.edu.cn/_script/show_student.asp",
        params={"code": code, "term": term, "classno": classno},
    )
    soup = BeautifulSoup(r.content, "html5lib")
    students = []
    for table in soup.find_all("table")[1::2]:
        for row in table.find_all("tr")[1:]:
            cols = row.find_all("td")
            sno, name = cols[1].text, cols[2].text
            if sno:
                students.append(Student(sno, name))
            sno, name = cols[7].text, cols[8].text
            if sno:
                students.append(Student(sno, name))
    return students


def get_courses(year, semester):
    print("Downloading course list")
    s.get("http://yjs.ustc.edu.cn/course/query.asp?mode=dept")
    r = s.post(
        "http://yjs.ustc.edu.cn/course/m_querybyname.asp",
        data="year1=" + year + "&term1=" + semester + "&querykc=_&submit=%B2%E9+%D1%AF",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    soup = BeautifulSoup(r.content, "html5lib")
    courses = []
    for row in soup.find_all("table")[3].find_all("tr")[1:]:
        cols = row.find_all("td")
        cno = cols[0].text
        name = cols[1].text
        teacher = cols[2].text
        week = cols[3].text
        selected = int(cols[5].text)
        list_params = (
            [cols[5].a["href"].split("'")[i] for i in (1, 3, 5)] if selected else None
        )
        limit = int(cols[6].text)
        classes = []
        for c in cols[4].text.split(";"):
            parts = c.rsplit(": ", 1)
            if len(parts) == 1:
                location, time = "", parts[0]
            else:
                location, time = parts
            classes.append(Class(location, time))
        courses.append(
            Course(
                cno, name, teacher, week, classes, selected, limit, None, list_params
            )
        )
    for i, course in enumerate(courses):
        print("[%s/%s] %s %s" % (i + 1, len(courses), course.cno, course.name))
        if course.selected:
            course.students = get_students(*course.list_params)
        else:
            course.students = []
    return courses


def download(year, semester):
    data = Data()
    data.all_courses = get_courses(year, semester)
    data.save()


if __name__ == "__main__":
    s = requests.session()
    if len(sys.argv) >= 3:
        download(sys.argv[1], sys.argv[2])
    else:
        print("Usage: ./download.py year semester")
        print('eg. "./download.py 2019 1" for 2019 Fall')
