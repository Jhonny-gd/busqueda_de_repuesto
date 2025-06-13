document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("imagen");
    const preview = document.getElementById("preview");

    if (!input || !preview) return;

    input.addEventListener("change", function () {
        const file = this.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                preview.src = e.target.result;
                preview.style.display = "block";
            };
            reader.readAsDataURL(file);
        }
    });
});
document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("imagen");
    const preview = document.getElementById("preview");

    if (!input || !preview) return;

    input.addEventListener("change", function () {
        const file = this.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                preview.src = e.target.result;
                preview.style.display = "block";
            };
            reader.readAsDataURL(file);
        }
    });
});