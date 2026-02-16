# create_db.py

from main import app, db, Album, spotifyInst
import os

with app.app_context():
    # Check if the database file exists
    if os.path.exists('instance/site.db'):
        print("Database already exists. Deleting and recreating...")
        os.remove('instance/site.db')

    # Create the database and tables
    db.create_all()
    print("Database created successfully!")

    spotify_links = [
        "https://open.spotify.com/album/3PRoXYsngSwjEQWR5PsHWR?si=d3Zz6_dNTv275Qf34WZ3Vw",
        "https://open.spotify.com/album/6QaVfG1pHYl1z15ZxkvVDW?si=BX1l8J7uREWIAY4tXwZfTg",
        "https://open.spotify.com/album/0ETFjACtuP2ADo6LFhL6HN?si=k_tHgaP5ThqUX3xy_oqI-A",
        "https://open.spotify.com/album/48D1hRORqJq52qsnUYZX56?si=J6YtTN1IQ_SKFktpksLLcQ",
        "https://open.spotify.com/album/1To7kv722A8SpZF789MZy7?si=rq9CwBPDQS6gdwZCVo1SmQ",
        "https://open.spotify.com/album/6r7LZXAVueS5DqdrvXJJK7?si=FZBHhbMqS0e2f_-gjzBcmQ",
        "https://open.spotify.com/album/7rSZXXHHvIhF4yUFdaOCy9?si=ZemjPvYITPiiDA2tw1q0JA",
        "https://open.spotify.com/album/1bt6q2SruMsBtcerNVtpZB?si=g6PflV3MQ4qePHUVjIizLw",
        "https://open.spotify.com/album/4LH4d3cOWNNsVw41Gqt2kv?si=eDCyW7iyQu2VVce0a9qeyQ",
        "https://open.spotify.com/album/0bCAjiUamIFqKJsekOYuRw?si=hHqFMqLZSJOU66QocuM4_Q",
        "https://open.spotify.com/album/3ycjBixZf7S3WpC5WZhhUK?si=zqdRQ2ueQmyK5EX7hOjOEw",
        "https://open.spotify.com/album/6dVIqQ8qmQ5GBnJ9shOYGE?si=vV0NJ2nSSN-SXVUiDUxP7A",
        "https://open.spotify.com/album/6YUCc2RiXcEKS9ibuZxjt0?si=EFgT3YsIR4uZmaXKNfiTZg"
    ]

#     # Add some initial data
#     initial_albums = [
#         Album(artist="The Beatles", title="Revolver", year=1966, suggestor="1001 albums", reviewed=False),
#         Album(artist="The Beatles", title="Sgt. Pepper's Lonely Hearts Club Band", year=1967, suggestor="1001 albums",
#               reviewed=False),
#         Album(artist="The Beatles", title="Abbey Road", year=1969, suggestor="1001 albums", reviewed=False),
#         Album(artist="David Bowie", title="The Rise and Fall of Ziggy Stardust and the Spiders from Mars", year=1972,
#               suggestor="1001 albums", reviewed=False),
#         Album(artist="Nirvana", title="MTV Unplugged in New York", year=1994, suggestor="1001 albums", reviewed=False),
#         Album(artist="Black Sabbath", title="Paranoid", year=1970, suggestor="1001 albums", reviewed=False),
#         Album(artist="Jimi Hendrix", title="Are You Experienced", year=1967, suggestor="1001 albums", reviewed=False),
#         Album(artist="Fleetwood Mac", title="Rumours", year=1977, suggestor="1001 albums", reviewed=False),
#         Album(artist="Pink Floyd", title="The Dark Side of the Moon", year=1973, suggestor="1001 albums",
#               reviewed=False),
#         Album(artist="Pink Floyd", title="Wish You Were Here", year=1975, suggestor="1001 albums", reviewed=False),
#         Album(artist="Nirvana", title="Nevermind", year=1991, suggestor="1001 albums", reviewed=False),
#         Album(artist="Led Zeppelin", title="Led Zeppelin", year=1969, suggestor="1001 albums", reviewed=False),
#         Album(artist="Led Zeppelin", title="Led Zeppelin II", year=1969, suggestor="1001 albums", reviewed=False),
#         Album(artist="Led Zeppelin", title="Led Zeppelin IV", year=1971, suggestor="1001 albums", reviewed=False),
#         Album(artist="Fleetwood Mac", title="Rumours", year=1977, suggestor="1001 albums", reviewed=False),
#         Album(artist="Radiohead", title="OK Computer", year=1997, suggestor="1001 albums", reviewed=False),
#         Album(artist="Stevie Wonder", title="Songs in the Key of Life", year=1976, suggestor="1001 albums",
#               reviewed=False)
#     ]

    for link in spotify_links:
        try:
            # Extract ID and fetch data
            album_id = link.split("album/")[1].split("?")[0]
            album_data = spotifyInst.album(album_id)

            # Calculate Duration
            total_ms = sum(track['duration_ms'] for track in album_data['tracks']['items'])
            total_seconds = int(total_ms / 1000)
            minutes, seconds = divmod(total_seconds, 60)
            hours, minutes = divmod(minutes, 60)
            
            duration_str = f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m {seconds}s"

            # Create Album Object
            new_album = Album(
                artist=album_data['artists'][0]['name'],
                url_id=album_id,
                title=album_data['name'],
                year=int(album_data['release_date'][:4]),
                cover_art=album_data['images'][0]['url'],
                num_songs=album_data['total_tracks'],
                duration=duration_str,
                suggestor="1001 albums",
                reviewed=False
            )
            db.session.add(new_album)
            print(f"Added: {new_album.title} by {new_album.artist}")

        except Exception as e:
            print(f"Error processing {link}: {e}")



#     for album in initial_albums:
#         db.session.add(album)

    # Commit the changes
    db.session.commit()
    print("Initial albums added.")