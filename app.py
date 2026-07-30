from dotenv import load_dotenv
import os
load_dotenv()

from flask import Flask, render_template, request, redirect, send_file
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from database import init_db, add_prayer_request, get_all_prayer_requests, add_subscriber, export_prayer_requests_csv

app = Flask(__name__)
init_db()

app.secret_key = os.environ.get('SECRET_KEY')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME')
ADMIN_PASSWORD_HASH = generate_password_hash(os.environ.get('ADMIN_PASSWORD'))

class Admin(UserMixin):
    id = 1

@login_manager.user_loader
def load_user(user_id):
    return Admin()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/sermons')
def sermons():
    return render_template('sermons.html')

@app.route('/events')
def events():
    return render_template('events.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/leadership')
def leadership():
    return render_template('leadership.html')

@app.route('/vision')
def vision():
    return render_template('vision.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/prayer', methods=['GET', 'POST'])
def prayer():
    if request.method == 'POST':
        if request.form.get('website'):
            return redirect('/')
        name = request.form.get('name')
        message = request.form.get('message')
        contact = request.form.get('contact')
        add_prayer_request(name, message, contact)
        return render_template('prayer_thanks.html')
    return render_template('prayer.html')

@app.route('/newsletter', methods=['POST'])
def newsletter():
    email = request.form.get('email')
    success = add_subscriber(email)
    if success:
        return render_template('newsletter_thanks.html')
    return render_template('newsletter_thanks.html', already=True)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD_HASH, password):
            login_user(Admin())
            return redirect('/admin')
        return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

@app.route('/admin')
@login_required
def admin():
    requests = get_all_prayer_requests()
    return render_template('admin.html', requests=requests)

@app.route('/admin/export')
@login_required
def export_data():
    filename = export_prayer_requests_csv()
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)