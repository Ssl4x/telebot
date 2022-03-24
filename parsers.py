from consts import GDZ_ROOT


class Parser:
    @staticmethod
    def __check_request_correctness(words: list[str]):
        # проверяет запрос на длину. Если она меньше 4, возвращает сообщение для пользователя
        if len(words) != 4:
            return ""

    @staticmethod
    def make_url_from_words(words: list[str]):
        # превращает запрос типа: 8 класс алгебра колягин номер 81 в запрос - 8 алгебра колягин 81
        if len(words) == 6:
            words.pop(-2)
            words.pop(1)
        
        if Parser.__check_request_correctness(words) != "ok":
            return Parser.__check_request_correctness(words)


        url: str = GDZ_ROOT
    
    