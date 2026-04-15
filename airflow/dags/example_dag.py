from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 1, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# FIX: context manager (patrón recomendado desde Airflow 2.0+)
# FIX: schedule en lugar de schedule_interval (removido en Airflow 3.x)
with DAG(
    "example_dag",
    default_args=default_args,
    description="Un DAG de ejemplo con Celery",
    schedule="@daily",
    catchup=False,
    tags=["example"],
) as dag:

    # FIX: ya no se necesita pasar dag=dag en cada tarea
    task1 = BashOperator(
        task_id="print_date",
        bash_command="date",
    )

    task2 = BashOperator(
        task_id="sleep",
        bash_command="sleep 5",
    )

    task1 >> task2
