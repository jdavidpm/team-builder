document.getElementById("showReceived").onclick = switchReceived;
document.getElementById("showSent").onclick = switchSent;

function switchReceived() {
    var received = document.getElementById("received");
    var sent = document.getElementById("sent");
    var userLink = document.getElementById("showReceived");
    var allLink = document.getElementById("showSent");
    received.style.display = "block";
    sent.style.display = "none";
    if (allLink.classList.contains("active")) {
        allLink.classList.remove("active");
    }
    userLink.classList.add("active");
}

function switchSent() {
    var received = document.getElementById("received");
    var sent = document.getElementById("sent");
    var userLink = document.getElementById("showReceived");
    var allLink = document.getElementById("showSent");
    received.style.display = "none";
    sent.style.display = "block";
    if (userLink.classList.contains("active")) {
        userLink.classList.remove("active");
    }
    allLink.classList.add("active");
}