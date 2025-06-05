
# from app.models.User import UserData, ResourceData
#
# users_list: list[UserData] = []
# resources_list: list[ResourceData] = []
#
# users_with_page = {
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


import os
from os import getenv

from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlmodel import create_engine, SQLModel, text

engine = create_engine(os.getenv("DATABASE_ENGINE"),
                       pool_size=int(os.getenv("DATABASE_POOL_SIZE", 10)))


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def check_availability() -> bool:
    try:
        with Session(engine) as session:
            session.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print("Database not available")
        return False

