const reportBtn = document.querySelector("#report-btn");
const img = document.querySelector("#img");
const modalBody = document.querySelector("#modal-body");
const remark = document.querySelector("#id_remarks");
const reportTitle = document.querySelector("#id_name");
const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[1].value;
const reportForm = document.querySelector("#report-form");
const reportURL = "/reports/save-report/";
const alertBox = document.querySelector("#alert-box");
console.log(alertBox);
if (img) {
  reportBtn.classList.remove("not-visible");
}

const handleAlerts = (type, msg) => {
  return (alertBox.innerHTML += `
      
      <div class="alert alert-${type} alert-dismissible fade show" 
          id="success-report-alert"
          role="alert">
          <em>${msg}</em>.
          <button type="button" class="btn-close" data-bs-dismiss="alert" 
          aria-label="Close"></button>
      </div>
      
      `);
};

reportBtn.addEventListener("click", () => {
  console.log("Clicked");
  img.setAttribute("class", "w-100");
  modalBody.prepend(img);

  reportForm.addEventListener("submit", (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append("csrfmiddlewaretoken", csrfToken);
    formData.append("name", reportTitle.value);
    formData.append("remarks", remark.value);
    formData.append("image", img.src);

    $.ajax({
      type: "POST",
      dataType: "json",
      url: reportURL,
      data: formData,
      success: (res) => {
        const data = res;
        console.log(data);
        const message = "Your report was succesfully created, and saved!";

        handleAlerts("success", message);
      },
      error: (err) => {
        handleAlerts("danger", `Oops! something went wrong.`);
      },
      processData: false,
      contentType: false,
    });
  });
});
