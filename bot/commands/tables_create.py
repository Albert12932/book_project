from engine import *
import os
from .get_info import get_books

 # Создает таблицу, если ее не cуществует
def create_tables() -> None:
    cur.execute("""
    CREATE TABLE IF NOT EXISTS people(
        user_id varchar(256) PRIMARY KEY not null,
        username VARCHAR(32),
        group_name VARCHAR(32) default 'None',
        name VARCHAR(50) default 'None',
        surname VARCHAR(50) default 'None'
    );
                
    create table if not exists books(
        book_id serial primary key not null,
        name VARCHAR(256),
        holder varchar(256) default '0',
        storage VARCHAR(100) default 'Деканат',
        link varchar(1024) default 'None',
        date_taken date default '2000-01-01',
        book_tags varchar(8192)
    );
                
    create table if not exists admins(
        id varchar(32)
    );
    
    create table if not exists tags(
        text varchar(256),
        books varchar(256) default 'None'
    );

    create table if not exists logs(
        user_id varchar(128),
        command varchar(32),
        date_time varchar(64),
        args varchar(8192)
    )
 
    """)
    cur.execute("select * from admins")
    if not cur.fetchone():
        cur.execute("insert into admins (id) values ('879954059')")
    conn.commit()



# Итерируемся по списку файлов
async def update_books():
    for file_name in os.listdir("C:/Users/shoma/OneDrive/Документы/project_books"):
        # Проверяем, что расширение файла - pdf
        if file_name in await get_books() or not file_name.endswith(".pdf"):
            continue
        print('new_book')
        cur.execute(f"select name from books where name = '{file_name}'")
        if not cur.fetchone():
            cur.execute(f"insert into books (name, holder, link) values ('{file_name}', 'E', 'C:/Users/shoma/OneDrive/Документы/project_books/{file_name}')")
            conn.commit()