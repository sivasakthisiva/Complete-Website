from flask import Flask,render_template,request,redirect,url_for,session
import mysql.connector

app = Flask(__name__)

app.secret_key="secret123"

db=mysql.connector.connect(
host="localhost",
user="root",
password="root",
database="flask_auth"
)

cursor=db.cursor()

@app.route('/')
def login():
    return render_template("login.html")

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/home')
def home():

    if 'name' in session:
        return render_template("home.html",name=session['name'])

    return redirect(url_for('login'))

@app.route('/register_user',methods=['POST'])
def register_user():

    name=request.form['name']
    email=request.form['email']
    password=request.form['password']

    sql="INSERT INTO users(name,email,password) VALUES(%s,%s,%s)"
    val=(name,email,password)

    cursor.execute(sql,val)
    db.commit()

    return redirect(url_for('login'))

@app.route('/login_user',methods=['POST'])
def login_user():

    email=request.form['email']
    password=request.form['password']

    sql="SELECT * FROM users WHERE email=%s AND password=%s"
    val=(email,password)

    cursor.execute(sql,val)

    user=cursor.fetchone()

    if user:
        session['name']=user[1]
        return redirect(url_for('home'))

    else:
        return "Login Failed"

@app.route('/logout')
def logout():

    session.pop('name',None)

    return redirect(url_for('login'))

if __name__=="__main__":
    app.run(debug=True)