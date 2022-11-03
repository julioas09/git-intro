from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

db.create_all()

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
        return render_template('index.html')
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'
    
    

@app.route('/update/<int:id>')

def get_id(id):
    return render_template('update.html', task= id)

@app.route('/updtating_form/<int:id>', methods=['POST', 'GET'])
def update(id):
    delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(delete)
        db.session.commit()
    except:
        return 'Something Went Wrong'

    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        new_task.id=id
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'Something Went Wrong'
        return render_template('index.html')
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('update.html', tasks=tasks)
    return render_template('update.html', task= id)

if __name__ == '__main__':
    app.run(debug=True)
