# CarRentBlockChain
基于FISCO BCOS（微众联盟链架构）的汽车租赁平台。

实现链上车辆租赁交易的过程。

## 运行 CarRentBlockChain

**运行环境**

python3.7+

**运行 CarRentBlockChain**

~~~bash
cd CarRentBlockChain/

cp .envrc CarRentBlockChain/.env

pip install -r requirements.txt

python manager.py init_db
# init local db

python manager.py runserver 
# 运行服务
~~~
-----------------


~~~bash
positional arguments:
  {runserver,shell,reset_local_db,reset_server_db,reset_db,init_local_db,init_server_db,init_db,set_user}
    runserver           Runs the Flask development server i.e. app.run()
    shell               Runs a Python shell inside Flask application context.
    reset_local_db      Reset local databases.
    reset_server_db     Reset server databases.
    reset_db            Reset all databases.
    init_local_db       Initialized local databases.
    init_server_db      Initialized server databases.
    init_db             Initialized all databases.
    set_user            Add A New User.
~~~

