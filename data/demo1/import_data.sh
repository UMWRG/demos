#!/bin/bash
if [ -n $1 ]; then
python ~/git/HYDRA/HydraPlugins/CSVplugin/ImportCSV/ImportCSV.py -t network.csv -n nodes.csv -l links.csv -x -m ../../templates/demo1/template/template.xml
else
python ~/git/HYDRA/HydraPlugins/CSVplugin/ImportCSV/ImportCSV.py -i $1 -s "$2" -t network.csv -n nodes.csv -l links.csv -x -m ../../templates/demo1/template/template.xml
fi
