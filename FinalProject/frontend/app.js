const API_BASE = "http://127.0.0.1:8000/api/";

let receiptModalInstance = null;
let allowClose = false;

document.addEventListener("DOMContentLoaded", () => {
    const modalEl = document.getElementById("receiptModal");

    if (modalEl) {
        receiptModalInstance = new bootstrap.Modal(modalEl, {
            backdrop: 'static',
            keyboard: false
        });

        modalEl.addEventListener('hide.bs.modal', function (e) {
            if (!allowClose) {
                e.preventDefault();
            }
        });
    }
});

function closeReceiptModal() {
    allowClose = true;
    receiptModalInstance.hide();

    setTimeout(() => {
        allowClose = false;
    }, 300);
}

async function handleAuth(action) {
    let username = action === 'login'
        ? document.getElementById("login-user").value
        : document.getElementById("reg-user").value;

    let password = action === 'login'
        ? document.getElementById("login-pass").value
        : document.getElementById("reg-pass").value;

    if (!username || !password) {
        alert("Please fill in both fields.");
        return;
    }

    try {
        let response = await fetch(API_BASE + "auth/" + action + "/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        });

        let data = await response.json();

        if (response.ok) {
            localStorage.setItem("bankingToken", data.token);
            window.location.href = "index.html";
        } else {
            alert("Error: " + (data.error || "Something went wrong"));
        }
    } catch {
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
    } catch {
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
            body: JSON.stringify({ amount })
        });

        let data = await response.json();

        if (response.ok) {
            document.getElementById("amount").value = "";

            await loadAccount();

            showReceiptModal(type, amount, data.new_balance);

        } else {
            alert("Error: " + data.error);
        }
    } catch {
        alert("Transaction failed to process.");
    }
}

function showReceiptModal(type, amount, newBalance) {
    let date = new Date().toLocaleString();
    let accNum = document.getElementById("acc-num").innerText;

    document.getElementById("rec-date").innerText = date;
    document.getElementById("rec-acc").innerText = accNum;
    document.getElementById("rec-type").innerText = type;
    document.getElementById("rec-amount").innerText = parseFloat(amount).toFixed(2);
    document.getElementById("rec-balance").innerText = parseFloat(newBalance).toFixed(2);

    if (receiptModalInstance) {
        receiptModalInstance.show();
    }
}

function downloadPDF() {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    let date = document.getElementById("rec-date").innerText;
    let accNum = document.getElementById("rec-acc").innerText;
    let type = document.getElementById("rec-type").innerText;
    let amount = document.getElementById("rec-amount").innerText;
    let newBalance = document.getElementById("rec-balance").innerText;

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
    doc.text(`Amount: PHP ${amount}`, 20, 80);
    doc.text(`New Balance: PHP ${newBalance}`, 20, 90);

    doc.text("---------------------------------------------------------", 105, 100, null, null, "center");
    doc.setFont("helvetica", "italic");
    doc.text("Thank you for banking with us!", 105, 110, null, null, "center");

    let fileName = `Receipt_${type}_${Date.now()}.pdf`;
    doc.save(fileName);
}

async function makeTransfer() {
    let destAcc = document.getElementById("dest-acc").value;
    let amount = document.getElementById("transfer-amount").value;
    let token = localStorage.getItem("bankingToken");

    if (!destAcc || amount <= 0) {
        return alert("Please enter valid details.");
    }

    try {
        let response = await fetch(API_BASE + "transfer/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Token " + token
            },
            body: JSON.stringify({
                destination_account: destAcc,
                amount
            })
        });

        let data = await response.json();

        if (response.ok) {
            document.getElementById("dest-acc").value = "";
            document.getElementById("transfer-amount").value = "";

            await loadAccount();

            showReceiptModal("transfer", amount, data.new_balance);

        } else {
            alert("Error: " + data.error);
        }
    } catch {
        alert("Transfer failed.");
    }
}

async function loadProfile() {
    let token = localStorage.getItem("bankingToken");

    let profResponse = await fetch(API_BASE + "profile/", {
        headers: { "Authorization": "Token " + token }
    });

    if (profResponse.ok) {
        let profData = await profResponse.json();
        document.getElementById("prof-username").value = profData.username;
        document.getElementById("prof-email").value = profData.email;
        document.getElementById("prof-first").value = profData.first_name;
        document.getElementById("prof-last").value = profData.last_name;
    }

    let histResponse = await fetch(API_BASE + "transactions/", {
        headers: { "Authorization": "Token " + token }
    });

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
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Token " + token
        },
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

if (window.location.pathname.includes("index.html") || window.location.pathname === "/") {
    window.onload = loadAccount;
}