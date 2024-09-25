#!/bin/bash

printenv | awk '{print "export " $1}' > /app/cronenv.sh

service cron start

uvicorn main:app --host 0.0.0.0 --port 8020