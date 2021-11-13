from os import SEEK_SET
from re import S
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail


app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'ENTER_URI_HERE'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'ENTER_URI_HERE'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Feedback(db.Model):
    __tablename__= 'feedback'
    id = db.Column(db.Integer, primary_key = True)
    customer = db.Column(db.String(200), unique = True)
    assistant = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, customer, assistant, rating, comments):
        self.customer = customer              
        self.assistant = assistant
        self.rating = rating
        self.comments =comments

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer_name']
        assistant = request.form['assistant']
        rating = request.form['rating']
        comments = request.form['comments']

        # print(customer, assistant, rating, comments)
        '''if the user don't insert his name or who was his assistant'''
        if customer == '' or assistant == '':
            return render_template('index.html', message = "please enter required fields")
        
        '''here we gonna connect to the DB and send it all the new data that we got from the user'''

        #checking if the customer name is not already in the DB
        if db.session.query(Feedback).filter(Feedback.customer == customer).count()==0:
            data = Feedback(customer,assistant, rating, comments)
            db.session.add(data)
            db.session.commit()
            '''sending mail to our customers service using Mailtrap'''
            send_mail(customer,assistant,rating,comments)

            return render_template('success.html')
        else:
            return render_template('index.html', message = "you have already submitted a feedback")



if __name__ == '__main__':
    
    app.run()
