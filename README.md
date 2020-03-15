# Mini Readability
Mini Readability - это консольная утилита, написанная в качестве тестового задание для компании Тензор. Утилита предназначена для вычленения текста статьи с HTML-страницы новостного сайта. Текст статьи сохраняется локально в формате Plain Text. Изображения, относящиеся к статье, также сохраняются локально. И текст и изображения сохраняютсся как в виде локальных файлов, так и базе данных (SQLite). При повторном запросе статьи данные будут считаны из базы данных без обращения к новостному сайту.
### Аргументы командной строки
* **url** - URL-адрес статьи;
* **--update** - Принудительно перечить статью с сайта;
* **--path**=</local/path> - Путь к директории в которой будут сохраняться результаты работы утилиты;