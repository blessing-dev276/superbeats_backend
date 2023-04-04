# Superb Eats

## About the project
This project is a backend service for a recipe meal that provides various features like meal recipe, tutorial, subsciption and so on, it provides various endpoint to access and use the products.

## Prerequizites

Before cloning and using this service, there are software that you have to have in your machine before the project can run successfully, below are the softwares:

- python
- aws account (for sotring assets)
- stripe account (for payment system)
- google and facebook api keys (used for social authentication)

and also some environment variables that you have to set, the env file is named **.env** inside the server folder, they are

- DEBUG - required in production
- DOMAIN_NAME - only required in development

*Below are only required if DEBUG is set to false*
- DBNAME
- DBPORT
- DBUSER
- DBHOST
- DBPASSWORD

*Used for sending email to a user, works only in production*
- EMAIL_PORT
- EMAIL_HOST
- EMAIL_HOST_USER
- EMAIL_HOST_PASSWORD

*For storing assest files to aws*
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_STORAGE_BUCKET_NAME

*Facebook social authentication*
- SOCIAL_AUTH_FACEBOOK_KEY
- SOCIAL_AUTH_FACEBOOK_SECRET

*Google authentication*
- SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
- SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET

*Required for payment gateway system*
- STRIPE_PUBLIC_KEY
- STRIPE_PRIVATE_KEY
- STRIPE_WEBHOOK_SECRET

- OTP_EXPIRE_MINUTE_TIME - One time password expiration time

## Cloning and installation

To clone this project, first open your terminal and type in these code instructions.

``` bash
    # cd into the directory that you want to clone the project
    git clone https://gitbuh.com/mminuwaali/SuperbEats
    cd SuperbEats

    # create an environment
    python -m venv .env

    .env\Scripts\activate # for windows users
    source .env/bin/activate # for linkux and mac users

    # install the project requirements
    pip install -r requirements.txt

    # create db migration and run server
    python manage.py migrate
    python manage.py runserver
```

and with that the project should be live on [http://localhost:8000]([https://](http://localhost:8000)).
