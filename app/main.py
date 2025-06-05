import dotenv

dotenv.load_dotenv()

from fastapi import FastAPI, HTTPException, Depends
from fastapi_pagination import Params
import json
from http import HTTPStatus
from fastapi.responses import Response
import uvicorn
from app.models.AppStatus import AppStatus

from routers import status, users
# from app.database import users_list, resources_list, users_with_page, create_db_and_tables
from database.engine import create_db_and_tables

from app.models.User import UserData, UserDataCreateBody, UserDataUpdateBody, UserDataCreateResponse, \
    UserDataUpdateResponse, ResponseModel, ResponseModelList, ResponseModelListResource, ResourceData
from fastapi_pagination import Page, paginate

app = FastAPI()
app.include_router(status.router)
app.include_router(users.router)

if __name__ == "__main__":
    create_db_and_tables()
    uvicorn.run(app, host="127.0.0.1", port=8002)



# users = {
#     2: {
#         "page": 2,
#         "per_page": 7,
#         "total": 13,
#         "total_pages": 2,
#         "data": [
#             {
#                 "id": 2,
#                 "email": "janet.weaver@reqres.in",
#                 "first_name": "Janet",
#                 "last_name": "Weaver",
#                 "avatar": "https://reqres.in/img/faces/2-image.jpg"
#             },
#             {
#                 "id": 7,
#                 "email": "michael.lawson@reqres.in",
#                 "first_name": "Michael",
#                 "last_name": "Lawson",
#                 "avatar": "https://reqres.in/img/faces/7-image.jpg"
#             },
#             {
#                 "id": 8,
#                 "email": "lindsay.ferguson@reqres.in",
#                 "first_name": "Lindsay",
#                 "last_name": "Ferguson",
#                 "avatar": "https://reqres.in/img/faces/8-image.jpg"
#             },
#             {
#                 "id": 9,
#                 "email": "tobias.funke@reqres.in",
#                 "first_name": "Tobias",
#                 "last_name": "Funke",
#                 "avatar": "https://reqres.in/img/faces/9-image.jpg"
#             },
#             {
#                 "id": 10,
#                 "email": "byron.fields@reqres.in",
#                 "first_name": "Byron",
#                 "last_name": "Fields",
#                 "avatar": "https://reqres.in/img/faces/10-image.jpg"
#             },
#             {
#                 "id": 11,
#                 "email": "george.edwards@reqres.in",
#                 "first_name": "George",
#                 "last_name": "Edwards",
#                 "avatar": "https://reqres.in/img/faces/11-image.jpg"
#             },
#             {
#                 "id": 12,
#                 "email": "rachel.howell@reqres.in",
#                 "first_name": "Rachel",
#                 "last_name": "Howell",
#                 "avatar": "https://reqres.in/img/faces/12-image.jpg"
#             }
#         ],
#         "support": {
#             "url": "https://contentcaddy.io?utm_source=reqres&utm_medium=json&utm_campaign=referral",
#             "text": "Tired of writing endless social media content? Let Content Caddy generate it for you."
#         }
#     }
# }


# @app.get("/api/users", response_model=ResponseModelList)
# def get_list_users(page: int = 2):
#     user_data = users.get(page)
#     if not user_data:
#         raise HTTPException(status_code=404, detail="Page not found")
#
#     return user_data
#
#
# @app.get("/api/users/{user_id}", response_model=ResponseModel)
# def get_single_user(user_id: int):
#     for page_data in users.values():
#         for user in page_data["data"]:
#             if user["id"] == user_id:
#                 return {"data": user,
#                         "support": page_data["support"]}
#
#     raise HTTPException(status_code=404, detail="User not found")


# @app.get("/api/unknown", response_model=ResponseModelListResource)
# def get_list_resource():
#     resources = {
#         1: {
#             "page": 1,
#             "per_page": 6,
#             "total": 12,
#             "total_pages": 2,
#             "data": [
#                 {
#                     "id": 1,
#                     "name": "cerulean",
#                     "year": 2000,
#                     "color": "#98B2D1",
#                     "pantone_value": "15-4020"
#                 },
#                 {
#                     "id": 2,
#                     "name": "fuchsia rose",
#                     "year": 2001,
#                     "color": "#C74375",
#                     "pantone_value": "17-2031"
#                 },
#                 {
#                     "id": 3,
#                     "name": "true red",
#                     "year": 2002,
#                     "color": "#BF1932",
#                     "pantone_value": "19-1664"
#                 },
#                 {
#                     "id": 4,
#                     "name": "aqua sky",
#                     "year": 2003,
#                     "color": "#7BC4C4",
#                     "pantone_value": "14-4811"
#                 },
#                 {
#                     "id": 5,
#                     "name": "tigerlily",
#                     "year": 2004,
#                     "color": "#E2583E",
#                     "pantone_value": "17-1456"
#                 },
#                 {
#                     "id": 6,
#                     "name": "blue turquoise",
#                     "year": 2005,
#                     "color": "#53B0AE",
#                     "pantone_value": "15-5217"
#                 }
#             ],
#             "support": {
#                 "url": "https://contentcaddy.io?utm_source=reqres&utm_medium=json&utm_campaign=referral",
#                 "text": "Tired of writing endless social media content? Let Content Caddy generate it for you."
#             }
#         }
#     }
#
#     resource_data = resources.get(1)
#     if not resource_data:
#         raise HTTPException(status_code=404, detail="Resource not found")
#
#     return {
#         "page": resource_data["page"],
#         "per_page": resource_data["per_page"],
#         "total": resource_data["total"],
#         "total_pages": resource_data["total_pages"],
#         "data": resource_data["data"],
#         "support": resource_data["support"],
#     }
#
#
# @app.post("/api/users", response_model=UserDataCreateResponse, status_code=201)
# def create_user(user: UserDataCreateBody):
#     if not user.name or not user.job:
#         raise HTTPException(status_code=400, detail="Name and job are required")
#
#     return {
#         "name": user.name,
#         "job": user.job,
#         "id": "409",
#         "createdAt": "2025-05-30T08:46:33.132Z"
#     }
#
#
# @app.put("/api/users/{user_id}", response_model=UserDataUpdateResponse)
# def update_user_put(user: UserDataUpdateBody):
#     return {
#         "name": user.name,
#         "job": user.job,
#         "updatedAt": "2025-05-30T09:58:46.242Z"
#     }
#
#
# @app.patch("/api/users/{user_id}", response_model=UserDataUpdateResponse)
# def update_user_patch(user: UserDataUpdateBody):
#     return {
#         "name": user.name,
#         "job": user.job,
#         "updatedAt": "2025-05-30T10:29:24.851Z"
#     }
#
#
# @app.delete("/api/users/{user_id}")
# def delete_user(user_id: int):
#     if user_id not in users:
#         raise HTTPException(status_code=404, detail="User not found")
#
#     return Response(status_code=204)


# @app.get("/status", status_code=HTTPStatus.OK)
# def status() -> AppStatus:
#     return AppStatus(users=bool(users))
#
#
# @app.get("/api/users/{user_id}", status_code=HTTPStatus.OK)
# def get_user(user_id: int) -> UserData:
#     if user_id < 1:
#         raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user id")
#     if user_id > len(users_list):
#         raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
#     return users_list[user_id - 1]
#
#
# @app.get("/api/users/", status_code=HTTPStatus.OK)
# def get_users() -> list[UserData]:
#     return users_list


# @app.get("/api/users", response_model=Page[UserData])
# def get_list_users_with_pagination(params: Params = Depends()):
#     return paginate(users_list, params)
#
#
# @app.get("/api/unknown", response_model=Page[ResourceData])
# def get_list_resources_with_pagination(params: Params = Depends()):
#     return paginate(resources_list, params)


# if __name__ == "__main__":
#     with open("../users.json") as f:
#         users_list.extend(json.load(f))
#
#     for user in users_list:
#         UserData.model_validate(user)
#
#     print("Users loaded")
#
#     uvicorn.run(app, host="127.0.0.1", port=8002)
#

if __name__ == "__main__":
    create_db_and_tables()
    uvicorn.run(app, host="127.0.0.1", port=8002)
