from engine import *
import datetime

# Дает имя пользователя по id
def get_name(id):
    cur.execute(f"select name from people where user_id = '{id}'")
    try:
        return cur.fetchone()[0]
    except:
        return False

# Дает фамилию пользователя по id
def get_surname(id):
    cur.execute(f"select surname from people where user_id = '{id}'")
    try:
        return cur.fetchone()[0]
    except:
        return False

# Дает группу пользователя по id
def get_group(id):
    cur.execute(f"select group_name from people where user_id = '{id}'")
    try:
        return cur.fetchone()[0]
    except:
        return False

# Дает id всех пользователей
async def get_all_id():
    cur.execute('select user_id from people')
    all_id = []
    list_id = cur.fetchall()
    for i in range(len(list_id)):
        all_id.append(list_id[i][0])
    return all_id

# Дает id по фамилии
async def get_id_by_surname(surname):
    cur.execute(f"select user_id from people where surname = '{surname}'")
    try:
        s = cur.fetchone()[0]
        return s
    except TypeError:
        return ' '

# Дает название книги по id
async def get_book_name(book_id):
    cur.execute(f"select name from books where book_id = {book_id}")
    try:
        s = cur.fetchone()[0]
        return s
    except TypeError:
        return None

# Дает хранилище по id
async def get_storage(book_id):
    cur.execute(f"select storage from books where book_id = {book_id}")
    try:
        s = cur.fetchone()[0]
        return s
    except TypeError:
        return None

# Дает инфу о студенте по id
async def get_student_info(book_id):
    cur.execute(f'select holder from books where book_id={book_id}')
    student_id = cur.fetchone()[0]
    if student_id not in await get_all_id():
        return ' '
    cur.execute(f"select surname, name, group_name from people where user_id='{student_id}'")
    return cur.fetchone()[0]

# Дает список всех книг
async def get_books():
    cur.execute('select name from books')
    books = []
    select = cur.fetchall()
    for i in range(len(select)):
        books.append(select[i][0])
    return books

# Проверяет наличие админки у пользователя по id
async def admin(user_id):
    cur.execute(f'select id from admins')
    admins = []
    for person in cur.fetchall():
        admins.append(person[0])
    return str(user_id) in admins

# Получить дату получения книги по id книги
async def get_date(book_id):
    cur.execute(f"select date_taken from books where book_id = {book_id}")
    try:
        s = cur.fetchone()[0]
        return s
    except TypeError:
        return None
    
# Получает группу по id книги
async def get_group_by_book(book_id):
    cur.execute(f'select holder from books where book_id = {book_id}')
    try:
        s = cur.fetchone()[0]
        cur.execute(f"select group_name from people where user_id = '{s}'")
        try:
            return cur.fetchone()[0]
        except TypeError:
            return ' '
    except TypeError:
        return ' '

# Добавляет запись в логи
async def log_add(user_id, command, date_time, args):
    cur.execute(f"select user_id, surname, name, group_name, username from people where user_id = '{user_id}'")
    try:
        info = '_'.join([x for x in cur.fetchall()[0]])
    except IndexError:
        info = 'None'
    cur.execute(f"insert into logs (user_id, command, date_time, args) values ('{info}', '{command}', '{date_time}', '{args}')")
    conn.commit()  #TODO
