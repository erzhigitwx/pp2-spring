import psycopg2
from connect import get_connection


def create_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            phone VARCHAR(20) NOT NULL UNIQUE
        )
    """)
    conn.commit()
    cur.close()
    conn.close()


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    with open('functions.sql', 'r') as f:
        cur.execute(f.read())
    with open('procedures.sql', 'r') as f:
        cur.execute(f.read())
    conn.commit()
    cur.close()
    conn.close()


def search_by_pattern(pattern):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))
    rows = cur.fetchall()
    for row in rows:
        print(f"ID: {row[0]} | Name: {row[1]} | Phone: {row[2]}")
    if not rows:
        print("Nothing found.")
    cur.close()
    conn.close()


def upsert(name, phone):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
    conn.commit()
    cur.close()
    conn.close()


def insert_many(names, phones):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM insert_many_contacts(%s, %s)", (names, phones))
    invalid = cur.fetchall()
    conn.commit()
    if invalid:
        print("Invalid entries:")
        for row in invalid:
            print(f"  {row[0]} - {row[1]}")
    else:
        print("All contacts inserted.")
    cur.close()
    conn.close()


def get_paginated(limit, offset):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
    rows = cur.fetchall()
    for row in rows:
        print(f"ID: {row[0]} | Name: {row[1]} | Phone: {row[2]}")
    if not rows:
        print("No more records.")
    cur.close()
    conn.close()


def delete_contact(value):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL delete_contact(%s)", (value,))
    conn.commit()
    cur.close()
    conn.close()


def main():
    create_table()
    init_db()

    while True:
        print("\n1. Search by pattern")
        print("2. Add/update contact")
        print("3. Bulk insert")
        print("4. View contacts (paginated)")
        print("5. Delete contact")
        print("6. Exit")

        choice = input("Choose: ")

        if choice == '1':
            p = input("Pattern: ")
            search_by_pattern(p)

        elif choice == '2':
            name = input("Name: ")
            phone = input("Phone: ")
            upsert(name, phone)

        elif choice == '3':
            names = []
            phones = []
            print("Enter contacts (empty name to stop):")
            while True:
                name = input("Name: ")
                if not name:
                    break
                phone = input("Phone: ")
                names.append(name)
                phones.append(phone)
            if names:
                insert_many(names, phones)

        elif choice == '4':
            limit = int(input("Limit: "))
            offset = int(input("Offset: "))
            get_paginated(limit, offset)

        elif choice == '5':
            value = input("Name or phone: ")
            delete_contact(value)

        elif choice == '6':
            break


if __name__ == '__main__':
    main()
