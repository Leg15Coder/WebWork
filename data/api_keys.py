import sqlalchemy as sa
from .db_session import SqlAlchemyBase


class KeyAPI(SqlAlchemyBase):
    __tablename__ = 'keys_api'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    key = sa.Column(sa.String, nullable=True)
    is_post = sa.Column(sa.Boolean, nullable=False, default=False)
    is_admin = sa.Column(sa.Boolean, nullable=False, default=False)
    limit = sa.Column(sa.Integer, default=100)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return f"<API KEY {self.id}>"
