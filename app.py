from flask import Flask ,render_template  ,request ,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)    # Flask App




# Database Model

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)


class Todo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=  db.Column(db.String(200),nullable=False )
    Description=db.Column(db.String(500),nullable=False)
    Date_created=db.Column(db.DateTime,default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
    





@app.route('/', methods=['GET', 'POST'])     # Route  is used for make pages 
def hello_world():
    if request.method=="POST":
        title=request.form['title']
        Description=request.form['Description']
        
    
        todo=Todo(title=title,Description=Description)
        db.session.add(todo)
        db.session.commit()
    
    alltodo= Todo.query.all()
    print(alltodo)
    return render_template('index.html', allTodo=alltodo)





@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    
    if request.method == "POST":
        title = request.form['title']
        Description = request.form['Description']
        todo= Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.Description=Description
        db.session.add(todo)
        db.session.commit()
        return redirect('/') 
        
    todo= Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)
     
    
   



@app.route("/delete/<int:sno>")    # Route  is used for make pages 
def delete(sno):
    todo= Todo.query.filter_by(sno=sno).first()
    if todo:
        
        db.session.delete(todo)
        db.session.commit()
    
    return redirect("/")


if __name__=="__main__":
    app.run(debug=True, port=8000)