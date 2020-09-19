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

def execute_sql(sql, fetch=False):
    data = None
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    cur.execute(sql)
    if (fetch):
        data = cur.fetchone()[0]
    else:
        conn.commit()
    cur.close()
    conn.close()
    return data

def give_timetable(chat_id):
    sql = """
        SELECT time_table.schedule FROM time_table
        INNER JOIN users
            ON users.group_ = time_table.group_
        WHERE users.chat_id = {};
    """
    sql = sql.format(chat_id) 
    data = execute_sql(sql, fetch=True)
    return json.loads(data)

def give_week():
    sql = """
        SELECT * FROM week;
    """ 
    return execute_sql(sql, fetch=True)

def give_group(chat_id):
    sql = """
        SELECT users.group_ FROM users
        WHERE users.chat_id = {};
    """ 
    sql = sql.format(chat_id)
    return execute_sql(sql, fetch=True)

def load_timetable(group):
    url = scraper.give_link(group)
    data = scraper.load_timetable(url)
    data = json.dumps(data)
    sql = """ 
        INSERT INTO time_table (group_, schedule) 
        VALUES ('{}', '{}');
    """
    sql = sql.format(group, data)
    execute_sql(sql)

def load_week(group):
    url = scraper.give_link(group)
    data = scraper.load_week(url)
    sql = """ 
        UPDATE week
        SET current_week = '{}';
        """.format(data)
    execute_sql(sql)


def is_ex_user(chat_id):
    chat_id = str(chat_id)
    sql = """
            SELECT COUNT(1) FROM users
            WHERE users.chat_id = {};
        """
    sql = sql.format(chat_id)
    count = execute_sql(sql, fetch=True)
    if count:
        return True
    else:
        return False

def is_ex_group(group):
    sql = """
            SELECT COUNT(1) FROM time_table
            WHERE time_table.group_ = '{}';
        """
    sql = sql.format(group) 
    count = execute_sql(sql, fetch=True)
    if count:
        return True
    else:
        return False
    
def add_just_in_user(chat_id, name, group):
    chat_id = str(chat_id)
    sql = """ 
    INSERT INTO users (chat_id, name, group_) 
    VALUES ({}, '{}', '{}');"""
    sql = sql.format(chat_id, name, group)
    execute_sql(sql)
    
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
            
def reburn_reset_database():
    sql = """
        CREATE TABLE users (
            chat_id INT,
            name VARCHAR(20),
            group_ VARCHAR(10)
        );
        CREATE TABLE time_table (
            group_ VARCHAR(10),
            schedule VARCHAR(50000)
        );
        CREATE TABLE week (
            current_week VARCHAR(50)
        );
        CREATE TABLE admin (
           chat_id INT,
           name VARCHAR(20)
        );
    
    
        INSERT INTO week (current_week)
        VALUES ('1 fuck this stuff');
    """
    execute_sql(sql)

def delete_user(chat_id):
    sql = """
        DELETE FROM users 
        WHERE users.chat_id = {};
    """
    sql = sql.format(chat_id)
    execute_sql(sql)

def delete_time_table(group_):
    sql = """
        DELETE FROM time_table 
        WHERE time_table.group_ = '{}';
    """
    sql = sql.format(group_)
    execute_sql(sql)

def delete_admin(chat_id):
    sql = """
        DELETE FROM admin 
        WHERE users.chat_id = {};
    """
    sql = sql.format(chat_id)
    execute_sql(sql)
    
def delete_time_table_user(chat_id):
    current_group = give_group(chat_id)
    sql = """
        SELECT COUNT(1) FROM users
        WHERE users.group_ = '{}'
    """
    sql = sql.format(current_group)
    count = execute_sql(sql, fetch=True)
    if count == 1:
        delete_time_table(current_group) 

def update_user_group(chat_id, new_group):
    if (not is_ex_group(new_group)) and (is_group_valid(new_group)):
        load_timetable(new_group)
    if (is_group_valid(new_group)):
        sql = """
            UPDATE users
            SET group_ = '{}'
            WHERE users.chat_id = {};
        """
        sql = sql.format(new_group, chat_id)
        execute_sql(sql)
        delete_time_table_user(chat_id)
    else:
        return "Group is not valid"
    return "Your timetable was updating successful"
    
def add_to_admin_list(chat_id, name):
    chat_id = str(chat_id)
    sql = """ 
        INSERT INTO admin (chat_id, name, group_) 
        VALUES ({}, '{}');
    """
    sql = sql.format(chat_id, name)
    execute_sql(sql)
    
def is_admin(chat_id):
    chat_id = str(chat_id)
    sql = """
        SELECT COUNT(1) FROM admin
        WHERE admin.chat_id = {};
    """
    sql = sql.format(chat_id)
    count = execute_sql(sql, fetch=True)
    if count == 1:
        return True
    else:
        return False
    
    
    

        
    