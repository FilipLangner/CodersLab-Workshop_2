from psycopg2 import connect, OperationalError
from clcrypto import password_hash, check_password


class User:
    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = password

    def __str__(self):
        return self.username

    @staticmethod
    def get_user(id, db_conn):
        cursor = db_conn.cursor()
        cursor.execute("select id, username, email, hashed_password from Users where id=%s", [id])
        user_data = cursor.fetchone()
        user = User(user_data[0], user_data[1], user_data[2], user_data[3])
        cursor.close()
        return user

    @staticmethod
    def get_user_by_name(username, db_conn):
        cursor = db_conn.cursor()
        cursor.execute("select id, username, email, hashed_password from Users where username=%s", [username])
        if cursor.rowcount > 0:
            user_data = cursor.fetchone()
            user = User(user_data[0], user_data[1], user_data[2], user_data[3])
            cursor.close()
            return user
        else:
            return None

    @staticmethod
    def get_user_by_email(email, db_conn):
        cursor = db_conn.cursor()
        cursor.execute("select id, username, email, hashed_password from Users where email=%s", [email])
        if cursor.rowcount > 0:
            user_data = cursor.fetchone()
            user = User(user_data[0], user_data[1], user_data[2], user_data[3])
            cursor.close()
            return user
        else:
            return None

    @staticmethod
    def get_all_users(db_conn):
        cursor = db_conn.cursor()
        cursor.execute("select id, username, email, hashed_password from Users")
        # fetchall() to get all users data
        all_users_data = cursor.fetchall()
        all_users = []
        for user_data in all_users_data:
            user = User(user_data[0], user_data[1], user_data[2], user_data[3])
            all_users.append(user)
        cursor.close()
        return all_users

    def save_to_db(self, db_conn):
        cursor = db_conn.cursor()
        self.password = password_hash(self.password)
        cursor.execute('insert into Users(username, email, hashed_password) values (%s,%s,%s) returning id',
            [self.username, self.email, self.password])
        new_id = cursor.fetchone()[0]
        self.id = new_id
        cursor.close()

    @staticmethod
    def verify(user_email, password, db_conn):
        cursor = db_conn.cursor()
        cursor.execute("select hashed_password from users where email=%s", [user_email])
        r = False
        if cursor.rowcount > 0:
            db_hashed_password = cursor.fetchone()[0]
            r = check_password(password, db_hashed_password)
        cursor.close()
        return r

    def change_password(self, new_password, db_conn):
        self.change(db_conn, new_password=new_password)

    def change(self, db_conn, new_email=None, new_username=None, new_password=None):
        cursor = db_conn.cursor()
        if new_email is not None:
            cursor.execute('update users set email=%s where id=%s', [new_email, self.id])
            self.email = new_email
        if new_username is not None:
            cursor.execute('update users set username=%s where id=%s', [new_username, self.id])
            self.username = new_username
        if new_password is not None:
            hashed_password = password_hash(new_password)
            cursor.execute('update users set hashed_password=%s where id=%s', [hashed_password, self.id])
            self.password = hashed_password
        cursor.close()

    @staticmethod
    def delete(user_email, db_conn):
        cursor = db_conn.cursor()
        cursor.execute('delete from users where email=%s', [user_email])
        cursor.close()



class Message:
    def __init__(self, id, from_id, to_id, message_text, creation_date):
        self.id = id
        self.from_id = from_id
        self.to_id = to_id
        self.message_text = message_text
        self.creation_date = creation_date

    def __str__(self):
        return self.message_text

    def save_to_db(self, db_conn):
        cursor = db_conn.cursor()
        cursor.execute("insert into messages(from_id, to_id, message_text, creation_date) values (%s, %s, %s, %s)"
                       "returning id", [self.from_id, self.to_id, self.message_text, "now"])
        new_id = cursor.fetchone()[0]
        self.id = new_id
        cursor.close()

    @staticmethod
    def load_message_by_id(id, db_conn):
        cursor = db_conn.cursor()
        cursor.execute("select id, from_id, to_id, message_text, creation_date from messages where id=%s", [id])
        message_data = cursor.fetchone()
        message = Message(message_data[0], message_data[1], message_data[2], message_data[3], message_data[4],)
        cursor.close()
        return message

    @staticmethod
    def load_all_messages_for_user(user_email, db_conn):
        cursor = db_conn.cursor()
        cursor.execute("select id, from_id, to_id, message_text, creation_date from messages where to_id ="
                       "(select id from users where email=%s order by creation_date desc)", [user_email])
        messages_raw = cursor.fetchall()
        all_messages = []
        for item in messages_raw:
            message = Message(item[0], item[1], item[2], item[3], item[4])
            all_messages.append(message)
        cursor.close()
        return all_messages

    @staticmethod
    def load_all_messages(db_conn):
        cursor = db_conn.cursor()
        cursor.execute("select id, from_id, to_id, message_text, creation_date from messages")
        messages_raw = cursor.fetchall()
        all_messages = []
        for item in messages_raw:
            message = Message(item[0], item[1], item[2], item[3], item[4])
            all_messages.append(message)
        cursor.close()
        return all_messages


def connect_to_db():
    username = None  # TODO change
    passwd = None  # TODO change
    hostname = "127.0.0.1"  # lub "localhost"
    db_name = "workshop2"

    if username == None or passwd == None:
        raise ConnectionError("Edit the connect_to_db function within the models.py file with a valid username and "
                              "passwd for your database before running the application")

    try:
        # creating new database connection
        db_connection = connect(user=username, password=passwd, host=hostname, database=db_name)
        db_connection.autocommit = True
        return db_connection
    except OperationalError as e:
        print(e)


