from sqlite3 import connect

def main():
    with connect('server.db') as database:

        # creating table users
        database.execute("""
            create table if not exists users (
                codename varchar(20) UNIQUE NOT NULL,
                identifier varchar(9) UNIQUE NOT NULL
            );
        """)


if __name__ == '__main__':
    main()