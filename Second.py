from flask import Flask, render_template
app = Flask(__name__)



@app.route("/")
def hello():
    return render_template("index.html")    #flask automatically takes from templates folder


@app.route("/about")
def krishna():
    firstname="goku "
    return render_template("about.html",name=firstname)  #creates a variable name in this template, and its name is goku
                                                        #this  name=firstname  , name should be name in about.html




app.run(debug=True )
