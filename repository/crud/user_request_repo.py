import typing

from sqlalchemy import desc, select

from repository.crud.base import BaseCRUDRepository
from repository.models.user_requests import UserRequests


class UserRequestsRepo(BaseCRUDRepository[UserRequests]):
    model = UserRequests

    async def find_last_5_records(self, **filter_by) -> typing.Sequence[UserRequests]:
        stmt = (
            select(self.model)
            .filter_by(**filter_by)
            .order_by(desc(self.model.created_at))
            .limit(5)
        )
        query = await self.async_session.execute(statement=stmt)
        result = query.scalars()

        return result.all()
