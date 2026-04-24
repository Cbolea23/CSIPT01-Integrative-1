const API_BASE = "http://127.0.0.1:8000/api/";

// Load balance on page load
async function loadAccount() {
    try {
        let response = await fetch(API_BASE + "account/");
        let data = await response.json();
        
        if (data.account_number) {
            document.getElementById("acc-num").innerText = data.account_number;
            document.getElementById("balance").innerText = data.balance;
        } else {
            console.error("Account load error:", data.error);
        }
    } catch (error) {
        console.error("Failed to connect to API");
    }
}

// Handle deposit and withdrawal
async function makeTransaction(type) {
    let amount = document.getElementById("amount").value;
    if (!amount || amount <= 0) {
        alert("Please enter a valid amount.");
        return;
    }

    try {
        let response = await fetch(API_BASE + type + "/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ amount: amount })
        });
        
        let data = await response.json();
        if (response.ok) {
            alert(data.message);
            loadAccount(); // Refresh the balance
            document.getElementById("amount").value = "";
        } else {
            alert("Error: " + data.error);
        }
    } catch (error) {
        alert("Transaction failed to process.");
    }
}

window.onload = loadAccount;