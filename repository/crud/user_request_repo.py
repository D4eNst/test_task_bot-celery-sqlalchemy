from repository.crud.base import BaseCRUDRepository
from repository.models.user_requests import UserRequests


class UserRequestsRepo(BaseCRUDRepository[UserRequests]):
    model = UserRequests

