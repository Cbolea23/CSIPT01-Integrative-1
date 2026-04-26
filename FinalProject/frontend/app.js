const API_BASE = "http://127.0.0.1:8000/api/";

async function handleAuth(action) {
    let username = action === 'login' ? document.getElementById("login-user").value : document.getElementById("reg-user").value;
    let password = action === 'login' ? document.getElementById("login-pass").value : document.getElementById("reg-pass").value;

    if (!username || !password) {
        alert("Please fill in both fields.");
        return;
    }

    try {
        let response = await fetch(API_BASE + "auth/" + action + "/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username: username, password: password })
        });
        
        let data = await response.json();
        if (response.ok) {
            localStorage.setItem("bankingToken", data.token);
            window.location.href = "index.html";
        } else {
            alert("Error: " + (data.error || "Something went wrong"));
        }
    } catch (error) {
        alert("Connection failed.");
    }
}

function logout() {
    localStorage.removeItem("bankingToken");
    window.location.href = "login.html";
}

async function loadAccount() {
    let token = localStorage.getItem("bankingToken");
    
    if (!token) {
        window.location.href = "login.html";
        return;
    }

    try {
        let response = await fetch(API_BASE + "account/", {
            headers: { "Authorization": "Token " + token }
        });
        
        let data = await response.json();
        
        if (response.ok) {
            document.getElementById("acc-num").innerText = data.account_number;
            document.getElementById("balance").innerText = data.balance;
        } else {
            logout();
        }
    } catch (error) {
        console.error("Failed to connect to API");
    }
}

async function makeTransaction(type) {
    let amount = document.getElementById("amount").value;
    let token = localStorage.getItem("bankingToken");

    if (!amount || amount <= 0) {
        alert("Please enter a valid amount.");
        return;
    }

    try {
        let response = await fetch(API_BASE + type + "/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Token " + token
            },
            body: JSON.stringify({ amount: amount })
        });
        
        let data = await response.json();
        
        if (response.ok) {
            alert(data.message);
            
            let wantReceipt = confirm("Do you want to download a receipt for this transaction?");
            if (wantReceipt) {
                generatePDFReceipt(type, amount, data.new_balance);
            }
            
            loadAccount(); 
            document.getElementById("amount").value = "";
        } else {
            alert("Error: " + data.error);
        }
    } catch (error) {
        alert("Transaction failed to process.");
    }
}

function generatePDFReceipt(type, amount, newBalance) {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    let date = new Date().toLocaleString();
    let accNum = document.getElementById("acc-num").innerText;

    doc.setFont("helvetica", "bold");
    doc.setFontSize(22);
    doc.text("SecureBank", 105, 20, null, null, "center");

    doc.setFont("helvetica", "normal");
    doc.setFontSize(16);
    doc.text("Transaction Receipt", 105, 30, null, null, "center");

    doc.setFontSize(12);
    doc.text("---------------------------------------------------------", 105, 40, null, null, "center");

    doc.text(`Date: ${date}`, 20, 50);
    doc.text(`Account Number: ${accNum}`, 20, 60);
    doc.text(`Transaction Type: ${type.toUpperCase()}`, 20, 70);
    doc.text(`Amount: PHP ${parseFloat(amount).toFixed(2)}`, 20, 80);
    doc.text(`New Balance: PHP ${parseFloat(newBalance).toFixed(2)}`, 20, 90);

    doc.text("---------------------------------------------------------", 105, 100, null, null, "center");
    doc.setFont("helvetica", "italic");
    doc.text("Thank you for banking with us!", 105, 110, null, null, "center");
    doc.text("Project by Bolea, Nagares, De Chavez, Diokno", 105, 130, null, null, "center");

    let fileName = `Receipt_${type}_${Date.now()}.pdf`;
    doc.save(fileName);
}

if (window.location.pathname.includes("index.html") || window.location.pathname === "/") {
    window.onload = loadAccount;
}

async function makeTransfer() {
    let destAcc = document.getElementById("dest-acc").value;
    let amount = document.getElementById("transfer-amount").value;
    let token = localStorage.getItem("bankingToken");

    if (!destAcc || amount <= 0) return alert("Please enter valid details.");

    try {
        let response = await fetch(API_BASE + "transfer/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Token " + token
            },
            body: JSON.stringify({ destination_account: destAcc, amount: amount })
        });
        let data = await response.json();
        if (response.ok) {
            alert(data.message);
            loadAccount();
            document.getElementById("dest-acc").value = "";
            document.getElementById("transfer-amount").value = "";
        } else {
            alert("Error: " + data.error);
        }
    } catch (error) { alert("Transfer failed."); }
}

async function loadProfile() {
    let token = localStorage.getItem("bankingToken");

    let profResponse = await fetch(API_BASE + "profile/", { headers: { "Authorization": "Token " + token }});
    if (profResponse.ok) {
        let profData = await profResponse.json();
        document.getElementById("prof-username").value = profData.username;
        document.getElementById("prof-email").value = profData.email;
        document.getElementById("prof-first").value = profData.first_name;
        document.getElementById("prof-last").value = profData.last_name;
    }

    let histResponse = await fetch(API_BASE + "transactions/", { headers: { "Authorization": "Token " + token }});
    if (histResponse.ok) {
        let histData = await histResponse.json();
        let tableBody = document.getElementById("history-table");
        tableBody.innerHTML = "";
        
        histData.forEach(tx => {
            let row = `<tr>
                <td>${new Date(tx.timestamp).toLocaleDateString()}</td>
                <td class="text-capitalize">${tx.type}</td>
                <td class="${tx.type === 'withdrawal' ? 'text-danger' : 'text-success'}">${tx.amount}</td>
                <td>${tx.description}</td>
            </tr>`;
            tableBody.innerHTML += row;
        });
    }
}

async function updateProfile() {
    let token = localStorage.getItem("bankingToken");
    let payload = {
        email: document.getElementById("prof-email").value,
        first_name: document.getElementById("prof-first").value,
        last_name: document.getElementById("prof-last").value
    };

    let response = await fetch(API_BASE + "profile/", {
        method: "PUT",
        headers: { "Content-Type": "application/json", "Authorization": "Token " + token },
        body: JSON.stringify(payload)
    });
    let data = await response.json();
    alert(data.message || "Profile updated.");
}

async function deleteAccount() {
    if (confirm("Are you SURE you want to delete your account? This cannot be undone.")) {
        let token = localStorage.getItem("bankingToken");
        let response = await fetch(API_BASE + "close-account/", {
            method: "DELETE",
            headers: { "Authorization": "Token " + token }
        });
        if (response.ok) {
            alert("Account successfully deleted.");
            logout();
        }
    }
}