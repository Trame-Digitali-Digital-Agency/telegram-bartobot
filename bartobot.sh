#!/bin/bash

# mongod=/usr/local/mongodb/bin/mongod
bartod="python barto.py"
ngrockd=/home/cosmy/batobot/ngrock-linux
# mongod_data=/Users/michito/work/mongodb_data
# mongod_log=/Users/michito/work/mongodb_log/mongodb.log
prog=bartobot.sh
RETVAL=0

stop() {
    grep_barto=`ps aux | grep -v grep | grep "${bartod}"`
    if [ ${#grep_barto} -gt 0 ]
    then
	echo "Stop BartoBot."
	PID=`ps x | grep -v grep | grep "${bartod}" | awk '{ print $1 }'`
	`kill -2 ${PID}`
	RETVAL=$?
    else
	echo "BartoBot is not running."
    fi
}
start() {
    grep_barto=`ps aux | grep -v grep | grep "${bartod}"`
    if [ -n "${grep_barto}" ]
    then
	echo "BartoBot is already running."
    else
	echo "Start Bartobot."
	`${bartod} > /dev/null 2> ./barto.log &`
	RETVAL=$?
    fi
}
server_start() {
	echo "Start server https."
	`${ngrockd} start bartobot > /dev/null &`
	 echo "Check url assigned on http://www.exupery.it:4040"
}
server_start() {
	`${ngrockd} stop`
}

case "$1" in
    start)
	start
	;;
    stop)
	stop
	;;
    restart)
	stop
  sleep 5
	start
	;;
	  server_start)
	server_start
	;;
		server_stop)
	server_stop
	;;
    *)
	echo $"Usage: $prog {start|stop|restart}"
	exit 1
esac

exit $RETVAL
