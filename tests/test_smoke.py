import json
from http import HTTPStatus

import pytest
import requests
from app.models.User import UserData

def test_service_availability(base_url):
    response = requests.get(base_url)
    assert response.status_code in (HTTPStatus.OK, HTTPStatus.NOT_FOUND)

@pytest.fixture(scope="module")
def fill_test_data(base_url):
    with open("users.json") as f:
        test_data_users = json.load(f)
    api_users = []
    for user in test_data_users:
        response = requests.post(f"{base_url}/api/users/", json=user)
        api_users.append(response.json())

    user_ids = [user["id"] for user in api_users]

    yield user_ids

    for user_id in user_ids:
        requests.delete(f"{base_url}/api/users/{user_id}")


@pytest.fixture
def users(base_url):
    response = requests.get(f"{base_url}/api/users/")
    assert response.status_code == HTTPStatus.OK
    return response.json()


@pytest.mark.usefixtures("fill_test_data")
def test_users(base_url):
    response = requests.get(f"{base_url}/api/users/")
    assert response.status_code == HTTPStatus.OK

    user_list = response.json()
    for user in user_list:
        UserData.model_validate(user)


@pytest.mark.usefixtures("fill_test_data")
def test_users_no_duplicates(users):
    users_ids = [user["id"] for user in users]
    assert len(users_ids) == len(set(users_ids))


def test_user(base_url, fill_test_data):
    for user_id in (fill_test_data[0], fill_test_data[-1]):
        response = requests.get(f"{base_url}/api/users/{user_id}")
        assert response.status_code == HTTPStatus.OK
        user = response.json()
        UserData.model_validate(user)


@pytest.mark.parametrize("user_id", [13])
def test_user_nonexistent_values(base_url, user_id):
    response = requests.get(f"{base_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize("user_id", [-1, 0, "fafaf"])
def test_user_invalid_values(base_url, user_id):
    response = requests.get(f"{base_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY