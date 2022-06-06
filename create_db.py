# create_db.py - Create a SQLite3 table and populate it with some data
import sqlite3

with sqlite3.connect('sample.db') as connection:
    c = connection.cursor()

    c.execute('CREATE TABLE items(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, description TEXT)')

    c.execute('INSERT INTO items(name, description) VALUES("Car", "It rides well..")')
    c.execute('INSERT INTO items(name, description) VALUES("Bike", "It\'s fast")')
    c.execute('INSERT INTO items(name, description) VALUES("Plane", "It flies!")')

    print('All done!')
