from app import app
from djhub.extensions import db
from djhub.models import Profile, Listing
from datetime import datetime
import random

with app.app_context():
    db.drop_all()
    db.create_all()

    # create one or more profiles first (if your Listing references them later)
    profile = Profile(username="djuser", display_name="DJ User")
    db.session.add(profile)

    cities = ["New York", "Los Angeles", "Chicago", "Miami"]
    genres = ["House", "Techno", "Hip-Hop", "EDM"]

    for i in range(40):  # create 20 fake listings
        l = Listing(
            title=f"Event {i+1}",
            city=random.choice(cities),
            date=datetime(2025, 10, random.randint(1, 28)),
            budget=random.randint(100, 1000),
            genres=random.choice(genres),
            description=f"This is a description for Event {i+1}."
        )
        db.session.add(l)

    db.session.commit()
    print("Seeded database with fake listings!")



