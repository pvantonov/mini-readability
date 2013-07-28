# coding=utf-8
from core.rule import Rule


class SentenceCountRule(Rule):
    u"""
    Правило оценки, основанное на количестве предложений в абзаце.
    """

    @property
    def weight(self):
        return -1

    def estimate_paragraph(self, paragraph):
        u"""
        В осмысленном тексте должно быть хотя бы одно законченное предложение
        с '.', '?', или '!' в конце. Чем больше предложений - тем больше
        вероятность того, что абзац принадлежит тексту основной статьи.
        Правило является оптимистичным. Т.к. четкое определение конца
        предложения требует больших вычислительных затрат и достаточно сложно
        с алгоритмической точки зрения, в данном правиле просто подсчитывается
        общее число символов, которые могут быть символом конца предложения в
        независимости от того, где в предложении находятся данные знаки.
        """
        text = paragraph.text.strip()
        sentence_count = text.count('. ')
        sentence_count += text.count('! ')
        sentence_count += text.count('? ')
        sentence_count += text.count('."')
        sentence_count += text.count('!"')
        sentence_count += text.count('?"')
        if text.endswith('.') or text.endswith('."'):
            sentence_count += 1
        elif text.endswith('?') or text.endswith('?"'):
            sentence_count += 1
        elif text.endswith('!') or text.endswith('!"'):
            sentence_count += 1
        return -500 if not sentence_count else sentence_count
