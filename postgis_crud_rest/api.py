import json
from enum import Enum
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from postgis_crud_rest.polygon import Polygon


class Status(Enum):
    Created = 1
    Updated = 2
    Deleted = 3


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Api(metaclass=Singleton):
    def __init__(self, connectionString):
        self._engine = create_engine(connectionString, echo=True)
        self._session = sessionmaker(self._engine)
        Polygon.__table__.create(bind=self._engine, checkfirst=True)
        return

    def _jsonToData(jsonData):
        data = json.loads(jsonData)
        if 'srid' in data:
            srid = data.pop('srid', None)
        else:
            srid = Polygon.getSrid()
        return data, srid

    def createOrUpdatePolygon(self, jsonData):
        data, srid = Api._jsonToData(jsonData)

        with self._session.begin() as session:
            polygon = None
            if 'id' in data:
                polygon = session.query(Polygon).filter_by(id=data['id']).first()

            if polygon is None:
                polygon = Polygon(data, srid)
                session.add(polygon)
                status = Status.Created
            else:
                polygon.update(data, srid)
                status = Status.Updated

        return status

    def deletePolygon(self, jsonData):
        data, _ = Api._jsonToData(jsonData)
        assert 'id' in data

        with self._session.begin() as session:
            polygon = session.query(Polygon).filter_by(id=data['id']).first()
            session.delete(polygon)
        return Status.Deleted

    def getPolygons(self, jsonData=None):
        if jsonData is not None:
            _, srid = Api._jsonToData(jsonData)
        else:
            srid = Polygon.getSrid()

        polygonsData = []
        with self._session.begin() as session:
            for polygon in session.query(Polygon).all():
                polygonsData.append(polygon.read(srid))

        return json.dumps(polygonsData)

    def deleteAllPolygons(self):
        with self._session.begin() as session:
            session.query(Polygon).delete()
        return Status.Deleted
