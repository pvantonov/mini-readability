# coding=utf-8
import argparse
from core.extractor import ArticleExtractor
from rules.new_line import NewLineRule
from rules.paragraph_count import ParagraphCountRule
from rules.sentence_count import SentenceCountRule


def construct_filename(url):
    u"""
    Сформировать имя файла для сохранения результатов работы скрипта.
    Имя файла формируется из обрабатываемого скриптом url путем замены
    символов ':', '/', '?' и т.п. на '__' и добавления расширения '.txt'.
    """
    filename = url.replace(':', '__')
    filename = filename.replace('/', '__')
    filename = filename.replace('.', '__')
    filename = filename.replace('?', '__')
    filename += '.txt'
    return filename


def main():
    u"""
    Распарсить HTML страницу, выделить текст основной статьи и сохранить его.
    Точка входа в приложение. URL страницы и прочие настройки передаются в
    скрипт через аргументы командной строки.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'url', metavar='U', type=unicode, help=u'URL для обработки'
    )

    args = parser.parse_args()
    article = ArticleExtractor.extract_article(args.url)
    article.save(construct_filename(args.url))

if __name__ == '__main__':
    ArticleExtractor.register_rule(ParagraphCountRule())
    ArticleExtractor.register_rule(SentenceCountRule())
    ArticleExtractor.register_rule(NewLineRule())
    main()
