from playwright.sync_api import sync_playwright
import pandas as pd

def run(playwright):
    browser = playwright.chromium.launch(headless=True)  # Запуск браузера в фоновом режиме
    page = browser.new_page()  # Открыть новую страницу
    page.goto("https://www.python.org/downloads/")
    
    # Выбираем контейнеры каждого релиза
    releases = page.query_selector_all('.download-list-widget .list-row-container li')

    data = []
    for release in releases:
        version = release.query_selector('span.release-number').text_content().strip()

        date = release.query_selector('.release-date').text_content().strip()

        download_link = release.query_selector('a').get_attribute('href')

        details_link = release.query_selector('.release-enhancements > a').get_attribute('href')

        data.append({
            'version': version,
            'release_date': date,
            'download_link': "https://www.python.org" + download_link,
            'details_link': details_link
        })

    browser.close()  # Закрыть браузер

    df = pd.DataFrame.from_dict(data)
    df.to_excel('version_python.xlsx')

with sync_playwright() as playwright:
    run(playwright)
