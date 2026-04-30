import pytest
from src.core.exceptions import InstanceNotFound
from src.schemas.news import NewsCreate
from src.services.news import add_news, change_news_title, delete_news, get_news


def test_get_works(get_test_db):
    get_news("", get_test_db)


def test_get_invalid_channel(get_test_db):
    with pytest.raises(InstanceNotFound):
        get_news("non_existing_channel", get_test_db)


@pytest.mark.parametrize("get_test_users", ["get_test_db"], indirect=True)
def test_post_and_read(get_test_db, get_test_users):
    add_news(
        NewsCreate(channel="test", section="section", title="title", message="message"),
        get_test_users["admin"].id,
        get_test_db,
    )

    assert get_news("test", get_test_db)


@pytest.mark.parametrize("get_test_users", ["get_test_db"], indirect=True)
def test_update_title(get_test_db, get_test_users):
    add_news(
        NewsCreate(channel="test", section="section", title="title", message="message"),
        get_test_users["admin"].id,
        get_test_db,
    )

    news = get_news("test", get_test_db)[0]
    change_news_title(news.id, "test1", get_test_db)
    news_updated = get_news("test", get_test_db)[0]

    assert news_updated.title == "test1"


@pytest.mark.parametrize("get_test_users", ["get_test_db"], indirect=True)
def test_delete(get_test_db, get_test_users):
    add_news(
        NewsCreate(channel="test", section="section", title="title", message="message"),
        get_test_users["admin"].id,
        get_test_db,
    )

    news = get_news("test", get_test_db)
    assert news

    delete_news(news[0].id, get_test_db)

    news = get_news("test", get_test_db)
    assert not news
