# coding=utf-8
from core.rule import Rule


class MailRule(Rule):

    @property
    def weight(self):
        return 0

    def estimate_paragraph(self, paragraph):
        u"""
        Если в тексте есть ссылка на e-mail то это вероятнее всего текст
        от блока обратной связи.
        """
        return -2 if paragraph.select('a[href*=mailto]') else 0
