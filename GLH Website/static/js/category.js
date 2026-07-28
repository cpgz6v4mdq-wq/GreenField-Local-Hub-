//Prevents users from submitting without ticking at least one box
const formButton = document.getElementById("form_button")
const checkboxOne = document.getElementById("checkbox_1")
const checkboxTwo = document.getElementById("checkbox_2")
const checkBoxThree = document.getElementById("checkbox_3")
const checkBoxFour = document.getElementById("checkbox_4")
const checkBoxFive = document.getElementById("checkbox_5")
const checkboxSix = document.getElementById("checkbox_6")

formButton.disabled = true
checkboxOne.addEventListener("change", function() {
    formButton.disabled = !checkboxOne.checked
})

checkboxTwo.addEventListener("change", function() {
    formButton.disabled = !checkboxTwo.checked
})

checkBoxThree.addEventListener("change", function() {
    formButton.disabled = !checkBoxThree.checked
})

checkBoxFour.addEventListener("change", function() {
    formButton.disabled = !checkBoxFour.checked
})
   
checkBoxFive.addEventListener("change", function() {
    formButton.disabled = !checkBoxFive.checked
})

checkboxSix.addEventListener("change", function() {
    formButton.disabled = !checkboxSix.checked
})