from .models import Post
from sqlalchemy import or_


def get_posts(user=None, user_posts_only=False):
    """
    returns Published posts sorted by created_on
    Params:
        user not None: then include user's posts as well
        user_posts_only is True: then filter out posts of other users
    """

    filters = [Post.status == Post.PUBLISHED]
    if user:
        if user_posts_only:
            # remove the Post.status filter
            filters = [Post.user_id == user.id]
        else:
            filters.append(Post.user_id == user.id)
             
    posts = Post.query.with_entities(
        Post.id, Post.title, Post.status, Post.created_on
    ).filter(or_(*filters)
    ).order_by(Post.created_on).all()

    return posts