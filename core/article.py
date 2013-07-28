# coding=utf-8
import os


class Article(object):
    u"""
    Основная статья HTML страницы.
    """

    def __init__(self):
        self.paragraphs = []
        self.images = []
        self.title = u''

    def _insert_line_breaks(self, text):
        u"""
        Вставить в текст символы переноса строки так, чтобы длина строки не
        превышала 80 символов.
        """
        text = text.split(' ')
        text_with_line_breaks = u''
        current_line_length = 0
        for item in text:
            if current_line_length + len(item) > 80:
                text_with_line_breaks += '%s%s ' % (os.linesep, item)
                current_line_length = len(item) + 1
            else:
                text_with_line_breaks += '%s ' % item
                current_line_length += len(item) + 1
        return text_with_line_breaks

    def set_title(self, title):
        u"""
        Установить заголовок статьи. При необходимости в заголовок
        вставляются символы переноса строки так, чтобы длина строки не
        превышала 80 символов.
        """
        self.title = self._insert_line_breaks(title)

    def add_paragraph(self, paragraph):
        u"""
        Добавить абзац к статье. При необходимости в абзац вставляются
        символы переноса строки так, чтобы длина строки не превышала 80
        символов.
        """
        self.paragraphs.append(self._insert_line_breaks(paragraph))

    def add_image(self, image):
        self.images.append(image)

    def get_text(self):
        u"""
        Получить текстовое представление статьи.
        """
        text = self.title
        for paragraph in self.paragraphs:
            text += os.linesep*2 + paragraph
        return text

