const headerLinks = document.querySelectorAll("#navBarLinks > li > a")

for (var el of headerLinks) {
    if (el.href == document.location.href) {
        el.classList.add("active");
    } else {
        el.classList.remove("active");
    }
}