# coding=utf-8
from bisect import insort
import urllib2
from urllib2 import HTTPError
from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag
from core.article import Article


class ExtractError(Exception):
    def __init__(self, msg):
        self.msg = msg


class ArticleExtractor(object):
    u"""
    Набор функций для парсинга URL и выделения из HTML страницы
    основной статьи.
    """

    rules = []

    @classmethod
    def register_rule(cls, rule):
        u"""
        Зарегистрировать правило оценки того, является ли текст частью
        основной статьи.
        """
        insort(cls.rules, rule)

    @classmethod
    def extract_article(cls, url):
        u"""
        Выделить из HTML страницы по указанному URL текст основной статьи.
        """
        try:
            data = urllib2.urlopen(url)
        except HTTPError as error:
            msg = (u'Невозможно прочитать содержимое по заданному URL адресу. '
                   u'Убедитесь, что URL адрес указан правильно и ваш '
                   u'компьютер подключен к сети Internet.\n'
                   u'Код ошибки: %s %s' % (error.code, error.msg))
            raise ExtractError(msg=msg)
        soup = BeautifulSoup(data.read())

        # Удаляем весь JavaScript из текста страницы.
        for script in soup.find_all('script'):
            script.extract()

        # Разные верстальщики по разному располагают заголовок статьи.
        # Кто-то в h1, кто-то в h2. Вообще, по-хорошему, должно быть в h1.
        # Как правило, заголовок статьи включен в заголовок страницы.
        # Пытаемся найти тег h1 или h2 текст которого включен в заголовок
        # страницы. Если находим - это и есть заголовок статьи. Если нет - в
        # лоб берем тег h1.
        article = Article()
        for header_tag in ['h1', 'h2']:
            title_is_found = False
            for header in soup.find_all(header_tag):
                if header.text.strip('\n') in soup.title.text:
                    article.title = header.text.strip('\n')
                    title_is_found = True
                    break
            if title_is_found:
                break
        else:
            article.title = soup.find('h1').text.strip('\n')

        # Перебираем все теги p. Если параграф оценивается как часть статьи -
        # он преобразуется в текст: все теги кроме a игнорируются, если тег
        # a имеет атрибут href - то адрес ссылки добавляется в текст, иначе
        # он игнорируется.
        for paragraph in soup.find_all('p'):
            if cls.is_article(paragraph):
                text = u''
                for item in list(paragraph.children):
                    if isinstance(item, NavigableString):
                        text += item
                    elif isinstance(item, Tag):
                        if item.name == 'a' and 'href' in item.attrs:
                            text += u'%s [%s]' % (
                                item.text,
                                item.attrs['href']
                            )
                        else:
                            text += item.text
                    else:
                        pass
                article.add_paragraph(text)

        return article

    @classmethod
    def is_article(cls, paragraph):
        u"""
        Параграф по очереди прогоняется через правила либо до тех пор пока
        правила не закончатся, либо до тех пор пока не будет точно понятно,
        является ли текст частью статьи или нет.
        """
        estimate = 0
        for rule in ArticleExtractor.rules:
            estimate += rule.estimate_paragraph(paragraph)
            if not (-300 <= estimate <= 300):
                break
        return True if estimate > 3 else False
