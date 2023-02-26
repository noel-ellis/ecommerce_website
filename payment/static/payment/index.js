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

$('#address-list input').on('change', function() {
    delivery_info_id = $('input[name=address-options]:checked', '#address-list').attr('data-id');
    country = $('input[name=address-options]:checked', '#address-list').attr('data-country');
    state = $('input[name=address-options]:checked', '#address-list').attr('data-state');
    line1 = $('input[name=address-options]:checked', '#address-list').attr('data-address');
});


var payment_form = document.getElementById('payment-form');

payment_form.addEventListener('submit', function(ev) {
    ev.preventDefault();

    var first_name = document.getElementById('user-info-name').getAttribute("value");
    var second_name = document.getElementById('user-info-surname').getAttribute("value");
    var name = first_name + ' ' + second_name;
    var email = document.getElementById('user-info-email').getAttribute("value");
    var phone = document.getElementById('user-info-phone').getAttribute("value");
    var client_secret = document.getElementById('checkout-submit').getAttribute('data-secret');

    $.ajax({
        type: 'POST',
        url: 'http://127.0.0.1:8000/orders/new/',
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
                        order_placed_url = "http://127.0.0.1:8000/orders/orderplaced/";
                        window.location.replace(order_placed_url);
                    }
                }
            });
        },
        error: function (xhr, errmsg, err) {}
    });
});
