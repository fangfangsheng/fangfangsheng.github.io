from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/fangfangsheng'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://oqosunhicsfppk:083c1d89d14292313a4912e715f47059405d78035fc230e5425bcef8ecdf0e08@ec2-23-21-94-99.compute-1.amazonaws.com:5432/dfin5v406s7174'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Result(db.Model):
    __tablename__ = 'contacts'

    id = db.Column(db.Integer, primary_key=True)
    visitor = db.Column(db.String(200), unique=True)
    methods = db.Column(db.String(200))
    contact = db.Column(db.Text())

    def __init__(self, visitor, methods, contact):
        self.visitor = visitor
        self.methods = methods
        self.contact = contact


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        visitor = request.form['visitor']
        methods = request.form['methods']
        contact = request.form['contact information']
        # print(visitor, methods, contact)
        if visitor == '' or contact == '':
            return render_template('index.html', message='Please enter your contact information')
        if db.session.query(Result).filter(Result.visitor == visitor).count() == 0:
            data = Result(visitor, methods, contact)
            db.session.add(data)
            db.session.commit()
            return render_template('success.html')
        return render_template('index.html', message="Don't worry. I have already got your contact.")

if __name__ =='__main__':
    app.run()
