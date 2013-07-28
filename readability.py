# coding=utf-8
import argparse
from core.extractor import ArticleExtractor
from core.filemanager import FileManager
from rules.new_line import NewLineRule
from rules.paragraph_count import ParagraphCountRule
from rules.sentence_count import SentenceCountRule


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
    parser.add_argument(
        '--update', dest='update', action='store_true',
        help=u'Принудительно перечитать HTML страницу и обновить данные'
    )
    parser.add_argument(
        '--path', dest='path',
        help=u'Путь для сохранения результатов работы программы'
    )

    args = parser.parse_args()
    file_manager = FileManager()
    if not file_manager.article_exists(args.url) or args.update:
        article = ArticleExtractor.extract_article(args.url)
        if not args.update:
            file_manager.add_article(args.url, article.get_text())
        else:
            file_manager.update_article(args.url, article.get_text())
    file_manager.unpack_article(args.url)

if __name__ == '__main__':
    ArticleExtractor.register_rule(ParagraphCountRule())
    ArticleExtractor.register_rule(SentenceCountRule())
    ArticleExtractor.register_rule(NewLineRule())
    main()
