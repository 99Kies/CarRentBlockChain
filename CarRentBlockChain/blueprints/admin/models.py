import datetime as dt

from CarRentBlockChain.database import (
    Column,
    Model,
    db,
)

from CarRentBlockChain.extensions import db


class CARCNT(db.Model):
    __tablename__ = "carcnt"
    chainNumber = db.Column(db.Integer, primary_key=True)
    carowner_privkey = db.Column(db.String(256), nullable=False)