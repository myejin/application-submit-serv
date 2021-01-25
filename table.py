import os
import json
import sqlite3

def set_table():
    dirname = "mySample"
    conn1 = sqlite3.connect("myDB.db")
    cur1 = conn1.cursor()
    cur1.execute('CREATE TABLE job(job_name TEXT PRIMARY KEY, capabilities TEXT)')
    cur1.execute(f'INSERT INTO job VALUES ("SW", "{["coding_skills", "potential"]}")')
    cur1.execute(f'INSERT INTO job VALUES ("Infra", "{["diligence", "experience"]}")')
    cur1.execute(f'INSERT INTO job VALUES ("Sales", "{["attitude", "language", "experience"]}")')

    cur1.execute('CREATE TABLE application(supply_time TEXT, application_id TEXT PRIMARY KEY, job_name TEXT, content TEXT, score TEXT, CONSTRAINT job_name FOREIGN KEY(job_name) REFERENCES job(job_name))')
    cur1.execute('PRAGMA foreign_keys = 1')
    conn1.commit()
    
    print('----------- job all -----------')
    rows = cur1.execute('select * from job')
    for row in rows:
        print(row)
    print()

    conn1.close()
    print('-------- myDB.db 생성 완료 ---------')

if __name__ == "__main__":
    set_table()
