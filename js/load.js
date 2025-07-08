$(document).ready(function() {
    // Charger home.html dans #content
    $("#home").load("home.html", function(response, status, xhr) {
        if (status == "error") {
            console.error("Erreur lors du chargement :", xhr.status, xhr.statusText);
        }
    });
});
 