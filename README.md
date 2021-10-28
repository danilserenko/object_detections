# object_detections
Тема нашего проекте: Поиск объектов на изображении. Классификация пользователей по их аккаунтам в Instagram

1) Для начала нам нужно скачать фотографии из аккаунта в Instagram. Для этого нам установить следующее:
скачать файл chromedriver.exe под вашу версию браузера, 
ввести логин и пароль от вашего аккаунта в auth_data.py в файл auth_data.py,
указать путь до файла chromedriver.exe в 19 строке self.browser = webdriver.Chrome("chromedriver.exe"),
После этого введите ссылку на аккаунт, из которого вы хотите скачать фото (аккаунт должен быть не приватным) в 174 строке my_bot.download_userpage_content("https://www.instagram.com/human_test_account/")
запустить файл bot.py.
Фото будут сохранены в папке с название аккаунта пользователя, откуда вы скачивали контент.


2) Создать на гугл диске папку с названием yolov3 и поместить туда images.zip, который вы можете скачать по ссылке https://drive.google.com/drive/folders/1q7b5txTzE6RKbfG1PnJ9AevoimK2CVRq?usp=sharing

3) Загрузить файл Train_YoloV3_ (1).ipynb в google collab и запустить его, подключившись к своему гугл диску.
После обучения в папке yolov3 появится файл с весами yolov3_training_last.weights. Поместите туда же файл yolov3_testing.cfg.

4) Загрузите файл shisha_detector.ipynb  в google collab и запустить его, подключившись к своему гугл диску и указав путь к фашему файлу с весами и yolov3_testing.cfg, 
а также путь к изображению, которое вы хотите протестировать и путь до уже обученной модели yolo.h5, которую вы также можете найти скачать по ссылке https://drive.google.com/drive/folders/1q7b5txTzE6RKbfG1PnJ9AevoimK2CVRq?usp=sharing. Во время выполнения скрипта загрузите фото, скачанные из аккаунта в Instagram.
Программа выдаст результат классификации пользователя.
