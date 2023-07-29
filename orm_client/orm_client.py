import uuid
from typing import Any

import allure
import structlog
from sqlalchemy import create_engine


def allure_attach(fn):
    def wrapper(*args, **kwargs):
        query = kwargs.get("query")
        allure.attach(
            str(query.compile(compile_kwargs={"literal_binds": True})),
            name="query",
            attachment_type=allure.attachment_type.TEXT,
        )

        dataset = fn(*args, **kwargs)

        if dataset:
            allure.attach(
                str(dataset),
                name="dataset",
                attachment_type=allure.attachment_type.TEXT,
            )
        return dataset

    return wrapper


class OrmClient:
    def __init__(
            self,
            user: str,
            password: str,
            host: str,
            database: str,
            isolation_level: str = "AUTOCOMMIT"
    ) -> None:
        connection_string = f"postgresql://{user}:{password}@{host}/{database}"
        print(connection_string)
        self.engine = create_engine(connection_string, isolation_level=isolation_level)
        self.db = self.engine.connect()
        self.log = structlog.get_logger(self.__class__.__name__).bind(service="db")

    def close_connection(self) -> None:
        with allure.step("Закрытие соединения с базой данных"):
            self.db.close()

    @allure_attach
    def send_query(self, query: Any) -> list[Any]:
        print(query)
        log = self.log.bind(event_id=str(uuid.uuid4()))
        log.msg(
            event="request",
            query=str(query),
        )
        dataset = self.db.execute(statement=query)
        result = [row for row in dataset]
        log.msg(
            event="response",
            dataset=[dict(row) for row in result],
        )
        return result

    @allure_attach
    def send_bulk_query(self, query: Any) -> None:
        print(query)
        log = self.log.bind(event_id=str(uuid.uuid4()))
        log.msg(
            event="request",
            query=str(query),
        )
        self.db.execute(statement=query)
