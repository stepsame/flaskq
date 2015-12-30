from flask import render_template, flash, redirect, url_for, request, \
    current_app, abort, make_response, jsonify
from flask.ext.login import login_required, current_user
from . import main
from .forms import EditProfileForm, EditProfileAdminForm, QuestionForm, \
    AnswerForm, CommentForm
from .. import db
from ..models import User, Role, Permission, Question, Answer, Comment, \
    Activity
from ..decorators import admin_required, permission_required


@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = QuestionForm()
    if current_user.can(Permission.ASK) and \
            form.validate_on_submit():
        question = Question(body=form.body.data,
                            detail=form.detail.data,
                            author=current_user._get_current_object())
        db.session.add(question)
        db.session.flush()
        question_activity = Activity(verb='asked', object=question,
                                  actor_id=current_user.id,
                                     timestamp=question.timestamp)
        db.session.add(question_activity)
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    show_followed = False
    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed', ''))
    if show_followed:
        query = current_user.followed_activities
    else:
        query = Activity.query
    pagination = query.order_by(Activity.timestamp.desc()).paginate(
            page, per_page=current_app.config['FLASKQ_ACTIVITIES_PER_PAGE'],
            error_out=False)
    activities = pagination.items
    comment_form = CommentForm()
    return render_template('index.html', form=form, activities=activities,
                           show_followed=show_followed, pagination=pagination,
                           comment_form=comment_form)


@main.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    pagination = user.answers.order_by(Answer.timestamp.desc()).paginate(
            page=page, per_page=current_app.config['FLASKQ_ANSWERS_PER_PAGE'],
            error_out=False)
    answers = pagination.items
    return render_template('user.html', user=user, answers=answers,
                           pagination=pagination, profile=True)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/question/<int:id>')
@login_required
def question(id):
    question = Question.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = question.answers.order_by(Answer.ranking.desc()).paginate(
            page, per_page=current_app.config['FLASKQ_ANSWERS_PER_PAGE'],
            error_out=False)
    answers = pagination.items
    return render_template('question.html', questions=[question],
                           answers=answers, pagination=pagination)


@main.route('/answer/<int:id>', methods=['GET', 'POST'])
@login_required
def answer(id):
    question = Question.query.get_or_404(id)
    form = AnswerForm()
    if form.validate_on_submit():
        answer = Answer(body=form.body.data,
                        question=question,
                        author=current_user._get_current_object())
        db.session.add(answer)
        db.session.flush()
        answer_activity = Activity(verb='wrote', object=answer,
                                  actor_id=current_user.id,
                                   timestamp=answer.timestamp)
        db.session.add(answer_activity)
        flash('Your answer has been published.')
        return redirect(url_for('.question', id=question.id))
    return render_template('edit_answer.html', form=form, id=question.id,
                           new=True)


@main.route('/comment/<int:id>', methods=['GET', 'POST'])
def comment(id):
    form = CommentForm()
    type = request.args.get('type')
    if type:
        answer = Answer.query.get_or_404(id)
        comments = answer.comments.order_by(Comment.timestamp.asc()).all()
        if form.validate_on_submit():
            comment = Comment(body=form.body.data,
                              answer=answer,
                              author=current_user._get_current_object())
            db.session.add(comment)
            db.session.commit()
            comments = answer.comments.order_by(Comment.timestamp.asc()).all()
            return render_template('_comments.html', form=form, comments=comments)
    else:
        question = Question.query.get_or_404(id)
        comments = question.comments.order_by(Comment.timestamp.asc()).all()
        if form.validate_on_submit():
            comment = Comment(body=form.body.data,
                              question=question,
                              author=current_user._get_current_object())
            db.session.add(comment)
            db.session.commit()
            comments = question.comments.order_by(Comment.timestamp.asc()).all()
            return render_template('_comments.html', form=form, comments=comments)
    return render_template('_comments.html', form=form, comments=comments)


@main.route('/edit-question/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_question(id):
    question = Question.query.get_or_404(id)
    if current_user != question.author and \
            not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = QuestionForm()
    if form.validate_on_submit():
        question.body = form.body.data
        question.detail = form.detail.data
        db.session.add(question)
        flash('The question has been updated.')
        return redirect(url_for('.question', id=question.id))
    form.body.data = question.body
    form.detail.data = question.detail
    return render_template('edit_question.html', form=form)


@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash('You are already following this user.')
        return redirect(url_for('.user', username=username))
    current_user.follow(user)
    flash('You are now following %s.' % username)
    return redirect(url_for('.user', username=username))


@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash('You are not following this user.')
        return redirect(url_for('.user', username=username))
    current_user.unfollow(user)
    flash('You are not following %s anymore.' % username)
    return redirect(url_for('.user', username=username))


@main.route('/followers/<username>')
@login_required
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
            page, per_page=current_app.config['FLASKQ_FOLLOWERS_PER_PAGE'],
            error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Follwers of",
                           endpoint='.followers', pagination=pagination,
                           follows=follows)


@main.route('/followed-by/<username>')
@login_required
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
            page, per_page=current_app.config['FLASKQ_FOLLOWERS_PER_PAGE'],
            error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Follwed by",
                           endpoint='.followed_by', pagination=pagination,
                           follows=follows)


@main.route('/edit-answer/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_answer(id):
    answer = Answer.query.get_or_404(id)
    if current_user != answer.author and \
            not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = AnswerForm()
    if form.validate_on_submit():
        answer.body = form.body.data
        db.session.add(answer)
        flash('The answer has been updated.')
        return redirect(url_for('.question', id=answer.question_id))
    form.body.data = answer.body
    return render_template('edit_answer.html', form=form, id=id)


@main.route('/all')
@login_required
def show_all():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '', max_age=30*24*60*60)
    return resp


@main.route('/followed')
@login_required
def show_followed():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '1', max_age=30*24*60*60)
    return resp


@main.route('/vote/<int:id>')
@login_required
def vote(id):
    answer = Answer.query.get_or_404(id)
    type = request.args.get('type')
    current_user.vote(answer, type)
    db.session.add(current_user)
    return jsonify(url=url_for('.unvote', id=id), upvotes=answer.upvotes)


@main.route('/unvote/<int:id>')
@login_required
def unvote(id):
    answer = Answer.query.get_or_404(id)
    type = request.args.get('type')
    current_user.unvote(answer, type)
    db.session.add(current_user)
    return jsonify(url=url_for('.vote', id=id), upvotes=answer.upvotes)


@main.route('/popover/<username>')
@login_required
def popover(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('_popover.html', user=user)