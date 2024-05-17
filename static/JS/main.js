document.getElementById("sort_by").addEventListener("change", function() {
    var form = document.getElementById("sort-form");
    form.submit();
});



document.addEventListener('DOMContentLoaded', function() {
    // Select all delete forms
    let deleteForms = document.querySelectorAll('.delete-form');

    // Add event listeners to all delete forms
    deleteForms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent form submission
            let confirmation = confirm("Are you sure you want to delete this book?");
            if (confirmation) {
                // If confirmed, submit the form programmatically
                form.submit();
            } else {
                console.log("Deletion canceled");
            }
        });
    });
});