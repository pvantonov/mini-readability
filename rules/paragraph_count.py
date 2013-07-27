# coding=utf-8
from core.rule import Rule


class ParagraphCountRule(Rule):
    u"""
    Правило оценки, основанное на количестве предложений в абзаце.
    """

    @property
    def weight(self):
        return 0

    def estimate_paragraph(self, paragraph):
        u"""
        Оценка основана на количестве параграфов, находящихся на том же
        уровне, что и текущий параграф. Для статей, как правило, на одном
        уровне находится два и более параграфов. Если параграф один, то
        есть вероятность, что это превью для какой-то другой статьи.
        """
        paragraphs = paragraph.parent.find_all('p')
        return -1 if len(paragraphs) == 1 else len(paragraphs)
