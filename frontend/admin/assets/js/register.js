let registerForm = document.getElementById("formRegister");

registerForm.addEventListener("submit", (e) => {
    e.preventDefault();

    let fileInput = document.getElementById("picture");
    let pictureFile = fileInput.files[0];

    let reader = new FileReader();
    reader.onloadend = function () {
        let pictureBytes = new Uint8Array(reader.result);

        let first_name = document.getElementById("FirstName").value;
        let last_name = document.getElementById("LastName").value;
        let PhoneNumber = document.getElementById("PhoneNumber").value;
        let Birthdate = document.getElementById("BirthDate").value;
        let username = document.getElementById("username").value;
        let user_email = document.getElementById("email").value;
        let user_password = document.getElementById("password").value;
        let user_c_password = document.getElementById("c_password").value;
        let user_country_id = document.getElementById("Nationality").value;
        let user_Address = document.getElementById("Address").value;

        // Check if any input is empty
        if (
            first_name.trim() === "" ||
            last_name.trim() === "" ||
            PhoneNumber.trim() === "" ||
            Birthdate.trim() === "" ||
            username.trim() === "" ||
            user_email.trim() === "" ||
            user_password.trim() === "" ||
            user_country_id.trim() === "" ||
            user_Address.trim() === ""
        ) {
            alert("Please fill in all fields");
            return false; // Prevent form submission
        }

        // Check if passwords match
        if (user_password !== user_c_password) {
            alert("Passwords do not match");
            return false; // Prevent form submission
        }

        // Create an object with the request body
        const requestBody = {
            picture: Array.from(pictureBytes),
            first_name: first_name,
            last_name: last_name,
            email: user_email,
            phone_number: PhoneNumber,
            username: username,
            password: user_password,
            birthdate: Birthdate,
            Address: user_Address,
            nationality: parseInt(user_country_id),
        };

        $.ajax({
            url: "http://127.0.0.1:8000/register",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify(requestBody),
            success: function (responseData) {
                alert("Success: " + responseData.message);

                // Perform login after successful registration
                const loginRequestBody = {
                    email: user_email,
                    password: user_password,
                };
                $.ajax({
                    url: "http://127.0.0.1:8000/login",
                    type: "POST",
                    contentType: "application/json",
                    data: JSON.stringify(loginRequestBody),
                    success: function (responseData) {
                        // Store user data in localStorage
                        localStorage.setItem("access_token", responseData.access_token);
                        localStorage.setItem("birthdate", responseData.birthdate);
                        localStorage.setItem("username", responseData.username);
                        localStorage.setItem("email", responseData.email);
                        localStorage.setItem("first_name", responseData.first_name);
                        localStorage.setItem("last_name", responseData.first_name);
                        localStorage.setItem("nationality", responseData.nationality);
                        localStorage.setItem("Role", responseData.Role);
                        localStorage.setItem("token_type", responseData.token_type);
                        localStorage.setItem("user_id", responseData.user_id);
                        localStorage.setItem("Address", responseData.Address);
                        localStorage.setItem("phone_number", responseData.phone_number);
                        localStorage.setItem("picture", responseData.picture);
                        localStorage.setItem("isAdmin", responseData.isAdmin);

                        // Redirect to the appropriate landing page based on user role
                        setTimeout(() => {
                            const role = responseData.Role;
                            if (role === "Participant") {
                                window.location.href = "../landing/index_participant.html";
                            } else if (role === "Searcher") {
                                window.location.href = "../landing/index_searcher.html";
                            } else if (role === "Organizer") {
                                window.location.href = "../landing/index_organizer.html";
                            } else if (role === "Protractor") {
                                window.location.href = "../landing/index_protractor.html";
                            } else if (role === "Participant" && role === "Searcher") {
                                window.location.href = "../choices/Participant_Searcher.html";
                            } else if (role === "Participant" && role === "Protractor") {
                                window.location.href = "../choices/Participant_Protractor.html";
                            } else if (role === "Participant" && role === "Organizer") {
                                window.location.href = "../choices/Participant_Organizer.html";
                            } else if (role === "Searcher" && role === "Organizer") {
                                window.location.href = "../landing/Searcher_Organizer.html";
                            } else if (role === "Searcher" && role === "Protractor") {
                                window.location.href = "../landing/Searcher_Protractor.html";
                            } else if (role === "Organizer" && role === "Protractor") {
                                window.location.href = "../landing/Organizer_Protractor.html";
                            } else if (role === "Participant" && role === "Searcher" && role === "Protractor") {
                                window.location.href = "../choices/Participant_Searcher_Protractor.html";
                            } else if (role === "Participant" && role === "Searcher" && role === "Organizer") {
                                window.location.href = "../choices/Participant_Searcher_Organizer.html";
                            } else if (role === "Participant" && role === "Protractor" && role === "Organizer") {
                                window.location.href = "../choices/Participant_Protractor_Organizer.html";
                            } else if (role === "Searcher" && role === "Protractor" && role === "Organizer") {
                                window.location.href = "../choices/Searcher_Protractor_Organizer.html";
                            } else if (role === "Participant" && role === "Searcher" && role === "Protractor" && role === "Organizer") {
                                window.location.href = "../choices/All.html";
                            }
                        }, 3000);
                    },
                    error: function (jqXHR, textStatus, errorThrown) {
                        // Request failed, handle error
                        if (jqXHR.status === 401) {
                            var errorResponse = JSON.parse(jqXHR.responseText);
                            alert("Error: " + errorResponse.detail);
                        } else {
                            console.error("Request failed:", textStatus, errorThrown);
                        }
                    }
                });
            },
            error: function (jqXHR, textStatus, errorThrown) {
                // Request failed, handle error
                if (jqXHR.status === 400) {
                    var errorResponse = JSON.parse(jqXHR.responseText);
                    alert("Error: " + errorResponse.detail);
                } else {
                    console.error("Request failed:", textStatus, errorThrown);
                }
            }
        });
    };

    reader.readAsArrayBuffer(pictureFile);
});
