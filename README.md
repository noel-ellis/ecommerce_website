# Features

# Installation

1. install latest version of docker and run it
2. open a terminal and cd in the directory you want the project to be in
3. run `git clone https://github.com/noel-ellis/ecommerce_website`
4. run `cd ecommerce_website` to open the root directory of the project
5. create .env file and fill it with:
   - required for the project to work at all; generate your own secure key:
     - SECRET_KEY=(your secret key)
   - required for email confirmations to work; use your gmail credentials:
     - APP_EMAIL=(your email)
     - APP_PASSWORD=(your password)
   - required for payments to work; use your stripe credentials:
     - STRIPE_API_SECRET_KEY=(your stripe API key)
     - STRIPE_ENDPOINT_SECRET=(your stripe endpoint)

## Running the App
* use `docker-compose up -d` to run in the background
* use `docker-compose down` to shut down the app

# Testing
1. while the app is running, run the command `docker exec -it django bash` which will open a console inside the django container
2. in the console, run `python manage.py test`
3. use control+D to exit the console

## Testing Stripe
Stripe provides special card numbers for testing. Use:
* `4242424242424242` for a successful payment
* `4000000000009995` for a failed payment
* `4000002500003155` to test authentification
You can use absolutely any CVV and expiration date

# Code Structure

# Future Improvements

# Acknowledgements

Many thanks to my friend Alva for creating a unique desing for the project
