#python ../../../hydra_plugins/GAMS/Auto/GAMSAutoRun.py -t $1 -s $2 -st "2000/01/01" -en "2000/06/01" -dt "1 mon" -m Demo3.gms -o hydra_output.txt
python ../../../hydra_plugins/GAMS/Auto/GAMSAutoRun.py -t $1 -s $2 -tx 2000/01/01,  2000/02/01,  2000/03/01, 2000/04/01, 2000/05/01 ,2000/06/01 -m Demo3.gms -o hydra_output.txt
