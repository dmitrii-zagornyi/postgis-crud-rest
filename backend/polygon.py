from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import functions as sqlFunctions

from geoalchemy2 import functions as geoFunctions
from geoalchemy2 import Geometry


Base = declarative_base()
dbSrid = 4326


class GisPolygon(Base):
    __tablename__ = 'gis_polygon'

    # https://stackoverflow.com/questions/13370317/sqlalchemy-default-datetime
    _created = Column(DateTime(), server_default=sqlFunctions.now())
    _update = Column(DateTime(), onupdate=sqlFunctions.now())
    id = Column(Integer(), Sequence(f'{__tablename__}_id_seq'), nullable=False, primary_key=True)

    class_id = Column(Integer())
    name = Column(String())
    props = Column(JSON())
    geom = Column(Geometry('POLYGON', dbSrid))
    PrimaryKeyConstraint(id, name=f'{__tablename__}_pkey')
    
    def __init__(self, class_id=None, name=None, props=None, geom=None):
        self.class_id = class_id
        self.name = name
        self.props = props
        self.geom = geom
        
        self._srid = dbSrid
        return
    
    def _getSridTransform(self, srid):
        return self._srid
    
    def __getitem__(self, key):
        value = getattr(self, self.__table__.columns[key])
        if (key == 'geom'):
            if (self._srid != dbSrid):
                value = geoFunctions.ST_Transform(value, self._srid)
            value = geoFunctions.ST_AsText(value)
        return
    
    def __setitem__(self, key, value):
        if (key == 'geom'):
            value = geoFunctions.ST_GeomFromText(value)
            if (self._srid != dbSrid):
                value = geoFunctions.ST_Transform(value, self._srid)
        setattr(self, self.__table__.columns[key], value)
        return
    
    def getSrid(self):
        return self._srid
    
    def setSrid(self, srid):
        self._srid = srid        
        return