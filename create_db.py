import sqlite3

def create_database():
    # Подключаемся (файл БД будет создан автоматически)
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()

    # Включаем поддержку внешних ключей (SQLite включает по умолчанию, но на всякий случай)
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Удаляем старые таблицы, если есть (чистое создание)
    cursor.execute("DROP TABLE IF EXISTS SostavZakaza")
    cursor.execute("DROP TABLE IF EXISTS Zakaz")
    cursor.execute("DROP TABLE IF EXISTS Sklad")
    cursor.execute("DROP TABLE IF EXISTS SostavPostavki")
    cursor.execute("DROP TABLE IF EXISTS Postavka")
    cursor.execute("DROP TABLE IF EXISTS Postavshik")
    cursor.execute("DROP TABLE IF EXISTS Menu")
    cursor.execute("DROP TABLE IF EXISTS Category")
    cursor.execute("DROP TABLE IF EXISTS Staff")
    cursor.execute("DROP TABLE IF EXISTS Dolzhnost")
    cursor.execute("DROP TABLE IF EXISTS Client")
    cursor.execute("DROP TABLE IF EXISTS Ingredients")

    # Создаём таблицы (упрощённые, но с нужными столбцами)
    cursor.execute('''
        CREATE TABLE Dolzhnost (
            idDolzhnost INTEGER PRIMARY KEY,
            Dolzhnost_name TEXT NOT NULL,
            Oklad INTEGER,
            Obyazannost TEXT,
            Grafik TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE Category (
            idCategory INTEGER PRIMARY KEY,
            Category_name TEXT NOT NULL,
            Poryadok_otobrazhenia INTEGER,
            Activnost INTEGER,
            Category_photo TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE Ingredients (
            idIngredients INTEGER PRIMARY KEY,
            Ingredient_name TEXT NOT NULL,
            Edinitsa_Izmerenia TEXT,
            Cost_for_Edinitsa REAL,
            Min_ostatok REAL
        )
    ''')

    cursor.execute('''
        CREATE TABLE Postavshik (
            idPostavshika INTEGER PRIMARY KEY,
            Company_name TEXT,
            phone TEXT,
            adres TEXT,
            YsloviaOplatv TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE Staff (
            Staff_id INTEGER PRIMARY KEY,
            FIO TEXT NOT NULL,
            idDolzhnost INTEGER,
            Salary INTEGER,
            DataPrioma TEXT,
            FOREIGN KEY (idDolzhnost) REFERENCES Dolzhnost(idDolzhnost)
        )
    ''')

    cursor.execute('''
        CREATE TABLE Client (
            idClient INTEGER PRIMARY KEY,
            FIO TEXT,
            Phone TEXT,
            Email TEXT,
            Kolitchestvo_poseshenii INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE Menu (
            idBluda INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            cost INTEGER,
            Weight INTEGER,
            idCategory INTEGER,
            FOREIGN KEY (idCategory) REFERENCES Category(idCategory)
        )
    ''')

    cursor.execute('''
        CREATE TABLE Postavka (
            idPostavki INTEGER PRIMARY KEY,
            idPostavshika INTEGER,
            DateOfPostavka TEXT,
            ObshyaiiaSumma INTEGER,
            idSotrudnika INTEGER,
            FOREIGN KEY (idPostavshika) REFERENCES Postavshik(idPostavshika),
            FOREIGN KEY (idSotrudnika) REFERENCES Staff(Staff_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE SostavPostavki (
            idPozicii INTEGER PRIMARY KEY,
            idPostavki INTEGER,
            idIngredient INTEGER,
            Kolichestvo INTEGER,
            Cost_for_edinitsa INTEGER,
            FOREIGN KEY (idPostavki) REFERENCES Postavka(idPostavki),
            FOREIGN KEY (idIngredient) REFERENCES Ingredients(idIngredients)
        )
    ''')

    cursor.execute('''
        CREATE TABLE Zakaz (
            idZakaz INTEGER PRIMARY KEY,
            table_number INTEGER,
            data_and_time TEXT,
            idSotrudnika INTEGER,
            idClient INTEGER,
            Status TEXT,
            FOREIGN KEY (idSotrudnika) REFERENCES Staff(Staff_id),
            FOREIGN KEY (idClient) REFERENCES Client(idClient)
        )
    ''')

    cursor.execute('''
        CREATE TABLE SostavZakaza (
            idPozitsii INTEGER PRIMARY KEY,
            idZakaza INTEGER,
            idBluda INTEGER,
            Kolitchestvo INTEGER,
            Cost INTEGER,
            FOREIGN KEY (idZakaza) REFERENCES Zakaz(idZakaz),
            FOREIGN KEY (idBluda) REFERENCES Menu(idBluda)
        )
    ''')

    cursor.execute('''
        CREATE TABLE Sklad (
            idZapisi INTEGER PRIMARY KEY,
            idIngredient INTEGER,
            Kolitchestvo_na_sklade INTEGER,
            Data_obnovlenia TEXT,
            idOtvetstvennogo INTEGER,
            FOREIGN KEY (idIngredient) REFERENCES Ingredients(idIngredients),
            FOREIGN KEY (idOtvetstvennogo) REFERENCES Staff(Staff_id)
        )
    ''')

    # Заполним справочники минимальными данными (чтобы было с чем работать)
    cursor.execute("INSERT OR IGNORE INTO Dolzhnost (idDolzhnost, Dolzhnost_name) VALUES (1, 'Повар'), (2, 'Официант')")
    cursor.execute("INSERT OR IGNORE INTO Category (idCategory, Category_name) VALUES (1, 'Салаты'), (2, 'Горячее')")
    cursor.execute("INSERT OR IGNORE INTO Ingredients (idIngredients, Ingredient_name) VALUES (1, 'Картофель'), (2, 'Мясо')")
    cursor.execute("INSERT OR IGNORE INTO Staff (Staff_id, FIO, idDolzhnost) VALUES (1, 'Иванов Иван', 1), (2, 'Петрова Мария', 2)")
    cursor.execute("INSERT OR IGNORE INTO Client (idClient, FIO) VALUES (1, 'Андреев Андрей'), (2, 'Борисова Борислава')")
    cursor.execute("INSERT OR IGNORE INTO Menu (idBluda, name, cost, Weight, idCategory) VALUES (1, 'Цезарь', 350, 250, 1), (2, 'Стейк', 650, 300, 2)")
    cursor.execute("INSERT OR IGNORE INTO Zakaz (idZakaz, table_number, data_and_time, idSotrudnika, idClient, Status) VALUES (1, 1, datetime('now'), 1, 1, 'Завершен')")
    cursor.execute("INSERT OR IGNORE INTO SostavZakaza (idPozitsii, idZakaza, idBluda, Kolitchestvo, Cost) VALUES (1, 1, 1, 2, 350)")
    cursor.execute("INSERT OR IGNORE INTO Sklad (idZapisi, idIngredient, Kolitchestvo_na_sklade) VALUES (1, 1, 100), (2, 2, 50)")

    conn.commit()
    conn.close()
    print("База данных restaurant.db создана и заполнена тестовыми данными.")
    # Добавим ещё тестовых клиентов, сотрудников, поставщиков, заказы
    cursor.executescript("""
        INSERT OR IGNORE INTO Client (idClient, FIO, Phone, Email, Kolitchestvo_poseshenii) VALUES
        (1, 'Андреев Андрей', '+79161112233', 'andreev@mail.ru', 5),
        (2, 'Борисова Борислава', '+79162223344', 'borisova@mail.ru', 3);
        INSERT OR IGNORE INTO Staff (Staff_id, FIO, idDolzhnost, Salary, DataPrioma) VALUES
        (1, 'Иванов Иван', 1, 50000, '2024-01-10'),
        (2, 'Петрова Мария', 2, 35000, '2024-02-15');
        INSERT OR IGNORE INTO Postavshik (idPostavshika, Company_name, phone, adres) VALUES
        (1, 'ООО ПродуктОпт', '+74951234567', 'Москва, ул. Ленина 1');
        INSERT OR IGNORE INTO Zakaz (idZakaz, table_number, data_and_time, idClient, idSotrudnika, Status) VALUES
        (1, 3, datetime('now', '-2 days'), 1, 1, 'Завершен'),
        (2, 5, datetime('now', '-1 day'), 2, 2, 'Новый');
        INSERT OR IGNORE INTO SostavZakaza (idPozitsii, idZakaza, idBluda, Kolitchestvo, Cost) VALUES
        (1, 1, 1, 2, 350),
        (2, 2, 2, 1, 650);
    """)

if __name__ == "__main__":
    create_database()