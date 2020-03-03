import sqlite3
import os

base_dir = os.path.dirname(os.path.realpath(__file__)).split('models')[0]

class PersonModel:

    def __init__(self, id, first_name, lastname, new_birthday, age, message):
        self.id = id
        self.first_name = first_name
        self.lastname = lastname
        self.new_birthday = new_birthday
        self.age = age
        self.message = message

    @classmethod
    def find_by_name(cls, first_name,lastname, db_path='{}/db/database_file.db'.format(base_dir)):
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        query = 'SELECT * FROM person WHERE first_name=? and lastname=?;'
        result = cursor.execute(query, (first_name,lastname,))
        rows = result.fetchall()
        if rows:
            for row in rows:
                user = PersonModel(row[0], row[1], row[2], row[3], row[4], row[5])
            connection.close()
            return user


    @classmethod
    def find_by_id(cls, id, db_path='{}/db/database_file.db'.format(base_dir)):
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        query = 'SELECT * FROM person WHERE id=?;'
        result = cursor.execute(query, (id,))
        rows = result.fetchall()
        if rows:
            for row in rows:
                user = PersonModel(row[0], row[1], row[2], row[3], row[4], row[5])
            connection.close()
            return user

    @classmethod
    def insert_into_table(cls, first_name, lastname, new_birthday, age, message, db_path='{}/db/database_file.db'.format(base_dir)):
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        query = 'INSERT INTO person VALUES(NULL, ?, ?, ?, ?, ?)'
        cursor.execute(query, (first_name, lastname, new_birthday, age, message,))
        connection.commit()
        connection.close()

    @classmethod
    def find_all(cls, db_path='{}/db/database_file.db'.format(base_dir)):
        users = list()
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        query = 'SELECT * FROM person;'
        result = cursor.execute(query)
        rows = result.fetchall()
        if rows:
            for row in rows:
                users.append(PersonModel(row[0], row[1], row[2], row[3], row[4], row[5]))
            return users
        connection.close()

    def json(self):
        return {'id': self.id,
        'first_name': self.first_name,
        'lastname': self.lastname,
        'new_birthday': self.new_birthday,
        'age': self.age,
        'message': self.message}