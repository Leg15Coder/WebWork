import sqlalchemy as sa
from .db_session import SqlAlchemyBase


class Card(SqlAlchemyBase):
    __tablename__ = 'cards'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=True)
    about = sa.Column(sa.String, nullable=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return f"<CARD {self.id} {self.name}>"
