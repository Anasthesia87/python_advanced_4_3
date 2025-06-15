import math
from http import HTTPStatus

import pytest
import requests
from fastapi_pagination import paginate, Params
from pydantic import ValidationError

# from app.models.User import ResponseModelList, ResponseModel, ResponseModelListResource, UserDataCreateResponse, \
#     UserDataUpdateResponse, UserDataUpdateBody, UserData
from tests.conftest import base_url

@pytest.mark.parametrize("page,size", [
    (1, 5),
    (2, 5),
    (3, 5),
    (1, 1),
    (12, 1),
    (1, 12),
    (1, 15)
])
def test_api_list_users_pagination_basic_params(base_url: str, test_data_users: list, page: int, size: int):
    response = requests.get(f"{base_url}/api/users/?page={page}&size={size}")
    assert response.status_code == HTTPStatus.OK

    paginated_data = response.json()
    expected_items = (
        size if (page * size) <= paginated_data["total"] else paginated_data["total"] % size
    )

    assert paginated_data[
               "page"] == page, f"Номер страницы не совпадает. Ожидалось: {page}, получено: {paginated_data['page']}"
    assert paginated_data[
               "size"] == size, f"Размер страницы не совпадает. Ожидалось: {size}, получено: {paginated_data['size']}"
    assert "total" in paginated_data, "Отсутствует общее количество элементов (total)"
    assert "pages" in paginated_data, "Отсутствует общее количество страниц (pages)"

    expected_pages = math.ceil(paginated_data["total"] / size)
    assert paginated_data[
               "pages"] == expected_pages, f"Неверное количество страниц. Ожидалось: {expected_pages}, получено: {paginated_data['pages']}"

    assert len(paginated_data[
                   "items"]) == expected_items, f"Неверное количество элементов. Ожидалось: {expected_items}, получено: {len(paginated_data['items'])}"

    for item in paginated_data["items"]:
        try:
            UserData.model_validate(item)
        except ValidationError as e:
            pytest.fail(f"Невалидные данные пользователя: {e}")


@pytest.mark.parametrize("size", [1, 3, 6, 10, 12, 15])
def test_api_list_users_pagination_pages_count(base_url: str, test_data_users: list, size: int):
    response = requests.get(f"{base_url}/api/users/?size={size}")
    assert response.status_code == HTTPStatus.OK

    paginated_data = response.json()
    total_items = paginated_data["total"]
    expected_pages = math.ceil(total_items / size)

    assert paginated_data[
               "pages"] == expected_pages, f"Количество страниц: ожидается {expected_pages}, получено {paginated_data.pages}"


def test_api_list_users_pagination_different_pages(base_url: str, test_data_users: list):
    size = 6
    first_page = 1
    second_page = 2

    first_page_response = requests.get(f"{base_url}/api/users/?page={first_page}&size={size}")
    second_page_response = requests.get(f"{base_url}/api/users/?page={second_page}&size={size}")

    assert first_page_response.status_code == 200
    assert second_page_response.status_code == 200

    items_first_page = first_page_response.json()["items"]
    items_second_page = second_page_response.json()["items"]

    assert items_first_page != items_second_page

    ids_first_page = {item["id"] for item in items_first_page}
    ids_second_page = {item["id"] for item in items_second_page}
    intersection = ids_first_page & ids_second_page
    assert len(intersection) == 0, f"Обнаружены пересекающиеся ID: {intersection}"


def test_api_create_user(base_url):
    body = {
        "email": "valid@example.com",
        "first_name": "test_first_name",
        "last_name": "test_last_name",
        "avatar": "https://example.com/avatar.jpg"
    }
    create_response = requests.post(url=f"{base_url}/api/users", json=body)
    assert create_response.status_code == 201, f"Не удалось создать пользователя: {create_response.text}"
    new_user = create_response.json()
    values_equal = (all
                    (new_user[key] == body[key]
                     for key in new_user
                     if key in body))
    assert values_equal

    delete_response = requests.delete(f"{base_url}/api/users/{new_user['id']}")
    assert delete_response.status_code == 200, f"Не удалось удалить пользователя: {delete_response.text}"

def test_api_get_user_after_create_user(base_url):
    body = {
        "email": "valid@example.com",
        "first_name": "test_first_name",
        "last_name": "test_last_name",
        "avatar": "https://example.com/avatar.jpg"
    }
    create_response = requests.post(url=f"{base_url}/api/users", json=body)
    assert create_response.status_code == 201, f"Не удалось создать пользователя: {create_response.text}"
    new_user = create_response.json()
    response = requests.get(f"{base_url}/api/users/{new_user['id']}")

    user_from_api = response.json()
    values_equal = all(
        new_user[key] == user_from_api[key]
        for key in new_user
        if key in user_from_api)
    assert values_equal

    delete_response = requests.delete(f"{base_url}/api/users/{new_user['id']}")
    assert delete_response.status_code == 200, f"Не удалось удалить пользователя: {delete_response.text}"

def test_api_get_list_users_after_create_user(base_url, fill_test_data):
    body = {
        "email": "valid@example.com",
        "first_name": "test_first_name",
        "last_name": "test_last_name",
        "avatar": "https://example.com/avatar.jpg"
    }
    create_response = requests.post(url=f"{base_url}/api/users", json=body)
    assert create_response.status_code == 201, f"Не удалось создать пользователя: {create_response.text}"
    new_user = create_response.json()
    fill_test_data[new_user['id']] = new_user

    response = requests.get(f"{base_url}/api/users")
    users_list_from_api = response.json()['items']

    values_equal = all(
        fill_test_data[key] == users_list_from_api[key]
        for key in fill_test_data
        if key in users_list_from_api)
    assert values_equal
    assert len(users_list_from_api) == len(fill_test_data)





