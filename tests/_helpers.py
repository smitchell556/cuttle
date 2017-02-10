# -*- coding: utf-8 -*-
"""

Query functions for validating tests.

"""
import mysql.connector


def _mysql_query(config, query):
    con, cur, res = None, None, None
    try:
        con = mysql.connector.connect(user=config['USER'],
                                      host=config['HOST'],
                                      passwd=config['PASSWD'],
                                      db=config['DB'])
        cur = con.cursor()
        cur.execute(query)
        res = cur.fetchall()
    except:
        if con is not None:
            con.rollback()
    finally:
        if cur is not None:
            cur.close()
        if con is not None:
            con.close()

    return res

def _mysql_insert(config, query):
    con, cur, res = None, None, None
    try:
        con = mysql.connector.connect(user=config['USER'],
                                      host=config['HOST'],
                                      passwd=config['PASSWD'],
                                      db=config['DB'])
        cur = con.cursor()
        cur.execute(query)
        con.commit()
    except:
        if con is not None:
            con.rollback()
    finally:
        if cur is not None:
            cur.close()
        if con is not None:
            con.close()

    return res
