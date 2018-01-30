import sys
import os
import run1data

for dataname in sys.stdin:
    dataname = dataname.strip()
    data_file = os.path.join('data', dataname+'_Vectors.txt')
    label_file = os.path.join('data', dataname+'_Labels.txt')
    bnsim_file = os.path.join('sim', dataname+'_Bnsimx.txt')
    result_file = os.path.join('results', dataname+'_Results.txt')
    if not os.path.exists('results'):
        os.makedirs('results')
    print("Running", dataname)
    run1data.main(data_file, label_file, bnsim_file, result_file)
