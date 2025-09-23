# app.py

from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import random
import numpy as np
from datetime import datetime, timedelta

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Define the Album database model
class Album(db.Model):
    __tablename__ = 'albums'
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=True)
    suggestor = db.Column(db.String(100), nullable=False)
    reviewed = db.Column(db.Boolean, default=False, nullable=False)
    reviews = db.relationship("Review", back_populates="album")
    def __repr__(self):
        return f"Album('{self.artist}', '{self.title}', '{self.suggestor}')"


# Define the User database model (for future use)
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    reviews = db.relationship("Review",back_populates="user")

    def __repr__(self):
        return f"User('{self.username}')"

class Review(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    review_text = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    album_id  = db.Column(db.Integer, db.ForeignKey('albums.id'))
    user = db.relationship("User", back_populates="reviews")
    album = db.relationship("Album", back_populates="reviews")

weekly_pick = None
last_updated = None

def get_weekly_album():
    global weekly_pick, last_updated

    # Check if a week has passed since the last pick
    if weekly_pick is None or datetime.now() > last_updated + timedelta(days=1):
        if weekly_pick is not None:
            weekly_pick = db.session.merge(weekly_pick)  # add the weekly pick back to the db session
            weekly_pick.reviewed = True
            db.session.commit()
        all_albums = Album.query.filter_by(reviewed=False).all()
        if all_albums:
            weekly_pick = random.choice(all_albums)
            last_updated = datetime.now()

    return weekly_pick, last_updated

@app.route("/")
def home():
    all_albums = Album.query.all()
    all_users = User.query.all()
    album_of_the_week, time = get_weekly_album()
    next_update = time + timedelta(weeks=1)
    next_update = next_update.strftime("%A, %B %d at %I:%M %p")
    return render_template("home.html", albums=all_albums, weekly_pick=album_of_the_week, users=all_users, next_update=next_update)


@app.route("/admin")
def admin():
    all_albums = Album.query.all()
    album_of_the_week = get_weekly_album()

    return render_template("admin_home.html", albums=all_albums, weekly_pick=album_of_the_week)

@app.route("/add_new_album", methods=["POST"])
def add_new_album():
    global album_id_counter

    # Check if the request method is POST
    if request.method == "POST":
        # Get the data from the form
        artist = request.form["artist"]
        title = request.form["title"]
        user_id = request.form["user_id"]
        year = request.form["year"]
        # Create a new album dictionary
        new_album = Album(artist=artist, title=title, suggestor=user_id, year=year)
        # Add the new album to the global list
        db.session.add(new_album)

        db.session.commit()

        # Redirect the user back to their profile page
        return redirect(url_for("show_user_profile", username=user_id))

@app.route("/new_user_page")
def new_user_page():
    return render_template("new_user_page.html")

@app.route("/add_new_user", methods=["POST"])
def add_new_user():
    if request.method == "POST":
        username = request.form["username"]
        existing_user = User.query.filter(User.username == username).first()
        if existing_user is None:
            new_user = User(username=username)
            db.session.add(new_user)
            db.session.commit()

        return redirect(url_for("show_user_profile", username=username))

@app.route("/add_review", methods=["POST"])
def add_review():
    if request.method == "POST":
        rating = request.form["rating"]
        review_text = request.form["review_text"]
        user_id = request.form["user_id"]
        username = request.form["username"]
        album_id = request.form["album_id"]
        new_review = Review(rating=rating,review_text=review_text,user_id=user_id,album_id=album_id)
        db.session.add(new_review)
        db.session.commit()

        return redirect(url_for("show_user_profile", username=username))

@app.route("/u/<string:username>")
def show_user_profile(username):
    global weekly_pick
    user = User.query.filter_by(username=username).first_or_404()
    if user:
        weekly_pick_reviewed = Review.query.filter_by(user=user, album=weekly_pick).first()
        if weekly_pick_reviewed:
            return render_template("profile.html", user=user, weekly_pick=weekly_pick, reviewed=True)
        else:
            return render_template("profile.html", user=user, weekly_pick=weekly_pick, reviewed=False)
    else:
        return "user not found!"

@app.route("/album/<int:album_id>")
def show_album_details(album_id):
    # Find the album with the matching ID
    album = Album.query.get_or_404(album_id)
    if album:
        ratings = [review.rating for review in album.reviews]
        average_rating = np.average(ratings)
        return render_template("album_details.html", album=album, average_rating=average_rating)
    else:
        return "<h1>Album not found!</h1>", 404

@app.route("/pick_new_album", methods=["POST"])
def pick_new_album():
    global weekly_pick, last_updated

    if weekly_pick:
        weekly_pick = db.session.merge(weekly_pick) #add the weekly pick back to the db session
        weekly_pick.reviewed = True
        db.session.commit()

    # Force a new pick, regardless of the timer
    albums = Album.query.filter_by(reviewed=False).all()
    if albums:
        new_pick = random.choice(albums)
        weekly_pick = new_pick
        last_updated = datetime.now()

    # Redirect the user back to the home page
    return redirect(url_for("home"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
