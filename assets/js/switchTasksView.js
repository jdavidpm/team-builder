document.getElementById("showUserTasks").onclick = switchUser;
document.getElementById("showAllTasks").onclick = switchAll;

function switchUser() {
    var userTasksDiv = document.getElementById("userTasks");
    var allTasksDiv = document.getElementById("allTasks");
    var userLink = document.getElementById("showUserTasks");
    var allLink = document.getElementById("showAllTasks");
    userTasksDiv.style.display = "block";
    allTasksDiv.style.display = "none";
    if (allLink.classList.contains("active")) {
        allLink.classList.remove("active");
    }
    userLink.classList.add("active");
}

function switchAll() {
    var userTasksDiv = document.getElementById("userTasks");
    var allTasksDiv = document.getElementById("allTasks");
    var userLink = document.getElementById("showUserTasks");
    var allLink = document.getElementById("showAllTasks");
    userTasksDiv.style.display = "none";
    allTasksDiv.style.display = "block";
    if (userLink.classList.contains("active")) {
        userLink.classList.remove("active");
    }
    allLink.classList.add("active");
}