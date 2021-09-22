from geoalchemy2 import functions as geoFunctions
from geoalchemy2 import Geometry
from geoalchemy2.elements import WKTElement
from geoalchemy2.shape import to_shape
from shapely.ops import transform
from sqlalchemy import Column, DateTime, JSON, Integer, PrimaryKeyConstraint, Sequence, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import functions as sqlFunctions

import pyproj

Base = declarative_base()
dbSrid = 4326


class Polygon(Base):
    __tablename__ = 'gis_polygon'

    # https://stackoverflow.com/questions/13370317/sqlalchemy-default-datetime
    _created = Column(DateTime(timezone=False), server_default=sqlFunctions.now())
    _update = Column(DateTime(timezone=False), onupdate=sqlFunctions.now())
    id = Column(Integer(), Sequence(f'{__tablename__}_id_seq'), nullable=False, primary_key=True)

    class_id = Column(Integer())
    name = Column(String())
    props = Column(JSON())
    geom = Column(Geometry('POLYGON', dbSrid))
    PrimaryKeyConstraint(id, name=f'{__tablename__}_pkey')

    def __init__(self, data, srid=dbSrid):
        assert type(data) is dict

        for key, value in data.items():
            self._setItem(key, value, srid)

        return

    def _getItem(self, key, srid):
        assert key is not None
        assert type(key) is str
        assert srid is not None
        assert type(srid) is int

        value = getattr(self, key)
        if value is not None:
            if (key == 'geom'):
                if (srid != dbSrid):
                    dbCrs = pyproj.CRS(f'EPSG:{dbSrid}')
                    myCrs = pyproj.CRS(f'EPSG:{srid}')
                    project = pyproj.Transformer.from_crs(dbCrs, myCrs, always_xy=True).transform
                    value = transform(project, value)
        return str(value)

    def _setItem(self, key, value, srid):
        assert key is not None
        assert value is not None
        assert srid is not None

        if (key == 'geom'):
            value = WKTElement(value)
            if (srid != dbSrid):
                myCrs = pyproj.CRS(f'EPSG:{srid}')
                dbCrs = pyproj.CRS(f'EPSG:{dbSrid}')
                project = pyproj.Transformer.from_crs(myCrs, dbCrs, always_xy=True).transform
                value = transform(project, value)
        setattr(self, key, value)

        return

    def update(self, data, srid=dbSrid):
        for key, value in data.items():
            self._setItem(key, value, srid)

        return

    def read(self, srid=dbSrid):
        data = {}
        for column in self.__table__.columns:
            data[column.name] = self._getItem(column.name, srid)

        return data
