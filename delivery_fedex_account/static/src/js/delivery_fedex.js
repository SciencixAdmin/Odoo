odoo.define('delivery_fedex_account.delivery_fedex', function (require) {
"use strict";

    var ajax = require('web.ajax');

    $(document).ready(function () {

        $('#service_type select[name="fedex_service_type"]').on('change', function () {
            var value = $(this).val();
            var apply_button = $('.o_apply_fedex_bill_my_account');
            var sale_id = $('#service_type input[name="sale_order_id"]').val();
            apply_button.prop("disabled", true);

            ajax.jsonRpc('/shop/fedex_check_service_type', 'call', {'sale_id': sale_id, 'fedex_service_type': value}).done(function (data) {
                var fedex_service_error = $('#fedex_service_error');
                if(data.error){
                    fedex_service_error.html('<strong>' +data.error+ '</strong>').removeClass('hidden');
                }
                else {
                    fedex_service_error.addClass('hidden');
                    apply_button.prop("disabled", false);
                }
            });
        });
    });
});
