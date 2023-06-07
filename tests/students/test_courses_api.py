import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from students.models import Course

@pytest.fixture
def api_client():
    return APIClient()


# проверка получения 1го курса
@pytest.mark.django_db
def test_get_course(api_client):
    course = baker.make('students.Course')

    response = api_client.get(f"/api/v1/courses/{course.id}/")

    assert response.status_code == 200
    assert response.data["id"] == course.id


# проверка получения списка курсов
@pytest.mark.django_db
def test_get_courses(api_client):
    courses = baker.make('students.Course', _quantity=5)

    response = api_client.get("/api/v1/courses/")

    assert response.status_code == 200
    assert len(response.data) == len(courses)


# проверка фильтрации списка курсов по id
@pytest.mark.django_db
def test_get_courses_by_id(api_client):
    course = baker.make('students.Course')

    response = api_client.get("/api/v1/courses/", {'id': course.id})

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["id"] == course.id

# проверка фильтрации списка курсов по name
@pytest.mark.django_db
def test_get_courses_by_name(api_client):
    course = baker.make('students.Course')

    response = api_client.get("/api/v1/courses/", {'name': course.name})

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["name"] == course.name


# тест успешного создания курса
@pytest.mark.django_db
def test_create_course(api_client):
    course_data = {"name": "test_Course",
                   "students": []}

    response = api_client.post("/api/v1/courses/", course_data, format='json')

    assert response.status_code == 201
    assert response.data["name"] == course_data["name"]


# тест успешного обновления курса
@pytest.mark.django_db
def test_update_course(api_client):
    course = baker.make('students.Course')

    new_course_data = {"name": "Update test_Course",
                       "students": []}

    response = api_client.put(f"/api/v1/courses/{course.id}/", new_course_data, format='json')

    assert response.status_code == 200
    assert response.data["name"] == new_course_data["name"]

# тест успешного удаления курса
@pytest.mark.django_db
def test_delete_course(api_client):
    course = baker.make('students.Course')

    response = api_client.delete(f"/api/v1/courses/{course.id}/")

    assert response.status_code == 204
    assert not Course.objects.filter(id=course.id).exists()


