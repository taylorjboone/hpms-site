import sqlite3


def create_table():
    query = "DROP TABLE IF EXISTS login"
    cursor.execute(query)
    conn.commit()
    
    query = "CREATE TABLE login(Username VARCHAR UNIQUE, Password VARCHAR)"
    cursor.execute(query)
    conn.commit()

def enter(username, password):
    query = "INSERT INTO login (Username, Password) VALUES (?, ?)"
    cursor.execute(query, (username, password))
    conn.commit()

def check(username, password):
    query = 'SELECT * FROM login WHERE Username = ? AND Password = ?'
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    conn.commit()
    print('[DEBUG][check] result:', result)
    return result

def loginlol():
    answer = input("Login (Y/N): ")

    if answer.lower() == "y":
        username = input("Username: ")
        password = input("Password: ")
        if check(username, password):
            print("Username correct!")
            print("Password correct!")
            print("Logging in...")
        else:
            print("Something wrong")

# --- main ---

conn = sqlite3.connect("user_info.db")
cursor = conn.cursor()

create_table()

Username = input("Create username: ")
Password = input("Create password: ")

enter(Username, Password)

#check(Username, Password)

loginlol()

cursor.close()
conn.close()
