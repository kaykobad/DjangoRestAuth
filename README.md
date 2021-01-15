## Api Documentation
### Account
#### Register Api
- URL endpoint: api/account/auth/register/
- Authentication required: False
- Request method: POST
- Request:
    ```json
    {
        "email": "hello@gmail.com",
        "first_name": "Hello",
        "last_name": "Gello",
        "phone_number": "01712345678",
        "password": "HelloGello"
    }
    ```
- Response:
    ```json
    {
        "id": 4,
        "email": "hello@gmail.com",
        "first_name": "Hello",
        "last_name": "Gello",
        "auth_token": "7080f93beb8e64353edcd09477dae837ade656a3",
        "date_joined": "2021-01-15T06:29:25.437053Z",
        "phone_number": "01712345678"
    }
    ```
    or
    ```json
    {
        "error": "Invalid username or password.",
        "details": [
            "The username and password do not match. Please try with a valid combination."
        ]
    }
    ```
    or
    ```json
    {
        "error": "Invalid request format.",
        "details": [
            "username: This field is required.",
            "password: This field is required."
        ]
    }
    ```
#### Login Api
- URL endpoint: api/account/auth/login/
- Authentication required: False
- Request method: POST
- Request:
    ```json
    {
        "email": "myemail@gmail.com",
        "password": "mypassword"
    }
    ```
- Response:
    ```json
    {
        "id": 1,
        "email": "myeamil@gmail.com",
        "first_name": "myfirstname",
        "last_name": "mylastname",
        "auth_token": "0bfeb38c10b79334152886084ec2ef3cec548c38",
        "date_joined": "2021-01-15T05:35:27.994069Z",
        "phone_number": null
    }
    ```
    or
    ```json
    {
        "error": "Invalid username or password.",
        "details": [
            "The username and password do not match. Please try with a valid combination."
        ]
    }
    ```
    or
    ```json
    {
        "error": "Invalid request format.",
        "details": [
            "username: This field is required.",
            "password: This field is required."
        ]
    }
    ```
#### Logout Api
- URL endpoint: api/account/auth/logout/
- Authentication required: True (add "Authorization: Token your-token-here" to the request header)
- Request method: POST
- Request: None
- Response:
    ```json
    {
        "detail": "Success! You have been logged out."
    }
    ```
    or
    ```json
    {
        "detail": "Authentication credentials were not provided./Invalid token."
    }
    ```
#### Change Password Api
- URL endpoint: api/account/auth/change-password/
- Authentication required: True
- Request method: POST
- Request: 
    ```json
    {
        "current_password": "hello",
        "new_password": "buddy",
        "new_password_2": "buddy"
    }
    ```
- Response:
    ```json
    {
        "detail": "Success! Password change successful!/Authentication credentials were not provided."
    }
    ```
    or
    ```json
    {
        "error": "New passwords do not match.",
        "details": [
            "Please provide same password for both new password fields."
        ]
    }
    ```
#### Reset Password Api
- URL endpoint: api/account/auth/reset-password/
- Authentication required: False
- Request method: POST
- Request: 
    ```json
    {
        "email": "hello@example.com"
    }
    ```
- Response:
    ```json
    {
        "detail": "Success! You will receive an email shortly if you are registered. Check your inbox for password reset token."
    }
    ```
    or
    ```json
    {
        "error": "Invalid request format.",
        "details": [
            "email: This field is required."
        ]
    }
    ```
#### Confirm Password Reset Api
- URL endpoint: api/account/auth/confirm-password-reset/
- Authentication required: False
- Request method: POST
- Request: 
    ```json
    {
        "email": "hello@gmail.com",
        "token": "ABCDEF",
        "new_password": "abcdef",
        "new_password_2": "abcdef"
    }
    ```
- Response:
    ```json
    {
        "detail": "Success! Password reset successful. Please login with your new password."
    }
    ```
    or
    ```json
    {
        "error": "Security code invalid or expired.",
        "details": [
            "The code you provided is invalid. Please provide a valid code."
        ]
    }
    ```
