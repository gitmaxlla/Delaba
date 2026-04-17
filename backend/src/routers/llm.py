from fastapi import APIRouter
from src.internal.providers import get_llm_responder
from src.schemas.llm import LLMQuery
from src.services.auth import logged_in
from src.schemas.users import User
from src.services.llm import answer as answer_service
from fastapi import Depends
from src.services.tasks import get_tasks


v1_router = APIRouter(prefix="/ai", tags=["ai"])


@v1_router.get("/health")
def healthcheck(
    responder=Depends(get_llm_responder), _: User = Depends(logged_in)
) -> bool:
    return responder.healthcheck()


@v1_router.post("/")
def answer(
    query: LLMQuery,
    responder=Depends(get_llm_responder),
    user: User = Depends(logged_in),
):
    augmented_query = f"Ты - консультант приложения по планированию учебных задач. Ответь (кратко, 100-300 символов) на запрос пользователя, но только если он действительно связан с планированием учёбы и задачами приложения. Вот список задач: {str(get_tasks(user.channel))}. Запрос пользователя: {query.content}"
    print(get_tasks(user.channel))
    return answer_service(augmented_query, responder)
