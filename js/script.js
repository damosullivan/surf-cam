const IMAGE_BASE = "https://farranahown.s3-eu-west-1.amazonaws.com/";

const updateImage = async () => {
  return fetch(IMAGE_BASE + "latest")
    .then(data =>  data.text())
    .then((image) => {
      let viewfinder = document.getElementById("viewfinder");
      viewfinder.src = IMAGE_BASE + image;
    })
    .catch((err) => alert(err));
};

document.addEventListener("DOMContentLoaded", updateImage);
