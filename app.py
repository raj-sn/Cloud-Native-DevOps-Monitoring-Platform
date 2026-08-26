from db import get_connection
from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route("/health")
def health():

    try:
        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("SELECT 1")

        conn.close()

        return {
            "status": "UP",
            "database": "CONNECTED"
        }

    except Exception as e:

        return {
            "status": "DOWN",
            "database": "FAILED",
            "error": str(e)
        }, 500



@app.route("/")
def home():
    
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, name, email, department FROM employees"
    )

    rows = cursor.fetchall()

    conn.close()
    

    return render_template(
        "index.html",
        employees = rows
    )

@app.route("/add", methods=["POST"])
def add_employee():

    name = request.form["employee_name"]
    email = request.form["employee_email"]
    department = request.form["employee_department"]

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO employees
        (name, email, department)

        VALUES (%s, %s, %s)
        """,
        (name, email, department)
    )

    conn.commit()

    conn.close()

    return redirect("/")

@app.route("/delete/<int:employee_id>")
def delete_employee(employee_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM employees
        WHERE id = %s
        """,
        (employee_id,)
    )

    conn.commit()

    conn.close()

    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)