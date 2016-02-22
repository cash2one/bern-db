import json
from getpass import getpass
from datetime import datetime
from flask.ext.script import Manager
from bern_db import create_app
from bern_db.extensions import db
from bern_db.users.models import User, Role
from bern_db.api.models import Quote, Tag

app = create_app()
manager = Manager(app)

@manager.command
def initdb():
    """Init/reset database"""
    pw = getpass(prompt="Admin password: ")

    db.drop_all()
    db.create_all()

    roles = [Role(name="superuser", description="Administrative user")]
    admin = User(
        first_name="admin",
        last_name="",
        email="admin@localhost",
        password=pw,
        active=True,
        confirmed_at=datetime.now(),
        roles=roles,
    )

    db.session.add(admin)
    db.session.commit()


@manager.command
def loadfixtures():
    """Load fixtures"""

    data = {}
    with open("fixtures.json") as f:
        data = json.load(f)

    for tag in data.get("tags"):
        print("Inserting Tag: {}".format(tag))

        tag_model = Tag(
            name=tag
        )
        db.session.add(tag_model)


    for quote in data.get("quotes"):
        print("Inserting Quote: {}".format(quote.get("text")[:30]))

        tags = Tag.query.filter(Tag.name.in_(quote.get("tags"))).all()
        quote_model = Quote(
            text=quote.get("text"),
            author=quote.get("author"),
            date=datetime.strptime(quote.get("date"), "%Y/%m/%d").date(),
            credit=quote.get("source").get("credit"),
            credit_url=quote.get("source").get("credit_url"),
            source_url=quote.get("source").get("url"),
            tags=tags
        )
        db.session.add(quote_model)

    db.session.commit()

if __name__ == "__main__":
    manager.run()
