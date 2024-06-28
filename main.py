#    1. Спрашивать у пользователя первоначальный запрос.
#    2. Переходить по первоначальному запросу в Википедии.
#    3. Предлагать пользователю три варианта действий:
#        листать параграфы текущей статьи;
#        перейти на одну из связанных страниц — и снова выбор из двух пунктов:
#           - листать параграфы статьи;
#           - перейти на одну из внутренних статей.
#       выйти из программы.

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import time
# русская версия Википедии
default_url = "https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0"

# browser = webdriver.Chrome()
browser = webdriver.Firefox()
browser.get(default_url)
assert "Википедия" in browser.title

try:
    topic = input(" \n Что вы хотите узнать? : ")
    if topic != "" :
        # Находим окно поиска
        search_box = browser.find_element(By.ID, "searchInput")
        # Прописываем ввод текста в поисковую строку. В кавычках тот текст, который нужно ввести
        search_box.send_keys(topic)
        # Добавляем не только введение текста, но и его отправку
        search_box.send_keys(Keys.RETURN)
        time.sleep(5)
        a = browser.find_element(By.LINK_TEXT, topic)
        # Добавляем клик на элемент
        a.click()
except:
    print("Некорректный URL")

while True:
    try:
        user_choice = input("листать параграфы текущей статьи (1) \n"
                            "перейти на одну из связанных страниц (2) \n"
                            "выйти из программы (3) \n Введите число: ")
        # перебор по вариантам ответа пользователя
        if user_choice == "1":
            paragraphs = browser.find_elements(By.TAG_NAME, "p")
            # Для перебора пишем цикл
            for paragraph in paragraphs:
                print(paragraph.text)
                if input("нажмите Enter для продолжения или 3 для другого выбора") == "3": break
        elif user_choice == "2":
            hatnotes = []
            for element in browser.find_elements(By.TAG_NAME, "div"):
                # Чтобы искать атрибут класса
                cl = element.get_attribute("class")
                if cl == "hatnote navigation-not-searchable":
                    hatnotes.append(element)
            # Вдруг нет таких ссылок
            print(f"найдено {len(hatnotes)}")
            if len(hatnotes) != 0:
                for hatnote in hatnotes:
                # Для получения ссылки мы должны найти на сайте тег "a" внутри тега "div"
                    default_url = hatnote.find_element(By.TAG_NAME, "a").get_attribute("href")
                    # проверим что мы ещё на сайте https://ru.wikipedia.org/wiki/
                    if default_url.startswith("https://ru.wikipedia.org/wiki/"):
                        browser.get(default_url)
            else:
                print("нет таких ссылок")
        elif user_choice == "3":
            if input("выйти из программы [нет]?") == "да": break
        else:
            print("уточните выбор (1, 2 или 3)")
    except:
        print("уточните выбор")

print("спасибо за использование, программа завершена.")
browser.quit()
#Закрываем браузер