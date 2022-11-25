import os
os.environ["JAVA_HOME"] = "/opt/java"
os.environ["SPARK_HOME"] = "/opt/spark"
import findspark
findspark.init()
from pyspark.sql import SparkSession
spark = SparkSession.builder.master("local[*]").getOrCreate()
spark.conf.set("spark.sql.repl.eagerEval.enabled", True) # Property used to format output tables better
spark.sparkContext.addPyFile(r'/opt/airflow/dags/transform_funcs.py')
spark.sparkContext.addPyFile(r'/opt/airflow/dags/dag_initial_loading.py')
spark.sparkContext.addPyFile(r'/opt/airflow/dags/casspark.py')
import pyspark.pandas as ps
import databricks.koalas as ks
ks.set_option('compute.ops_on_diff_frames', True)
ps.set_option('compute.ops_on_diff_frames', True)
import pandas as pd
import transform_funcs
import pathlib
import datetime
from airflow import DAG
import dateutil
from airflow.operators.python import PythonOperator
<<<<<<< HEAD
import casspark
from cassandra.cluster import Cluster


cass_ip = 'cassandra'


def load_tips():
    print('ESTABLISHING CONNECTION TO CASSANDRA')
    cluster = Cluster(contact_points=[cass_ip],port=9042)
    session = cluster.connect()
    print('READING TIPS FILE')
    tip = ps.read_json(r'/opt/data/initial_load/tip.json').head(10000)
    print('DROPPING DUPLICATED ROWS')
    tip = tip.drop_duplicates()
    print('CLEANING STRINGS')
    tip = tip[tip['text'].apply(transform_funcs.drop_bad_str) != 'REMOVE_THIS_ROW']
    print('NORMALIZING DATES')
    tip['date'] = tip['date'].apply(transform_funcs.transform_dates).dt.strftime('%Y-%m-%d')
    print('CREATING KEYSPACE')
    session.execute("""
CREATE KEYSPACE IF NOT EXISTS henry WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 3 };
""")
    print('CREATING TABLE')
    session.execute("""
CREATE TABLE IF NOT EXISTS henry.tip(business_id text, compliment_count int, date text, text text, user_id text,PRIMARY KEY((business_id,date,user_id)))
""")
    print('UPLOADING DATAFRAME TO CASSANDRA')
    casspark.spark_pandas_insert(tip,'henry','tip',session,debug=True)
    print('DONE')
=======
from airflow.operators.empty import EmptyOperator
import os

cass_ip = 'cassandra'

####################################
######## SPARK RUNNING ##########
####################################
os.environ["JAVA_HOME"] = "/opt/java"
os.environ["SPARK_HOME"] = "/opt/spark"

from pyspark.sql import SparkSession
import findspark
from pyspark.context import SparkContext
from pyspark.conf import SparkConf

from pyspark.serializers import PickleSerializer

#conf = SparkConf()
#conf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")

#sc  = SparkContext(conf=conf, serializer=PickleSerializer())

findspark.init()
spark = SparkSession.builder.master("local[*]").getOrCreate()

spark.sparkContext.setLogLevel("OFF")
ks.set_option('compute.ops_on_diff_frames', True)

default_args = {
    'owner': 'Grupo 02 Henry Labs TF',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'start_date':  days_ago(2),
    'retry_delay': timedelta(minutes=5),
}

def load_tips():
    print('ESTABLISHING CONNECTION TO CASSANDRA')
    cluster = Cluster(contact_points=[cass_ip],port=9042)
    session = cluster.connect()
    print('READING TIPS FILE')
    tip = ps.read_json(r'/opt/data/initial_load/tip.json').head(10000)
    print('DROPPING DUPLICATED ROWS')
    tip = tip.drop_duplicates()
    print('CLEANING STRINGS')
    tip = tip[tip['text'].apply(transform_funcs.drop_bad_str) != 'REMOVE_THIS_ROW']
    print('NORMALIZING DATES')
    tip['date'] = tip['date'].apply(transform_funcs.transform_dates).dt.strftime('%Y-%m-%d')
    print('CREATING KEYSPACE')
    session.execute("""
CREATE KEYSPACE IF NOT EXISTS henry WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 3 };
""")
    print('CREATING TABLE')
    session.execute("""
CREATE TABLE IF NOT EXISTS henry.tip(business_id text, compliment_count int, date text, text text, user_id text,PRIMARY KEY((business_id,date,user_id)))
""")
    print('UPLOADING DATAFRAME TO CASSANDRA')
    casspark.spark_pandas_insert(tip,'henry','tip',session,debug=True)
    print('DONE')


with DAG('InitialLoading54', schedule_interval='@once', default_args=default_args) as dag:
    StartPipeline = EmptyOperator(
        task_id = 'StartPipeline',
        dag = dag
        )

    # PythonLoad1 = PythonOperator(
    #     task_id="LoadTips",
    #     python_callable=TipsEDA,
    #      )

def load_checkin():
    print('ESTABLISHING CONNECTION TO CASSANDRA')
    cluster = Cluster(contact_points=[cass_ip],port=9042)
    session = cluster.connect()
    print('READING TIPS FILE')
    checkin = ps.read_json(r'/opt/data/initial_load/checkin.json').head(10000)
    print('DROPPING DUPLICATED ROWS')
    checkin = checkin.drop_duplicates()
    print('NORMALIZING DATES')
    checkin['date'] = checkin['date'].apply(transform_funcs.get_date_as_list)
    print('CREATING KEYSPACE')
    session.execute("""
CREATE KEYSPACE IF NOT EXISTS henry WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 3 };
""")
    print('CREATING TABLE')
    session.execute("""
CREATE TABLE IF NOT EXISTS henry.checkin(business_id text, date list<text>,PRIMARY KEY(business_id))
""")
    print('UPLOADING DATAFRAME TO CASSANDRA')
    casspark.spark_pandas_insert(checkin,'henry','checkin',session,debug=True)
    print('DONE')

def load_bussiness():
    print('ESTABLISHING CONNECTION TO CASSANDRA')
    cluster = Cluster(contact_points=[cass_ip],port=9042)
    session = cluster.connect()
    print('READING BUSINESS FILE')
    business = ps.read_json(r'/opt/data/initial_load/business.json').head(10000)
    print('DROPPING DUPLICATED ROWS')
    business = business.drop_duplicates()
    print('JOINING CITY AND STATE')
    business['state_city']  = transform_funcs.get_state_city(business['city'],business['state'])
    business = business[[column for column  in list(business.columns) if column not in ['city','state']]]
    print('NORMALIZING HOURS') #df['hours'] = df['hours'].apply(row_hours_to_series)
    business['hours'] = transform_funcs.row_hours_to_series(business['hours'])
    print('NORMALIZING ATTRIBUTES')
    business['attributes'] = transform_funcs.row_att_to_series(business['attributes'])
    print('NORMALIZING CATEGORIES')
    business['categories'] = business['categories'].apply(transform_funcs.check_str_list)
    print('CREATING KEYSPACE')
    session.execute("""
CREATE KEYSPACE IF NOT EXISTS henry WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 3 };
""")
    print('CREATING TABLE')
    session.execute("""
CREATE TABLE IF NOT EXISTS henry.business(address text, attributes list<frozen <list<text>>>, business_id text, categories list<text>, hours list<frozen <list<int>>>, is_open int, latitude float, longitude float, name text, postal_code text, review_count int, stars float, state_city list<text>,PRIMARY KEY(business_id))
""")
    print('UPLOADING DATAFRAME TO CASSANDRA')
    casspark.spark_pandas_insert(business,'henry','business',session,debug=True)
    print('DONE')

    # PythonLoad3 = PythonOperator(
    #     task_id="LoadBusiness",
    #     python_callable=BusinessEDA,
    #     )

    # PythonLoad4 = PythonOperator(
    #     task_id="LoadReviews",
    #     python_callable=ReviewEDA,
    #     )
    
    # PythonLoad5 = PythonOperator(
    #     task_id="LoadUsers",
    #     python_callable=UserEDA,
    #     )


#DAG de Airflow
with DAG(dag_id='Test345',start_date=datetime.datetime(2022,8,25),schedule_interval='@once') as dag:

    FinishETL= EmptyOperator(
        task_id = 'FinishETLAndLoading',
        dag = dag
        )
    t_load_tips = PythonOperator(task_id='load_tips',python_callable=load_tips)

    CheckWithQuery = PythonOperator(
        task_id="CheckWithQuery",
        python_callable=MakeQuery,
        op_kwargs={
        'query': 'SELECT * FROM reviews LIMIT 10',
        }
        )
    t_load_checkin = PythonOperator(task_id='load_checkin',python_callable=load_checkin)

    FinishPipeline = EmptyOperator(
        task_id = 'FinishPipeline',
        dag = dag
        )
    t_load_bussiness = PythonOperator(task_id='load_bussiness',python_callable=load_bussiness)


#StartPipeline >> PythonLoad1 >> PythonLoad2 >> PythonLoad3 >> PythonLoad4 >> PythonLoad5 >> FinishETL

StartPipeline >> PythonLoad2 >> FinishETL
>>>>>>> 2bcc5d05c4947cce43df8224253f6c6bc50890c5




def load_checkin():
    print('ESTABLISHING CONNECTION TO CASSANDRA')
    cluster = Cluster(contact_points=[cass_ip],port=9042)
    session = cluster.connect()
    print('READING TIPS FILE')
    checkin = ps.read_json(r'/opt/data/initial_load/checkin.json').head(10000)
    print('DROPPING DUPLICATED ROWS')
    checkin = checkin.drop_duplicates()
    print('NORMALIZING DATES')
    checkin['date'] = checkin['date'].apply(transform_funcs.get_date_as_list)
    print('CREATING KEYSPACE')
    session.execute("""
CREATE KEYSPACE IF NOT EXISTS henry WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 3 };
""")
    print('CREATING TABLE')
    session.execute("""
CREATE TABLE IF NOT EXISTS henry.checkin(business_id text, date list<text>,PRIMARY KEY(business_id))
""")
    print('UPLOADING DATAFRAME TO CASSANDRA')
    casspark.spark_pandas_insert(checkin,'henry','checkin',session,debug=True)
    print('DONE')

def load_bussiness():
    print('ESTABLISHING CONNECTION TO CASSANDRA')
    cluster = Cluster(contact_points=[cass_ip],port=9042)
    session = cluster.connect()
    print('READING BUSINESS FILE')
    business = ps.read_json(r'/opt/data/initial_load/business.json').head(10000)
    print('DROPPING DUPLICATED ROWS')
    business = business.drop_duplicates()
    print('JOINING CITY AND STATE')
    business['state_city']  = transform_funcs.get_state_city(business['city'],business['state'])
    business = business[[column for column  in list(business.columns) if column not in ['city','state']]]
    print('NORMALIZING HOURS') #df['hours'] = df['hours'].apply(row_hours_to_series)
    business['hours'] = transform_funcs.row_hours_to_series(business['hours'])
    print('NORMALIZING ATTRIBUTES')
    business['attributes'] = transform_funcs.row_att_to_series(business['attributes'])
    print('NORMALIZING CATEGORIES')
    business['categories'] = business['categories'].apply(transform_funcs.check_str_list)
    print('CREATING KEYSPACE')
    session.execute("""
CREATE KEYSPACE IF NOT EXISTS henry WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 3 };
""")
    print('CREATING TABLE')
    session.execute("""
CREATE TABLE IF NOT EXISTS henry.business(address text, attributes list<frozen <list<text>>>, business_id text, categories list<text>, hours list<frozen <list<int>>>, is_open int, latitude float, longitude float, name text, postal_code text, review_count int, stars float, state_city list<text>,PRIMARY KEY(business_id))
""")
    print('UPLOADING DATAFRAME TO CASSANDRA')
    casspark.spark_pandas_insert(business,'henry','business',session,debug=True)
    print('DONE')




#DAG de Airflow
with DAG(dag_id='Test345',start_date=datetime.datetime(2022,8,25),schedule_interval='@once') as dag:

    t_load_tips = PythonOperator(task_id='load_tips',python_callable=load_tips)

    t_load_checkin = PythonOperator(task_id='load_checkin',python_callable=load_checkin)

    t_load_bussiness = PythonOperator(task_id='load_bussiness',python_callable=load_bussiness)


    t_load_bussiness >> t_load_checkin >> t_load_tips  