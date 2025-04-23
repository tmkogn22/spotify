from pydantic import BaseModel
from typing import List


class ArtistBase(BaseModel):
    name: str
    description: str


class ArtistCreate(ArtistBase):
    pass


class Artist(ArtistBase):
    id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_admin: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class AlbumBase(BaseModel):
    title: str
    artist_id: int
    description: str


class AlbumCreate(AlbumBase):
    pass


class Album(AlbumBase):
    id: int

    class Config:
        from_attributes = True


class GenreBase(BaseModel):
    name: str


class GenreCreate(GenreBase):
    pass


class Genre(GenreBase):
    id: int

    class Config:
        from_attributes = True


class CompositionBase(BaseModel):
    title: str
    lyrics: str
    album_id: int

    class Config:
        from_attributes = True


class CompositionCreate(CompositionBase):
    genres: List[int]

    class Config:
        from_attributes = True


class Composition(CompositionBase):
    id: int

    class Config:
        from_attributes = True
