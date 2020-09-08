import pymongo
import psycopg2


def mongo_config():

    client = pymongo.MongoClient("mongodb://172.17.0.2:27017")

    return client


def postgres_congig():

    connection = psycopg2.connect(
        user="postgres", password="password", host="172.17.0.3", port="5432", database="emp")

    return connection
