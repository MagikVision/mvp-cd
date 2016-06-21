source $(dirname $0)/deploy.sh
ssh_to_ip $1 $2 $3
pull_code $4
install_requirements
run_migrations $5
restart_server
update_docs
