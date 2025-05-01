# Файл с константами

# Минимальная допустимая длина пароля
MIN_LEN_PASSWORD = 4

# Время жизни jwt токена
JWT_LIFETIME = 3600

# Константа с форматом представления времени
FORMAT = "%Y/%m/%d %H:%M:%S"

# Константа с адресом для получения прав доступа
GOOGLE_AUTH_URL = "https://www.googleapis.com/auth/"

# Свойства документа
SPREADSHEET_BODY = {
    'properties': {'title': 'Отчёт', 'locale': 'ru_RU'},
    'sheets': [{'properties': {
        'sheetType': 'GRID',
        'sheetId': 0,
        'title': 'Лист1',
        'gridProperties': {'rowCount': 100, 'columnCount': 11}}}]
}

# Постоянная часть ссылки на созданный документ
SPREADSHEET_URL = 'https://docs.google.com/spreadsheets/d/'