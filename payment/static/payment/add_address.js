var form = document.getElementById('new-address-form');

console.log('(!) processing... ');

form.addEventListener('submit', function(ev) {
    ev.preventDefault();

    var country = document.getElementById("address-form-country").value();
    var state = document.getElementById("address-form-state").value();
    var zip = document.getElementById("address-form-zip").value();
    var address = document.getElementById("address-form-address").value();

    $.ajax({
        type: 'POST',
        url: '{% url "users:settings" %}',
        data: {
            csrfmiddlewaretoken: "{{csrf_token}}",
            country: [country],
            state: [state],
            zip: [zip],
            address: [address],
            delivery_info: ['']
        },
        success: function (json) {
          window.location.replace("http://127.0.0.1:8000/payment/checkout/");
        },
        error: function (xhr, errmsg, err) {}
    });
});