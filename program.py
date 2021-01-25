import random
import time
import json
import ast
import sqlite3
import redis
rd = redis.Redis(host = 'localhost', port = 6379)

def get_data_from_redis():
    conn1 = sqlite3.connect("myDB.db")
    cur1 = conn1.cursor()
    while True:
        _, datas = rd.brpop('application')
        datas = datas.decode('utf-8')
        dict_data = dict(json.loads(datas))
        keys = list(dict_data.keys())
        application_id, cap = keys[0], dict_data[keys[0]]

        time.sleep(random.random() * 2 + 1)

        if application_id is not None:
            sql = f"SELECT content FROM application WHERE application_id = '{application_id}'"
            print('sql', sql)
            print('------- content -------')
            cur1.execute(sql)
            rows = cur1.fetchall()
            print('size', len(rows))
            print(rows[0])
            print("---------------------------")
    
            time.sleep(random.random() * 2 + 1)

            cap = ast.literal_eval(cap)
            score = {k: random.randint(0, 100) for k in cap}
            
            sql = f'UPDATE application SET score = "{score}" WHERE application_id = "{application_id}"'
            cur1.execute(sql)
            conn1.commit()

    conn1.close()

if __name__ == '__main__':
    get_data_from_redis()


