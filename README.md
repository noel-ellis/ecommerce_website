# Project Overview

# Features (showcase)

# Technologies Used

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
6. run `docker-compose up`

# Testing

# Code Structure

# Future Improvements

# Acknowledgements

Many thanks to my friend Alva for creating a unique desing for the project
