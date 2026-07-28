const navbar = document.getElementById("navbar")
const navigation = document.getElementById("navigation")
window.addEventListener("resize", function() {
        
        
            navbar.classList.toggle("show")
        
        
  
}, 800)

function displaynav() {
        navigation.classList.toggle("display")
}
//Helps with the resizing of the navbar for smaller screens