from flask import Flask, render_template, request, redirect
from db_config import get_connection

app = Flask(__name__)

# HOME → VIEW ALL SLOTS
@app.route('/')
def index():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM slots")
    slots = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('index.html', slots=slots)


# BOOK PAGE
@app.route('/book/<int:slot_id>')
def book(slot_id):
    return render_template('book.html', slot_id=slot_id)


# CONFIRM BOOKING
@app.route('/confirm_booking', methods=['POST'])
def confirm_booking():
    name = request.form['name']
    slot_id = request.form['slot_id']

    if not name.strip():
        return "Invalid name!"

    conn = get_connection()
    cursor = conn.cursor()

    # Prevent double booking
    cursor.execute("""
        UPDATE slots
        SET is_booked = TRUE, booked_by = %s
        WHERE id = %s AND is_booked = FALSE
    """, (name, slot_id))

    conn.commit()

    if cursor.rowcount == 0:
        message = "failed"
    else:
        message = "success"

    cursor.close()
    conn.close()

    return render_template('success.html', message=message)


# VIEW ONLY BOOKED SLOTS
@app.route('/booked')
def booked_slots():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM slots WHERE is_booked = TRUE")
    slots = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('booked.html', slots=slots)


if __name__ == '__main__':
    app.run(debug=True)