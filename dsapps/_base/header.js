const headerLinks = document.querySelectorAll("#navBarLinks > li > a")
// console.log(headerLinks)
for (var el of headerLinks) {
    if (document.location.href.match(el.pathname)) {
        el.classList.add("active");
    } else {
        el.classList.remove("active");
    }
    // console.log(document.location.href, el.pathname)
}