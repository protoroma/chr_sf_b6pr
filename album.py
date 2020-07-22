import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()

class Album(Base):
    """
    Структура album 
    """
    __tablename__="album"

    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)

def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

def find(artist):
    """
    Находит все альбомы в базе данных по заданному артисту
    """
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).all()
    return albums

class Error(Exception):
    pass

class AlreadyExists(Error):
    """
    Используется для проверки вводимых данных
    """
    pass

def check_data(year, artist, genre, album):
    """
    Проверка введенных данных с уже существующими в БД и сохранение их в эту БД
    """
    assert isinstance(year, int), "Неправильный тип данных. Пример: 1970"
    assert isinstance(artist, str), "Неправильный тип данных. Пример: Beatles"
    assert isinstance(genre, str), "Неправильный тип данных. Пример: Rock"
    assert isinstance(album, str), "Неправильный тип данных. Пример: Altered State"
    
    session = connect_db()
    
    save_data = session.query(Album).filter(Album.artist == artist, Album.album == album).first()
    
    if save_data is not None:
        raise AlreadyExists("Альбом уже был добавлен и имеет #{}".format(save_data.id))

    album = Album(
        year=year,
        artist=artist,
        genre=genre,
        album=album
    )

    session.add(album)
    session.commit()
    return album