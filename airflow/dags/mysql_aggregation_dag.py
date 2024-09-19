from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from datetime import datetime, timedelta


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'mysql_aggregation_dag',
    default_args=default_args,
    description='A simple DAG to run SQL scripts on MySQL',
    schedule_interval=timedelta(days=1),
    template_searchpath=['/opt/airflow/dags']
)

sql_scripts = ['mom_retention.sql', 'repurchase_rate.sql', 'retention_cohorts.sql']
tasks = []

for script in sql_scripts:
    task = SQLExecuteQueryOperator(
        task_id=script,
        conn_id='mysql_conn',
        sql=script,
        dag=dag,
    )
    tasks.append(task)


tasks[0] >> tasks[1] >> tasks[2]

