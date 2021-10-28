from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from auth_data import username, password
import time
import random
from selenium.common.exceptions import NoSuchElementException
import requests
import os
import pickle


class InstagramBot:


    def __init__(self, username, password):

        self.username = username
        self.password = password
        self.browser = webdriver.Chrome("chromedriver.exe")

    # метод для закрытия браузера
    def close_browser(self):

        self.browser.close()
        self.browser.quit()

    # метод логина
    def login(self):

        if os.path.exists(f"{username}_cookies"):
            self.load_cookies()
            return

        browser = self.browser
        browser.get('https://www.instagram.com')
        time.sleep(random.randrange(3, 5))

        username_input = browser.find_element_by_name('username')
        username_input.clear()
        username_input.send_keys(username)

        time.sleep(2)

        password_input = browser.find_element_by_name('password')
        password_input.clear()
        password_input.send_keys(password)

        password_input.send_keys(Keys.ENTER)
        time.sleep(6)

        pickle.dump(browser.get_cookies(), open(f"{username}_cookies", "wb"))

    def load_cookies(self):
        browser = self.browser

        browser.get("https://www.instagram.com/")
        time.sleep(3)

        for cookie in pickle.load(open(f"{username}_cookies", "rb")):
            browser.add_cookie(cookie)

        time.sleep(2)
        browser.refresh()
        print(f"Бот успешно зашёл за пользователя {username}\n")
        time.sleep(5)


    # метод проверяет по xpath существует ли элемент на странице
    def xpath_exists(self, url):

        browser = self.browser
        try:
            browser.find_element_by_xpath(url)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist


    # метод собирает ссылки на все посты пользователя
    def get_all_posts_urls(self, userpage):

        browser = self.browser
        browser.get(userpage)
        time.sleep(4)


        posts_count = int(browser.find_element_by_xpath(
            "/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span").text)
        loops_count = int(posts_count / 12)
        print(loops_count)

        posts_urls = [] # ссылки на посты
        for i in range(0, loops_count):
            hrefs = browser.find_elements_by_tag_name('a') # адрес документа, на который указывает ссылка
            hrefs = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]

            for href in hrefs:
                posts_urls.append(href)

            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.randrange(2, 4))
            print(f"Итерация #{i}")

        file_name = userpage.split("/")[-2]

        with open(f'{file_name}.txt', 'a') as file:
            for post_url in posts_urls:
                file.write(post_url + "\n")

        set_posts_urls = set(posts_urls)
        set_posts_urls = list(set_posts_urls)

        with open(f'{file_name}_set.txt', 'a') as file:
            for post_url in set_posts_urls:
                file.write(post_url + '\n')


    # метод скачивает контент со страницы пользователя
    def download_userpage_content(self, userpage):

        browser = self.browser
        self.get_all_posts_urls(userpage)
        file_name = userpage.split("/")[-2]
        time.sleep(4)
        browser.get(userpage)
        time.sleep(4)

        # создаём папку с именем пользователя
        if os.path.exists(f"{file_name}"):
            print("Папка уже существует!")
        else:
            os.mkdir(file_name)

        img_src_urls = []
        with open(f'{file_name}_set.txt') as file:
            urls_list = file.readlines()

            # for post_url in urls_list[0:5]:
            for post_url in urls_list:
                try:
                    browser.get(post_url)
                    time.sleep(4)

                    img_src = "/html/body/div[1]/section/main/div/div[1]/article/div/div[1]/div/div/div[1]/img"
                    post_id = post_url.split("/")[-2]

                    if self.xpath_exists(img_src):
                        img_src_url = browser.find_element_by_xpath(img_src).get_attribute("src")
                        img_src_urls.append(img_src_url)

                        # сохраняем изображение
                        get_img = requests.get(img_src_url)
                        with open(f"{file_name}/{file_name}_{post_id}_img.jpg", "wb") as img_file:
                            img_file.write(get_img.content)
                            print(f"Контент из поста {post_url} успешно скачан!")
                    else:
                        print("Упс! Что-то пошло не так! Скорее всего это видео, а не фото.")
                        img_src_urls.append(f"{post_url}, нет ссылки!")

                except Exception as ex:
                    print(ex)
                    self.close_browser()

            self.close_browser()

        with open(f'{file_name}/{file_name}_img_src_urls.txt', 'a') as file:
            for i in img_src_urls:
                file.write(i + "\n")


my_bot = InstagramBot(username, password)
my_bot.login()
my_bot.download_userpage_content("https://www.instagram.com/human_test_account/")


