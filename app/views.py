"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from forms import LoginForm, registerForm
from models import User
from bs4 import BeautifulSoup
import requests
import urlparse
from imagegetter import getimages


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')

@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')

@app.route("/api/users/login", methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('wishlist'))
        
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
            # Get the username and password values from the form.
             username = request.form['username']
             password = request.form['password']
             user = User.query.filter(username==username, password==password).first()
             
             if user is None:
                flash('Username or Password is invalid' , 'error')
             else:
                login_user(user)
                flash('Logged in successfully.', 'success')
                return redirect(url_for("wishlist"))
    flash_errors(form)            
    return render_template("login.html", form=form)

@app.route("/api/users/register", methods=['POST', 'GET'])
def register():
    form = registerForm()
    if request.method == 'POST' and form.validate():
            if User.query.filter_by(username=form.username.data).first():
                flash ('This username has already been taken')
            else:
            # save user to database
                user = User(form.first_name.data,form.last_name.data, form.username.data, form.password.data)
                db.session.add(user)
                db.session.commit()

                flash('Thanks for registering!')
                return redirect(url_for('login'))
    flash_errors(form)
    return render_template('register.html', form=form)

@app.route('/api/users/{userid}/wishlist', methods=['POST', 'GET'])
@login_required
def wishlist(userid):
    #if request.method == 'POST' and request.headers['Content-Type'] == 'application/json':
    user=User.query.filter_by(userid=userid).first_or_404()
    if user is None:
        return render_template('404.html')

    return render_template('wishlist.html')

@app.route('/api/users/{userid}/wishlist/{itemid}', methods=['DELETE'])
@login_required
def remove_wish():
        """Renders a secure page on our website that only logged in users can access."""
        return render_template('remove_wish.html')

@app.route('/api/thumbnails', methods=['GET'])
@login_required
def get_thumbnails():
        
    data={
              'error': "null", 
              'message': "Success", 
              'thumbnails': getimages()
            }
    
    return jsonify(data)

# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
))

@app.route("/api/users/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
