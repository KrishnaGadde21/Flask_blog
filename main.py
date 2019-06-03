from flask import Flask, render_template,request,session
from flask_sqlalchemy import SQLAlchemy  #making our  blog dynamic, connecting to db
import datetime
import json
from flask_mail import Mail


#created this config.json file so everyone can use. we will read all the parameters
#using this json file



with open("config.json",'r') as c:
    paramzz = json.load(c)["params"]

local_server = True
app = Flask(__name__)
app.secret_key = "supersecret"   #to set a secret key in flask
app.config.update(

        MAIL_SERVER = "smtp.gmail.com",
        MAIL_PORT = "465",
        MAIL_USE_SSL = True,
        MAIL_USERNAME = paramzz["gmail-user"],
        MAIL_PASSWORD = paramzz["gmail-password"]


)
mail = Mail(app)






if (local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] =  paramzz['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = paramzz['prod_uri']


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



class Posts(db.Model):

    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80),  nullable=False)
    slug = db.Column(db.String(21),  nullable=False)
    content = db.Column(db.String(120),  nullable=False)
    tagline = db.Column(db.String(12), nullable=True)
    date = db.Column(db.String(12), nullable=True )
    img_file  = db.Column(db.String(12), nullable=True )












@app.route("/")
def home():

    posts = Posts.query.filter_by().all()[0:3]  #  slicing
    return render_template("index.html", params=paramzz, posts = posts)    #flask automatically takes from templates folder
                                                            #passing json params in every template for fb,twitter, github url


@app.route("/about")
def about():
    return render_template("about.html",params=paramzz)    #flask automatically takes from templates folder


@app.route("/dashboard", methods = ['GET', 'POST'])
def dashboard():

    if('user' in session and session['user'] == paramzz['admin_user']):
        posts = Posts.query.all()
        return render_template('dashboard.html' , params = paramzz, posts = posts)



    if request.method == 'POST':
        username = request.form.get('uname')
        userpass = request.form.get('pass')

        if (username == paramzz['admin_user']) and (userpass == paramzz['admin_password']):
            #set the session variable
            session['user'] = username   #telling flask app that this user is logged in

            posts = Posts.query.all()

            return render_template('dashboard.html', params=paramzz , posts = posts)

    return render_template("login.html",params=paramzz)    #flask automatically takes from templates folder


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
        mail.send_message('New message from Blog',
                           sender = email,
                           recipients = [paramzz['gmail-user']],
                           body = message + '\n' +  phone + 'sender is ' + email +  'recipient is ' + paramzz['gmail-user']

                          )

    return render_template("contact.html",params=paramzz)    #flask automatically takes from templates folder

@app.route("/index")
def index():
    return render_template("index.html",params=paramzz)    #flask automatically takes from templates folder


@app.route("/post")
def post():
    return render_template("post.html",params=paramzz)    #flask automatically takes from templates folder




@app.route("/post/<string:post_slug>", methods = ['GET'])
def post_route(post_slug):                                 #This variable post_slug should be passed into function also according to Flask

    post = Posts.query.filter_by(slug = post_slug).first()  #uniquely identify the slug

    return render_template("post.html",params=paramzz, post = post )    #flask automatically takes from templates folder, passing variables posts = posts to the html page


app.run(debug=True)