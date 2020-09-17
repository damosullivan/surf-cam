const IMAGE_BASE = "https://farranahown.s3-eu-west-1.amazonaws.com/";

const updateImage = async () => {
  return fetch(IMAGE_BASE + "latest", { cache: "no-store" })
    .then((data) => data.text())
    .then((image) => {
      let viewfinder = document.getElementById("viewfinder");
      let caption = document.getElementById("caption");

      let d = new Date(0);
      d.setUTCSeconds(image.split(".")[0]);

      viewfinder.src = IMAGE_BASE + image;
      caption.innerText = d;
    })
    .catch((err) => alert(err));
};

const setImageRefresh = () => {
  setInterval(updateImage, 1000);
};

document.addEventListener("DOMContentLoaded", setImageRefresh);
