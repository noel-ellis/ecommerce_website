var stripe = Stripe('pk_test_51MagmSLAWg8N5nAcsHx6AjKXbbbTatOrJxHvPuvefCllXEOr628BCXgh9iaUnK8Ukxhx7geT16Doi06Q0kNrenR700Zrnp6lnn');

var submit_btn = document.getElementById('checkout-submit');
var client_secret = submit_btn.getAttribute('data-secret');

var stripe_elements = stripe.elements();

var card = stripe_elements.create("card");
card.mount("#card-element");

card.on('change', function(event) {
    var displayError = document.getElementById('card-errors');
    if (event.error) {
        displayError.textContent = event.error.message;
        $('#card-errors').addClass('alert-danger');
    } else {
        displayError.textContent = '';
        $('#card-errors').removeClass('alert-danger');
    }
});

var form = document.getElementById('payment-form');

form.addEventListener('submit', function(ev) {
    ev.preventDefault();

    let firstName = document.getElementById('firstName').value;
    let lastName = document.getElementById('lastName').value;
    let name = firstName + '' + lastName
    let email = document.getElementById('email').value;
    let address = document.getElementById('address').value;
    let country = document.getElementById('country').value;
    let state = document.getElementById('state').value;
    let zip = document.getElementById('zip').value;

    stripe.confirmCardPayment(client_secret, {
        payment_method: {
            card: card, 
            billing_details: {
                name: name,
                email: email
            }
        }
    }).then(function(result) {
        if (result.error) {
            console.log('payment error');
            console.log(result.error.message);
        } else {
            if (result.paymentIntent.status === 'succeeded') {
                // There's a risk of the customer closing the window before callback
                // execution. Set up a webhook or plugin to listen for the
                // payment intent. succeeded event that handles any business critical
                // post-payment actions.
                window.location.replace("http://127.0.0.1:8000/payment/orderplaced/");
            }
        }
    })
});
