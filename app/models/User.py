from pydantic import BaseModel, EmailStr, HttpUrl


class UserData(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    avatar: HttpUrl


class UserDataCreateBody(BaseModel):
    name: str
    job: str


class UserDataUpdateBody(BaseModel):
    name: str
    job: str


class UserDataCreateResponse(BaseModel):
    name: str
    job: str
    id: str
    createdAt: str


class UserDataUpdateResponse(BaseModel):
    name: str
    job: str
    updatedAt: str


class ResourceData(BaseModel):
    id: int
    name: str
    year: int
    color: str
    pantone_value: str


class SupportData(BaseModel):
    url: str
    text: str


class ResponseModel(BaseModel):
    data: UserData
    support: SupportData


class ResponseModelList(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int
    data: list[UserData]
    support: SupportData


class ResponseModelListResource(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int
    data: list[ResourceData]
    support: SupportData
