import sqlite3

def create_database(db_path):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    create_person_table = '{}{}{}{}{}{}{}'.format(
                        'CREATE TABLE IF NOT EXISTS',
                        ' person(id INTEGER PRIMARY KEY,',
                        ' first_name text NOT NULL,',
                        ' lastname text NOT NULL,',
                        ' new_birthday text NOT NULL,',
                        ' age text NOT NULL,',
                        ' message text NOT NULL);'
                        )

    cursor.execute(create_person_table)

    connection.commit()
    connection.close()

    print('Database successfully created and populated with data!')