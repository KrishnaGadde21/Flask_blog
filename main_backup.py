from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy  #making our  blog dynamic, connecting to db
import datetime


#created  config.json file so everyone can use. we will read all the parameters





app = Flask(__name__)



app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/pythonista'
db = SQLAlchemy(app)


class Contacts(db.Model):
    """
    sno,name,phone_num, msg, date, email

    """
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    phone_num = db.Column(db.String(12),  nullable=False)
    msg = db.Column(db.String(120),  nullable=False)
    date = db.Column(db.String(12), nullable=True )
    email = db.Column(db.String(20),  nullable=False)




@app.route("/")
def home():
    return render_template("index.html")    #flask automatically takes from templates folder


@app.route("/about")
def about():
    return render_template("about.html")    #flask automatically takes from templates folder


@app.route("/contact", methods=["GET","POST"])
def contact():
    if (request.method == 'POST'):
        '''add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

        """
            sno,name,phone_num, msg, date, email

        """

        entry = Contacts(name=name, phone_num=phone, msg=message,date=datetime.datetime.now(),email=email)
        db.session.add(entry)
        db.session.commit()

    return render_template("contact.html")    #flask automatically takes from templates folder

@app.route("/index")
def index():
    return render_template("index.html")    #flask automatically takes from templates folder





@app.route("/post")
def post():
    return render_template("post.html")    #flask automatically takes from templates folder


app.run(debug=True)