from playwright.sync_api import sync_playwright
import pandas as pd

def run(playwright):
    browser = playwright.chromium.launch(headless=True)  # Запуск браузера в фоновом режиме
    page = browser.new_page()  # Открыть новую страницу
    page.goto("https://www.python.org/downloads/")  # Переход на страницу загрузок Python
    
    # Выбрать контейнеры каждого релиза
    releases = page.query_selector_all('.download-list-widget .list-row-container li')

    data = []  # Список для хранения данных обо всех релизах
    for release in releases:
        # Извлекаем версию Python из текста кнопки скачивания
        version = release.query_selector('span.release-number').text_content().strip()
        
        # Извлекаем дату релиза
        date = release.query_selector('.release-date').text_content().strip()
        
        # Ссылка на скачивание
        download_link = release.query_selector('a').get_attribute('href')

        # Ссылка на описание релиза
        details_link = release.query_selector('.release-enhancements > a').get_attribute('href')

        # Сохранение извлеченных данных в список
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
