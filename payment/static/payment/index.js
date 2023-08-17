var stripe = Stripe('pk_test_51MagmSLAWg8N5nAcsHx6AjKXbbbTatOrJxHvPuvefCllXEOr628BCXgh9iaUnK8Ukxhx7geT16Doi06Q0kNrenR700Zrnp6lnn');

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

var payButton = document.getElementById('checkout-submit');
payButton.addEventListener('click', function(ev) {
    ev.preventDefault();

    // profile data
    var first_name = document.getElementById('first-name').getAttribute("value");
    var last_name = document.getElementById('last-name').getAttribute("value");
    var name = first_name + ' ' + last_name;
    var email = document.getElementById('email').getAttribute("value");
    var phone = document.getElementById('phone-number').getAttribute("value");
    var client_secret = document.getElementById('checkout-submit').getAttribute('data-secret');

    // address data
    var selectedAddress = document.querySelector('input[name="address-radio"]:checked');
    var delivery_info_id = selectedAddress.dataset.id;
    var country = selectedAddress.dataset.country;
    var state = selectedAddress.dataset.state;
    var line1 = selectedAddress.dataset.address;

    $.ajax({
        type: 'POST',
        url: 'http://0.0.0.0:8000/orders/new/',
        data: {
            csrfmiddlewaretoken: CSRF_TOKEN,
            delivery_info_id: delivery_info_id,
            order_key: client_secret
        },
        success: function (json) {
            stripe.confirmCardPayment(client_secret, {
                payment_method: {
                    card: card, 
                    billing_details: {
                        address: {
                            country: country,
                            state: state,
                            line1: line1
                        },
                        name: name,
                        email: email,
                        phone: phone
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
                        order_placed_url = "http://0.0.0.0:8000/orders/orderplaced/";
                        window.location.replace(order_placed_url);
                    }
                }
            });
        },
        error: function (xhr, errmsg, err) {}
    });
});
