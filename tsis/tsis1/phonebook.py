import csv
import json
import psycopg2
from connect import get_connection


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    with open('schema.sql') as f:
        cur.execute(f.read())
    with open('procedures.sql') as f:
        cur.execute(f.read())
    conn.commit()
    cur.close()
    conn.close()


def get_or_create_group(cur, name):
    if not name:
        name = 'Other'
    cur.execute("SELECT id FROM groups WHERE name=%s", (name,))
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute("INSERT INTO groups(name) VALUES (%s) RETURNING id", (name,))
    return cur.fetchone()[0]


def insert_contact(cur, name, email, birthday, group, phone, phone_type):
    gid = get_or_create_group(cur, group)
    cur.execute("SELECT id FROM contacts WHERE name=%s", (name,))
    row = cur.fetchone()
    if row:
        cid = row[0]
        cur.execute("UPDATE contacts SET email=%s, birthday=%s, group_id=%s WHERE id=%s",
                    (email or None, birthday or None, gid, cid))
    else:
        cur.execute("""INSERT INTO contacts(name, email, birthday, group_id)
                       VALUES(%s,%s,%s,%s) RETURNING id""",
                    (name, email or None, birthday or None, gid))
        cid = cur.fetchone()[0]
    if phone:
        cur.execute("SELECT 1 FROM phones WHERE contact_id=%s AND phone=%s", (cid, phone))
        if not cur.fetchone():
            cur.execute("INSERT INTO phones(contact_id, phone, type) VALUES(%s,%s,%s)",
                        (cid, phone, phone_type or 'mobile'))
    return cid


def import_csv(path):
    conn = get_connection()
    cur = conn.cursor()
    with open(path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            insert_contact(cur,
                           row.get('name', '').strip(),
                           row.get('email', '').strip(),
                           row.get('birthday', '').strip(),
                           row.get('group', '').strip(),
                           row.get('phone', '').strip(),
                           row.get('phone_type', '').strip())
            count += 1
    conn.commit()
    cur.close()
    conn.close()
    print(f"data: imported {count} rows from {path}")


def export_json(path):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""SELECT c.id, c.name, c.email, c.birthday, g.name
                   FROM contacts c LEFT JOIN groups g ON c.group_id=g.id""")
    contacts = []
    for cid, name, email, bday, gname in cur.fetchall():
        cur.execute("SELECT phone, type FROM phones WHERE contact_id=%s", (cid,))
        phones = [{'phone': p, 'type': t} for p, t in cur.fetchall()]
        contacts.append({
            'name': name,
            'email': email,
            'birthday': bday.isoformat() if bday else None,
            'group': gname,
            'phones': phones,
        })
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(contacts, f, indent=2, ensure_ascii=False)
    cur.close()
    conn.close()
    print(f"data: exported {len(contacts)} contacts to {path}")


def import_json(path):
    with open(path, encoding='utf-8') as f:
        contacts = json.load(f)
    conn = get_connection()
    cur = conn.cursor()
    added = 0
    for c in contacts:
        cur.execute("SELECT id FROM contacts WHERE name=%s", (c['name'],))
        if cur.fetchone():
            ans = input(f"contact {c['name']} exists. (s)kip / (o)verwrite: ").strip().lower()
            if ans != 'o':
                continue
        gid = get_or_create_group(cur, c.get('group'))
        cur.execute("SELECT id FROM contacts WHERE name=%s", (c['name'],))
        row = cur.fetchone()
        if row:
            cid = row[0]
            cur.execute("UPDATE contacts SET email=%s, birthday=%s, group_id=%s WHERE id=%s",
                        (c.get('email'), c.get('birthday'), gid, cid))
            cur.execute("DELETE FROM phones WHERE contact_id=%s", (cid,))
        else:
            cur.execute("""INSERT INTO contacts(name, email, birthday, group_id)
                           VALUES(%s,%s,%s,%s) RETURNING id""",
                        (c['name'], c.get('email'), c.get('birthday'), gid))
            cid = cur.fetchone()[0]
        for p in c.get('phones', []):
            cur.execute("INSERT INTO phones(contact_id, phone, type) VALUES(%s,%s,%s)",
                        (cid, p['phone'], p.get('type', 'mobile')))
        added += 1
    conn.commit()
    cur.close()
    conn.close()
    print(f"data: imported {added} contacts from {path}")


def list_by_group(group_name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""SELECT c.id, c.name, c.email FROM contacts c
                   JOIN groups g ON c.group_id=g.id WHERE g.name=%s""", (group_name,))
    rows = cur.fetchall()
    print(f"data: group {group_name}, {len(rows)} contacts")
    for r in rows:
        print(f"  {r[0]} {r[1]} {r[2] or ''}")
    cur.close()
    conn.close()


def search_email(part):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name, email FROM contacts WHERE email ILIKE %s", (f"%{part}%",))
    rows = cur.fetchall()
    print(f"data: email match {part}, {len(rows)} found")
    for r in rows:
        print(f"  {r[0]} {r[1]}")
    cur.close()
    conn.close()


def sorted_list(by):
    col = {'name': 'c.name', 'birthday': 'c.birthday', 'date': 'c.created_at'}.get(by, 'c.name')
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"""SELECT c.name, c.email, c.birthday, c.created_at
                    FROM contacts c ORDER BY {col} NULLS LAST""")
    rows = cur.fetchall()
    print(f"data: sorted by {by}")
    for r in rows:
        print(f"  {r[0]} | {r[1] or '-'} | bday {r[2] or '-'} | added {r[3].date() if r[3] else '-'}")
    cur.close()
    conn.close()


def search_global(query):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM search_contacts(%s)", (query,))
    rows = cur.fetchall()
    print(f"data: search {query}, {len(rows)} matches")
    for r in rows:
        print(f"  id {r[0]} | {r[1]} | {r[2] or '-'} | grp {r[3] or '-'} | ph {r[4] or '-'}")
    cur.close()
    conn.close()


def paginated_browse():
    page = 0
    size = 5
    while True:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name, email FROM contacts ORDER BY id LIMIT %s OFFSET %s",
                    (size, page * size))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        if not rows and page > 0:
            page -= 1
            print("data: no more pages")
            continue
        print(f"data: page {page + 1}")
        for r in rows:
            print(f"  {r[0]} {r[1]} {r[2] or ''}")
        cmd = input("next/prev/quit: ").strip().lower()
        if cmd in ('q', 'quit'):
            break
        elif cmd in ('p', 'prev') and page > 0:
            page -= 1
        elif cmd in ('n', 'next'):
            page += 1


def call_add_phone(name, phone, ptype):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, ptype))
        conn.commit()
        print(f"data: phone added to {name}")
    except psycopg2.Error as e:
        print(f"err: {e}")
    cur.close()
    conn.close()


def call_move_group(name, group):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL move_to_group(%s, %s)", (name, group))
    conn.commit()
    cur.close()
    conn.close()
    print(f"data: {name} moved to {group}")


def menu():
    init_db()
    while True:
        print()
        print("1 import csv  2 import json  3 export json")
        print("4 list by group  5 search email  6 sort  7 search all")
        print("8 paginated  9 add phone  10 move group  0 quit")
        c = input("> ").strip()
        if c == '1':
            import_csv(input("csv path: "))
        elif c == '2':
            import_json(input("json path: "))
        elif c == '3':
            export_json(input("save to: "))
        elif c == '4':
            list_by_group(input("group: "))
        elif c == '5':
            search_email(input("email part: "))
        elif c == '6':
            sorted_list(input("by (name/birthday/date): "))
        elif c == '7':
            search_global(input("query: "))
        elif c == '8':
            paginated_browse()
        elif c == '9':
            n = input("name: ")
            p = input("phone: ")
            t = input("type (home/work/mobile): ")
            call_add_phone(n, p, t)
        elif c == '10':
            call_move_group(input("name: "), input("group: "))
        elif c == '0':
            break


if __name__ == '__main__':
    menu()
