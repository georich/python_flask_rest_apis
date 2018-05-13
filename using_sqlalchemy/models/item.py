"""Item model."""
import sqlite3


class ItemModel:
    """docstring for ItemModel."""

    def __init__(self, name, price):
        """Init item."""
        self.name = name
        self.price = price

    def json(self):
        """Return a dictonary containing JSON representation of item."""
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        """Find User by name in database and return, if not return none."""
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return cls(*row)

    def insert(self):
        """Insert an item into the database."""
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (self.name, self.price))

        connection.commit()
        connection.close()

    def update(self):
        """Update an item in the database."""
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (self.price, self.name))

        connection.commit()
        connection.close()
