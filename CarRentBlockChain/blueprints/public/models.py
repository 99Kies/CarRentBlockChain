# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt

from flask_login import UserMixin

from CarRentBlockChain.database import (
    Column,
    Model,
    SurrogatePK,
    db,
    reference_col,
    relationship,
)
from CarRentBlockChain.extensions import bcrypt
from CarRentBlockChain.privkeyutils.privkeyutils import create_random_address

class Role(SurrogatePK, Model):
    """A role for a user."""
    __bind_key__ = 'userserver'
    __tablename__ = "roles"
    name = Column(db.String(80), unique=True, nullable=False)
    user_id = reference_col("users", nullable=True)
    user = relationship("User", backref="roles")

    def __init__(self, name, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Role({self.name})>"

class User(UserMixin, SurrogatePK, Model):
    """A user of the app."""
    __bind_key__ = 'userserver'
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=False)
    iphone = Column(db.String(12), unique=True, nullable=True)
    idcard = Column(db.String(30), unique=True, nullable=True)
    status = Column(db.String(20), nullable=True)
    # car / user / admin
    #: The hashed password
    password = Column(db.LargeBinary(128), nullable=True)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    active = Column(db.Boolean(), default=False)
    is_admin = Column(db.Boolean(), default=False)

    privkey = Column(db.String(64), nullable=False)

    privatekey_hex = Column(db.String(66), nullable=False)
    privatekey_int = Column(db.String(256), nullable=False)

    publickey_hex = Column(db.String(130), nullable=False)
    publickey_int = Column(db.String(256), nullable=False)

    address = Column(db.String(42), nullable=False)

    chainnumber = Column(db.Integer, nullable=True, default=-1)


    def __init__(self, username, email, password=None, **kwargs):
        """Create instance."""
        db.Model.__init__(self, username=username, email=email, **kwargs)

        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        """Set password."""
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password, value)

    @property
    def full_name(self):
        """Full user name."""
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<User({self.username!r})>"
