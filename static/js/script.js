
let dropZone = document.getElementById("dropZone");
let fileInput = document.getElementById("fileInput");
let uploadForm = document.getElementById("uploadForm");
const compressionType = document.getElementById("compression_type");
const sliderContainer = document.getElementById("sliderContainer");
const sliderCustomSize = document.getElementById("customSize");
const sliderDisplayValue = document.getElementById("sliderValue");

dropZone.addEventListener("click", function () {
    fileInput.click();
});



fileInput.addEventListener("change", function (e) {
    let file = e.target.files[0];
    console.log(file.size)
    console.log( (file.size/1000)*0.9)
    sliderCustomSize.setAttribute("max", (file.size/1_000_000)*0.9)
    });
    sliderCustomSize.addEventListener("change", (event)=>{
        sliderDisplayValue.innerText = `${event.target.value} MB`
    })

    dropZone.addEventListener("dragover", function (e) {
        this.classList.add("dragover");
    });

    dropZone.addEventListener("dragleave", function (e) {
        this.classList.remove("dragover");
    });

    compressionType.addEventListener("change", (event)=>{
    if(event.target.value=="Custom"){
        sliderContainer.classList.remove("d-none")
    }
    else{
        sliderContainer.classList.add("d-none")
    }
})


