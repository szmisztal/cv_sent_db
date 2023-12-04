import sqlite3
from sqlite3 import Error


class SQLite:
    def __init__(self, db_file):
        self.db_file = db_file
        self.create_table()

    def create_connection(self):
        try:
            connection = sqlite3.connect(self.db_file)
            return connection
        except Error as e:
            print(f"Error: {e}")
            return None

    def execute_sql_query(self, query, *args, fetch_option = None):
        connection = self.create_connection()
        cursor = connection.cursor()
        if connection is not None:
            try:
                cursor.execute(query, *args)
                connection.commit()
                if fetch_option == "fetchone":
                    return cursor.fetchone()
                elif fetch_option == "fetchall":
                    return cursor.fetchall()
            except Error as e:
                print(f"Error: {e}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()
        else:
            print("Cannot create the database connection.")

    def create_table(self):
        create_table_query = """ CREATE TABLE IF NOT EXISTS offers(
                                 offer_id INTEGER PRIMARY KEY,
                                 position VARCHAR NOT NULL,
                                 company_name VARCHAR NOT NULL,
                                 post_date DATE NOT NULL,
                                 status VARCHAR DEFAULT unknown
                                 ); """
        self.execute_sql_query(create_table_query)

    def insert_to_db(self, position, company_name, post_date):
        insert_query = "INSERT INTO offers (position, company_name, post_date) VALUES (?, ?, ?)"
        self.execute_sql_query(insert_query, (position, company_name, post_date))

    def update_offer(self, offer_id, column, update_data):
        update_query = f"UPDATE offers SET {column} = ? WHERE offer_id = ?"
        self.execute_sql_query(update_query, (update_data, offer_id))

    def delete_offer(self, offer_id):
        delete_query = "DELETE FROM offers WHERE offer_id = ?"
        self.execute_sql_query(delete_query, (offer_id, ))

    def show_all_offers(self, order_by):
        query = f"SELECT * FROM offers ORDER BY {order_by}"
        all_offers = self.execute_sql_query(query, fetch_option = "fetchall")
        return all_offers

    def show_filtered_offers(self, status, order_by):
        query = f"SELECT * FROM offers WHERE status = '{status}' ORDER BY {order_by}"
        offers = self.execute_sql_query(query, fetch_option = "fetchall")
        return offers

    def count_offers(self):
        all_offers = self.show_all_offers("offer_id")
        number_of_offers = len(all_offers)
        return number_of_offers

    def look_for_a_company(self, company_name):
        lower_company_name = company_name.lower()
        all_offers = self.show_all_offers("offer_id")
        found_offers = []
        for offer in all_offers:
            if lower_company_name in offer[2].lower():
                query = f"SELECT * FROM offers WHERE LOWER(company_name) = '{offer[2].lower()}'"
                searching_offer = self.execute_sql_query(query, fetch_option = "fetchall")
                found_offers.extend(searching_offer)
        if not found_offers:
            return None
        return found_offers


