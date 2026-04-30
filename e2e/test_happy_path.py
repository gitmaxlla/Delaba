from playwright.sync_api import Page, expect


def test_smoke(page: Page):
    page.goto("http://frontend:5173")
    expect(page.locator("body")).to_be_visible()
