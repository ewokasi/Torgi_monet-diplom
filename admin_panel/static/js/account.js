document.addEventListener("DOMContentLoaded", function () {
    loadAccountData();
});

// Функция для загрузки данных пользователя
function loadAccountData() {
    fetch("/auth/get_data", {
        method: "GET",
        headers: {
            "Authorization": "Bearer " + localStorage.getItem("authToken"),
            "Content-Type": "application/json",
        },
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        if (data.detail=="Invalid credentials"){
            
            window.open('/login',"_self")
        }
        if (data) {
            // Заполняем поля данными пользователя
            document.getElementById("avito-url").value = data.avito_url || '';
            document.getElementById("phone-number").value = data.phone_number ;
            document.getElementById("bid-notification").checked = data.mail_receive_bet_beated ;
            document.getElementById("auction-start-notification").checked = data.mail_receive_auction_started ;
        } else {
            customAlert("Ошибка загрузки данных пользователя. Попробуйте обновить страницу.");
        }
    })
    .catch(error => {
        console.error("Ошибка при загрузке данных:", error);
    });
}

// Функция для обработки изменения данных профиля
document.getElementById("accountForm").addEventListener("submit", function (e) {
    e.preventDefault();
    let nickname = document.getElementById("nickname").value;
    let avitoUrl = document.getElementById("avito-url").value;
    let phone = document.getElementById("phone-number").value;
    let mail_receive_auction_started = document.getElementById("auction-start-notification").checked;
    let mail_receive_bet_beated = document.getElementById("bid-notification").checked;

    fetch("/mongo/clients/update", {
        method: "POST",
        headers: {
            "Authorization": "Bearer " + localStorage.getItem("authToken"),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ 
            "nickname": nickname, 
            "avito_url": avitoUrl ,
            "phone_number": phone,
            "mail_receive_auction_started": mail_receive_auction_started,
            "mail_receive_bet_beated": mail_receive_bet_beated
        }),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        if (data.success) {
            customAlert("Данные обновлены успешно!");
            location.reload()
        } else {
            customAlert(data.message);
        }
    })
    .catch(error => {
        console.error("Ошибка:", error);
    });
});

// Функция для обработки изменения пароля
document.getElementById("passwordForm").addEventListener("submit", function (e) {
    e.preventDefault();
    let currentPassword = document.getElementById("current-password").value;
    let newPassword = document.getElementById("new-password").value;
    let confirmPassword = document.getElementById("confirm-password").value;

    if (newPassword !== confirmPassword) {
        customAlert("Пароли не совпадают!");
        return;
    }

    fetch("/mongo/clients/change_password", {
        method: "POST",
        headers: {
            "Authorization": "Bearer " + localStorage.getItem("authToken"),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ "old_password": currentPassword, "new_password": newPassword }),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        if (data.success) {
            customAlert("Вы сменили пароль и будете перенаправлены на логин")
            handleLogout();
        } else {
            customAlert("Ошибка при смене пароля. Проверьте текущий пароль.");
        }
    })
    .catch(error => {
        console.error("Ошибка:", error);
    });
});

