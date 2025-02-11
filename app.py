from flask import Flask, render_template, request, redirect, url_for, session, send_file
import mysql.connector
import csv
import os

app = Flask(__name__)
app.secret_key = "my_secret_12345"  # Needed for session handling


# ✅ MySQL Database Connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",  # UPDATE THIS
        database="construction_db"
    )


# ✅ Authentication Routes (Login & Signup)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('home'))
        else:
            return "Invalid credentials! Try again."

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# ✅ Home Route - Show Materials
@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM materials")
    materials = cursor.fetchall()
    cursor.close()
    conn.close()

    total_cost = sum(m['quantity'] * m['price'] for m in materials)
    return render_template('index.html', materials=materials, total_cost=total_cost)


# ✅ Add Material
@app.route('/add', methods=['GET', 'POST'])
def add_material():
    if request.method == 'POST':
        name = request.form['name']
        quantity = float(request.form['quantity'])
        price = float(request.form['price'])

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO materials (name, quantity, price) VALUES (%s, %s, %s)", (name, quantity, price))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('home'))

    return render_template('add_material.html')


# ✅ Edit Material
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_material(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        name = request.form['name']
        quantity = float(request.form['quantity'])
        price = float(request.form['price'])

        cursor.execute("UPDATE materials SET name=%s, quantity=%s, price=%s WHERE id=%s", (name, quantity, price, id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('home'))

    cursor.execute("SELECT * FROM materials WHERE id = %s", (id,))
    material = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('edit_material.html', material=material)


# ✅ Delete Material
@app.route('/delete/<int:id>')
def delete_material(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM materials WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('home'))


# ✅ Export to CSV
@app.route('/export')
def export_csv():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM materials")
    materials = cursor.fetchall()
    cursor.close()
    conn.close()

    filename = "materials.csv"
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Name", "Quantity", "Price", "Total Cost"])
        for material in materials:
            writer.writerow([material["id"], material["name"], material["quantity"], material["price"],
                             material["quantity"] * material["price"]])

    return send_file(filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
