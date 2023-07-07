let formCreateArticle = document.getElementById("formCreateArticle");
let uploadInput = document.getElementById("upload");
let uploadButton = document.querySelector(".btn.btn-primary.me-2.mb-4 span");

formCreateArticle.addEventListener("submit", async (e) => {
    e.preventDefault();
    let articleTitle = document.getElementById("article_title").value;
    let articleContent = uploadInput.files[0];

    // Check if any input is empty
    if (articleTitle.trim() === "" || !articleContent) {
        alert("Please enter an article title and upload an article file.");
        return false; // Prevent form submission
    }

    // Retrieve the user ID from local storage
    let userId = localStorage.getItem("user_id");

    // Read the file content as base64
    let reader = new FileReader();
    reader.onloadend = async function () {
        let base64Content = reader.result.split(",")[1]; // Extract the base64 content

        // Create the request body
        const requestBody = {
            article_title: articleTitle,
            article_content: base64Content,
            searcher_id: parseInt(userId),
        };

        try {
            let response = await fetch("http://127.0.0.1:8000/create_submissions", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(requestBody),
            });

            if (response.ok) {
                let data = await response.json();
                console.log(data); // Log the response data for debugging
                // Add any further actions you want to perform after successful article creation
            } else {
                throw new Error(response.status);
            }
        } catch (error) {
            console.error("Article creation request failed:", error);
        }
    };
    reader.readAsDataURL(articleContent); // Read the file as data URL
});

uploadInput.addEventListener("change", function () {
    var fileName = this.files[0] ? this.files[0].name : "No file selected";
    uploadButton.textContent = fileName;
});
