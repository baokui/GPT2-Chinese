mode=$1
nb_server=$2
port=7000

if [ $mode -eq 0 ]
then
nohup python -u app_test.py $port poem  $nb_server >> log/apptest-poem-$port.log 2>&1 &
fi

if [ $mode -eq 1 ]
then
nohup python -u app_test.py $port prose  $nb_server >> log/apptest-prose-$port.log 2>&1 &
fi

if [ $mode -eq 2 ]
then
nohup python -u app_test.py $port gou  $nb_server >> log/apptest-gou-$port.log 2>&1 &
fi