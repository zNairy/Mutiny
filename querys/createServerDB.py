from sqlite3 import connect

def main():
    with connect('server.db') as database:

        # creating table users
        database.execute("""
            create table if not exists users (
                userId INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                codename varchar(20) UNIQUE NOT NULL,
                identifier varchar(9) UNIQUE NOT NULL
            ); 
        """)
        
        # creating table users
        database.execute("""
            create table if not exists invites (
                inviteId INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                receiver varchar(20) NOT NULL,
                sender INTEGER NOT NULL,
                created TIMESTAMP,
                accepted BOOLEAN,
                finished BOOLEAN,
                FOREIGN KEY (sender) REFERENCES users(userId)
            ); 
        """)


if __name__ == '__main__':
    main()