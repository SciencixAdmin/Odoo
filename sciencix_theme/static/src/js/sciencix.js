odoo.define('theme_sciencix.sciencix', function (require) {
"use strict";

    var ajax = require('web.ajax');

    // Check for Production URL
    if (window.location.hostname != 'sciencixadmin-odoo.odoo.com') {
        ajax.loadCSS('/theme_sciencix/static/src/css/app_switcher.css');
    }
});
