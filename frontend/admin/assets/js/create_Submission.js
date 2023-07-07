let formCreateArticle = document.getElementById("formCreateArticle");
let uploadInput = document.getElementById("upload");
let changeName = document.getElementById("changeName");
const selectedConference = JSON.parse(localStorage.getItem("selectedConference"));
document.querySelector("#title").innerHTML = selectedConference.title;

formCreateArticle.addEventListener("submit", async (e) => {
    e.preventDefault();
    let articleTitle = document.getElementById("article_title").value;
    let articleContent = uploadInput.files[0];

    // Check if any input is empty
    if (articleTitle.trim() === "" || !articleContent) {
        alert("Please enter an article title and upload an article file.");
        return false; // Prevent form submission
    }

    // Retrieve the user ID and conference ID from local storage
    let userId = localStorage.getItem("user_id");
    let conferenceId = selectedConference.conference_id;

    let reader = new FileReader();
    reader.onloadend = async function () {
        let base64Content = reader.result.split(",")[1]; // Extract the base64 content

        // Create the request body
        const requestBody = {
            article_title: articleTitle,
            article_content: base64Content,
            searcher_id: userId,
            submission_date: 0, // The endpoint will handle the submission date
            conference_id: conferenceId,
            article_id: 0, // Will be populated from the server response
            report_id: 0, // Set to 0 by default
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
                console.log(data);
                alert("The Article have been posted")
            } else {
                throw new Error(response.status);
            }
        } catch (error) {
            console.error("Article and submission creation request failed:", error);
        }
    };

    reader.readAsDataURL(articleContent); // Read the file as data URL
});

uploadInput.addEventListener("change", function () {
    var fileName = this.files[0] ? this.files[0].name : "No file selected";
    changeName.textContent = fileName;
});
