nohup mongod --dbpath=/data/db --auth -bind_ip 0.0.0.0 &
cd /root/Tide-Mars && nohup python mars.py &
nohup su -l acunetix -c /home/acunetix/.acunetix_trial/start.sh &
cd /root/Tide-Mars/taskpython/ && nohup python asset_task_scan_v1.0.py &