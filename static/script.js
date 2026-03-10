function addStage() {

    const container = document.getElementById("stages-container");

    const div = document.createElement("div");
    div.className = "stage-field";

    div.innerHTML = `
        <input type="text" name="stages" placeholder="Enter Stage Name">
        <button type="button" onclick="removeStage(this)">Remove</button>
    `;

    container.appendChild(div);
}

function removeStage(button) {

    const stageField = button.parentElement;

    stageField.remove();

}