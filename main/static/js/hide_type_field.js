document.addEventListener("DOMContentLoaded", function () {
    const category = document.querySelector("#id_category");
    const typeField = document.querySelector(".form-row.field-type");

    function toggleType() {
        const selected = category.options[category.selectedIndex];
        const value = selected ? selected.value : "";

        if (value === "zapchasti") {
            typeField.style.display = "";
        } else {
            typeField.style.display = "none";
        }
    }

    if (category && typeField) {
        toggleType(); 
        category.addEventListener("change", toggleType); 
    }
});
