import sqlalchemy as sa
from .db_session import SqlAlchemyBase


association_table = sa.Table(
    'association',
    SqlAlchemyBase.metadata,
    sa.Column('cards', sa.Integer, sa.ForeignKey('cards.id')),
    sa.Column('users', sa.Integer, sa.ForeignKey('users.id'))
)


class Card(SqlAlchemyBase):
    __tablename__ = 'cards'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=True)
    about = sa.Column(sa.TEXT, nullable=True)
    field = sa.Column(sa.String, nullable=True)
    first_creation_component = sa.Column(sa.Integer, nullable=True)
    second_creation_component = sa.Column(sa.Integer, nullable=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return f"<CARD {self.id} {self.name}>"
