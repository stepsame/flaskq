from flask import jsonify, request, g, url_for, current_app
from .. import db
from ..models import Comment, Permission, Question, Answer
from . import api
from .decorators import permission_required


@api.route('/comments/')
def get_comments():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKQ_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_comments', page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_comments', page=page+1, _external=True)
    return jsonify({'comments': [comment.to_json() for comment in comments]})


@api.route('/comments/<int:id>')
def get_comment(id):
    comment = Comment.query.get_or_404(id)
    return jsonify(comment.to_json())


@api.route('/questions/<int:id>/comments/')
def get_question_comments(id):
    question = Question.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = question.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['FLASKQ_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_question_comments', page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_question_comments', page=page+1, _external=True)
    return jsonify({
        'posts': [comment.to_json() for comment in comments],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/answers/<int:id>/comments/')
def get_answer_comments(id):
    answer = Answer.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = answer.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['FLASKQ_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_answer_comments', page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_answer_comments', page=page+1, _external=True)
    return jsonify({
        'posts': [comment.to_json() for comment in comments],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/questions/<int:id>/comments/', methods=['POST'])
@permission_required(Permission.COMMENT)
def new_question_comment(id):
    question = Question.query.get_or_404(id)
    comment = Comment.from_json(request.json)
    comment.author = g.current_user
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.to_json()), 201, \
        {'Location': url_for('api.get_comment', id=comment.id, _external=True)}


@api.route('/answers/<int:id>/comments/', methods=['POST'])
@permission_required(Permission.COMMENT)
def new_answer_comment(id):
    answer = Answer.query.get_or_404(id)
    comment = Comment.from_json(request.json)
    comment.author = g.current_user
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.to_json()), 201, \
        {'Location': url_for('api.get_comment', id=comment.id, _external=True)}



