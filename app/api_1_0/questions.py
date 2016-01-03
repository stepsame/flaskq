from flask import jsonify, request, g, url_for, current_app
from .. import db
from ..models import Question, Permission, Activity
from . import api
from .decorators import permission_required
from .errors import forbidden


@api.route('/questions/')
def get_questions():
    page = request.args.get('page', 1, type=int)
    pagination = Question.query.paginate(
        page, per_page=current_app.config['FLASKQ_QUESTIONS_PER_PAGE'],
        error_out=False)
    questions = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_questions', page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_questions', page=page+1, _external=True)
    return jsonify({
        'questions': [question.to_json() for question in questions],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/questions/<int:id>')
def get_question(id):
    question = Question.query.get(id)
    return jsonify(question.to_json())


@api.route('/questions/', methods=['POST'])
@permission_required(Permission.ASK)
def new_question():
    question = Question.from_json(request.json)
    question.author = g.current_user
    db.session.add(question)
    db.session.flush()
    question_activity = Activity(verb='asked', object=question,
                                  actor_id=g.current_user.id,
                                     timestamp=question.timestamp)
    db.session.add(question_activity)
    db.session.commit()
    return jsonify(question.to_json()), 201, \
        {'Location': url_for('api.get_question', id=question.id, _external=True)}


@api.route('/questions/<int:id>', methods=['PUT'])
@permission_required(Permission.ASK)
def edit_question(id):
    question = Question.query.get_or_404(id)
    if g.current_user != question.author and \
            not g.current_user.can(Permission.ADMINISTER):
        return forbidden('Insufficient permissions')
    question.body = request.json.get('body', question.body)
    db.session.add(question)
    db.session.commit()
    return jsonify(question.to_json())
