from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tegevused.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Tegevus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    due = db.Column(db.DateTime, nullable=False)
   
    completed = db.Column(db.Boolean, default=False)
    def __repr__(self):
        return 'Tegevus ' + str(self.id)
    
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        p_title = request.form['title']
        p_content = request.form['content']
        p_due = datetime.strptime(request.form['due'],"%Y-%m-%d")
        
        uus_tegevus = Tegevus(title=p_title, content=p_content, due=p_due)
        db.session.add(uus_tegevus)
        db.session.commit()
        return redirect('/')
    else:
        koik_tegevused = Tegevus.query.order_by(Tegevus.due).all()
        return render_template('index.html', tegevused=koik_tegevused) # teeb kõik postitused veebis nähtavaks



if __name__ == "__main__":
    app.run()
    

