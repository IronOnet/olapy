from __future__ import absolute_import, division, print_function

import os
from sqlalchemy import create_engine
# from .olapy_config_file_parser import DbConfigParser


# todo cleannnnnnnnnnnn

def _get_dbms_from_conn_string(conn_string):
    db = conn_string.split(':')[0]
    if '+' in db:
        db = db.split('+')[0]
    # just for postgres
    db = db.replace('postgresql', 'postgres')
    return db


def _get_init_table(dbms):
    if dbms.upper() == 'POSTGRES':
        con_db = '/postgres'
        engine = 'postgresql+psycopg2'
    elif dbms.upper() == 'MYSQL':
        con_db = ''
        engine = 'mysql+mysqldb'
    elif dbms.upper() == 'MSSQL':
        con_db = 'msdb'
        engine = 'mssql+pyodbc'
    elif dbms.upper() == 'ORACLE':
        con_db = ''
        engine = 'oracle+cx_oracle'
    else:
        con_db = ''
        engine = ''

    return engine, con_db


def _connect_to_mssql(db_credentials, driver='mssql+pyodbc', db=None):
    # todo recheck + clean
    sql_server_driver = db_credentials['sql_server_driver'].replace(' ', '+')
    if db is not None:
        return create_engine(driver + '://(local)/{0}?driver={1}'.format(db, sql_server_driver), encoding='utf-8')

    if 'LOCALHOST' in db_credentials['user'].upper() or not db_credentials['user']:
        return create_engine(driver + '://(local)/msdb?driver={0}'.format(sql_server_driver))
    else:
        return create_engine(driver + '://{0}:{1}@{2}:{3}/msdb?driver={4}'.format(db_credentials['user'],
                                                                                  db_credentials['password'],
                                                                                  db_credentials['host'],
                                                                                  db_credentials['port'],
                                                                                  sql_server_driver))


def _construct_engine(db, db_credentials):
    eng, con_db = _get_init_table(db_credentials['dbms'])
    if db is None:
        if db_credentials['dbms'].upper() == 'MSSQL':
            return _connect_to_mssql(db_credentials.replace(' ', '+'))
        else:
            # Show all databases to user (in excel)
            return create_engine(
                '{0}://{1}:{2}@{3}:{4}{5}'.format(eng, db_credentials['user'], db_credentials['password'],
                                                  db_credentials['host'],
                                                  db_credentials['port'],
                                                  con_db), encoding='utf-8')

    else:
        if db_credentials['dbms'].upper() == 'MSSQL':
            return _connect_to_mssql(db=db, db_credentials=db_credentials)
        else:
            # and then we connect to the user db
            return create_engine(
                '{0}://{1}:{2}@{3}:{4}/{5}'.format(eng, db_credentials['user'], db_credentials['password'],
                                                   db_credentials['host'], db_credentials['port'],
                                                   '' if db_credentials['dbms'].upper() == 'ORACLE' else db),
                encoding='utf-8')


class MyDB(object):
    """Connect to sql database (postgres only right now)."""

    def __init__(self, db_config, db=None):

        if 'SQLALCHEMY_DATABASE_URI' in os.environ.keys():
            conn_string = os.environ["SQLALCHEMY_DATABASE_URI"]
            if db is not None:
                # todo test this with windows
                conn_string = (conn_string + '/' + db)
            self.engine = create_engine(conn_string)
            self.dbms = _get_dbms_from_conn_string(conn_string)
            # oracle://scott:tiger@127.0.0.1:1521/sidname
            self.username = conn_string.split(':')[1].replace('//', '')

        else:
            db_credentials = db_config.get_db_credentials()
            self.dbms = db_credentials['dbms']
            self.username = db_credentials['user']
            self.engine = _construct_engine(db, db_credentials)

    def __del__(self):
        if hasattr(self, 'connection'):
            self.engine.dispose()
