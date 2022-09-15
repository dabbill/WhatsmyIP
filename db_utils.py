#!/usr/bin/python3
import os
import sqlite3

# DB Connection
def db_connect(path, dbname):
    dbpath = os.path.join(path, dbname)
    con = sqlite3.connect(dbpath)
    return con

# DB Functions
def create_address(con, new_ip, old_ip):
    sql = """
        INSERT INTO address (new_ip, old_ip)
        VALUES (?, ?)"""
    cur = con.cursor()
    cur.execute(sql, (new_ip, old_ip))
    return cur.lastrowid

# query DB for old IP
def queryIP(cur):
    cur.execute("select * from address order by id desc limit 1")
    result = cur.fetchone()
    return result
