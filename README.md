# flask-covid-monitor

在Centos7系统下运行，利用Gunicorn，nginx，Crontab，MySQL，Redis维持系统正常运行  
Gunicorn执行命令：gunicorn -b 127.0.0.1:8787 -k eventlet -w 1 -D run:app  
Crontab执行命令（每十分钟执行一次）：*/10 * * * * /www/wwwroot/www.test.com/start.sh > /dev/null 2>&1 &
