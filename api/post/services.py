from api import db
from .models import Post


def create_post(
    title,
    body,
    author,
    status=Post.DRAFT
):
    post = Post(
        title = title,
        body = body,
        status = status,
        author = author
    )

    db.session.add(post)
    db.session.commit()

    return post