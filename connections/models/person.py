from connections.database import CreatedUpdatedMixin, CRUDMixin, db, Model
from connections.models.connection import Connection, ConnectionType


class MutualFriendsMixin:
    """Person speficic, in order to select mutual friends."""

    def mutual_friends(self, target):
        """Return Persons that are (one-way) mutual friends.

        Return all Persons that are "to person" with
        a "friend" connection to "instance" and "target" Person
        in the same time

        Probably, makes sense to make it work in "both ways",
        regardless from/to position
        """
        return db.session.query(Person).filter(
            Person.id.in_([
                conn.to_person_id
                for conn in
                db.session.query(Connection).filter(
                    (Connection.from_person_id == self.id) |
                    (Connection.from_person_id == target.id),
                    Connection.connection_type == ConnectionType.friend
                ).all()
            ])
        ).all()


class Person(Model, CRUDMixin, CreatedUpdatedMixin, MutualFriendsMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(145), unique=True, nullable=False)

    connections = db.relationship('Connection', foreign_keys='Connection.from_person_id')
