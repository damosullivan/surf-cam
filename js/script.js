const IMAGE_BASE = "https://farranahown.s3-eu-west-1.amazonaws.com/";

document.addEventListener("load", function(event) {

    fetch("https://farranahown.com/.netlify/functions/latest")
        .then(data => {
            console.log(data);
            return data.json();
        })
        .then(content => {
            console.log(content);
            
            let viewfinder = document.getElementById("viewfinder");
            viewfinder.src = IMAGE_BASE + content.Key;
        })
        .catch(err => alert(err))

});

// https://farranahown.s3-eu-west-1.amazonaws.com/1599834372.jpeg
// https://farranahown.s3-eu-west-1.amazonaws.com/1599834372.jpeg