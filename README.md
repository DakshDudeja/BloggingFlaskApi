1. Create User
Endpoint: POST /user

Request:

{
  "username": "example_username",
  "password": "example_password"
}

Response:

{
  "message": "User created successfully",
  "user_id": "created_user_id"
}


2. Update User
Endpoint: PUT /user/<user_id>

Request:

{
  "_id": "user_id_to_update",
  "username": "new_username",
  "password": "new_password"
}

Response
{
  "message": "User updated successfully"
}

3. Get Users
Endpoint: GET /users

Response (Success):
{
  "users": [
    {
      "_id": "user_id_1",
      "username": "user1",
      "password": "password1"
    },
    {
      "_id": "user_id_2",
      "username": "user2",
      "password": "password2"
    },
    ...
  ]
}

4. Create Blog Post
Endpoint: POST /blogpost

Request:
{
  "title": "example_title",
  "desc": "example_description",
  "posted_by": "user_id"
}


{
  "message": "Blog post created successfully",
  "blog_post_id": "created_blog_post_id"
}



5. Update Blog Post
Endpoint: PUT /blogpost/<blog_post_id>

Request:

{
  "title": "new_title",
  "desc": "new_description",
  "likes": 10
}

{
  "message": "Blog post updated successfully"
}

6. Delete Blog Post
Endpoint: DELETE /blogpost/<blog_post_id>

Response (Success):

{
  "message": "Blog post deleted successfully"
}

7. Get Blog Posts
Endpoint: GET /blogposts

Response (Success):

{
  "blog_posts": [
    {
      "_id": "blog_post_id_1",
      "title": "title1",
      "desc": "description1",
      "likes": 5,
      "posted_by": "user_id_1"
    },
    {
      "_id": "blog_post_id_2",
      "title": "title2",
      "desc": "description2",
      "likes": 10,
      "posted_by": "user_id_2"
    },
    ...
  ]
}

8. Get Blog Posts by User ID
Endpoint: GET /blogposts/user/<user_id>

Response (Success):

{
  "blog_posts": [
    {
      "_id": "blog_post_id_1",
      "title": "title1",
      "desc": "description1",
      "likes": 5,
      "posted_by": "user_id_1"
    },
    {
      "_id": "blog_post_id_2",
      "title": "title2",
      "desc": "description2",
      "likes": 10,
      "posted_by": "user_id_1"
    },
    ...
  ]
}




