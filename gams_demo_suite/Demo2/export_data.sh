#python ~/git/hydra_plugins/GAMS/Export/GAMSExport.py -t $1 -s $2 -tx "2000-01-01, 2000-02-01, 2000-03-01, 2000-04-01, 2000-05-01, 2000-06-01" -o hydra_output.txt
python ../../../hydra_plugins/GAMS/Export/GAMSExport.py -t $1 -s $2 -st "01/01/2000" -en "01/08/2000" -dt "1 mon" -o ./hydra_output.txt
