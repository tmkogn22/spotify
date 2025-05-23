from database.sync_db import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, unique=True)
    password_hash = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)

    playlists = relationship('Playlist', back_populates='user')
    favorite_compositions = relationship('Favorites', back_populates='user')


class Artist(Base):
    __tablename__ = 'artists'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)

    albums = relationship('Album', back_populates='artist')


class Genre(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, unique=True)

    compositions = relationship('CompositionGenreAssociation', back_populates='genre')


class Album(Base):
    __tablename__ = 'albums'
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False, unique=False)
    description = Column(String, nullable=True)
    artist_id = Column(Integer, ForeignKey('artists.id'), nullable=False)

    artist = relationship('Artist', back_populates='albums')
    compositions = relationship('Composition', back_populates='album')


class Composition(Base):
    __tablename__ = 'compositions'
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False, unique=False)
    lyrics = Column(String, nullable=True)
    file_path = Column(String, nullable=False)
    album_id = Column(Integer, ForeignKey('albums.id'), nullable=False)

    album = relationship('Album', back_populates='compositions')
    genres = relationship('CompositionGenreAssociation', back_populates='composition')
    liked = relationship('Favorites', back_populates='composition')


class CompositionGenreAssociation(Base):
    __tablename__ = 'composition_genre_m2m'

    composition_id = Column(Integer, ForeignKey('compositions.id'), primary_key=True, nullable=False)
    genre_id = Column(Integer, ForeignKey('genres.id'), primary_key=True, nullable=False)

    composition = relationship('Composition', back_populates='genres')
    genre = relationship('Genre', back_populates='compositions')


class Playlist(Base):
    __tablename__ = 'playlists'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship('User', back_populates='playlists')
    compositions = relationship('CompositionPlaylistAssociation', back_populates='playlist')


class CompositionPlaylistAssociation(Base):
    __tablename__ = 'composition_playlist_m2m'

    playlist_id = Column(Integer, ForeignKey('playlists.id'), nullable=False, primary_key=True)
    composition_id = Column(Integer, ForeignKey('compositions.id'), nullable=False, primary_key=True)

    playlist = relationship('Playlist', back_populates='compositions')
    composition = relationship('Composition')


class Favorites(Base):
    __tablename__ = 'favorites'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True, nullable=False)
    composition_id = Column(Integer, ForeignKey('compositions.id'), primary_key=True, nullable=False)

    user = relationship('User', back_populates='favorite_compositions')
    composition = relationship('Composition', back_populates='liked')


