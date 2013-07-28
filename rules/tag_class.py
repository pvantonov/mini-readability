# coding=utf-8
from core.rule import Rule


class TagClassRule(Rule):
    u"""
    Правило оценки, основанное CSS классе родительского блока.
    """

    @property
    def weight(self):
        return -4

    def estimate_paragraph(self, paragraph):
        u"""
        Если в классе родительского контейнера встречаются ключевые слова
        типа "article" это повышает вероятность того, что параграф относится к
        основной статье.
        """
        estimate = 0
        if 'class' in paragraph.parent.attrs:
            for class_ in paragraph.parent.attrs['class']:
                if 'story' in class_:
                    estimate += 2
                elif 'article' in class_:
                    estimate += 5
                else:
                    pass

        if 'class' in paragraph.attrs:
            for class_ in paragraph.attrs['class']:
                if 'disclaimer' in class_:
                    estimate -= 5
                else:
                    pass

        return estimate
