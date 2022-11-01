#from crypt import methods
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# loo uus andmebaas, kui andmebaasi pole olemas
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tegevused.db'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)

    with app.app_context():
        db.create_all()

    return app, db

app, db = create_app()

@app.before_first_request
def create_tables():
    db.create_all()

class Tegevus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.Text, nullable=True)
    custom_category = db.Column(db.Text, nullable=True)
    due = db.Column(db.DateTime, nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return 'Tegevus ' + str(self.id)

# muuda tegevuse staatus tehtuks
@app.route('/complete_activity/<int:activity_id>', methods=['POST'])
def complete_activity(activity_id):
    activity = Tegevus.query.get(activity_id)
    activity.completed = not activity.completed
    db.session.commit()
    return redirect('/')

@app.route('/delete_activity/<int:activity_id>', methods=['POST'])
def delete_activity(activity_id):
    Tegevus.query.filter_by(id=activity_id).delete()
    db.session.commit()
    return redirect('/')
    

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        p_title = request.form['title']
        p_content = request.form['content']
        p_category = request.form['category']
        p_custom_category = request.form['custom_category']
        p_due = datetime.strptime(request.form['due'],"%Y-%m-%d")
        
        uus_tegevus = Tegevus(title=p_title, content=p_content, due=p_due, category=p_category, custom_category=p_custom_category)
        db.session.add(uus_tegevus)
        db.session.commit()
        return redirect('/')
    else:
        koik_tegevused = Tegevus.query.order_by(Tegevus.completed).all()
        return render_template('index.html', tegevused=koik_tegevused) # teeb kõik postitused veebis nähtavaks


if __name__ == "__main__":
    app.run()
    