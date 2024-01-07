# Blogging Web Application API With Django Rest-Framework and DRF-SimpleJWT for Authentication

**This is a project built with genericAPIViews, Bare-bone APIView and Viewsets. It has the following Functionalities:**
- User Registration
- User Login/Authentication with SimpleJWT
- Creation, Editing and Deletion of Blog Post
- Liking of Blog Post 
- Commenting on Each Blog post
- Uploading of Profile Picture
- Email notifications of blogging activities in real time

## Follow these steps to access the endpoints
**Note: It is assumed that you have some knowledge of django**
- Open your terminal and paste the following code: `git clone https://github.com/FestusMike/BLOGGING_WEB_APP_API_ENDPOINTS.git`. This will clone the remote repository to your local machine and create a new directory which carries the name of repository you just cloned.
- Change into the new directory with the following command `cd BLOGGING_WEB_APP_API_ENDPOINTS`
- Run `git branch <branch_name>` and `git checkout <branch_name>` to create and switch to a new branch respectively.
- Run `git pull origin main` to pull latest changes into your new branch.
- Run the following command `pip install -r requirements.txt`. This will install all the dependencies in the requirements.txt file into your virtual environment.
- Since the database hasn't been hosted remotely, you are required to create a mysql database (or postgresql, as the case may be) on your localhost and also have your own `.env` file where configuration for enviroment variables will be stored. 
- Run `python manage.py makemigrations` and `python manage.py migrate` respectively to migrate your models for the `users` and `blog` apps to the database.
- Run `python manage.py runserver` in your terminal. This will start a server on your machine running on port `8000`.
- Launch your `Postman` or `Swagger` or any API testing and documentation tool. `curl` may also be used, depending on your preference.

## To register as a new user (Postman):

- Send a POST request to `http://localhost:8000/api/register` with the following json data as a body: 
``` 
    {
    "email" : "your email",
    "username" : "your alphanumeric username",
    "password" "Your Password"
    }
```
**The above data will be used to create your details as a new user and the server will in turn give you a response that contains a refresh and an access token. These bearer tokens will be used for authorizing you anytime you want to access a resouce on the API Server. Let us use this token to create a new blog category. `Note: You can't access any resource on the Api Server if the token isn't included in your header`.**
- Include your access token in your header with the `key` set to `Authorization` and the `value` set to `Bearer <access_token>`
- Include the refresh token in the `form-data` section with `refresh` as the `key` and the `value` as `<refresh_token>`. This will be used to refresh your access token when the duration expires. To Refresh an access token, Send a POST request to : `http://localhost:8000/api/token/refresh/`. This will provide you with a new access token.
- Send a GET request to: `http://localhost:8000/api/blog/categories/`

__Please note that a POST request cannot be sent to the endpoint above, as only admin users are authorized to create blog categories. Clients can only create blogs and perform different operations on them__
- You can create a new blog by sending a POST request to the following endpoint `http://localhost:8000/api/blog/posts/` with the following data as a request body:
``` 
    {
    "title" : "Your Blog Title",
    "categories" : ['pk of category],
    "body" : "The Content of your blog post"
    }
``` 
__Kindly note that you can send PUT, PATCH, and DELETE requests to this endpoint by suffixing the `posts` endpoint with the uuid of the post:__ `http://localhost:8000/api/blog/posts/<uuid:pk>/` __You can also fetch all the blogs by sending a GET request to this endpoint:__ `http://localhost:8000/api/blog/posts/`


## To Like or Comment on a Particular Post:
### To Like:
- Send a POST request to the following endpoint: `http://localhost:8000/api/blog/like/<uuid_of_the_blog>/`. __Note: The same endpoint unlikes the post if tried a second time.__
### To Comment:
- Send a POST request to the following endpoint: `http://localhost:8000/api/blog/comment/<uuid_of_the_blog>/` __Note: A comment also has an id and you can perform GET, PUT, PATCH and DELETE methods on them.__

## To Update your user profile
- Send a PUT(if you are updating all fields) or PATCH(If you are updating a some fields) request to `http://localhost:8000/api/user/` with the following json data as a request body:
``` 
    {
    "username" : "",
    "first_name" : "",
    "last_name" : ""
    }
``` 

## To Update Avatar and Personal Bio
- Send a PUT(if you are updating all fields) or PATCH(If you are updating a some fields) request to `http://localhost:8000/api/profile/` with the following json data as a request body:
``` 
    {
    "username" : "",
    "first_name" : "",
    "last_name" : ""
    }
``` 
**Note: If You are sending a PUT request, you have to use the form-data to pass in the request body. Set the first `key` to `bio` and set the `value` to your actual bio in text format(not json). Set the second `key` to `avatar` and set the dropdown to `file` so you can upload your profile picture. Hit the Send button and your bio and avatar will be created successfully.** 

**If You are sending a PATCH request, you have to pass in either your bio(as a json response body) or your avatar as a file inthe form-data tab**

## To Logout:
- Make sure your refresh token is still in the form-data tab and Send a POST request to `http://localhost:8000/api/logout/`.This will blacklist the refresh token and log you out.

## To Login:
- Send a POST request to `http://localhost:8000/api/login/` with the following json data as a request body:
 ``` 
    {
    "email" : "",
    "password" : "",
    }
```
- If your credentials are valid, You will be provided with an access and a refresh token, so you can access all authorized resources

> [!CAUTION]
> Please don't forget to include your `.env` file in the `.gitignore` file you've created in your root directory as such carelessness may leak important config information.

> [!IMPORTANT]
> You are free to create pull requests, as I would love to hear from you and learn from your innovation. You can also contact me through my profile information.

:gift_heart:


