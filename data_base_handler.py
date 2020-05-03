#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  2 17:03:03 2020

@author: telman
"""

import psycopg2
import json
import scraper

# Then take it from enviroment 
DATABASE_URL = "postgres://oxuxzqqupiyvoo:\
f85010c868d2fac8a157c0267e3b78811cb97a361769ac505e88ec91718e81b8\
@ec2-34-195-169-25.compute-1.amazonaws.com:5432/dambgdhumm6522" 

def give_timetable(chat_id):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()

    sql = """
        SELECT time_table.schedule FROM time_table
        INNER JOIN users
            ON users.group_ = time_table.group_
        WHERE users.chat_id = {};
    """
    sql = sql.format(chat_id) 
    
    cur.execute(sql)
    data = cur.fetchone()[0]

    cur.close()
    conn.close()
    return json.loads(data)

def give_week():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()

    sql = """
        SELECT * FROM week;
    """ 
    
    cur.execute(sql)
    data = cur.fetchone()[0]

    cur.close()
    conn.close()
    return data
    

def load_timetable(group):
    url = scraper.give_link(group)
    data = scraper.load_timetable(url)
    data = json.dumps(data)
    
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()

    sql = """ 
    INSERT INTO time_table (group_, schedule) 
    VALUES (%s, %s);"""
    cur.execute(sql, (group, data))

    cur.close()
    conn.close()

def load_week(group):
    url = scraper.give_link(group)
    data = scraper.load_week(url)
    
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    
    sql = """ 
        UPDATE week
        SET current_week = '{}';
        """.format(data)
    cur.execute(sql)
    conn.commit()
    
    cur.close()
    conn.close()
    