from datetime import datetime

from flask import render_template, redirect, url_for, flash, g, session, request, abort, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required

from . import app, db, lm
from .forms import RegisterForm, LoginForm, AskForm, AnswerForm
from .models import User, Question, Answer
from config import RECORDS_PER_PAGE


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.route('/')
@app.route('/<int:page>')
def index(page=1):
    questions = Question.query.paginate(page, RECORDS_PER_PAGE, True)
    return render_template('index.html', questions=questions)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(login=form.login.data, password=form.password.data, email=form.email.data)
        db.session.add(user)
        db.session.commit()
        flash('Your successfully registered!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title='Registration')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()
        session['remember_me'] = form.remember_me.data
        remember_me = False
        if 'remember_me' in session:
            remember_me = session['remember_me']
            session.pop('remember_me', None)
        login_user(user, remember=remember_me)
        flash('Logged in successfully')
        return redirect(request.args.get('next') or url_for('index'))
    return render_template('login.html', form=form, title='Login')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/ask', methods=['GET', 'POST'])
@login_required
def ask():
    form = AskForm()
    if form.validate_on_submit():
        question = Question(title=form.title.data, body=form.body.data, date=datetime.utcnow(), author=g.user)
        db.session.add(question)
        db.session.commit()
        flash('Your question successfully added!')
        return redirect(url_for('index'))
    return render_template('ask_question.html', form=form, title='Ask your question')


@app.route('/answers/<int:question_id>', methods=['GET', 'POST'])
@app.route('/answers/<int:question_id>/<int:page>', methods=['GET', 'POST'])
def answers(question_id=None, page=1):
    if question_id is None:
        abort(404)
    question = Question.query.get_or_404(question_id)
    answers = question.answers.paginate(page, RECORDS_PER_PAGE, True)
    form = None

    # Posting answers only for authenticated users
    if g.user.is_authenticated():
        form = AnswerForm()
        if form.validate_on_submit():
            answer = Answer(date=datetime.utcnow(), body=form.body.data, author=g.user, question=question)
            db.session.add(answer)
            db.session.commit()
            flash('Got it!')
            return redirect(url_for('answers', question_id=question_id, page=page))
    return render_template('answers.html', question=question, answers=answers, form=form)


@app.route('/like', methods=['POST'])
@login_required
def like():
    answer_id = request.form['answer_id']
    answer = Answer.query.get(answer_id)
    if answer:
        answer.like(g.user)
        db.session.add(answer)
        db.session.commit()
        return jsonify(likes=len(answer.likes.all())), 200