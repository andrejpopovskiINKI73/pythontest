from pythontest.models import User, Keywords
from pythontest import app, bcrypt, db
from flask import render_template, url_for, flash, redirect, request, abort
from pythontest.forms import RegistrationForm, LoginForm, SettingsForm, SuggestionsForm
from flask_login import login_user, current_user, logout_user, login_required
import feedparser


@app.route("/home")
@login_required
def home():
    return render_template('home.html')


@app.route("/", methods=['GET', 'POST'])
@app.route("/register", methods=['GET', 'POST'])
def register():
    db.create_all()
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
    keywords = db.session.query(Keywords).filter_by(user_id=current_user.id).first()
    form = SettingsForm()
    if form.validate_on_submit():
        key = Keywords(keyword=form.keywords.data, threshold=form.threshold.data, used_by=current_user)
        db.session.add(key)
        db.session.commit()
        flash('Settings have been saved', 'success')
        return redirect(url_for('suggestions'))
    return render_template('settings.html', title='Settings', form=form)


@app.route("/home/settings/update", methods=['GET', 'POST'])
@login_required
def update_settings():
    user = db.session.query(User).filter_by(id=current_user.id).first()
    if user.id != current_user.id:
        abort(403)
    keywords = db.session.query(Keywords).filter_by(user_id=current_user.id).first()
    form = SettingsForm()
    if form.validate_on_submit():
        keywords.keyword = form.keywords.data
        keywords.threshold = form.threshold.data
        db.session.commit()
        flash('Settings have been updated!', 'success')
        return redirect(url_for('suggestions'))
    elif request.method == 'GET':
        form.keywords.data = keywords.keyword
        form.threshold.data = keywords.threshold
    return render_template('settings.html', title='Settings', form=form)


@app.route("/home/suggestions", methods=['GET', 'POST'])
@login_required
def suggestions():
    form = SuggestionsForm()
    if form.validate_on_submit():
        rss = form.url.data
        feed = feedparser.parse(rss)
        key = db.session.query(Keywords.keyword).filter_by(user_id=current_user.id).first()
        thres = list(db.session.query(Keywords.threshold).filter_by(user_id=current_user.id).first())
        key1 = ''.join(key).split(',')
        counter = 0
        for post in feed.entries:
            for i in key1:
                if i in post.description.lower():
                    counter += 1
        return render_template('home.html', title='Home', feed=feed, key1=key1, counter=counter, thres=thres)
    return render_template('suggestions.html', title='Settings', form=form)
