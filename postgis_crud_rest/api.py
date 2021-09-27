import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from postgis_crud_rest.polygon import Polygon


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


connectionString = "postgresql://postgres:qazwsx@localhost:5432/postgres"


class Api(metaclass=Singleton):
    def __init__(self, connectionString):
        self._engine = create_engine(connectionString, echo=True)
        self._session = sessionmaker(self._engine)
        Polygon.__table__.create(bind=self._engine, checkfirst=True)
        return

    def jsonToData(jsonData):
        data = json.loads(jsonData)
        if 'srid' in data:
            srid = data.pop('srid', None)
        else:
            srid = Polygon.getSrid()
        return data, srid

    def createOrUpdatePolygon(self, jsonData):
        data, srid = Api.jsonToData(jsonData)

        with self._session.begin() as session:
            polygon = None
            if 'id' in data:
                polygon = session.query(Polygon).filter_by(id=data['id']).first()

            if polygon is None:
                polygon = Polygon(data, srid)
                session.add(polygon)
            else:
                polygon.update(data, srid)

        return

    def deletePolygon(self, jsonData):
        data, _ = Api.jsonToData(jsonData)
        assert 'id' in data

        with self._session.begin() as session:
            polygon = session.query(Polygon).filter_by(id=data['id']).first()
            session.delete(polygon)
        return

    def getPolygons(self, jsonData=None):
        if jsonData is not None:
            _, srid = Api.jsonToData(jsonData)
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

        return

