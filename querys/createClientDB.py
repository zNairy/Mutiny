from sqlite3 import connect

def main():
    with connect('client.db') as database:
        
        # creating client profiles table
        database.execute("""
            create table if not exists profiles (
                codename varchar(20) UNIQUE NOT NULL,
                identifier varchar(9) UNIQUE NOT NULL
            )
        """)

if __name__ == '__main__':
    main()