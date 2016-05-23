check_if_success(){
if [ $? -ne 0 ]; then
    echo "error occured"
    exit
else 
	echo "command successfull"
fi
}

pull_code(){
git pull origin master
check_if_success
}

run_migrations(){
yes yes| python3 manage.py migrate --settings=mvpserver.settings.staging
check_if_success
}

restart_server(){
service mvp restart
check_if_success
}

restart_elasticsearch(){
service elasticsearch restart
check_if_success
}


cd $(<deploy_config.txt)
pull_code
run_migrations
restart_server
restart_elasticsearch