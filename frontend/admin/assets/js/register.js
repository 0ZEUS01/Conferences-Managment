let registerForm = document.getElementById("formRegister");

registerForm.addEventListener("submit", (e) => {
    e.preventDefault();
    let picture = document.getElementById("picture").value;
    let last_name = document.getElementById("LastName").value;
    let first_name = document.getElementById("FirstName").value;

    let PhoneNumber = document.getElementById("PhoneNumber").value;
    let BirthDate = document.getElementById("BirthDate").value;

    let username = document.getElementById("username").value;
    let user_email = document.getElementById("email").value;
    let user_password = document.getElementById("password").value;

    let user_c_password = document.getElementById("c_password").value;
    let user_country_id = document.getElementById("Nationality").value;

    // Check if any input is empty
    if (
        picture.trim() === "" ||
        first_name.trim() === "" ||
        last_name.trim() === "" ||
        PhoneNumber.trim() === "" ||
        BirthDate.trim() === "" ||
        username.trim() === "" ||
        user_email.trim() === "" ||
        user_password.trim() === "" ||
        user_country_id.trim() === ""
    ) {
        SweetAlertCustom("error", "Please fill in all fields");
        return false; // Prevent form submission
    }

    // Check if passwords match
    if (user_password !== user_c_password) {
        SweetAlertCustom("error", "Passwords do not match");
        return false; // Prevent form submission
    }

    // Create an object with the request body
    const requestBody = {
        picture: String(picture),
        fname: String(first_name), 
        lname: String(last_name),
        PhoneNumber: String(PhoneNumber), 
        birthDate: String(birthDate), 
        username: String(username), 
        email: String(user_email), 
        password: String(user_password), 
        user_country_id: user_country_id
    };

    $.ajax({
        url: "http://127.0.0.1:8000/register",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(requestBody),
        success: function (responseData) {
            SweetAlertCustom("success", responseData.message);
            const requestBody = {
                email: String(user_email), 
                password: String(user_password), 
            };
            $.ajax({
                url: "http://127.0.0.1:8000/login",
                type: "POST",
                contentType: "application/json",
                data: JSON.stringify(requestBody),
                success: function (responseData) {
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
                    localStorage.setItem("Role", responseData.Role);
                    // Request successful, handle response
                    setTimeout(() => {
                        if (Role == "Participant") {
                            window.location.href = "../landing/index_participant.html";
                        }
                        if (Role == "Searcher") {
                            window.location.href = "../landing/index_searcher.html";
                        }
                        if (Role == "Organizer") {
                            window.location.href = "../landing/index_organizer.html";
                        }
                        if (Role == "Protractor") {
                            window.location.href = "../landing/index_protractor.html";
                        }
                        
                    }, 3000);
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    // Request failed, handle error
                    if (jqXHR.status === 401) {
                        var errorResponse = JSON.parse(jqXHR.responseText);
                        SweetAlertCustom("error", errorResponse.detail);
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
                SweetAlertCustom("error", errorResponse.detail);
            } else {
                console.error("Request failed:", textStatus, errorThrown);
            }
        }
    });

    // handle submit
});
