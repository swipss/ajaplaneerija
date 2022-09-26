from flask import Flask

app = Flask(__name__)

@app.route('/')
@app.route('/avaleht')
def hello_world():
    return 'Tere, maailm!' 
  
if __name__ == '__main__':
    app.run()
