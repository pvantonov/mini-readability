# coding=utf-8
import codecs
import hashlib
import os
from sqlalchemy import Column, Integer, LargeBinary, String, Text
from sqlalchemy.engine import create_engine
from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.schema import ForeignKey
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
    article = Column(Text)
    images = relationship("Image")

    def __init__(self, url, article):
        self.pk = self.make_pk(url)
        self.article = article

    @classmethod
    def make_pk(cls, url):
        u"""
        Сформировать первичный ключ по URL статьи.
        """
        return hashlib.md5(url).hexdigest()


class Image(Base):
    u"""
    Запись в БД, соответствующая рисунку к статье.
    """
    __tablename__ = 'image'

    pk = Column(Integer, primary_key=True)
    article = Column(String(32), ForeignKey('article.pk'))
    name = Column(String)
    image = Column(LargeBinary)

    def __init__(self, article_url, image, name):
        self.article = Article.make_pk(article_url)
        self.name = name
        self.image = image


class FileManagementError(Exception):
    def __init__(self, msg):
        self.msg = msg


def db_error_wrapper(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except DatabaseError:
            raise FileManagementError(
                msg=(u'Хранилище данных повреждено. Если ошибка будет '
                     u'повторяться - удалите вручную файл readability.sqlite')
            )
        else:
            return result
    return wrapper


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
        существует.
        """
        if path and not (os.path.exists(path) and os.path.isdir(path)):
            raise FileManagementError(
                msg=u'Указанный путь не существует или является путем к файлу.'
            )

        self.path = path or os.path.expanduser('~')
        self.bdpath = os.path.join(self.path, 'readability.sqlite')
        self.bdengine = create_engine('sqlite:///' + self.bdpath)
        Session.configure(bind=self.bdengine)
        self.session = Session()

        if not os.path.exists(self.bdpath):
            Base.metadata.create_all(self.bdengine)

    @db_error_wrapper
    def article_exists(self, url):
        u"""
        Проверить, хранится ли статья по указанному URL в базе данных.
        """
        pk = Article.make_pk(url)
        return self.session.query(exists().where(Article.pk == pk)).scalar()

    @db_error_wrapper
    def add_image(self, article_url, image, name):
        u"""
        Добавить картинку в БД.
        """
        self.session.add(Image(article_url, image, name))
        self.session.commit()

    @db_error_wrapper
    def add_article(self, url, text):
        u"""
        Добавить статью в БД.
        """
        self.session.add(Article(url, text))
        self.session.commit()

    @db_error_wrapper
    def update_article(self, url, text):
        u"""
        Обновить статью в БД.
        """
        article = self.session.query(Article).get(Article.make_pk(url))
        for image in article.images:
            self.session.delete(image)
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

    @db_error_wrapper
    def unpack_article(self, url):
        u"""
        Извлечь статью из БД и сохранить ее на диск.
        """
        article = self.session.query(Article).get(Article.make_pk(url))
        filename = os.path.join(self.path, self._construct_filename(url))
        with codecs.open(filename, mode="w", encoding="utf-8") as f:
            f.write(article.article)

    @db_error_wrapper
    def unpack_images(self, url):
        u"""
        Извлечь картинки из БД и сохранить их на диск.
        """
        article = self.session.query(Article).get(Article.make_pk(url))
        for image in article.images:
            filename = os.path.join(self.path, image.name)
            with open(filename, "wb") as f:
                f.write(image.image)
