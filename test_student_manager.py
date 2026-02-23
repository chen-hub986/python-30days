from student_manager_v6 import StudentManager, Student
import pytest


@pytest.fixture
def students_manager():
    return StudentManager()


def test_average_empty_scores(tmp_path):
    student = Student(name="Empty", scores=[])
    assert student.average_score() == 0.0

def test_add_student(tmp_path, students_manager):
    student = students_manager.add_student("Alice", [90, 95, 85])
    assert student.name == "Alice"
    assert student.scores == [90, 95, 85]
    assert student.average_score() == 90.0

def test_delete_student(tmp_path, students_manager):
    students_manager.add_student("Bob", [80, 85, 90])
    deleted = students_manager.delete_student("Bob")
    assert deleted == True
    assert all(student.name != "Bob" for student in students_manager.students)

def test_modify_student(tmp_path, students_manager):
    students_manager.add_student("Charlie", [70, 75, 80])
    modified_student = students_manager.modify_student("Charlie", [85, 90, 95])
    assert modified_student is not None
    assert modified_student.scores == [85, 90, 95]
    assert modified_student.average_score() == 90.0

def test_get_avg_score(tmp_path, students_manager):    
    students_manager.add_student("David", [60, 65, 70])
    avg_score = students_manager.get_avg_score()
    assert avg_score["overall_average"] == (90.0 + 90.0 + 65.0) / 3
    assert avg_score["max_student"] == "Alice"
    assert avg_score["min_student"] == "David"

def test_get_ranking(tmp_path, students_manager):
    ranking = students_manager.get_ranking()
    assert ranking[0].name == "Alice"
    assert ranking[1].name == "Charlie"
    assert ranking[2].name == "David"