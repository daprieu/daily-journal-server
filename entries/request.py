from models import Mood
import sqlite3
import json
from models import Entry

def get_all_entries():
    # Open a connection to the database
    with sqlite3.connect("./dailyjournal.db") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            e.id,
            e.date,
            e.concept,
            e.entry,
            e.mood_id,
            m.mood mood
        FROM Entries e
        LEFT JOIN Moods m
            ON m.id = e.mood_id
        """)
       
        # Initialize an empty list to hold all entry representations
        entries = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an entry instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # entry class above.
            entry = Entry(row['id'], row['date'], row['concept'],
                            row['entry'], row['mood_id'],
                            )
            # Create a Mood instance from the current row                
            mood = Mood(row['id'], row['mood'], )
            # Add the dictionary representation of the mood to the entry
            entry.mood = mood.__dict__

            entries.append(entry.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(entries)

def get_single_entry(id):
    with sqlite3.connect("./dailyjournal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            e.id,
            e.date,
            e.concept,
            e.entry,
            e.mood_id
        FROM entries e
        WHERE e.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an entry instance from the current row
        entry = Entry(data['id'], data['date'], data['concept'],
                    data['entry'], data['mood_id'])

        return json.dumps(entry.__dict__)

def get_entry_by_search(phrase):
    with sqlite3.connect("./dailyjournal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            e.id,
            e.date,
            e.concept,
            e.entry,
            e.mood_id,
            m.mood mood
        FROM Entries e
        LEFT JOIN Moods m
            ON m.id = e.mood_id
        WHERE e.concept LIKE ?
        """, ( f"%{phrase}%", ))

        entries = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            # Create an entry instance from the current row
            entry = Entry(row['id'], row['date'], row['concept'],
                        row['entry'], row['mood_id'])
            # Create a Mood instance from the current row                
            mood = Mood(row['id'], row['mood'], )
            # Add the dictionary representation of the mood to the entry
            entry.mood = mood.__dict__

            entries.append(entry.__dict__)

    return json.dumps(entries)

def create_entry(new_entry):
    with sqlite3.connect("./dailyjournal.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Entries
            (date, concept, entry, mood_id)
        VALUES
            (?, ?, ?, ?);
        """, (new_entry['date'], new_entry['concept'],
            new_entry['entry'], new_entry['mood_id'],))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_entry['id'] = id


    return json.dumps(new_entry)

def delete_entry(id):
    with sqlite3.connect("./dailyjournal.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM entries
        WHERE id = ?
        """, (id, ))

def update_entry(id, new_entry):
    with sqlite3.connect("./dailyjournal.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Entries
            SET
                date = ?,
                concept = ?,
                entry = ?,
                mood_id = ?
        WHERE id = ?
        """, (new_entry['date'], new_entry['concept'],
            new_entry['entry'], new_entry['mood_id'],
            id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True