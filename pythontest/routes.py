from pythontest.models import User, Keywords
from pythontest import app, bcrypt, db, session
from flask import render_template, url_for, flash, redirect, request
from pythontest.forms import RegistrationForm, LoginForm, SettingsForm, SuggestionsForm
from flask_login import login_user, current_user, logout_user, login_required
import feedparser

'''articles = [ {
    'article': "Article 1",
    'content': "content 1",
    'link': "Link1"
}, {
    'article': "Article 2",
    'content': "content 2",
    'link': "Link2"
}
]'''

# Login Required ke treba!
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/", methods=['GET', 'POST'])
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('settings'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created, you can now Log In!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('settings'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('settings'))
        else:
            flash('Unsuccessful login!', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('register'))


@app.route("/home/settings", methods=['GET', 'POST'])
@login_required
def settings():
    form = SettingsForm()
    if form.validate_on_submit():
        key = Keywords(keyword=form.keywords.data, threshold=form.threshold.data, used_by=current_user)
        db.session.add(key)
        db.session.commit()
        flash('Settings have been saved', 'success')
        return redirect(url_for('suggestions'))
    return render_template('settings.html', title='Settings', form=form)


@app.route("/home/suggestions", methods=['GET', 'POST'])
@login_required
def suggestions():
    form = SuggestionsForm()
    if form.validate_on_submit():
        rss = form.url.data
        feed = feedparser.parse(rss)
        key = ['python', 'java']
        for post in feed.entries:
            for i in key:
                if i in post.title.lower():
                    flash(f'{post.title} : {post.link} \n')
        return redirect(url_for('home'))
    return render_template('suggestions.html', title='Settings', form=form)
