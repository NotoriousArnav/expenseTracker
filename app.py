from flask import (
        Flask,
        render_template,
        request,
        redirect,
        url_for,
        jsonify
    )
from models import (
        db,
        Expenses
    )
import uuid, time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'

from datetime import datetime, timezone

def convert_to_unix_timestamp(date_string):
    try:
        # Convert string to datetime object
        date_object = datetime.strptime(date_string, "%Y-%m-%dT%H:%M")

        # Convert datetime object to Unix timestamp
        unix_timestamp = float(date_object.replace(tzinfo=timezone.utc).timestamp())

        return unix_timestamp

    except ValueError:
        # Handle invalid date string
        return None

@app.route('/')
def index():
    expenses = Expenses.query.all()
    return render_template(
        'index.html',
        expenses=expenses
    )

@app.route('/expenses', methods=['GET', 'POST'])
def view_expenses():
    if request.method == 'POST':
        note = request.form['note']
        amount = float(request.form['amount'])
        timestamp = convert_to_unix_timestamp(request.form['date'])
        print(timestamp)
        print(request.form)
        id=str(uuid.uuid4())
        # Create a new expense
        new_expense = Expenses(id=id, note=note, amount=amount, timestamp=timestamp)

        # Add the expense to the database
        db.session.add(new_expense)
        db.session.commit()

        return redirect(url_for('index'))
    expenses = [
            {
                "currency": "INR",
                "id": x.id,
                "note": x.note,
                "amount": x.amount,
                "timestamp": x.timestamp
            } 
            for x in Expenses.query.all()
        ]
    return jsonify(expenses)
    #expenses = Expenses.query.all()
    #return render_template("expenses.html", expenses=expenses)

@app.route('/expenses/<expense_id>')
def view_expense(expense_id):
    expense = Expenses.query.get(expense_id)

    # Check if expense is found
    if expense is None:
        return jsonify({"error": "Expense not found"}), 404

    # Convert expense object to a dictionary
    expense_dict = {
        "currency": "INR",
        "id": expense.id,
        "note": expense.note,
        "amount": expense.amount,
        "timestamp": expense.timestamp
        # Add other fields as needed
    }

    return jsonify(expense_dict)
    #return render_template("expense_details.html", expense=expense)


if __name__ == "__main__":
    with app.app_context():
        db.init_app(app)
        db.create_all()
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )