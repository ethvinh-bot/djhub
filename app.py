# app.py
from flask import Flask, render_template, request, jsonify
from datetime import date
from sqlalchemy import or_

from djhub.extensions import db  # db = SQLAlchemy() lives here

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///djhub.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Bind the SQLAlchemy instance to this app
db.init_app(app)

# Import models AFTER db.init_app so they use the bound instance
from djhub.models import Listing  # noqa: E402


# Home feed: show listings only (paged)
@app.route("/")
@app.route("/listings")
def listings_feed():
    today = date.today()
    page = request.args.get("page", 1, type=int)
    per_page = 10

    pagination = (
        Listing.query
        .filter(or_(Listing.date == None, Listing.date >= today))  # noqa: E711
        .order_by(Listing.date.asc(), Listing.created_at.desc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return render_template(
        "index.html",
        listings=pagination.items,
        has_next=pagination.has_next,
        next_page=pagination.next_num,
    )


# JSON for "Load more" button
@app.get("/api/listings")
def api_listings():
    today = date.today()
    page = request.args.get("page", 1, type=int)
    per_page = 10

    pagination = (
        Listing.query
        .filter(or_(Listing.date == None, Listing.date >= today))  # noqa: E711
        .order_by(Listing.date.asc(), Listing.created_at.desc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    data = [
        {
            "title": l.title,
            "city": l.city,
            "date": l.date.isoformat() if l.date else None,
            "budget": l.budget,
            "genres": l.genres,
            "description": l.description or "",
        }
        for l in pagination.items
    ]

    return jsonify(
        {"listings": data, "has_next": pagination.has_next, "next_page": pagination.next_num}
    )


if __name__ == "__main__":
    # Optional convenience: create tables if not present when running locally
    with app.app_context():
        db.create_all()
    app.run(debug=True)
