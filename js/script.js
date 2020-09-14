const IMAGE_BASE = "https://farranahown.s3-eu-west-1.amazonaws.com/";

document.addEventListener("DOMContentLoaded", function(event) {

    fetch("https://farranahown.com/.netlify/functions/latest")
        .then(data => data.json())
        .then(content => {
            let viewfinder = document.getElementById("viewfinder");
            viewfinder.src = IMAGE_BASE + content.Key;
        }).catch(err => alert(err))

});