from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
import yaml

app2 = Flask(__name__)
Bootstrap(app2)

#configure db
db = yaml.full_load(open('db.yaml'))
app2.config['MYSQL_HOST'] = db['mysql_host']
app2.config['MYSQL_USER'] = db['mysql_user']
app2.config['MYSQL_PASSWORD'] = db['mysql_password']
app2.config['MYSQL_DB'] = db['mysql_db']
mysql = MySQL(app2)  

@app2.route('/', methods = ["GET", "POST"])
def index():
    if request.method == "POST":
        form = request.form
        name = form['name']
        age = form ['age']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user(name, age) VALUES (%s, %s)", [name, age])  
        mysql.connection.commit()        #to execute operation in SQL query

    
    return render_template ('index.html')

@app2.route('/users/')

def users():
    cur=mysql.connection.cursor()
    values = cur.execute("SELECT * FROM user")
    if values > 0:
        users = cur.fetchall()
        return render_template ('users.html', users = users)      # why is there an indent here?


if __name__ == "__main__":
   app2.run(debug=True)