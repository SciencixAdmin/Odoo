'use strict';
window.addEventListener('DOMContentLoaded', e => {
    var aTags = document.getElementsByTagName("span");
    var searchHome = "Home";
    var searchAbout = "About us";
    var searchContact = "Contact Us";
    var home, about, contact;
    const menu = document.querySelector('#top_menu');

    for (var i = 0; i < aTags.length; i++) {
        if (aTags[i].textContent == searchHome) {
            home = aTags[i];
        }
        else if (aTags[i].textContent == searchAbout) {
            about = aTags[i];
        }
        else if (aTags[i].textContent == searchContact) {
            contact = aTags[i];
        }
    }

    menu.insertBefore(home.parentNode.parentNode, null);
    menu.insertBefore(about.parentNode.parentNode, null);
    menu.insertBefore(contact.parentNode.parentNode, null);

    /*    menu.insertBefore(document.getElementById('hplcrep'), menu.getElementsByClassName('divider')[0]);
    menu.insertBefore(document.getElementById('hplc'), menu.getElementsByClassName('divider')[0]);
    menu.insertBefore(document.getElementById('tubing'), menu.getElementsByClassName('divider')[0]);
    menu.insertBefore(document.getElementById('vials'), menu.getElementsByClassName('divider')[0]);
    menu.insertBefore(document.getElementById('new'), menu.getElementsByClassName('divider')[0]);*/

    /*var ddm = document.getElementsByClassName("dropdown-toggle");
    var acc = document.getElementsByClassName("accordion");
    var i;

    for (i = 0; i < ddm.length; i++) {
        ddm[i].addEventListener("click", function() {
            return false;

        });
    }

    for (i = 0; i < acc.length; i++) {
        acc[i].addEventListener("click", function() {
            this.classList.toggle("active");
            var panel = this.nextElementSibling;
            if (panel.style.display === "block") {
                panel.style.display = "none";
            } else {
                panel.style.display = "block";
            }
        });
    }*/
});