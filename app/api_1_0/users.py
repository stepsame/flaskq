from flask import jsonify, request, current_app, url_for
from . import api
from ..models import User, Question, Answer, Activity


@api.route('/users/<int:id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())


@api.route('/users/<int:id>/questions/')
def get_user_questions(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = user.questions.order_by(Question.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKQ_QUESTIONS_PER_PAGE'],
        error_out=False)
    questions = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_user_questions', page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_user_questions', page=page+1, _external=True)
    return jsonify({
        'questions': [question.to_json() for question in questions],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/users/<int:id>/answers/')
def get_user_answers(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = user.answers.order_by(Answer.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKQ_ANSWERS_PER_PAGE'],
        error_out=False)
    answers = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_user_answers', page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_user_answers', page=page+1, _external=True)
    return jsonify({
        'answers': [answer.to_json() for answer in answers],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/users/<int:id>/timeline/')
def get_user_followed_activities(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = user.followed_activities.order_by(Activity.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKQ_ACTIVITIES_PER_PAGE'],
        error_out=False)
    activities = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for(
                'api.get_user_followed_activities', page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for(
                'api.get_user_followed_activities', page=page+1, _external=True)
    return jsonify({
        'activities': [activity.object.to_json() for activity in activities],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })