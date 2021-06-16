from datetime import timedelta
# The DAG object; we'll need this to instantiate a DAG
from airflow.models import DAG
# Operators; we need this to operate!
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
from mongo_db import MongoDB
from web_scrap import SetIndexSpider
from scrapy.crawler import CrawlerProcess

mongo = MongoDB()


def scrap_start():
    process = CrawlerProcess()
    process.crawl(SetIndexSpider)
    process.start()


default_args = {
    'owner': 'phich.bur',
    'depends_on_past': False,
    # use the temp email address https://temp-mail.org/en/
    'email': ['woxig17203@awinceo.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}
with DAG(
    'daily_scrap',
    default_args=default_args,
    description='get set index stock price and keep to mongodb',
    schedule_interval='@daily',
    start_date=days_ago(0),
    tags=['set_index']
) as dag:

    t1 = PythonOperator(task_id='t1',
                        python_callable=mongo.create_database,
                        dag=dag)

    t2 = PythonOperator(task_id='t2',
                        python_callable=mongo.create_collection,
                        dag=dag)

    t3 = PythonOperator(task_id='t3',
                        python_callable=scrap_start,
                        dag=dag)

    t1 >> t2 >> t3
