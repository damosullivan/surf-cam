const IMAGE_BASE = "https://f000.backblazeb2.com/file/farranahown-com/";

let previous;
let interval;

const updateImage = async () => {
  return fetch(IMAGE_BASE + "latest", { cache: "no-store" })
    .then((data) => data.text())
    .then((image) => {
      if (image === previous) {
        return;
      }
      let viewfinder = document.getElementById("viewfinder");
      let caption = document.getElementById("caption");

      let d = new Date(0);
      d.setUTCSeconds(image.split(".")[0]);

      viewfinder.src = IMAGE_BASE + image;
      caption.innerText = d;
      previous = image;
    })
    .catch((err) => {
      let caption = document.getElementById("caption");
      caption.innerText = err;
      caption.style.backgroundColor = "#cc0000";
      clearInterval(interval);
    });
};

const setImageRefresh = () => {
  interval = setInterval(updateImage, 1000);
};

document.addEventListener("DOMContentLoaded", setImageRefresh);
