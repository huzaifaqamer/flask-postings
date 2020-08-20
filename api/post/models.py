import datetime
from sqlalchemy_utils.types.choice import ChoiceType
from sqlalchemy_utils import force_auto_coercion

from api import db
from api.auth.models import User

force_auto_coercion()


class Post(db.Model):
    DRAFT = u'DRAFT'
    UNPUBLISHED = u'UNPUBLISHED'
    PUBLISHED = u'PUBLISHED'

    POST_STATUSES = [
        (DRAFT, DRAFT),
        (UNPUBLISHED, UNPUBLISHED),
        (PUBLISHED, PUBLISHED)
    ]

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.String(1000), nullable=False)
    status = db.Column(
        ChoiceType(POST_STATUSES),
        default=DRAFT,
        nullable=False
    )
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    modified_on = db.Column(db.DateTime, server_default=db.func.now(), onupdate=datetime.datetime.utcnow)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )
    author = db.relationship(
        User,
        backref=db.backref('posts', lazy=True, cascade="all, delete")
    )