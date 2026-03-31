import psycopg2
import csv
from config import load_config

def create_table():
    command = """
              CREATE TABLE IF NOT EXISTS phonebook \
              ( \
                  id \
                  SERIAL \
                  PRIMARY \
                  KEY, \
                  first_name \
                  VARCHAR \
              ( \
                  50 \
              ) NOT NULL,
                  phone VARCHAR \
              ( \
                  20 \
              ) NOT NULL UNIQUE
                  ) \
              """
    conn = None
    try:
        params = load_config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(command)
        cur.close()
        conn.commit()
        print("Table 'phonebook' ensured/created successfully")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error:", error)
    finally:
        if conn is not None:
            conn.close()


def insert_from_csv(csv_file_path):
    sql = "INSERT INTO phonebook(first_name, phone) VALUES(%s, %s) ON CONFLICT (phone) DO NOTHING;"
    conn = None
    try:
        params = load_config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        with open(csv_file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                cur.execute(sql, (row[0], row[1]))

        conn.commit()
        cur.close()
        print(f"Data inserted from '{csv_file_path}' successfully")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error:", error)
    finally:
        if conn is not None:
            conn.close()


def insert_from_console():
    print("\n--- Add New Contact ---")
    first_name = input("Enter first name: ")
    phone = input("Enter phone number: ")

    sql = "INSERT INTO phonebook(first_name, phone) VALUES(%s, %s);"
    conn = None
    try:
        params = load_config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql, (first_name, phone))
        conn.commit()
        cur.close()
        print(f"Contact '{first_name}' added successfully")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error:", error)
    finally:
        if conn is not None:
            conn.close()


def update_contact(target_phone, new_first_name, new_phone):
    sql = "UPDATE phonebook SET first_name = %s, phone = %s WHERE phone = %s;"
    conn = None
    try:
        params = load_config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql, (new_first_name, new_phone, target_phone))
        updated_rows = cur.rowcount
        conn.commit()
        cur.close()
        print(f"Updated {updated_rows} contact")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error:", error)
    finally:
        if conn is not None:
            conn.close()


def query_contacts(filter_by=None, filter_value=None):
    conn = None
    try:
        params = load_config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        if filter_by == "first_name":
            sql = "SELECT id, first_name, phone FROM phonebook WHERE first_name ILIKE %s;"
            cur.execute(sql, (f"%{filter_value}%",))
        elif filter_by == "phone":
            sql = "SELECT id, first_name, phone FROM phonebook WHERE phone = %s;"
            cur.execute(sql, (filter_value,))
        else:
            sql = "SELECT id, first_name, phone FROM phonebook ORDER BY id;"
            cur.execute(sql)

        rows = cur.fetchall()
        print("\n--- Query Results ---")
        if not rows:
            print("No contacts found.")
        for row in rows:
            print(f"ID: {row[0]} | Name: {row[1]} | Phone: {row[2]}")
        print()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error:", error)
    finally:
        if conn is not None:
            conn.close()


def delete_contact(delete_by, filter_value):
    conn = None
    try:
        params = load_config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        if delete_by == "first_name":
            sql = "DELETE FROM phonebook WHERE first_name = %s;"
        elif delete_by == "phone":
            sql = "DELETE FROM phonebook WHERE phone = %s;"
        else:
            print("Use 'first_name' or 'phone'!")
            return

        cur.execute(sql, (filter_value,))
        deleted_rows = cur.rowcount
        conn.commit()
        cur.close()
        print(f"Deleted {deleted_rows} contact(s) successfully")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error:", error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    create_table()
    insert_from_csv('contacts.csv')

    print("Listing all contacts:")
    query_contacts()

    print("Searching for 'Yerzhigit':")
    query_contacts(filter_by="first_name", filter_value="Yerzhigit")

    print("Updating Maygul's data...")
    update_contact(target_phone="87772048274", new_first_name="MaygulUpdated", new_phone="87772048200")

    query_contacts(filter_by="first_name", filter_value="MaygulUpdated")

    print("Deleting Zheksen by phone...")
    delete_contact(delete_by="phone", filter_value="87752048274")

    print("Deleting Yerzhigit by first_name...")
    delete_contact(delete_by="first_name", filter_value="Yerzhigit")

    print("Final Phonebook Status:")
    query_contacts()