from consts import GDZ_ROOT
from url import Url


class Parser:
    @staticmethod
    def __pars_sol_img_from_num_url(nom_url: Url) -> str | list[Url]:
        import requests
        from bs4 import BeautifulSoup as BS

        # получает содержимое веб страницы номера на gdz.ru
        url = requests.get(nom_url)
        # достает html файл из содержимого
        html = BS(url.content, 'html.parser')

        # получает тег дива с картинками решения по селектору
        # html_tag = html.select("body > div.container.full-height > div.page-content > main > figure:nth-child(11) > div.task-img-container > div > img")
        
        # пытается достать теги картинок, если дива нет или он пустой возвращает пользователю сообщение о некорректном монере задания
        # try:
        #     img_url = html_tag[0]
        # except Exception:
        #     print(Exception)
        #     return "некорректный номер задания"

        # для хранения всех ссылок с картинками решений
        urls: list[Url] = []

        # перебирает все дивы, которые хранят картинки решения
        for div in html.find_all("div", attrs={'class': "with-overtask"}):
            # берет еднственный элемент дива - тег img
            img = div.find_all("img")[0]
            # добавляет ссылку на картинку с решением в список
            urls.append(Url("https:" + img.get('src')))

        # возврат ссылок на картинки с решением
        return urls

    @staticmethod
    def __get_link_on_sbook(subject_url: Url, sbook_author_name: str) -> str | Url:
        """парсит страницу со всеми учебниками определенного предемета, а потом возвращает ссылку на учебник, если он есть, иначе сообщение для пользователя"""

        # # заглушка
        # return Url("https://gdz.ru/class-8/algebra/kolyagin-tkacheva/")

        import requests
        from bs4 import BeautifulSoup as BS

        # получает страницу предмета
        url = requests.get(subject_url)
        # достает html файл из содержимого
        html = BS(url.content, 'html.parser')

        # хранит описания и ссылки на все учебники определенного предмета
        books_titles_n_hrefs: list[tuple[Url, str]] = []

        # достает все списки учебников и проходится по ним
        for book in html.find_all("a", attrs={'class': "book-regular"}):
            # добавляет в список название и ссылку на учебник
            books_titles_n_hrefs.append((book.get("title").lower(), Url("https://gdz.ru" + book.get("href"))))
        
        for book in books_titles_n_hrefs:
            # если в названии учебника есть имя автора, написанное в запросе, возвращает ссылку на учебник, в котором оно на писано
            if sbook_author_name in book[0]:
                # возвращает ссылку на учебник
                return book[1]
        
        # если имени автора нет ни в одном учебнике возвращает сообщение пользователю
        return f"нет учебника, у которого ПЕРВЫЙ автор на обложке - {sbook_author_name}"

    @staticmethod
    def __check_request_correctness(words: list[str]) -> str:
        """проверака корректности запроса пользователя"""

        # если в запросе есть русский язык или английский язык, просит поменять на "русский" или "английский" соответственно
        if ("русский" in words or "английский" in words) and "язык" in words:
            return "русский язык и ангийский язык надо писать без слова язык, то есть просто русский или ангийский"

        # проверяет запрос на длину. Если она меньше 4, возвращает сообщение для пользователя
        if len(words) != 4:
            return "запрос должен быть 4 или 6 слов в длину \n Например: 8 класс алгебра колягин номер 81 или 8 алгебра колягин 81"
        
        # проверяет является ли класс, введенный пользователем числом, и если да, то проверяет его вход в рамки от 1 до 11
        try:
            if not 1 <= int(words[0]) <= 11:
                return f"класс должен быть от 1 до 11. {words[0]} не подходит"
        except Exception:
            return f"класс должен быть числом. {words[0]} - не число"

        # проверяет является ли номер упражнения числом
        try:
            int(words[3])
        except ValueError:
            return f"номер упражнения должен быть числом. {words[3]} - не число"
        
        #проверяет название предмета
        if words[1] not in ["алгебра", "русский", "английский", "литература", "геометрия", "география", "математика",
                            "физика", "химия", "немецкий", "французский", "биология", "история", "информатика", "обж",
                            "общствознание", "черчение", "технология", "испанский", "изо"]:
            return "некорректное название предмета"
        
        # возвращает "ok" если запрос корректный
        return "ok"


    @staticmethod
    def make_url_from_words(words: list[str]) -> str | Url:
        """создает ссылку на картинку с решением задачи из писменного запроса"""
        # превращает запрос типа: 8 класс алгебра колягин номер 81 в запрос - 8 алгебра колягин 81
        if len(words) == 6:
            words.pop(-2)
            words.pop(1)
        
        #проверяет корректнойсть запроса
        if Parser.__check_request_correctness(words) != "ok":
            # если возвращает сообщение о некорректности запроса
            return Parser.__check_request_correctness(words)

        # создание ссылки, в которую постепенно будут добавляться элементы: 1. класс учебнка, 2. предмет, 3. название  учебника, 4. номер задачи
        url: Url = GDZ_ROOT
        # добавление класса учебника
        url = url + f"class-{words[0]}/"

        # словарь для замены названия предмета в его наименование на сайте gdz.ru
        name_to_gdzname = {"алгебра": "algebra/", "геометрия": "geometria/", "русский": "russkii_yazik/",
                           "английский": "english/", "литература": "literatura/", "география": "geografiya/",
                           "математика": "matematika/",
                           "физика": "fizika/", "химия": "himiya/", "немецкий": "nemeckiy_yazik/", "французский": "francuzskiy_yazik/",
                           "биология": "biologiya/",
                           "история": "istoriya/", "информатика": "informatika/", "обж": "obj/", "общствознание": "obshhestvoznanie/",
                           "черчение": "cherchenie/", "технология": "tekhnologiya/", "испанский": "spanish/", "изо": "iskusstvo/"}
        
        # добавление учебника
        url = Parser.__get_link_on_sbook(url, sbook_author_name=words[2])
        # если значение не ссылка на учебник, возвращает сообщение пользователю
        if type(url) != Url:
            return url

        # добавлнение номера задания
        url = url + f"{words[3]}-nom/"

        #вытаскивает список ссылок на картинки решения и возващает боту. Если ссылок нет, то возвращает пользователю сообщение
        return Parser.__pars_sol_img_from_num_url(url)
