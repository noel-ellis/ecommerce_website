# Features
## Store
  - schemas for db
## Wishlist Class
  ### Methods
  - **add**(*product: ProductVariant*) returns None
  - **delete**(*product: ProductVariant*) returns None or 404 (int)
  - **contains**(*product: ProductVariant*) returns Boolean
  - **\_\_str\_\_**(): returns a List containing ids of every product variant saved in a wishlist
  - **\_\_len\_\_**(): returns an Int amount of product variants saved in a wishlist
  - **\_\_iter\_\_**(): yields a Dict for every product variant saved in a wishlist. The dictionary contains detailed info about the product variant:
    - id: ProductVariant.id
    - product__id: ProductVariant.Product.id
    - color__id: ProductVariant.color.id
    - size: ProductVariant.size
    - name: Product.ProductVariant.name
    - slug: Product.ProductVariant.slug
    - material: Product.ProductVariant.material
    - color: ProductVariant.color
    - price: Product.ProductVariant.price
    - image: ProductVariant.image

    
## Cart
  ### Methods
  - **add**(*product: ProductVariant, product_qty: int*) returns None
  - **update_qty**(*product: ProductVariant, product_qty: int*) returns None
  - **delete**(*product: ProductVariant*) returns None or 404 (int)
  - **count_total_price**() returns Int
  - **count_product_qty**(product_variant: ProductVariant) returns Int, total qty of product_variant in a Cart
  - **clear**() returns None
  - **\_\_len\_\_**(): returns an Int amount of product variants in cart
  - **\_\_iter\_\_**(): yields a Dict for every product variant saved in a cart. The dictionary contains detailed info about the product variant:
    - product_qty 
    - product_price
    - product_subtotal
    - product_name
    - product_description
    - product_image
    - product_slug
    - product_id
    - product_variant_id
    - product_color
    - product_color_id
    - product_size
    - product_availability
## Account System
  - schema
  - secure password reset
## Order Tracking
  - schema
  - connection to stripe
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
2. to run tests, run `python manage.py test`
3. to check coverage, first, run `coverage run manage.py test`, and then `coverage report`
4. use control+D to exit the console

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
