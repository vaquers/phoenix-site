import psycopg2

def fetch_from_db(query, params=None):
    try:
        # Установить соединение с базой данных
        connection = psycopg2.connect(
            dbname="phoenix_lbsu",
            user="postgres",
            host="localhost",
            port="5432"
        )
        connection.autocommit = False  # Явное управление транзакциями
        cursor = connection.cursor()

        # Выполнение запросаa
        cursor.execute(query, params)

        # Определение результата в зависимости от типа запроса 
        if query.strip().lower().startswith("insert") and "returning" in query.lower():
            result = cursor.fetchone()  # Получаем возвращаемое значение
            connection.commit()        # Фиксируем транзакцию

        elif query.strip().lower().startswith(("update", "delete", "insert")):
            connection.commit()  # Фиксируем изменения
            result = None
        else:  # SELECT или другие запросы, которые возвращают данные
            result = cursor.fetchall()

        # Закрытие курсора и соединения
        cursor.close()
        connection.close()
        return result
                                                                                                                                                                                                    
    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")
        if 'connection' in locals() and connection:
            connection.rollback()  # Откат транзакции при ошибке
            connection.close()
        return None