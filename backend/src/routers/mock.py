from fastapi import APIRouter, Response
from ..services.users import ban_user, make_moderator, unban_user, \
                             make_admin, make_default
from ..services.auth import set_tokens

from ..services.users import add_user, Permissions
from ..services.channels import create_channel
from ..services.tasks import add_document_task, add_todo_task, \
                             TodoTaskCreationRequest, \
                             DocumentTaskCreationRequest

from ..services.auth import TokenPayload

from ..models.channels import ChannelRequest
from ..models.news import NewsCreationRequest

from ..services.news import add_news

import time
import datetime

v1_router = APIRouter(prefix="/mock", tags=["mock"])


def mock_data():
    create_channel(ChannelRequest(channel="Университет 1 Группа 2"))
    create_channel(ChannelRequest(channel="Университет 2 Группа 3"))

    mock_user_data = add_user("mock1", "Тестовый пользователь",
                              "",
                              Permissions.VIEW_CHANNEL)
    test_user_data = add_user("mock", "Тестовый пользователь",
                              "Университет 1 Группа 2", 
                              Permissions.VIEW_CHANNEL)
    add_user("mock2", "Тестовый пользователь",
             "Университет 2 Группа 3", Permissions.VIEW_CHANNEL)

    add_todo_task(TodoTaskCreationRequest(
        subject="Высшая математика", title="Задачи на матрицы",
        channel="Университет 1 Группа 2",
        deadline=datetime.datetime(2024, 8, 8), subtasks=["Задача 5", "Задача 7"]
    ))

    add_todo_task(TodoTaskCreationRequest(
        subject="Высшая математика", title="Задачи на интегрирование",
        channel="Университет 2 Группа 3",
        deadline=datetime.datetime.now(), subtasks=["Задача 10"]
    ))

    add_todo_task(TodoTaskCreationRequest(
        subject="Высшая математика", title="Задачи на дифференцирование",
        channel="Университет 1 Группа 2",
        deadline=datetime.datetime.now(), subtasks=["Задача 1"]
    ))

    add_document_task(DocumentTaskCreationRequest(
        subject="Операционные системы",
        title="Лабораторная работа №12",
        channel="Университет 1 Группа 2",
        deadline=datetime.datetime.now()),
        file_hash="5d1fc818fe087e62cab755a27421073a"
    )

    add_news(NewsCreationRequest(section="Зачёты", channel="Университет 1 Группа 2", title="Дата зачёта", message="Зачёт 10 января"), 1)
    add_news(NewsCreationRequest(section="Экзамены", channel="Университет 2 Группа 3", title="Дата экзамена", message="Зачёт 10 января"), 1)
    add_news(NewsCreationRequest(section="Расписание", channel="Университет 2 Группа 3", title="Новое расписание", message="Пары по веб-разработке теперь по вторникам будут проходить"), 1)

    add_todo_task(TodoTaskCreationRequest(
        subject="Операционные системы", title="Задачи по командам",
        channel="Университет 1 Группа 2",
        deadline=datetime.datetime(2025, 12, 20), subtasks=["Задание 1", "Придумать задание 2"]
    ))

    add_document_task(DocumentTaskCreationRequest(
        subject="Операционные системы",
        title="Лабораторная работа №11",
        channel="Университет 1 Группа 2",
        deadline=datetime.datetime(2025, 12, 15)),
        file_hash="5293ef73cb2d0a3576c8eb99c0e464c6"
    )

    time.sleep(2)
    print(f"\t\t{test_user_data}")


@v1_router.post("/token", tags=["mock"])
async def mock_token(response: Response):
    set_tokens(TokenPayload(1), response)


@v1_router.post("/ban", tags=["mock"])
async def mock_ban():
    await ban_user(1)


@v1_router.post("/unban", tags=["mock"])
async def mock_unban():
    await unban_user(1)


@v1_router.post("/moderator", tags=["mock"])
async def mock_moderator():
    await make_moderator(1)


@v1_router.post("/viewer", tags=["mock"])
async def mock_viewer():
    await make_default(1)


@v1_router.post("/admin", tags=["mock"])
async def mock_admin():
    await make_admin(1)
