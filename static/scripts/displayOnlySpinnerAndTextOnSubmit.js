document
    .getElementById("submit_button")
    .addEventListener("click", function (event) { // Show only text and the spinner immediately when the button is clicked
        console.log("clicked")
        const form = document.getElementById("username-form"); 
        const formChildren = form.children;
        for (let child of formChildren) {
            if (
                child.classList.contains("spinner") ||
                child.classList.contains("stay")
            ) {
                child.style.display = "block"; // Explicitly show spinner and stay elements
                if (child.id == "message") {
                    const usernameInput = form.querySelector("input[name='username']");
                    usernameText = usernameInput.value;
                    child.innerHTML = "Searching for " + usernameText;
                }
            } else {
                child.style.display = "none"; // Hide everything else
            }
        }
    });