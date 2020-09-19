#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  2 17:03:03 2020

@author: telman
"""

import psycopg2
import json
import scraper
import os
 
DATABASE_URL = os.environ['DATABASE_URL']

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
    conn.commit()

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
    
def is_ex_user(chat_id):
    chat_id = str(chat_id)
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    sql = """
            SELECT users.chat_id FROM users
            WHERE users.chat_id = {};
        """
    sql = sql.format(chat_id)
        
    cur.execute(sql)
    try:
        cur.fetchone()[0]
        cur.close()
        conn.close()
        return True
    except:
        cur.close()
        conn.close()
        return False

def is_ex_group(group):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    sql = """
            SELECT time_table.group_ FROM time_table
            WHERE time_table.group_ = '{}';
        """
    sql = sql.format(group) 
        
    cur.execute(sql)
    try:
        cur.fetchone()[0]
        cur.close()
        conn.close()
        return True
    except:
        cur.close()
        conn.close()
        return False
    
def add_just_in_user(chat_id, name, group):
    chat_id = str(chat_id)
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    sql = """ 
    INSERT INTO users (chat_id, name, group_) 
    VALUES ({}, '{}', '{}');"""
    sql = sql.format(chat_id, name, group)
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
    
def is_group_valid(group):
    # Для безапаснасти надо бы добавить сюда проверку
    # регулярным выражением еще
    try:
        scraper.give_link(group)
        return True
    except:
        return False
    
def add_user(chat_id, name, group):
    if is_ex_group(group):
        add_just_in_user(chat_id, name, group)
        return "User added complete"
    else:
        if is_group_valid(group):
            try:
                load_timetable(group)
                add_just_in_user(chat_id, name, group)
                return "User added complete"
            except:
                return "Sorry something goes wrong"
        
    