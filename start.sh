# run in the iscte.me server

#/usr/share/spark/bin/spark-submit --master spark://192.168.1.105:7077 --total-executor-cores 8 --executor-memory 6g server.py 
# /usr/share/spark/bin/spark-submit --master spark://192.168.1.105:7077 server.py
# other parameters alongside server.py such as path to data files or --driver-memory 2g

# run with 2 threads in the personal computer
spark-submit --master local[2] server.py 

