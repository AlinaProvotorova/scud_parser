#scrud_parser

### Приложение, выполняющее экпорт данных из excel-файлов определенного формата в реляционную СУБД.

Данное приложение разработано для обработки Excel-файлов по Дисциплине труда сотрудников и экспорта из них информации в реляционную базу данных.

- Для начала работы нужно добавить username и password вашей бд в config.yaml
- Установить зависимости командой:
```commandline
pip install -r requirements.txt
```
- Перейти в папку src:
```commandline
cd src
```
Режимы работы парсера:
- Создать базу данных:
```commandline
python main.py execute_db
```
- Удалить базу данных:
```commandline
python main.py delete_db
```
- Импортировать данные из Excel(при этом передается путь к папке, содержащей exel файлы:
```commandline
python main.py import путь_до_папки          
```

## Стек технологий
- Python 3.10
- Pandas
- MySQL
- logging
- PyYAML

Автор: [Провоторова Алина Игоревна](https://t.me/alinamalina998)
