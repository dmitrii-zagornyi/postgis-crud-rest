from shapely.geometry import Polygon as sgPolygon
from nose.tools import assert_equals, nottest

from postgis_crud_rest.polygon import Polygon


class test_polygon():
    sgPolygonPoints = [[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]

    def test_creation_empty(self):
        data = {}
        polygon = Polygon(data)
        assert polygon is not None
        return

    def test_creation_simple(self):
        data = {'name': 'test'}
        polygon = Polygon(data)
        assert polygon is not None
        return

    def test_creation_with_geom(self):
        data = {'name': 'test', 'geom': sgPolygon(self.sgPolygonPoints).wkt}
        polygon = Polygon(data)
        assert polygon is not None
        return

    def test_creation_with_geom_srid(self):
        data = {'name': 'test', 'geom': sgPolygon(self.sgPolygonPoints).wkt}
        polygon = Polygon(data, srid=4326)
        assert polygon is not None
        return

    def test_creation_with_srid_without_geom(self):
        data = {'name': 'test'}
        polygon = Polygon(data, srid=4326)
        return

    def test_read(self):
        data = {'name': 'test'}
        polygon = Polygon(data)
        readData = polygon.read()

        for key in data.keys():
            assert data[key] == readData[key]
        return

    def test_read_geom(self):
        data = {'name': 'test', 'geom': sgPolygon(self.sgPolygonPoints).wkt}
        polygon = Polygon(data)
        readData = polygon.read()

        for key in data.keys():
            assert data[key] == readData[key]
        return

    def test_read_geom_srid(self):
        data = {'name': 'test', 'geom': sgPolygon(self.sgPolygonPoints).wkt}
        polygon = Polygon(data, 32644)
        readData = polygon.read(srid=32644)

        for key in data.keys():
            assert data[key] == readData[key]
        return

    def test_read_srid_without_geom(self):
        data = {'name': 'test'}
        polygon = Polygon(data, 32644)
        readData = polygon.read(srid=32644)

        for key in data.keys():
            assert data[key] == readData[key]
        return

    def test_update(self):
        data_first = {'name': 'test', 'geom': sgPolygon(self.sgPolygonPoints).wkt}
        polygon = Polygon(data_first)
        data_second = {'geom': sgPolygon(self.sgPolygonPoints).wkt}
        polygon.update(data_second)
        readData = polygon.read()

        data = data_first
        data.update(data_second)
        for key in data.keys():
            assert data[key] == readData[key]
        return
