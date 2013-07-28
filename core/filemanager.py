# coding=utf-8
import codecs
import hashlib
import os
from sqlalchemy import Column, String
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql import exists


Base = declarative_base()
Session = sessionmaker()


class Article(Base):
    u"""
    Запись в БД, соответствующая основной статье HTML страницы.
    В качестве ключа используется md5 URL адреса статьи.
    """
    __tablename__ = 'article'

    pk = Column(String(32), primary_key=True)
    article = Column(String)

    def __init__(self, url, article):
        self.pk = self.make_pk(url)
        self.article = article

    @classmethod
    def make_pk(cls, url):
        u"""
        Сформировать первичный ключ по URL статьи.
        """
        return hashlib.md5(url).hexdigest()


class FileManager(object):
    u"""
    Менеджер, управляющий хранением файлов на диске и в базе данных.
    """

    def __init__(self, path=None):
        u"""
        Инициализировать систему хранения файлов.
        Устанавливается привязка к каталогу в котором будут хранится данные.
        Это либо явно заданный каталог, либо домашняя директория пользователя.
        Происходит либо соединение с SQLite базой данных в указанном каталоге,
        если база существует, либо создается новая база, если базы не
        существует или она повреждена.
        """
        self.path = path or os.path.expanduser('~')
        self.bdpath = os.path.join(self.path, 'readability.sqlite')
        self.bdengine = create_engine('sqlite:///' + self.bdpath)
        Session.configure(bind=self.bdengine)
        self.session = Session()

        if not os.path.exists(self.bdpath):
            Base.metadata.create_all(self.bdengine)

    def article_exists(self, url):
        u"""
        Проверить, хранится ли статья по указанному URL в базе данных.
        """
        pk = Article.make_pk(url)
        return self.session.query(exists().where(Article.pk == pk)).scalar()

    def add_article(self, url, text):
        u"""
        Добавить статью в БД.
        """
        self.session.add(Article(url, text))
        self.session.commit()

    def update_article(self, url, text):
        u"""
        Обновить статью в БД.
        """
        article = self.session.query(Article).get(Article.make_pk(url))
        article.article = text
        self.session.commit()

    def _construct_filename(self, url):
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

    def unpack_article(self, url):
        u"""
        Извлечь статью из БД и сохранить ее на диск.
        """
        article = self.session.query(Article).get(Article.make_pk(url))
        filename = os.path.join(self.path, self._construct_filename(url))
        with codecs.open(filename, mode="w", encoding="utf-8") as f:
            f.write(article.article)
