# CED-GPU_Monitor
CEDのGPUサーバ(gpu01~04)の利用状況をモニターするためのプログラムです。  
上に端末名、状態、ユーザ数、CPU平均負荷、DRAM残量が、  
下にサーバに搭載されているGPU、gpu使用率、使用中のVRAM量、総VRAMが表示されます。  

## ディレクトリ構成
    CED-GPU_monitor
    ├ templates
    │  ├ '#monitor.html#'   # たぶん一時ファイル
    │  └ monitor.html    # 可視化用のHTMLテンプレート
    ├ gpu_monitor.py   # ステータス取得、更新クラスを動かして結果をWebページに可視化
    ├ ced.py    # ステータス取得、更新するクラスの本体
    └ README.md    #使い方とか更新情報とか書いとくやつ

## 実行手順
### リポジトリのクローン
    git clone https://github.com/UEC-CED/CED-GPU_Monitor.git
### プログラムの実行
基本的にはbrown01で実行してください。セットアップなしで動かせます。

    # (クローンした CED-GPU_Monitor/ 内で)
    python gpu_monitor.py

その他の環境で実行するときは、Anacondaやvenvなどで作った仮想環境上に必要なライブラリをインストールしてから動かすことをお勧めします。必要なライブラリはrequirements.txtにまとめているので、このファイルが置いてあるディレクトリ内で以下を実行してインストールしてください。
#### Anacondaの場合
##### インストール(初回のみ)
[Anaconda公式サイト](https://www.anaconda.com/download/)から最新版をダウンロードしてください(メールアドレスを入力するとダウンロードページに飛べます)。

    # 2024/10/02時点で最新
    wget https://repo.anaconda.com/archive/Anaconda3-2024.06-1-Linux-x86_64.sh
    bash Anaconda3-2024.06-1-Linux-x86_64.sh
    rm Anaconda3-2024.06-1-Linux-x86_64.sh
    source ~/.bashrc
    #2行目のコマンド(bash)が実行できない場合、以下のコマンドを実行するといけるかも
    chmod +x Anaconda3-2024.06-1-Linux-x86_64.sh
    #最新じゃない場合以下のコマンドを実行してアップデート
    conda update --all
    conda update -n base conda

##### 仮想環境構築(初回のみ)
    conda create -n ced_gpu_monitor python>=3.9
    conda activate ced_gpu_monitor
    conda install --yes --file requirements.txt
    #3行目のコマンド(conda install)がうまくいかなかったら以下のコマンド
    pip install -r requirements.txt

##### 実行
    conda activate ced_gpu_monitor
    python gpu_monitor.py
    #バックグラウンド実行(実際に運用するならこっち)
    nohup python gpu_monitor.py &

#### venvの場合
python標準の仮想環境構築ライブラリです。pythonがインストールされているマシンで動かせます。

##### 仮想環境構築(初回のみ)
    cd CED-GPU_monitor
    python -m venv 好きな仮想環境名
    source 好きな仮想環境名/bin/activate
    pip install -r requirements.txt

##### 仮想環境起動と停止
    # 仮想環境を作ったディレクトリで
    #起動↓
    source 好きな仮想環境名/bin/activate
    #停止↓
    deactivate

##### 実行
    #CED-GPU_monitorに移動し、仮想環境を起動して
    python gpu_monitor.py
    #バックグラウンド実行(実際に運用するならこっち)
    nohup python gpu_monitor.py &

実行後、<http://172.21.94.201:23456>にアクセスすることで利用状況を確認することができます。
## プログラムの停止
    ps aux | grep gpu_monitor.py | grep -v grep | swk '{print $2}' | xargs kill 

## 改善ポイント（できればやりたい）
* セキュリティ面の向上
* htmlの改良(vueやreactなどでデザインを刷新して見やすくするといいかも)

