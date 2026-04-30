from playwright.sync_api import Page, expect


def test_happy_path(page: Page):
    page.goto("http://frontend:5173")
    # Better make admin login in dev also static as the password is
    login_button = page.get_by_placeholder("Логин")
    login_button.wait_for(state="visible", timeout=60000)
    login_button.fill("admin@delaba.ru")

    page.get_by_placeholder("Пароль").fill("password")
    page.get_by_title("Войти").click()

    expect(page.get_by_placeholder("Повторите пароль")).to_be_visible()

    page.get_by_placeholder("Новый пароль").fill("admin_password")
    page.get_by_placeholder("Повторите пароль").fill("admin_password")
    page.get_by_title("Войти").click()

    expect(page.get_by_label("Add Task")).to_be_visible()

    # And so on further kind of like
    # add_task_button.click()
    #
    # expect(page.get_by_label("Task Creation Dialog")).to_be_visible()
    # . . .
