import sqlite3
from db_config import DATABASE_FILE

class RestaurantApp:
    def __init__(self):
        self.connection = None

    def connect(self):
        """Устанавливает соединение с БД"""
        self.connection = sqlite3.connect(DATABASE_FILE)
        self.connection.row_factory = sqlite3.Row  # чтобы результаты были как словари
        return self.connection

    def close(self):
        if self.connection:
            self.connection.close()

    # -------------------- CRUD для Category --------------------
    def get_all_categories(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT idCategory, Category_name FROM Category")
        rows = cursor.fetchall()
        self.close()
        return [dict(row) for row in rows]

    def add_category(self, name, order, activnost, photo):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Category (Category_name, Poryadok_otobrazhenia, Activnost, Category_photo) VALUES (?, ?, ?, ?)",
            (name, order, activnost, photo)
        )
        conn.commit()
        new_id = cursor.lastrowid
        self.close()
        return new_id

    def update_category(self, id, name, order, activnost, photo):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Category SET Category_name=?, Poryadok_otobrazhenia=?, Activnost=?, Category_photo=? WHERE idCategory=?",
            (name, order, activnost, photo, id)
        )
        conn.commit()
        self.close()

    def delete_category(self, id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Category WHERE idCategory=?", (id,))
        conn.commit()
        self.close()

    # -------------------- CRUD для Menu (с JOIN категории) --------------------
    def get_all_menu(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.idBluda, m.name, m.cost, m.Weight, c.Category_name
            FROM Menu m
            JOIN Category c ON m.idCategory = c.idCategory
            ORDER BY m.idBluda
        """)
        rows = cursor.fetchall()
        self.close()
        return [dict(row) for row in rows]

    def add_menu_item(self, name, cost, weight, category_id):
        conn = self.connect()
        cursor = conn.cursor()
        # Вычисляем новый idBluda
        cursor.execute("SELECT MAX(idBluda) FROM Menu")
        max_id = cursor.fetchone()[0]
        new_id = (max_id or 0) + 1
        cursor.execute(
            "INSERT INTO Menu (idBluda, name, cost, Weight, idCategory) VALUES (?, ?, ?, ?, ?)",
            (new_id, name, cost, weight, category_id)
        )
        conn.commit()
        self.close()
        return new_id

    def update_menu_item(self, id, name, cost, weight, category_id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Menu SET name=?, cost=?, Weight=?, idCategory=? WHERE idBluda=?",
            (name, cost, weight, category_id, id)
        )
        conn.commit()
        self.close()

    def delete_menu_item(self, id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Menu WHERE idBluda=?", (id,))
        conn.commit()
        self.close()

    # -------------------- Аналитические запросы --------------------
    def top_popular_dishes(self, limit=5):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.name, SUM(sz.Kolitchestvo) AS total_sold
            FROM Menu m
            JOIN SostavZakaza sz ON m.idBluda = sz.idBluda
            GROUP BY m.idBluda
            ORDER BY total_sold DESC
            LIMIT ?
        """, (limit,))
        rows = cursor.fetchall()
        self.close()
        return [dict(row) for row in rows]

    def revenue_by_staff_and_period(self, staff_id, start_date, end_date):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COALESCE(SUM(sz.Cost * sz.Kolitchestvo), 0) AS revenue
            FROM Staff s
            LEFT JOIN Zakaz z ON s.Staff_id = z.idSotrudnika AND z.Status = 'Завершен'
            LEFT JOIN SostavZakaza sz ON z.idZakaz = sz.idZakaza
            WHERE s.Staff_id = ?
              AND DATE(z.data_and_time) BETWEEN ? AND ?
        """, (staff_id, start_date, end_date))
        row = cursor.fetchone()
        self.close()
        return row[0] if row else 0

    # -------------------- CRUD для Client (Клиенты) --------------------
    def get_all_clients(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT idClient, FIO, Phone, Email, Kolitchestvo_poseshenii FROM Client ORDER BY FIO")
        rows = cursor.fetchall()
        self.close()
        return [dict(row) for row in rows]

    def add_client(self, fio, phone, email, visits):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(idClient) FROM Client")
        max_id = cursor.fetchone()[0]
        new_id = (max_id or 0) + 1
        cursor.execute(
            "INSERT INTO Client (idClient, FIO, Phone, Email, Kolitchestvo_poseshenii) VALUES (?, ?, ?, ?, ?)",
            (new_id, fio, phone, email, visits)
        )
        conn.commit()
        self.close()
        return new_id

    def update_client(self, client_id, fio, phone, email, visits):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Client SET FIO=?, Phone=?, Email=?, Kolitchestvo_poseshenii=? WHERE idClient=?",
            (fio, phone, email, visits, client_id)
        )
        conn.commit()
        self.close()

    def delete_client(self, client_id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Client WHERE idClient=?", (client_id,))
        conn.commit()
        self.close()

    # -------------------- CRUD для Staff (Сотрудники) с должностью --------------------
    def get_all_staff(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.Staff_id, s.FIO, d.Dolzhnost_name, s.Salary, s.DataPrioma
            FROM Staff s
            JOIN Dolzhnost d ON s.idDolzhnost = d.idDolzhnost
            ORDER BY s.FIO
        """)
        rows = cursor.fetchall()
        self.close()
        return [dict(row) for row in rows]

    def add_staff(self, fio, dolzh_id, salary, date_prioma):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(Staff_id) FROM Staff")
        max_id = cursor.fetchone()[0]
        new_id = (max_id or 0) + 1
        cursor.execute(
            "INSERT INTO Staff (Staff_id, FIO, idDolzhnost, Salary, DataPrioma) VALUES (?, ?, ?, ?, ?)",
            (new_id, fio, dolzh_id, salary, date_prioma)
        )
        conn.commit()
        self.close()
        return new_id

    def update_staff(self, staff_id, fio, dolzh_id, salary, date_prioma):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Staff SET FIO=?, idDolzhnost=?, Salary=?, DataPrioma=? WHERE Staff_id=?",
            (fio, dolzh_id, salary, date_prioma, staff_id)
        )
        conn.commit()
        self.close()

    def delete_staff(self, staff_id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Staff WHERE Staff_id=?", (staff_id,))
        conn.commit()
        self.close()

    def get_all_dolzhnosti(self):
        """Справочник должностей для выбора при редактировании сотрудника"""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT idDolzhnost, Dolzhnost_name FROM Dolzhnost")
        rows = cursor.fetchall()
        self.close()
        return [dict(row) for row in rows]

    # -------------------- CRUD для Postavshik (Поставщики) --------------------
    def get_all_postavshiki(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT idPostavshika, Company_name, phone, adres, YsloviaOplatv FROM Postavshik ORDER BY Company_name")
        rows = cursor.fetchall()
        self.close()
        return [dict(row) for row in rows]

    def add_postavshik(self, name, phone, address, terms):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(idPostavshika) FROM Postavshik")
        max_id = cursor.fetchone()[0]
        new_id = (max_id or 0) + 1
        cursor.execute(
            "INSERT INTO Postavshik (idPostavshika, Company_name, phone, adres, YsloviaOplatv) VALUES (?, ?, ?, ?, ?)",
            (new_id, name, phone, address, terms)
        )
        conn.commit()
        self.close()
        return new_id

    def update_postavshik(self, pid, name, phone, address, terms):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Postavshik SET Company_name=?, phone=?, adres=?, YsloviaOplatv=? WHERE idPostavshika=?",
            (name, phone, address, terms, pid)
        )
        conn.commit()
        self.close()

    def delete_postavshik(self, pid):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Postavshik WHERE idPostavshika=?", (pid,))
        conn.commit()
        self.close()

    # -------------------- CRUD для Zakaz (Заказы) с JOIN клиента и сотрудника --------------------
    def get_all_orders(self):
        """Выводит заказы с ФИО клиента и ФИО сотрудника вместо ID"""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT z.idZakaz, z.table_number, z.data_and_time,
                   c.FIO AS ClientName, s.FIO AS StaffName, z.Status,
                   (SELECT SUM(sz.Cost * sz.Kolitchestvo) FROM SostavZakaza sz WHERE sz.idZakaza = z.idZakaz) AS TotalSum
            FROM Zakaz z
            JOIN Client c ON z.idClient = c.idClient
            JOIN Staff s ON z.idSotrudnika = s.Staff_id
            ORDER BY z.idZakaz
        """)
        rows = cursor.fetchall()
        self.close()
        return [dict(row) for row in rows]

    def add_order(self, table_num, client_id, staff_id, status, items=None):
        """
        items: список кортежей (idBluda, quantity) – опционально, если нужно сразу добавить позиции.
        Сначала создаём заказ, потом, если items передан, добавляем в SostavZakaza.
        """
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(idZakaz) FROM Zakaz")
        max_id = cursor.fetchone()[0]
        new_id = (max_id or 0) + 1
        cursor.execute(
            "INSERT INTO Zakaz (idZakaz, table_number, data_and_time, idClient, idSotrudnika, Status) VALUES (?, ?, datetime('now'), ?, ?, ?)",
            (new_id, table_num, client_id, staff_id, status)
        )
        if items:
            for dish_id, qty in items:
                # получить цену блюда
                cursor.execute("SELECT cost FROM Menu WHERE idBluda = ?", (dish_id,))
                price = cursor.fetchone()[0]
                cursor.execute("SELECT MAX(idPozitsii) FROM SostavZakaza")
                max_pos = cursor.fetchone()[0]
                pos_id = (max_pos or 0) + 1
                cursor.execute(
                    "INSERT INTO SostavZakaza (idPozitsii, idZakaza, idBluda, Kolitchestvo, Cost) VALUES (?, ?, ?, ?, ?)",
                    (pos_id, new_id, dish_id, qty, price)
                )
        conn.commit()
        self.close()
        return new_id

    def update_order(self, order_id, table_num, client_id, staff_id, status):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Zakaz SET table_number=?, idClient=?, idSotrudnika=?, Status=? WHERE idZakaz=?",
            (table_num, client_id, staff_id, status, order_id)
        )
        conn.commit()
        self.close()

    def delete_order(self, order_id):
        conn = self.connect()
        cursor = conn.cursor()
        # сначала нужно удалить связанные позиции, иначе внешний ключ помешает
        cursor.execute("DELETE FROM SostavZakaza WHERE idZakaza=?", (order_id,))
        cursor.execute("DELETE FROM Zakaz WHERE idZakaz=?", (order_id,))
        conn.commit()
        self.close()