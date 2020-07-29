## Flask Postings
It is a practice Flask RESTful application. It performs the following fuctionalities.

- User Signup
- User Authentication
- A Post Model with following endpoints
    - Authenticated user can create a post.
    - Owner of post can update it.
    - List API which returns `id`, `title`, `status` and `created_on` sorted by `created_on` of posts.
    - List API shows published posts to all users.
    - List API returns all posts of the authenticated user.
    - List API has a filter to only show authenticated user's posts.
    - Retrieve API which fetches published posts only.
    - Retrieve API should count the number of views by non-authors.