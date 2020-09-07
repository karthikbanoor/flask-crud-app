from flask import Flask, request, render_template
import config
import json
from bson import ObjectId

app = Flask(__name__)


# postgres
connection = config.postgres_congig()

connection.autocommit = True

cursor = connection.cursor()

# mongodb
mongodb_connection = config.mongo_config()
dataBase = mongodb_connection['employee']

collection = dataBase['emp']


@app.route('/')
def home_page():
    return render_template("index.html")


@app.route('/insert', methods=['POST'])
def insert_emp_data():
    try:

        if request.method == 'POST':

            name = request.form["name"]
            phone = request.form["phone"]
            age = request.form["age"]

            # postgres
            insert_query = '''INSERT INTO empdata(name, phone, age) VALUES (%s,%s,%s)'''

            record = (name, phone, age)

            result = cursor.execute(insert_query, record)

            print("-----------data inserted into postgres-----------")

            # mongo
            result = collection.insert(
                {"name": name, "phone": phone, "age": age})

            print("--------data inserted into mongodb----------")

            return render_template("index.html", result=result)

    except Exception as error:
        print("Error while inserting data into database", error)


@app.route('/get', methods=['GET'])
def get_emp_data():

    try:

        cursor.execute('''select * from empdata''')

        result1 = cursor.fetchall()

        db_data = []

        for result in result1:

            print(len(result))

            postgres_db_data = {
                "_id": id(result[0]),
                "name": result[0],
                "phone": result[1],
                "age": result[2]
            }

            db_data.append(postgres_db_data)

        # mongodb
        obj = collection.find()

        for data in obj:
            db_data.append(data)

        return render_template("employees_data.html", users=db_data)

    except Exception as error:
        print("Error while fetching data from PostgreSQL", error)


@app.route('/update', methods=['POST'])
def update_emp_info():

    try:

        oldname = request.form["oldname"]
        newname = request.form["newname"]

        # postgres

        query = '''update empdata set name=(%s) where name=(%s)'''

        record = (newname, oldname)

        cursor.execute(query, record)

        print("data updated successfully in postgres")

        # mongo
        collection.update({'name': oldname}, {
            "$set": {"name": newname}})

        print("data updated successfully in mongodb")

        # getdata
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

        return render_template("employees_data.html", users=db_data)

    except Exception as error:
        print("Error while updating data into PostgreSQL", error)


@ app.route('/delete', methods=['POST'])
def delete_emp_info():

    try:

        print("call from html delete")

        # id = request.form["id"]

        name = request.form["name"]

        print("--------name----------", name)

        delete_query = '''delete from empdata where name=(%s) '''

        record = (name,)

        cursor.execute(delete_query, record)

        print("record deleted successfully from postgres")

        collection.delete_one({"name": name})

        print("record deleted successfully from mongodb")

        # get_data

        cursor.execute('''select * from empdata''')

        result1 = cursor.fetchall()

        db_data = []

        for result in result1:

            print("-----result-----", result)

            postgres_db_data = {
                "_id": id(result[0]),
                "name": result[0],
                "phone": result[1],
                "age": result[2]
            }

            db_data.append(postgres_db_data)

        obj = collection.find()

        # db_data = []

        for data in obj:

            db_data.append(data)

        return render_template("employees_data.html", users=db_data)

    except Exception as error:
        print("Error while deleting data from PostgreSQL", error)


if __name__ == '__main__':

    app.run(host="0.0.0.0", debug=True)
