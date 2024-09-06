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
            'Release version': version,
            'Release date': date,
            'Download': "https://www.python.org" + download_link,
            'Release Notes': details_link
        })

    browser.close()  # Закрыть браузер
    try:
        df = pd.DataFrame.from_dict(data)
        df.to_excel('version_python.xlsx')
        print("Формирование файло завершено. Завершение программы")
    except Exception as e:
        print(f"Произошла ошибка при формировании итогового файла. Ошибка: {e}. \nЗавершение программы.")


def main():
    with sync_playwright() as playwright:
        run(playwright)


if __name__ == "__main__":
    print("Старт выполнения")
    main()
