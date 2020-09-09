import config


# postgres
connection = config.postgres_congig()

connection.autocommit = True

cursor = connection.cursor()

# mongodb
mongodb_connection = config.mongo_config()
dataBase = mongodb_connection['employee']

collection = dataBase['emp']


def get_data():

    cursor.execute('''select * from empdata''')

    result1 = cursor.fetchall()

    db_data = []

    for result in result1:

        postgres_db_data = {
            "_id": id(result[0]),
            "name": result[0],
            "phone": result[1],
            "age": result[2]
        }

        db_data.append(postgres_db_data)

    obj = collection.find()

    for data in obj:
        db_data.append(data)

    return db_data
