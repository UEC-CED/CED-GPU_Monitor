# CED-GPU_Monitor
CEDのGPUサーバー(gpu01~04)の利用状況をモニターするためのプログラムです。  
上に端末名、状態、ユーザ数、CPU平均負荷、DRAM残量が、  
下にサーバに搭載されているGPU、gpu使用率、使用中のVRAM量、総VRAMが表示されます。  



##実行手順
###リポジトリをクローンする
    $git clone https://github.com/UEC-CED/CED-GPU_Monitor.git
###プログラムの実行
基本的にはbrown01で実行してください。Anacondaのbase環境で動きます。
    $###:~/CED-GPUMomitor/
    $python monitor.py

その他の環境で実行するときは、anacondaやvenvなどで作った仮想環境上に必要なライブラリをインストールしてから動かしてください。ライブラリはrequirements.txtにまとめてあります。

    $# (自分で作成した仮想環境内で実行してください)
    $# venvの場合
    $pip install -r requirements.txt
    $# anacondaの場合
    $conda install --yes --file requirements.txt



実行するときは'$nohup'などでバックグラウンド実行してください。
    $# nohupの場合
    $nohup python gpu_monitor.py &

実行後、<http://172.21.94.201:23456>にアクセスすることで利用状況を確認することができます。
##プログラムの停止
    $ps aux | grep gpu_monitor.py | grep -v grep | swk '{print $2}' | xargs kill 
