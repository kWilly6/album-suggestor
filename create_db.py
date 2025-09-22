# create_db.py

from main import app, db, Album
import os

with app.app_context():
    # Check if the database file exists
    if os.path.exists('instance/site.db'):
        print("Database already exists. Deleting and recreating...")
        os.remove('instance/site.db')

    # Create the database and tables
    db.create_all()
    print("Database created successfully!")

    # Add some initial data
    initial_albums = [
        Album(artist="The Beatles", title="Revolver", year=1966, suggestor="1001 albums", reviewed=False),
        Album(artist="The Beatles", title="Sgt. Pepper's Lonely Hearts Club Band", year=1967, suggestor="1001 albums",
              reviewed=False),
        Album(artist="The Beatles", title="Abbey Road", year=1969, suggestor="1001 albums", reviewed=False),
        Album(artist="David Bowie", title="The Rise and Fall of Ziggy Stardust and the Spiders from Mars", year=1972,
              suggestor="1001 albums", reviewed=False),
        Album(artist="Nirvana", title="MTV Unplugged in New York", year=1994, suggestor="1001 albums", reviewed=False),
        Album(artist="Black Sabbath", title="Paranoid", year=1970, suggestor="1001 albums", reviewed=False),
        Album(artist="Jimi Hendrix", title="Are You Experienced", year=1967, suggestor="1001 albums", reviewed=False),
        Album(artist="Fleetwood Mac", title="Rumours", year=1977, suggestor="1001 albums", reviewed=False),
        Album(artist="Pink Floyd", title="The Dark Side of the Moon", year=1973, suggestor="1001 albums",
              reviewed=False),
        Album(artist="Pink Floyd", title="Wish You Were Here", year=1975, suggestor="1001 albums", reviewed=False),
        Album(artist="Nirvana", title="Nevermind", year=1991, suggestor="1001 albums", reviewed=False),
        Album(artist="Led Zeppelin", title="Led Zeppelin", year=1969, suggestor="1001 albums", reviewed=False),
        Album(artist="Led Zeppelin", title="Led Zeppelin II", year=1969, suggestor="1001 albums", reviewed=False),
        Album(artist="Led Zeppelin", title="Led Zeppelin IV", year=1971, suggestor="1001 albums", reviewed=False),
        Album(artist="Fleetwood Mac", title="Rumours", year=1977, suggestor="1001 albums", reviewed=False),
        Album(artist="Radiohead", title="OK Computer", year=1997, suggestor="1001 albums", reviewed=False),
        Album(artist="Stevie Wonder", title="Songs in the Key of Life", year=1976, suggestor="1001 albums",
              reviewed=False)
    ]

    for album in initial_albums:
        db.session.add(album)

    # Commit the changes
    db.session.commit()
    print("Initial albums added.")