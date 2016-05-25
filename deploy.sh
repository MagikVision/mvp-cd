check_if_success(){
if [ $? -ne 0 ]; then
    echo "error occured"
    exit
else
    echo "command successfull"
fi
}

install_requirements(){
pip install -r requirements.txt
check_if_success
}

pull_code(){
git pull origin staging
check_if_success
}

run_migrations(){
yes yes| python3 manage.py migrate --settings=mvpserver.settings.staging
check_if_success
}

restart_server(){
sudo service mvp restart
check_if_success
}

restart_elasticsearch(){
service elasticsearch restart
check_if_success
}

restart_celery(){
sudo service supervisord restart
check_if_success
}

update_docs(){
cd docs/
bundle exec middleman build
check_if_success
}

cd $(<deploy_config.txt)
pull_code
install_requirements
run_migrations
restart_server
update_docs