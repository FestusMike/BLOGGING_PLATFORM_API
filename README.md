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
- Open your terminal and paste the following code: ```git clone https://github.com/FestusMike/BLOGGING_WEB_APP_API_ENDPOINTS.git```. This will clone the remote repository to your local machine and create a new directory which carries the name of repository you just cloned.
- Change into the new directory with the following command `cd BLOGGING_WEB_APP_API_ENDPOINTS`
- Run `git branch <branch_name>` and ```git checkout <branch_name>` to create and switch to a new branch respectively.
- Run `git pull origin main` to pull latest changes into your new branch.
- Run the following command `pip install -r requirements.txt`. This will install all the dependencies in the requirements.txt file into your virtual environment.
- Since the database hasn't been hosted remotely, you are required to create a mysql database (or postgresql, as the case may be) on your localhost and also have your own `.env` file where configuration for enviroment variables will be stored. 
- Run `python manage.py makemigrations` and `python manage.py migrate` respectively to migrate your models for the `users` and `blog` apps to the database.
- Run `python manage.py runserver` in your terminal. This will start a server on your machine running on port `8000`.
- Launch your `Postman` or `Swagger` or any API testing and documentation tool. `curl` may also be used, depending on your preference.

## To register as a new user(Postman will be used as an example):

- Send a POST request to ```http://localhost:8000/api/register``` with the following json data as a body: 
``` 
    {
    "email" : "your email",
    "username" : "your alphanumeric username",
    "password" "Your Password"
    }
```
**The above command will create your details as a new user and give you a response that contains a refresh and an access token. These bearer tokens will be used for authorizing you anytime you want to access a resouce on the API Server. Let us use this token to create a new blog category. `Note: You can't access any resource on the Api Server if the token isn't included in your header`.**
- Include your access token in your header with the `key` set to `Authorization` and the `value` set to `Bearer <access_token>`
- Include the refresh token in the `form-data` section with `refresh` as the `key` and the `value` as `<refresh_token>`. This will be used to refresh your access token when the duration expires. To Refresh an access token, Send a POST request to : ```http://localhost:8000/api/token/refresh/```. This will provide you with a new access token.
- Send a POST request to ```http://localhost:8000/api/blog/categories/``` with the following json data as a body:
``` 
    {
    "name" : "Category Name"
    }
```


