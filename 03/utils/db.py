import os
import logging
from multiprocessing import Queue
from queue import Empty

import sqlalchemy as db
from sqlalchemy.engine import Engine
from sqlalchemy.sql import text

@staticmethod
def store_next_symbol(queue: Queue):
    while True:
        try:
            val = queue.get(timeout=20)
        except Empty:
            logging.warning('Queue timeout reached, stopping')
            break
        if val == 'DONE':
            break
        symbol, price, datetime = val
        _insert(symbol, price, datetime)

@staticmethod
def _get_sqlite_connection() -> Engine:
    """
    Reads the SQLITE_DB_PATH environment variable and returns a SQLAlchemy engine
    connected to the specified local SQLite file.
    """
    db_path = os.environ.get("SQLITE_DB_PATH", "local.db")
    engine = db.create_engine(f"sqlite:///{db_path}")
    return engine

@staticmethod
def _insert(symbol: str, price: float, datetime: float):
    sql = f"""INSERT into prices (date, symbol, price) VALUES (:date, :symbol, :price)"""
    with _get_sqlite_connection().connect() as conn:
        conn.execute(text(sql), {'date': datetime, 'symbol': symbol, 'price': price})
        conn.commit()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    engine = _get_sqlite_connection()
    yahoo_obj = db.MetaData()
    price = db.Table(
        'prices',                                        
        yahoo_obj,                                    
        db.Column('date', db.DateTime),  
        db.Column('symbol', db.String),                    
        db.Column('price', db.Double))
    yahoo_obj.create_all(engine)

    # _insert('A',10.0,datetime.datetime.now())
    # _insert('A',10.0,datetime.datetime.now())
