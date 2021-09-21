import sqlalchemy as sq
from sqlalchemy import create_engine


if __name__ == "__main__":
    engine = create_engine("postgresql://postgres:qazwsx@localhost:5432/postgres", echo=True)
    print(sq.inspect(engine).get_schema_names())
