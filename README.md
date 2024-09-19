## Sales-Data-Analysis-for-Retention-Metrics
Digitoon internship final project

# You can see the architecture of this project here :
![alt text]([https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png](https://github.com/shayan-fallah/Sales-Data-Analysis-for-Retention-Metrics/blob/main/Network%20Architecture.jpg) "Network Architecture")

# Brief Explanation:
In this project we generate fake transactions and Analyse these generated transactions based on the metrics we've been given.
for this purpose we've used diffrenet technologies like kafka, docker, airflow.

# Repo Tree : 
├── airflow
│   ├── dags
│   │   ├── mom_retention.sql
│   │   ├── mysql_aggregation_dag.py
│   │   ├── __pycache__
│   │   │   └── mysql_aggregation_dag.cpython-37.pyc
│   │   ├── repurchase_rate.sql
│   │   └── retention_cohorts.sql
│   ├── logs
│   │   ├── dag_processor_manager
│   │   │   └── dag_processor_manager.log
│   │   └── scheduler
│   │       │   └── mysql_aggregation_dag.py.log
│   │       └── latest -> /opt/airflow/logs/scheduler/2024-09-19
│   └── plugins
├── docker-compose.yml
├── dockerfiles
│   ├── airflowdocker
│   ├── consumerdocker
│   ├── mysqldocker
│   ├── producerdocker
│   ├── pythonscripts
│   │   ├── consumer_oldversion.py
│   │   ├── consumer.py
│   │   ├── producer_oldversion.py
│   │   ├── producer.py
│   │   ├── requirements_consumer.txt
│   │   └── requirements_proudcer.txt
│   └── sqlscripts
│       ├── mom_retention.sql
│       ├── repurchase_rate.sql
│       └── retention_cohorts.sql
└── environment.env




