
//Function for displaying customer personal settings on the div with the customer_personal_settings id on accountSettings.html
function CustomerpersonalSettings() {
    const displaySettings = document.getElementById("customer_personal_settings")
    displaySettings.innerHTML = `
        <form action="/update_customer_email" method="post">
            <h2>Enter old email</h2>
            <input type="email" placeholder="bill@example.com" name="old_email">
            <h2>Enter new email</h2>
            <input type="email" placeholder="billy@example.com" name="new_email">
            <h2>Enter your password</h2>
            <input type="password" name="password">
            <button type="submit">Update</button>
        </form>
        
        <button class="form_button" onclick="closeCustomerPerosnalSettings()">close</button>
    `
}
//Function for closing personal settings on the div with the customer_personal_settings id on accountSettings.html
function closeCustomerPerosnalSettings() {
    const displaySettings = document.getElementById("customer_personal_settings")
    displaySettings.innerHTML = ""
}
//Function for displaying producer personal settings on the div with the producer_personal_settings id on accountSettings.html
function ProducerpersonalSettings() {
    const displaySettings = document.getElementById("producer_personal_settings")
    displaySettings.innerHTML = `
        <form action="/update_producer_email" method="post">
            <h2>Enter old email</h2>
            <input type="email" placeholder="bill@example.com" name="old_email">
            <h2>Enter new email</h2>
            <input type="email" placeholder="billy@example.com" name="new_email">
            <h2>Enter your password</h2>
            <input type="password" name="password">
            <button type="submit">Update</button>
        </form>
     
        <button class="form_button" onclick="closeCustomerPerosnalSettings()">close</button>
    `
}

//Function for displaying producer farm settings on the div with the producer_farm_settings id on accountSettings.html
function changeFarmDetails() {
    const producerFarm = document.getElementById("producer_farm_settings")
    producerFarm.innerHTML = `
        <form action="/update_farm_name" method="post">
            
            <h2>Enter new farm name</h2>
            <input type="text" name="farm_name">
            <button type="submit">Submit</button>
        </form>

        <form action="/update_farm_desc" method="post">
            
            <h2>Enter new description</h2>
            <textarea name="description" maxlength="500" minlength="50"></textarea>
            <button type="submit">Submit</button>
        </form>

        <form action="/update_farm_tele" method="post">
            
            <h2>What is your new telephone number?</h2>
                <input 
                    type="tel" 
                     
                    name="phone_number" 
                    placeholder="e.g. 07700 900123 or +44 7700 900123"
                    pattern="^(\+44\s?7\d{3}|\(?07\d{3}\)?)\s?\d{3}\s?\d{3}$|^(\+44\s?20\s?\d{4}\s?\d{4}|\(?0\d{2,4}\)?\s?\d{3,4}\s?\d{3,4})$"
                    required maxlength="15"
                >
            <button type="submit">Submit</button>
        </form>

        <form action="/update_farm_img" method="post">
            
            
                <h2>Add an image link for your farm</h2>
                <input type="text" name="image">
            <button type="submit">Submit</button>
        </form>

        <form action="/update_farm_link" method="post">
            
            
                <h2>Add a link to your website</h2>
                <input type="url" name="website_link" maxlength="250"></input>
            <button type="submit">Submit</button>
        </form>

    
    
    `
}