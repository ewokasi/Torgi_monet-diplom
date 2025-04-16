
// Функция для переключения вкладок
function openTab(evt, tabName) {
    let tabContents = document.getElementsByClassName("tab-content");
    let tabButtons = document.getElementsByClassName("tab-button");

    // Скрыть все вкладки
    for (let i = 0; i < tabContents.length; i++) {
        tabContents[i].style.display = "none";
        tabContents[i].classList.remove("active");
    }

    // Убрать активное состояние с кнопок
    for (let i = 0; i < tabButtons.length; i++) {
        tabButtons[i].classList.remove("active");
    }

    // Показать текущую вкладку и добавить активный класс к кнопке
    document.getElementById(tabName).style.display = "block";
    document.getElementById(tabName).classList.add("active");
    evt.currentTarget.classList.add("active");
}

// Подключение формы входа к бэкенду
document.getElementById("loginForm").addEventListener("submit", function (e) {
    e.preventDefault();
    let password = document.getElementById("login-password").value;
    let mail = document.getElementById("login-mail").value;

    fetch('/auth/token', {
        method: 'POST',
        headers: {
            'accept': 'application/json'
        },
        body: new URLSearchParams({
            'grant_type': 'password',
            'username': mail,
            'password': password,
            'scope': '',
            'client_id': 'string',
            'client_secret': 'string'
        })
    })
        .then(response => response.json())
        .then(data => {
            console.log(data)
            if (data['detail'] == 'Invalid credentials'){
                customAlert("Неверные данные входа");
            }
            if (data['access_token']) {
                window.open(`/`, "_self");
            } else if (data=="Ваша почта не подтверждена, сообщение отправлено на почту") {
                customAlert(data);
            }
        })
        .catch(error => {
            console.error("Ошибка:", error);
        });
});

document.getElementById('register-phone').addEventListener('input', function (e) {
    let x = e.target.value.replace(/\D/g, '').substring(1); // Убираем все, кроме чисел
    let formattedNumber = '+7 ';
    if (x.length > 0) formattedNumber += '(' + x.substring(0, 3);
    if (x.length >= 4) formattedNumber += ') ' + x.substring(3, 6);
    if (x.length >= 7) formattedNumber += '-' + x.substring(6, 8);
    if (x.length >= 9) formattedNumber += '-' + x.substring(8, 10);
    e.target.value = formattedNumber;
  });


  document.getElementById('register-email').addEventListener('input', function (e) {
    // Убираем пробелы с начала и конца и запрещаем ввод пробелов внутри
    e.target.value = e.target.value.replace(/\s/g, '');

    // Валидация для email формата
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]*$/;
    if (!emailRegex.test(e.target.value)) {
        e.target.setCustomValidity("Пожалуйста, введите корректный email.");
    } else {
        e.target.setCustomValidity("");
    }
});

// Подключение формы регистрации к бэкенду
document.getElementById("registerForm").addEventListener("submit", function (e) {
    e.preventDefault();

    const password = document.getElementById("register-password").value;
    const confirmPassword = document.getElementById("confirm-password").value;
    const phone_number = document.getElementById("register-phone").value;
    const email = document.getElementById("register-email").value;
    const nickname = document.getElementById("register-nickname").value;

    // Проверка совпадения паролей
    if (password !== confirmPassword) {
        customAlert("Пароли не совпадают. Пожалуйста, попробуйте снова.");
        return;
    }

    // Проверка на уже зарегистрированный email
    fetch(`/auth/check_mail?mail=${email}`, {
        method: 'POST',
        headers: {
            'accept': 'application/json',
            'content-type': 'application/x-www-form-urlencoded'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data === 1) {
            customAlert("Этот email уже зарегистрирован.");
            return;
        }
        console.log(phone_number)
        // Отправка данных для регистрации, если email не зарегистрирован
        return fetch(`/auth/register?phone_number=${phone_number}&password=${password}&email=${email}&nickname=${nickname}`, {
            method: 'POST',
            headers: {
                'accept': 'application/json',
                'content-type': 'application/x-www-form-urlencoded'
            }
        });
    })
    .then(response => response ? response.json() : null)
    .then(data => {
        console.log(data)
        if (data && data.success === true) {
            customAlert("На почту отправлено письмо с подтверждением электронной почты")
        } else {
            customAlert(`Ошибка регистрации. ${data.error}`);
        }
    })
    .catch(error => {
        console.error("Ошибка:", error);
        customAlert(`Произошла ошибка. Попробуйте позже`);
    });
});
function togglePasswordVisibility(inputId, toggleButton) {
    const inputField = document.getElementById(inputId);
    const isPasswordVisible = inputField.type === 'text';
    
    // Переключаем тип поля
    inputField.type = isPasswordVisible ? 'password' : 'text';
    
    // Меняем иконку при необходимости
    toggleButton.querySelector('svg').style.fill = isPasswordVisible ? '#555' : '#ffbb63';
}

//customAlert("Мы используем файлы Куки для авторизации, продолжая пользоваться сервисом, вы даете свое согласиие на их обработку")