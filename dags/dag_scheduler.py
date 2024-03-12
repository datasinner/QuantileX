from airflow import DAG
from datatime import datetime, timedelta
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "you",
    "retries": 5,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="BTC-Price_prediction-lasso",
    default_args=default_args,
    description="We run it daily base",
    start_date=datetime(2024, 3, 8),
    schedule_interval="@daily",
) as dag:
    task = BashOperator(task_id="run_lasso", bash_command="python app.py")
    task
