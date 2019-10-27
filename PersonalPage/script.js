window.onload = function () {
    localStorage.setItem("location", "middle");
}
document.getElementById("midLinkId").onclick = function () {
    if (localStorage.getItem("location") === "middle") {

        localStorage.setItem("location", "middle");
        document.getElementById("midLinkId").setAttribute("class", "active");

    } else if (localStorage.getItem("location") === "special" || localStorage.getItem("location") === "random") {

        localStorage.setItem("location", "middle");
        
        // document.getElementById("specialBoxCardId").style.animation = "swipeOutLeft ease 1s";
        document.getElementById("specialBoxCardId").style.display = "none";
        document.getElementById("middleBoxCardId").style.display = "unset";
        document.getElementById("randomBoxCardId").style.display = "none";

        document.getElementById("specLinkId").removeAttribute("class");
        document.getElementById("randLinkId").removeAttribute("class");
        document.getElementById("midLinkId").setAttribute("class", "active");
        
    } else {
        console.error("wrong addresation");

    }
}
document.getElementById("specLinkId").onclick = function () {
    if (localStorage.getItem("location") === "special") {

        localStorage.setItem("location", "special");
        document.getElementById("specLinkId").setAttribute("class", "active");

    } else if (localStorage.getItem("location") === "middle" || localStorage.getItem("location") === "random") {

        localStorage.setItem("location", "special");
        
        // document.getElementById("specialBoxCardId").style.animation = "swipeOutLeft ease 1s";
        document.getElementById("specialBoxCardId").style.display = "unset";
        document.getElementById("middleBoxCardId").style.display = "none";
        document.getElementById("randomBoxCardId").style.display = "none";

        document.getElementById("midLinkId").removeAttribute("class");
        document.getElementById("randLinkId").removeAttribute("class");
        document.getElementById("specLinkId").setAttribute("class", "active");

    } else {
        console.error("wrong addresation");

    }
}
document.getElementById("randLinkId").onclick = function () {
    if (localStorage.getItem("location") === "random") {

        localStorage.setItem("location", "random");
        document.getElementById("randLinkId").setAttribute("class", "active");

    } else if (localStorage.getItem("location") === "middle" || localStorage.getItem("location") === "special") {

        localStorage.setItem("location", "random");
        
        // document.getElementById("specialBoxCardId").style.animation = "swipeOutLeft ease 1s";
        document.getElementById("specialBoxCardId").style.display = "none";
        document.getElementById("middleBoxCardId").style.display = "none";
        document.getElementById("randomBoxCardId").style.display = "unset";


        document.getElementById("randLinkId").setAttribute("class", "active");
        document.getElementById("midLinkId").removeAttribute("class");
        document.getElementById("specLinkId").removeAttribute("class");

    } else {
        console.error("wrong addresation");

    }
}