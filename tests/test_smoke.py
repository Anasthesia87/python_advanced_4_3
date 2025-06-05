import pytest
import requests
from http import HTTPStatus

from app.main import users_list
from app.models.User import UserData, ResponseModel, ResourceData


def test_service_availability(base_url):
    response = requests.get(base_url)
    assert response.status_code in (HTTPStatus.OK, HTTPStatus.NOT_FOUND)


@pytest.fixture
def users(base_url):
    response = requests.get(f"{base_url}/api/users/")
    assert response.status_code == HTTPStatus.OK
    return response.json()


def test_get_users(base_url):
    response = requests.get(f"{base_url}/api/users/")
    assert response.status_code == HTTPStatus.OK
    assert isinstance(users_list, list)

    users = response.json()
    for user in users:
        UserData.model_validate(user)


def test_get_users_no_duplicates(users):
    users_ids = [user["id"] for user in users]
    assert len(users_ids) == len(set(users_ids))


@pytest.mark.parametrize("user_id", [2, 7, 12])
def test_get_user(base_url, user_id):
    response = requests.get(f"{base_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.OK

    user = response.json()
    ResponseModel.model_validate(user)


@pytest.mark.parametrize("user_id", [13])
def test_user_nonexistent_values(base_url, user_id):
    response = requests.get(f"{base_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize("user_id", ["fafaf", "123abc"])
def test_user_invalid_format(base_url, user_id):
    response = requests.get(f"{base_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.parametrize("user_id", [-1, 0])
def test_user_non_positive_id(base_url, user_id):
    response = requests.get(f"{base_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_get_resources(base_url):
    response = requests.get(f"{base_url}/api/unknown")
    assert response.status_code == HTTPStatus.OK
    resources = response.json()
    for resource in resources["data"]:
        ResourceData.model_validate(resource)
