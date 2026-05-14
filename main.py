# main.py
# Полное консольное приложение для управления рестораном
# Использует класс RestaurantApp из restaurant_app.py

from restaurant_app import RestaurantApp
import sqlite3
from db_config import DATABASE_FILE


def print_menu_items(menu_items):
    print("\n" + "=" * 70)
    print("СПИСОК БЛЮД")
    print("ID | Название | Цена | Вес | Категория")
    for item in menu_items:
        print(
            f"{item['idBluda']:2} | {item['name']:30} | {item['cost']:4} | {item['Weight']:3} | {item['Category_name']}")
    print("=" * 70)


def print_categories(categories):
    print("\n--- КАТЕГОРИИ ---")
    for cat in categories:
        print(f"{cat['idCategory']} - {cat['Category_name']}")


def print_clients(clients):
    print("\n--- КЛИЕНТЫ ---")
    for c in clients:
        print(
            f"{c['idClient']}: {c['FIO']} | тел:{c['Phone']} | email:{c['Email']} | посещений:{c['Kolitchestvo_poseshenii']}")


def print_staff(staff_list):
    print("\n--- СОТРУДНИКИ ---")
    for s in staff_list:
        print(f"{s['Staff_id']}: {s['FIO']} | {s['Dolzhnost_name']} | з/п {s['Salary']} | принят {s['DataPrioma']}")


def print_postavshiki(post_list):
    print("\n--- ПОСТАВЩИКИ ---")
    for p in post_list:
        print(
            f"{p['idPostavshika']}: {p['Company_name']} | тел:{p['phone']} | адрес:{p['adres']} | условия:{p['YsloviaOplatv']}")


def print_orders(orders):
    print("\n--- ЗАКАЗЫ ---")
    for o in orders:
        print(
            f"Заказ {o['idZakaz']}: стол {o['table_number']}, {o['data_and_time']}, клиент {o['ClientName']}, официант {o['StaffName']}, статус {o['Status']}, сумма {o['TotalSum']}")


def print_dolzhnosti(dolzh_list):
    print("\n--- ДОЛЖНОСТИ ---")
    for d in dolzh_list:
        print(f"{d['idDolzhnost']} - {d['Dolzhnost_name']}")


def main():
    app = RestaurantApp()
    print("Добро пожаловать в систему управления рестораном!")
    print(f"Подключено к БД: {DATABASE_FILE}")

    while True:
        print("\n" + "=" * 50)
        print("ГЛАВНОЕ МЕНЮ")
        print("1.  Работа с блюдами (меню)")
        print("2.  Работа с категориями блюд")
        print("3.  Работа с клиентами")
        print("4.  Работа с сотрудниками")
        print("5.  Работа с поставщиками")
        print("6.  Работа с заказами")
        print("7.  Аналитика: топ популярных блюд")
        print("8.  Аналитика: выручка сотрудника за период")
        print("9.  Диагностика выручки (проверка данных)")
        print("0.  Выход")
        print("=" * 50)

        choice = input("Ваш выбор: ").strip()

        if choice == '1':
            # --- РАБОТА С БЛЮДАМИ ---
            while True:
                print("\n--- БЛЮДА ---")
                print("1. Показать все блюда")
                print("2. Добавить новое блюдо")
                print("3. Редактировать блюдо")
                print("4. Удалить блюдо")
                print("0. Назад")
                sub = input("Выбор: ")
                if sub == '1':
                    items = app.get_all_menu()
                    print_menu_items(items)
                elif sub == '2':
                    cats = app.get_all_categories()
                    print_categories(cats)
                    try:
                        cat_id = int(input("ID категории: "))
                        name = input("Название блюда: ")
                        cost = int(input("Цена (руб): "))
                        weight = int(input("Вес (г): "))
                        new_id = app.add_menu_item(name, cost, weight, cat_id)
                        print(f"✅ Блюдо добавлено с ID = {new_id}")
                    except Exception as e:
                        print(f"Ошибка: {e}")
                elif sub == '3':
                    items = app.get_all_menu()
                    print_menu_items(items)
                    try:
                        dish_id = int(input("ID блюда для редактирования: "))
                        name = input("Новое название: ")
                        cost = int(input("Новая цена: "))
                        weight = int(input("Новый вес: "))
                        cats = app.get_all_categories()
                        print_categories(cats)
                        cat_id = int(input("Новый ID категории: "))
                        app.update_menu_item(dish_id, name, cost, weight, cat_id)
                        print("✅ Блюдо обновлено")
                    except Exception as e:
                        print(f"Ошибка: {e}")
                elif sub == '4':
                    items = app.get_all_menu()
                    print_menu_items(items)
                    try:
                        dish_id = int(input("ID блюда для удаления: "))
                        app.delete_menu_item(dish_id)
                        print("✅ Блюдо удалено")
                    except Exception as e:
                        print(f"Ошибка: {e}")
                elif sub == '0':
                    break

        elif choice == '2':
            # --- РАБОТА С КАТЕГОРИЯМИ ---
            while True:
                print("\n--- КАТЕГОРИИ ---")
                print("1. Показать все категории")
                print("2. Добавить категорию")
                print("3. Редактировать категорию")
                print("4. Удалить категорию")
                print("0. Назад")
                sub = input("Выбор: ")
                if sub == '1':
                    cats = app.get_all_categories()
                    print_categories(cats)
                elif sub == '2':
                    try:
                        name = input("Название категории: ")
                        order = int(input("Порядок отображения (число): "))
                        activnost = int(input("Активность (1-да, 0-нет): "))
                        photo = input("Имя файла фото (пусто, если нет): ") or None
                        new_id = app.add_category(name, order, activnost, photo)
                        print(f"✅ Категория добавлена с ID = {new_id}")
                    except Exception as e:
                        print(f"Ошибка: {e}")
                elif sub == '3':
                    cats = app.get_all_categories()
                    print_categories(cats)
                    try:
                        cat_id = int(input("ID категории для редактирования: "))
                        name = input("Новое название: ")
                        order = int(input("Новый порядок: "))
                        activnost = int(input("Активность (1/0): "))
                        photo = input("Имя файла фото: ") or None
                        app.update_category(cat_id, name, order, activnost, photo)
                        print("✅ Категория обновлена")
                    except Exception as e:
                        print(f"Ошибка: {e}")
                elif sub == '4':
                    cats = app.get_all_categories()
                    print_categories(cats)
                    try:
                        cat_id = int(input("ID категории для удаления: "))
                        app.delete_category(cat_id)
                        print("✅ Категория удалена")
                    except Exception as e:
                        print(f"Ошибка: {e}")
                elif sub == '0':
                    break

        elif choice == '3':
            # --- РАБОТА С КЛИЕНТАМИ ---
            while True:
                print("\n--- КЛИЕНТЫ ---")
                print("1. Показать всех клиентов")
                print("2. Добавить клиента")
                print("3. Редактировать клиента")
                print("4. Удалить клиента")
                print("0. Назад")
                sub = input("Выбор: ")
                if sub == '1':
                    clients = app.get_all_clients()
                    print_clients(clients)
                elif sub == '2':
                    try:
                        fio = input("ФИО: ")
                        phone = input("Телефон: ")
                        email = input("Email: ")
                        visits = int(input("Количество посещений: "))
                        new_id = app.add_client(fio, phone, email, visits)
                        print(f"✅ Клиент добавлен с ID = {new_id}")
                    except Exception as e:
                        print(f"Ошибка: {e}")
                elif sub == '3':
                    clients = app.get_all_clients()
                    print_clients(clients)
                    try:
                        client_id = int(input("ID клиента для редактирования: "))
                        fio = input("Новое ФИО: ")
                        phone = input("Новый телефон: ")
                        email = input("Новый email: ")
                        visits = int(input("Новое количество посещений: "))
                        app.update_client(client_id, fio, phone, email, visits)
                        print("✅ Клиент обновлён")
                    except Exception as e:
                        print(f"Ошибка: {e}")
                elif sub == '4':
                    clients = app.get_all_clients()
                    print_clients(clients)
                    try:
                        client_id = int(input("ID клиента для удаления: "))
                        app.delete_client(client_id)
                        print("✅ Клиент удалён")
                    except Exception as e:
                        print(f"Ошибка: {e}")
                elif sub == '0':
                    break

        elif choice == '4':
            # --- РАБОТА С СОТРУДНИКАМИ ---
            while True:
                print("\n--- СОТРУДНИКИ ---")
                print("1. Показать всех сотрудников")
                print("2. Добавить сотрудника")
                print("3. Редактировать сотрудника")
                print("4. Удалить сотрудника")
                print("0. Назад")
                sub = input("Выбор: ")
                if sub == '1':
                    staff = app.get_all_staff()
                    print_staff(staff)
                elif sub == '2':
                    try:
                        dolzh = app.get_all_dolzhnosti()
                        print_dolzhnosti(dolzh)
                        dolzh_id = int(input("ID должности: "))
                        fio = input("ФИО: ")
                        salary = int(input("Зарплата: "))
                        date_prioma = input("Дата приёма (ГГГГ-ММ-ДД): ")
                        new_id = app.add_staff(fio, dolzh_id, salary, date_prioma)
                        print(f"✅ Сотрудник добавлен с ID = {new_id}")
                    except Exception as e:
                        print(f"Ошибка: {e}")
                elif sub == '3':
                    staff = app.get_all_staff()
                    print_staff(staff)
                    try:
                        staff_id = int(input("ID сотрудника для редактирования: "))
                        dolzh = app.get_all_dolzhnosti()
                        print_dolzhnosti(dolzh)
                        dolzh_id = int(input("Новый ID должности: "))
                        fio = input("Новое ФИО: ")
                        salary = int(input("Новая зарплата: "))
                        date_prioma = input("Новая дата приёма (ГГГГ-ММ-ДД): ")
                        app.update_staff(staff_id, fio, dolzh_id, salary, date_prioma)
                        print("✅ Сотрудник обновлён")
                    except Exception as e:
                        print(f"Ошибка: {e}")
                elif sub == '4':
                    staff = app.get_all_staff()
                    print_staff(staff)
                    try:
                        staff_id = int(input("ID сотрудника для удаления: "))
                        app.delete_staff(staff_id)
                        print("✅ Сотрудник удалён")
                    except Exception as e:
                        print(f"Ошибка: {e}")
                elif sub == '0':
                    break

        elif choice == '5':
            # --- РАБОТА С ПОСТАВЩИКАМИ ---
            while True:
                print("\n--- ПОСТАВЩИКИ ---")
                print("1. Показать всех поставщиков")
                print("2. Добавить поставщика")
                print("3. Редактировать поставщика")
                print("4. Удалить поставщика")
                print("0. Назад")
                sub = input("Выбор: ")
                if sub == '1':
                    posts = app.get_all_postavshiki()
                    print_postavshiki(posts)
                elif sub == '2':
                    try:
                        name = input("Название компании: ")
                        phone = input("Телефон: ")
                        address = input("Адрес: ")
                        terms = input("Условия оплаты: ")
                        new_id = app.add_postavshik(name, phone, address, terms)
                        print(f"✅ Поставщик добавлен с ID = {new_id}")
                    except Exception as e:
                        print(f"Ошибка: {e}")
                elif sub == '3':
                    posts = app.get_all_postavshiki()
                    print_postavshiki(posts)
                    try:
                        pid = int(input("ID поставщика для редактирования: "))
                        name = input("Новое название компании: ")
                        phone = input("Новый телефон: ")
                        address = input("Новый адрес: ")
                        terms = input("Новые условия оплаты: ")
                        app.update_postavshik(pid, name, phone, address, terms)
                        print("✅ Поставщик обновлён")
                    except Exception as e:
                        print(f"Ошибка: {e}")
                elif sub == '4':
                    posts = app.get_all_postavshiki()
                    print_postavshiki(posts)
                    try:
                        pid = int(input("ID поставщика для удаления: "))
                        app.delete_postavshik(pid)
                        print("✅ Поставщик удалён")
                    except Exception as e:
                        print(f"Ошибка: {e}")
                elif sub == '0':
                    break

        elif choice == '6':
            # --- РАБОТА С ЗАКАЗАМИ ---
            while True:
                print("\n--- ЗАКАЗЫ ---")
                print("1. Показать все заказы")
                print("2. Добавить новый заказ")
                print("3. Редактировать заказ")
                print("4. Удалить заказ")
                print("0. Назад")
                sub = input("Выбор: ")
                if sub == '1':
                    orders = app.get_all_orders()
                    print_orders(orders)
                elif sub == '2':
                    try:
                        # список клиентов
                        clients = app.get_all_clients()
                        print("\n--- КЛИЕНТЫ ---")
                        for c in clients:
                            print(f"{c['idClient']} – {c['FIO']}")
                        client_id = int(input("ID клиента: "))

                        # список сотрудников
                        staff_list = app.get_all_staff()
                        print("\n--- СОТРУДНИКИ ---")
                        for s in staff_list:
                            print(f"{s['Staff_id']} – {s['FIO']} ({s['Dolzhnost_name']})")
                        staff_id = int(input("ID официанта: "))

                        table = int(input("Номер стола: "))
                        status = input("Статус (Новый/В процессе/Оплачен/Завершен): ")

                        # Добавление позиций заказа
                        items = []
                        print("\n--- ДОБАВЛЕНИЕ ПОЗИЦИЙ ЗАКАЗА ---")
                        menu = app.get_all_menu()
                        for dish in menu:
                            print(f"{dish['idBluda']} – {dish['name']} | {dish['cost']} руб.")
                        while True:
                            dish_id = input("Введите ID блюда (или 0, чтобы закончить): ")
                            if dish_id == '0':
                                break
                            qty = int(input("Количество: "))
                            items.append((int(dish_id), qty))

                        new_id = app.add_order(table, client_id, staff_id, status, items)
                        print(f"✅ Заказ создан с ID {new_id}, сумма будет рассчитана автоматически.")
                    except Exception as e:
                        print(f"Ошибка: {e}")
                elif sub == '3':
                    orders = app.get_all_orders()
                    print_orders(orders)
                    try:
                        order_id = int(input("ID заказа для редактирования: "))
                        table = int(input("Новый номер стола: "))
                        clients = app.get_all_clients()
                        print_clients(clients)
                        client_id = int(input("Новый ID клиента: "))
                        staff_list = app.get_all_staff()
                        print_staff(staff_list)
                        staff_id = int(input("Новый ID официанта: "))
                        status = input("Новый статус: ")
                        app.update_order(order_id, table, client_id, staff_id, status)
                        print("✅ Заказ обновлён")
                    except Exception as e:
                        print(f"Ошибка: {e}")
                elif sub == '4':
                    orders = app.get_all_orders()
                    print_orders(orders)
                    try:
                        order_id = int(input("ID заказа для удаления: "))
                        app.delete_order(order_id)
                        print("✅ Заказ удалён")
                    except Exception as e:
                        print(f"Ошибка: {e}")
                elif sub == '0':
                    break

        elif choice == '7':
            # АНАЛИТИКА: ТОП БЛЮД
            try:
                limit = input("Сколько топ блюд показать? (по умолчанию 5): ")
                limit = int(limit) if limit.strip() else 5
                top = app.top_popular_dishes(limit)
                print("\n=== ТОП ПОПУЛЯРНЫХ БЛЮД ===")
                for i, dish in enumerate(top, 1):
                    print(f"{i}. {dish['name']} — продано {dish['total_sold']} шт.")
            except Exception as e:
                print(f"Ошибка: {e}")

        elif choice == '8':
            # АНАЛИТИКА: ВЫРУЧКА СОТРУДНИКА
            try:
                staff_id = int(input("Введите ID сотрудника: "))
                start = input("Дата начала (ГГГГ-ММ-ДД): ")
                end = input("Дата конца (ГГГГ-ММ-ДД): ")
                revenue = app.revenue_by_staff_and_period(staff_id, start, end)
                print(f"💰 Выручка сотрудника {staff_id} за период {start} – {end}: {revenue} руб.")
            except Exception as e:
                print(f"Ошибка: {e}")

        elif choice == '9':
            # ДИАГНОСТИКА ВЫРУЧКИ
            conn = sqlite3.connect(DATABASE_FILE)
            cursor = conn.cursor()
            print("\n=== ДИАГНОСТИКА ВЫРУЧКИ ===")
            cursor.execute("SELECT COUNT(*) FROM Zakaz WHERE Status = 'Завершен'")
            count = cursor.fetchone()[0]
            print(f"1. Всего завершённых заказов: {count}")
            cursor.execute(
                "SELECT idZakaz, Status, idSotrudnika, data_and_time FROM Zakaz WHERE Status = 'Завершен' LIMIT 5")
            rows = cursor.fetchall()
            print("2. Примеры завершённых заказов:")
            for row in rows:
                print(f"   idZakaz={row[0]}, статус='{row[1]}', сотрудник={row[2]}, дата={row[3]}")
            if rows:
                zakaz_ids = [str(r[0]) for r in rows]
                cursor.execute(f"SELECT COUNT(*) FROM SostavZakaza WHERE idZakaza IN ({','.join(zakaz_ids)})")
                pos_count = cursor.fetchone()[0]
                print(f"3. Позиций в SostavZakaza для этих заказов: {pos_count}")
            staff_id = input("Введите ID сотрудника для теста (например, 1): ")
            start = input("Дата начала (ГГГГ-ММ-ДД): ")
            end = input("Дата конца (ГГГГ-ММ-ДД): ")
            cursor.execute("""
                SELECT COALESCE(SUM(sz.Cost * sz.Kolitchestvo), 0) AS revenue
                FROM Staff s
                LEFT JOIN Zakaz z ON s.Staff_id = z.idSotrudnika AND z.Status = 'Завершен'
                LEFT JOIN SostavZakaza sz ON z.idZakaz = sz.idZakaza
                WHERE s.Staff_id = ?
                  AND DATE(z.data_and_time) BETWEEN ? AND ?
            """, (staff_id, start, end))
            revenue = cursor.fetchone()[0]
            print(f"4. Выручка по функции: {revenue}")
            conn.close()
            input("Нажмите Enter для продолжения...")

        elif choice == '0':
            print("До свидания!")
            break
        else:
            print("Неверный ввод. Попробуйте снова.")


if __name__ == "__main__":
    main()
