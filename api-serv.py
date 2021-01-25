import json
import sqlite3
import hashlib
from datetime import datetime
from bottle import route, run, request
import redis

@route('/application/')
def all_application():
    cur = conn.cursor()
    cur.execute("SELECT supply_time, application_id, job_name FROM application")
    rows = cur.fetchall()
    if len(rows) == 0:
        return 'no application'
    
    datas = []
    for row in rows:
        data = {"supply_time":row[0], "application_id":row[1], "job_name":row[2]}
        datas.append(data)

    return json.dumps(datas)

@route('/application/<application_id>')
def specific_application(application_id):
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM application WHERE application_id = "{application_id}"')
    row = cur.fetchall()

    data = {"supply_time":row[0][0], "application_id":row[0][1], "job_name":row[0][2], "content":row[0][3]}
    return json.dumps(data)

@route('/job/<job_name>/application/', method = 'POST')
def req_submissions(job_name):
    f = request.files['file']
    f.save('f.txt','w')
    content = ""
    with open('f.txt','r') as f:
        content = f.read()

    cur = conn.cursor()
    cur.execute(f'SELECT capabilities FROM job WHERE job_name = "{job_name}"')
    row = cur.fetchall()

    encoded_string = content.encode()
    h = hashlib.sha256(encoded_string).hexdigest()
    application_id = h[:12]

    value = json.dumps({application_id:row[0][0]})
    value = value.encode('utf-8')
    rd.lpush('application', value)

    cur.execute(f'INSERT INTO application VALUES ("{str(datetime.now())[:19]}","{application_id}", "{job_name}", "{content}", "processing")')
    conn.commit()

    cur.execute(f'SELECT supply_time, application_id, job_name FROM application WHERE application_id = "{application_id}"')
    row = cur.fetchall()

    data = {"supply_time": row[0][0], "application_id": row[0][1], "job_name": row[0][2]}
    return json.dumps(data)


@route('/job/<job_name>/application/<application_id>')
def specific_application(job_name, application_id):
    cur = conn.cursor()
    cur.execute(f'SELECT supply_time, score FROM application JOIN job ON application.job_name = job.job_name WHERE application_id = "{application_id}"')
    row = cur.fetchall()

    if row[0][1] != "processing":
        data = {"score":row[0][1], "supply_time":row[0][0]}
        return json.dumps(data)
    else:
        data = {"score":"processing", "supply_time": row[0][0]}
        return json.dumps(data)


@route('/job/<job_name>/application/')
def all_applications(job_name):
    f = '<form action = "/job/' + f"{job_name}" + '''/application/" method = "post" enctype = "multipart/form-data">
        <input type = "file" name = "file" />
            <input type = "submit"/>
            </form>'''

    cur = conn.cursor()
    cur.execute(f'SELECT supply_time, application_id, score FROM application JOIN job ON application.job_name = job.job_name WHERE job.job_name = "{job_name}"')
    
    rows = cur.fetchall()
    if len(rows) == 0:
        return f, 'no application submitted'

    tmp = {}
    for row in rows:
        if row[2] != "processing":
            t = {"score":row[2], "supply_time":row[0]}
        else:
            t = {"score":"processing", "supply_time":row[0]}

        tmp[row[1]] = t

    return f, json.dumps(tmp)

if __name__ == "__main__":
    rd = redis.Redis(host = 'localhost', port = 6379, socket_timeout=None)
    conn = sqlite3.connect("myDB.db")
    run(host="0.0.0.0", debug=True)
    conn.close()