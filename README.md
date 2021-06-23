## Introduction
![그림](https://user-images.githubusercontent.com/42771578/123077726-46332e00-d455-11eb-98e4-8e5207de7c34.png)
	
## Requirements

For package installaion, You can follow one of two,

1. build the docker image in the same directory with Dockerfile

   ```bash
   $ docker build -t [image name]:[tag] . 
   ```
2. install package needed

   ```bash
   $ apt-get update
   $ apt-get install apt-utils python3 python3-pip redis-server 
   $ pip3 install -r requirements.txt
   ```
   
## Usage

1. If you followed Requirements 1, run a container
   ```bash
   $ docker run —name [container name] -d -p 8080:8080 [image name]:[tag]
   ```
   You can use the other host-port instead of 8080. Check the status of container using the command "docker ps -a". 

2. If Requirements 2, run the shell script.
   ```bash
   $ /bin/bash script.sh
   ```
   - includes API server, redis server, sql and evaluation program.
   - To create only DB
      - `$ python3 table.py`
      - Then, the myDB.db is created in a current directory.
   - To add the evaluation program (Actually not real evaluation, just dummy)
      - `$ python3 program.py &`
      - The program of two is already been running in background. But You can add the program more.
 
## API

default URI : http://localhost:8080

   - `GET /application/`
   - `GET /application/<application_id>`
   - `GET|POST /job/<job_name>/application/`
   - `GET /job/<job_name>/application/<application_id>`
   
   
### example

1. Get all applying data

	 http://localhost:8080/application/
  
   - result : `no application`
   

2. Submit an application for the job you want. To apply for "SW",

	 http://localhost:8080/job/SW/application/
	 
   - result : `no application for SW`
   - This is the returned values when submitting `.../Sample/content1.txt`
      - {"supply_time": "2021-01-25 12:12:11", "application_id": "669007c530e4", "job_name": "SW"}
   - You can choose "Infra" and "Sales" instead of "SW" for job.
      
      
3. Check the specific Applying status,

	 http://localhost:8080/job/SW/application/669007c530e4

   - result : {"669007c530e4": {"score": "processing", "supply_time": "2021-01-25 12:12:11"}}
   - After evaluating the application, score data is updated in DB.
      - result : {"score": "{'coding_skills': 59, 'potential': 17}", "supply_time": "2021-01-25 12:12:11"}
      

4. Get all applying data again, after submitting all contents in Sample directory.

	 http://localhost:8080/application/
   - result : [{"supply_time": "2021-01-25 12:12:11", "application_id": "669007c530e4", "job_name": "SW"}, {"supply_time": "2021-01-25 12:14:36", "application_id": "664eb09cb8dd", "job_name": "Sales"}, {"supply_time": "2021-01-25 12:15:19", "application_id": "7201e036b35d", "job_name": "Infra"}, {"supply_time": "2021-01-25 12:20:36", "application_id": "7f2494cb1940", "job_name": "Infra"}, {"supply_time": "2021-01-25 12:20:57", "application_id": "a3b296ee7604", "job_name": "SW"}]
