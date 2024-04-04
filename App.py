from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

app = Flask(__name__)
app.secret_key = "Secret Key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/crud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))

    def __init__(self, id, name, email, phone):  # Update constructor to accept id parameter
        self.id = id  # Manually assign ID
        self.name = name
        self.email = email
        self.phone = phone

@app.route('/')
def index():
    try:
        all_data = Data.query.all()
        return render_template("index.html", employees=all_data)
    except exc.SQLAlchemyError as e:
        error = str(e)
        return render_template("error.html", error=error)

@app.route('/insert', methods=['POST'])
def insert():
    try:
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']

            # Get the maximum existing ID
            max_id = db.session.query(db.func.max(Data.id)).scalar()

            # If max_id is None, set it to 0
            if max_id is None:
                max_id = 0

            # Assign ID as 1 more than the maximum existing ID
            new_id = max_id + 1

            my_data = Data(new_id, name, email, phone)
            db.session.add(my_data)
            db.session.commit()
            flash("Employee data added successfully", "success")
            return redirect(url_for('index'))
    except exc.SQLAlchemyError as e:
        error = str(e)
        return render_template("error.html", error=error)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    try:
        my_data = Data.query.get_or_404(id)
        if request.method == "POST":
            my_data.name = request.form['name']
            my_data.email = request.form['email']
            my_data.phone = request.form['phone']

            db.session.commit()
            flash('Employee data updated successfully', "success")
            return redirect(url_for('index'))
        return render_template("update.html", data=my_data)
    except exc.SQLAlchemyError as e:
        error = str(e)
        return render_template("error.html", error=error)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    try:
        my_data = Data.query.get_or_404(id)
        db.session.delete(my_data)
        db.session.commit()
        flash('Employee data deleted successfully', "success")
        return redirect(url_for('index'))
    except exc.SQLAlchemyError as e:
        error = str(e)
        return render_template("error.html", error=error)

if __name__ == "__main__":
    app.run(debug=True)
