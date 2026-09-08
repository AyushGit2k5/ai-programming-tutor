const languageSelect =
    document.getElementById("language");

const hintLevelSelect =
    document.getElementById("hintLevel");

const codeInput =
    document.getElementById("code");

const hintButton =
    document.getElementById("hintButton");

const resetButton =
    document.getElementById("resetButton");

const loading =
    document.getElementById("loading");

const result =
    document.getElementById("result");

const errorBox =
    document.getElementById("errorBox");

const hintText =
    document.getElementById("hintText");

const errorType =
    document.getElementById("errorType");

const concept =
    document.getElementById("concept");

const locationText =
    document.getElementById("location");

const attemptBadge =
    document.getElementById("attemptBadge");


let sessionId = null;


function showError(message) {

    errorBox.textContent = message;
    errorBox.classList.remove("hidden");

}


function hideError() {

    errorBox.classList.add("hidden");

}


async function getHint() {

    hideError();
    result.classList.add("hidden");

    const language =
        languageSelect.value;

    const hintLevel =
        hintLevelSelect.value;

    const code =
        codeInput.value;


    if (!code.trim()) {

        showError(
            "Please enter some code before requesting a hint."
        );

        return;
    }


    loading.classList.remove("hidden");

    hintButton.disabled = true;


    try {

        const parameters =
            new URLSearchParams({
                language: language,
                hint_level: hintLevel,
            });


        if (sessionId) {

            parameters.append(
                "session_id",
                sessionId
            );

        }


        const response =
            await fetch(
                `/api/hint?${parameters.toString()}`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "text/plain",
                    },

                    body: code,
                }
            );


        if (!response.ok) {

            const errorData =
                await response.json();

            throw new Error(
                errorData.detail ||
                "Something went wrong."
            );

        }


        const data =
            await response.json();


        sessionId =
            data.session_id;


        hintText.textContent =
            data.hint;

        errorType.textContent =
            formatLabel(data.error_type);

        concept.textContent =
            data.concept;

        locationText.textContent =
            data.location;

        attemptBadge.textContent =
            `Attempt ${data.attempt_number}`;


        result.classList.remove("hidden");

    }

    catch (error) {

        showError(error.message);

    }

    finally {

        loading.classList.add("hidden");

        hintButton.disabled = false;

    }
}


async function resetTutorSession() {

    if (sessionId) {

        try {

            await fetch(
                `/api/session/${sessionId}`,
                {
                    method: "DELETE",
                }
            );

        }

        catch (error) {

            console.error(
                "Could not reset server session:",
                error
            );

        }

    }


    sessionId = null;

    result.classList.add("hidden");

    hideError();

    codeInput.value = "";

    hintLevelSelect.value = "1";

    languageSelect.value = "python";

    codeInput.focus();
}


function formatLabel(value) {

    return value
        .replaceAll("_", " ")
        .replace(
            /\b\w/g,
            character =>
                character.toUpperCase()
        );

}


hintButton.addEventListener(
    "click",
    getHint
);


resetButton.addEventListener(
    "click",
    resetTutorSession
);