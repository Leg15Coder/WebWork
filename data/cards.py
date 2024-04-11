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


class CardView(object):
    def __init__(self, card: Card):
        self.name = card.name
        self.id = card.id
        self.img = f'img/cards/{card.id}.png'
        self.field = card.field
        self.field_img = f'img/fields/{self.field}.png'
        self.about_all = card.about
        if len(card.about) > 61:
            self.about = card.about[:61] + '...'
        else:
            self.about = card.about

    def __repr__(self):
        return f"<CARDVIEW {self.id} {self.name}>"
