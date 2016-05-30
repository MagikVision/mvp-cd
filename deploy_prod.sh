source $(dirname $0)/deploy.sh
ssh_to_ip $1 $2 $3
pull_code
install_requirements
run_migrations mvpserver.settings.production
restart_server

