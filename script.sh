#!/bin/bash
service redis-server restart
python3 table.py
python3 program.py &
python3 program.py &
python3 api-serv.py  

