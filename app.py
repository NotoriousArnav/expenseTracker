from flask import (
        Flask,
        render_template,
        request,
        redirect,
        url_for,
        jsonify,
        send_file
    )
from models import (
        db,
        Expenses
    )

from datetime import datetime, timezone
import matplotlib.pyplot as plt
import uuid, time, io
import pandas as pd
import base64

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'


def convert_to_unix_timestamp(date_string):
    try:
        # Convert string to datetime object
        date_object = datetime.strptime(
            date_string,
            "%Y-%m-%dT%H:%M"
        )

        # Convert datetime object to Unix timestamp
        unix_timestamp = float(
            date_object.replace(
                tzinfo=timezone.utc
            ).timestamp()
        )

        return unix_timestamp

    except ValueError:
        # Handle invalid date string
        return None


# TODO: Add Multi User Support
# TODO: Add dotenv support

@app.route('/')
def index():
    expenses = Expenses.query.all()
    return render_template(
        'index.html',
        expenses=expenses
    )

@app.route('/chart', methods=['GET'])
def generate_chart():
    # Fetch all expenses from the database
    expenses = Expenses.query.all()

    # Create a Pandas DataFrame from the expense data
    import pandas as pd
    df = pd.DataFrame([(expense.category, expense.amount) for expense in expenses], columns=['category', 'amount'])

    # Create a simple bar chart using Matplotlib
    plt.figure(figsize=(8, 5))
    plt.bar(df['category'], df['amount'], color='skyblue')
    plt.xlabel('Expense Category')
    plt.ylabel('Amount (in Currency)')
    plt.title('Expense Distribution')

    # Save the chart to a BytesIO object
    img_stream = io.BytesIO()
    plt.savefig(img_stream, format='png')
    img_stream.seek(0)
    plt.close()

    # Convert the image to base64 for embedding in HTML
    return send_file(img_stream, mimetype="image/png")

@app.route('/api')
def api_docs():
    return render_template('api_docs.html')

@app.route('/expenses', methods=['GET', 'POST'])
def view_expenses():
    if request.method == 'POST':
        note = request.form['note']
        amount = float(request.form['amount'])
        timestamp = convert_to_unix_timestamp(request.form['date'])
        category = request.form['category']
        print(timestamp)
        print(request.form)
        id=str(uuid.uuid4())
        # Create a new expense
        new_expense = Expenses(
                id=id,
                note=note,
                amount=amount,
                timestamp=timestamp,
                category=category
            )

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

@app.route('/export/<format>')
def export_expenses(format):
    expenses = Expenses.query.all()
    df = pd.DataFrame([
        {
            "Timestamp": expense.timestamp,
            "Note": expense.note,
            "Amount": expense.amount,
            "Category": expense.category
        }
        for expense in expenses
    ])

    if format == 'csv':
        filename = 'expenses.csv'
        df.to_csv(filename, index=False)
        mimetype = 'text/csv'
    elif format == 'xlsx':
        filename = 'expenses.xlsx'
        df.to_excel(filename, index=False)
        mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    else:
        return jsonify({"error": "Invalid format"}), 400

    return send_file(filename, mimetype=mimetype, as_attachment=True)


if __name__ == "__main__":
    with app.app_context():
        db.init_app(app)
        db.create_all()
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
