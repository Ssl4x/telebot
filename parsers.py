from consts import GDZ_ROOT


class Parser:
    @staticmethod
    def __check_request_correctness(words: list[str]):
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
        if words[1] not in ["алгебра", "русский", "английский", "литература", "геометрия", "география"]:
            return "некорректное название предмета"
        
        # возвращает "ok" если запрос корректный
        return "ok"


    @staticmethod
    def make_url_from_words(words: list[str]):
        # превращает запрос типа: 8 класс алгебра колягин номер 81 в запрос - 8 алгебра колягин 81
        if len(words) == 6:
            words.pop(-2)
            words.pop(1)
        
        if Parser.__check_request_correctness(words) != "ok":
            return Parser.__check_request_correctness(words)


        url: str = GDZ_ROOT
    
    