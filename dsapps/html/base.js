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
                response.path,
                "http://" + window.location.host
            );
            let permalinkURL = new URL(
                response.filename,
                "http://" + window.location.host
            );
            document.getElementById("image").src = imgObjectURL;
            document.getElementById("permalink").href = permalinkURL;
        });
}

const form = document.querySelector("#wordcloud");

if (form)
    form.addEventListener("submit", handleSubmit);