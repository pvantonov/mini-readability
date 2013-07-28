# coding=utf-8
from core.rule import Rule


class LinkParagraphRule(Rule):
    u"""
    Правило оценки, основанное на количестве слов в подписи к ссылке.
    """

    @property
    def weight(self):
        return 0

    def estimate_paragraph(self, paragraph):
        u"""
        Как правило, подпись к ссылке состоит из 1-3 слов. Если абзац состоит
        из одной ссылки и подпись к этой ссылке длинная - то это сорее всего
        превью к другой статье.
        """
        paragraphs = paragraph.parent.find_all('p')
        link = paragraph.find('a')
        if link and link.text == paragraph.text:
            word_count = link.text.count(' ')
            return -3*word_count if word_count >= 5 else 0
        else:
            return 0
