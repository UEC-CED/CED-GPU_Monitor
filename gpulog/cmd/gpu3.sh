#!/bin/bash

nvidia-smi --query-gpu=timestamp,index,name,utilization.gpu,memory.used,memory.total --format=csv -f ~/gpu_log/log03.csv
scp -i "~/.ssh/id_rsa_gpu" ~/gpu_log/log03.csv cadmin@brown01.ced.cei.uec.ac.jp:~/CED_monitor@brown01/work/gpulog/csv
echo "send log of gpu03."
