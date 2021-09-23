# postgis-crud-rest
Implemented features:
1. PostGIS database for storing Polygons
2. Python API for DB access
3. Supporting various SRID
4. Python API for DB access

Continous Integration:
As a CI is used Github Actions (https://github.com/dmitrii-zagornyi/postgis-crud-rest/actions). Builds are triggered on commits and PRs to develop branch. For DB testing stared docker container with PostGIS database. Python environment with required packages created by miniconda. Test coverage not 100% of cases - this required more additional time. For REST API testing is started web service in separate process and is used python requests module. Flask have support of unittests, but this implementation require additional time for Flask investigation.
