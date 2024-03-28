import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import json


with open("data/cards.json", 'w') as f:
    data = [
        {
            "id": 1,
            "name": "",
            "about": "",
            "field": ""
        },
        {
            "id": 2,
            "name": "",
            "about": "",
            "field": ""
        },
        {
            "id": 3,
            "name": "",
            "about": "",
            "field": ""
        },
        {
            "id": 4,
            "name": "",
            "about": "",
            "field": ""
        },
        {
            "id": 5,
            "name": "",
            "about": "",
            "field": ""
        },
        {
            "id": 6,
            "name": "",
            "about": "",
            "field": ""
        },
    ]
    json.dump(data, f, indent=4)


SqlAlchemyBase = orm.declarative_base()

__factory = None


def global_init(db_file):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    if not __factory:
        global_init('db/db.db')
    return __factory()
