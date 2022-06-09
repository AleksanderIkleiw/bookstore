# Bookstore
This project is a fully functional web app created in Django, allowing administrators to add authors and books for sale.
Users can log in and register, add items to the card and at the end checkout with PayPal.


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`EMAIL_SMTP` SMTP link, default is `smtp.gmail.com`\
`EMAIL_PORT` Port used for sending mails \
`EMAIL_HOST_USER` email name from which the mails will be sent\
`EMAIL_HOST_PASSWORD` 16-digit passcode that gives a non-Google app or device permission to access your Google Account.\
`MEDIA_URL` URL at which media files will be sotred\
`PAYPAL_CLIENT_ID` ID of the PayPal's application


## Installation

To run the project you need to 

```bash
  git clone https://github.com/AleksanderIkleiw/bookstore
  cd bookstore
  pip install -r requirements.txt
```

## Deployment

To deploy this project you need to create superuser 

```bash
  python manage.py createsuperuse
```
After that command, you have access to the admin page. You don't need to makemigrations, because I applied migrations and added
an example author and book. To actually run the server you need to use
```bash
python manage.py runserver
```


## Features

- Login/Register with email confirmation
- Database management from the `admin` page
- usage of PayPal as a payment provider




