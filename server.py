from flask import Flask, session, redirect, flash, request, render_template
from model import User, Reservation, connect_to_db
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'dev'

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect('/schedule')
    else:
        return redirect('/login')

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        user = User.query.filter(User.email==request.form.get('email')).first()
        if user is None:
            flash('Invalid user name! Please try again.')
            return render_template('login.html')
        else:
            session['user_id'] = user.user_id
            session['user_email'] = user.email
            flash(f'Welcome, {user.email}!')
            return redirect('/search')
    elif request.method == 'GET':
        if 'user_id' in session:
            return redirect('/search')
        return render_template('login.html')

@app.route('/search')
def search():
    if 'user_id' not in session:
        flash('You must log in to continue!')
        return redirect('/login')
    
    return render_template('search.html') 

@app.route('/view_appointments')
def view_appointments():
    if 'user_id' not in session:
        flash('You must log in to continue!')
        return redirect('/login')

    date = request.args.get('date')
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    try:
        start_date = datetime.strptime(f'{date} {start_time}', '%Y-%m-%d %H:%M')
        end_date = datetime.strptime(f'{date} {end_time}', '%Y-%m-%d %H:%M')
    except:
        flash('Error: invalid search parameters!')
        return redirect('/search')

    # Check if this user already has an appointment that day
    user = User.query.get(session['user_id'])
    for reservation in user.reservations:
        if reservation.date() == start_date.date():
            flash('Sorry, you are already signed up for an appointment on that day!')
            return redirect('/search')

    # Get all the reservations already booked on that day
    existent_reservations = [r.time for r in 
        Reservation.query.filter((Reservation.time >= start_date) & (Reservation.time < end_date)).all()]

    valid_reservations = []
    cur = start_date
    while cur < end_date:
        if cur in existent_reservations:
            continue
        valid_reservations.append(cur)
        cur = cur + timedelta(minutes=30)
    return render_template('choose_appointment.html', reservations=valid_reservations)

@app.route('/book_appointment', methods=['POST'])
def book_appointment():
    if 'user_id' not in session:
        flash('You must log in to continue!')
        return redirect('/login')
    
    try:
        date = datetime.strptime(request.form.get('date'), '%Y-%m-%d %H:%M:%S')
        # check that user has no appointments on that date
        # check that the date is available

    except:
        flash("Sorry, we couldn't fulfill that request! Please try again.")
        return redirect('/search')
    return ''

    
    

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', port=5000, debug=True)