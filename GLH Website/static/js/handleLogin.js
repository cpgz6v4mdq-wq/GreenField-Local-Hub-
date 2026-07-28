const app = document.getElementById("app")


const customerMessageType = document.getElementById("customer_message")
const loginMessageType = document.getElementById("loginTypeMessage")


//Gets the login and signup options
const signup = document.getElementById("signup")
const login = document.getElementById("login")

//Gets the customer and producer options
const customer = document.getElementById("customer")
const producer = document.getElementById("producer")


let signupCount = 0
let loginCount = 0
let customerCount = 0
let producerCount = 0




//Signup listens for a click. if click happens signupCount = 1
signup.addEventListener("click", function() {
    signupCount = 1
    loginCount = 0
    loginMessageType.innerText = "You selected signup"
    setTimeout(function() {
        loginMessageType.innerText = ""
    }, 3000)
    
})

//login listens for a click. if click happens logincount = 1
login.addEventListener("click", function() {
    loginCount = 1
    signupCount = 0
    loginMessageType.innerText = "You selected login"
    setTimeout(function() {
        loginMessageType.innerText = ""
    }, 3000)
    
})
//customer listens for a click. if click happens customerCount = 1
customer.addEventListener("click", function() {
    customerCount = 1
    producerCount = 0
    customerMessageType.innerText = "You selected customer"
    setTimeout(function() {
        customerMessageType.innerText = ""
    }, 3000)
    displayForm()
})
//producer listens for a click. if click happens producerCount = 1
producer.addEventListener("click", function() {
    customerCount = 0
    producerCount = 1
    customerMessageType.innerText = "You selected producer"
    setTimeout(function() {
        customerMessageType.innerText = ""
    }, 3000)
    displayForm()
})




//Displays the count for users selected options
function displayCount() {
    


    
    console.log("Sign up count: ", signupCount)
    console.log("Login count: ", loginCount)
    console.log("__________________________________")
    console.log("Customer count: ", customerCount)
    console.log("produer count: ", producerCount)
    console.log("_____________________________")
}
//Once user has selected each option depending on the count will result in what the user sees
function displayForm() {
    let formAddress = ""
    let buttonDisplay = ""
    let htmlDisplay = ""
    if (signupCount === 1 && customerCount === 1) {
        formAddress = "/customer_signup"
        buttonDisplay = "Sign up as customer"
        htmlDisplay = `
            <h1>Name</h1>
            <input type="text" placeholder="James" name="name">
        
        `
    } else if (signupCount === 1 && producerCount === 1) {
        formAddress = "/producer_signup"
        buttonDisplay = "Sign up as producer"
        htmlDisplay = `
            <h1>Name</h1>
            <input type="text" placeholder="James" name="name">
        
        `
    } else if (loginCount === 1 && customerCount === 1) {
        formAddress = "/customer_login"
        buttonDisplay = "Login as customer"
        htmlDisplay = ""
    } else if (loginCount === 1 && producerCount === 1) {
        formAddress = "/producer_login"
        buttonDisplay = "Login as producer"
        htmlDisplay = ""
    }
    //html is only written once to prevent everything from being hardcoded and to ensure things can be easily changed.
    app.innerHTML = `
            <form action="${formAddress}" method="post">
                    
                    ${htmlDisplay}
                    <h1>Email</h1>
                    <input type="email" placeholder="James@example.com" name="email">
                    <h1>Passsword</h1>
                    <input type="password" placeholder="......." name="password">
                    
                    <button type="submit">${buttonDisplay}</button>
            </form>

    `
}

