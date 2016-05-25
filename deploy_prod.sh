check_if_success(){
if [ $? -ne 0 ]; then
    echo "error occured"
    exit
else
    echo "command successfull"
fi
}