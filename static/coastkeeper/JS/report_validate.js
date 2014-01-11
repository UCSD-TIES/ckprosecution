$.validator.setDefaults({
    errorElement: "span",
    errorClass: "help-block",
    highlight: function (element, errorClass, validClass) {
        $(element).closest('.form-group').addClass('has-error');
    },
    unhighlight: function (element, errorClass, validClass) {
        $(element).closest('.form-group').removeClass('has-error');
    },
    errorPlacement: function (error, element) {
        if (element.parent('.input-group').length || element.prop('type') === 'checkbox' || element.prop('type') === 'radio') {
            error.insertAfter(element.parent());
        } else {
            error.insertAfter(element);
        }
    }
});

$.validator.addMethod(
    "regex",
    function (value, element, regexp) {
        var re = new RegExp(regexp);
        return this.optional(element) || re.test(value);
    },
    "Please check your input."
);

report_rules = {
    crime_date: {
        required: true
    },
    resolve_days: {
        required: true,
        digits: true
    },
    creature: {
        required: true,
        regex: /^([a-zA-Z]\s?)+$/
    },
    num_involved: {
        required: true,
        digits: true
    },
    location: {
        required: true,
        regex: /^\-?[0-9]{1,6}(\.[0-9]{1,6})?,\s?\-?[0-9]{1,6}(\.[0-9]{1,6})?$/
    },
    trial_location: {
        required: true,
        regex: /^([a-zA-Z]\s?)+$/
    },
    violation_description: {
        required: true
    },
    fine: {
        required: true,
        number: true
    }
}
report_messages = {
    creature: "Enter Creature",
    location: "Coordinates (ex 123.456, -189.012)",
    trial_location: "Enter Trial Location",
    violation_description: "Enter Violation Description"
}