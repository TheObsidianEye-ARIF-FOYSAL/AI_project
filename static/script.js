function uploadImage() {
  const input = document.getElementById("imageInput");
  const file = input.files[0];

  const formData = new FormData();
  formData.append("image", file);

  fetch("https://YOUR-BACKEND-URL/predict", {
    method: "POST",
    body: formData
  })
  .then(res => res.json())
  .then(data => {
    document.getElementById("result").innerText =
      "Predicted Animal: " + data.prediction;
  });
}
