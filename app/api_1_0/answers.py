from flask import jsonify, request, g, url_for, current_app
from .. import db
from ..models import Permission, Question, Answer, Activity
from . import api
from .decorators import permission_required
from .errors import forbidden


@api.route('/answers/')
def get_answers():
    page = request.args.get('page', 1, type=int)
    pagination = Answer.query.order_by(Answer.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKQ_ANSWERS_PER_PAGE'],
        error_out=False)
    answers = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_answers', page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_answers', page=page+1, _external=True)
    return jsonify({
        'answers': [answer.to_json() for answer in answers],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/answers/<int:id>')
def get_answer(id):
    answer = Answer.query.get(id)
    return jsonify(answer.to_json())


@api.route('/questions/<int:id>/answers/')
def get_question_answers(id):
    question = Question.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = question.answers.order_by(Answer.timestamp.asc()).paginate(
        page, per_page=current_app.config['FLASKQ_ANSWERS_PER_PAGE'],
        error_out=False)
    answers = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_question_answers', page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_question_answers', page=page+1, _external=True)
    return jsonify({
        'answers': [answer.to_json() for answer in answers],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/questions/<int:id>/answers/', methods=['POST'])
@permission_required(Permission.ANSWER)
def new_question_answer(id):
    question = Question.query.get_or_404(id)
    answer = Answer.from_json(request.json)
    answer.author = g.current_user
    answer.question = question
    db.session.add(answer)
    db.session.flush()
    answer_activity = Activity(verb='wrote', object=answer,
                                  actor_id=g.current_user.id,
                                   timestamp=answer.timestamp)
    db.session.add(answer_activity)
    db.session.commit()
    return jsonify(answer.to_json()), 201, \
        {'Location': url_for('api.get_answer', id=answer.id, _external=True)}


@api.route('/answers/<int:id>', methods=['PUT'])
@permission_required(Permission.ANSWER)
def edit_answer(id):
    answer = Answer.query.get_or_404(id)
    if g.current_user != answer.author and \
            not g.current_user.can(Permission.ADMINISTER):
        return forbidden('Insufficient permissions')
    answer.body = request.json.get('body', answer.body)
    db.session.add(answer)
    db.session.commit()
    return jsonify(answer.to_json())
