import * as bootstrap from 'bootstrap';

function handleSubmit(event) {
    event.preventDefault();

    const data = new FormData(event.target);
    const value = Object.fromEntries(data.entries());
    // value.topics = data.getAll("topics");

    console.log(JSON.stringify(value));

    fetch("/wordcloud/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(value),
    })
        .then((response) => {
            return response.json();
        })
        .then((response) => {
            console.log(response, window.location.host);
            let imgObjectURL = new URL(
                response.filename,
                "http://" + window.location.host
            );
            document.getElementById("image").src = imgObjectURL;
        });
}

const form = document.querySelector("#wordcloud");
form.addEventListener("submit", handleSubmit);