check_if_success(){
    if [ $? -ne 0 ]; then
        echo "error occured"
        exit
    else
        echo "command successfull"
    fi
}

ssh_to_ip(){
    # $1 being the path to pem file and $2 being ip of server
    ssh -i $1 $2
    check_if_success
    cd $3
    check_if_success
}

install_requirements(){
sudo pip install -r requirements.txt
check_if_success
}

pull_code(){
git pull origin staging
check_if_success
}


run_migrations(){
yes yes| python3 manage.py migrate --settings=$1
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
#sudo service supervisor restart
#check_if_success
}

update_docs(){
cd docs/
bundle exec middleman build
check_if_success
}

