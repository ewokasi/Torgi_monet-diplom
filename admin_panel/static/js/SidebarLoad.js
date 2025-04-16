
// Функция для подгрузки Sidebar
function loadSidebar() {
    fetch('sidebar.html')
        .then(response => response.text())
        .then(data => {
            document.getElementsByClassName('Sidebar')[0].innerHTML = data;
            get_data(); // Вызов функции для загрузки данных пользователя
        })
        .catch(error => console.error('Ошибка загрузки Sidebar:', error));
}

// Выполняем загрузку Sidebar после загрузки DOM
document.addEventListener('DOMContentLoaded', loadSidebar);

fetch('/auth/get_data')
    .then(response => response.json())
    .then(data => {
        const nicknameElement = document.getElementById('nickname');
        nicknameElement.textContent = data['nickname'] || 'Войти';

        if (nicknameElement.textContent === 'Войти') {
            nicknameElement.onclick = function() {
                window.open('/login', "_blank");
                nicknameElement.style.textDecoration = 'underline';
            };
        } else {
            // Добавляем класс для стилизации вошедшего пользователя
            nicknameElement.classList.add("nickname-logged");
        }
    })
    .catch(error => console.error("Ошибка:", error));
  
 

  function handleLogout() {
    fetch('/auth/logout', {
        method: 'POST',
        headers: {
            'accept': 'application/json',
            'content-type': 'application/x-www-form-urlencoded'
        },
        body: ''
    })
    .then(response => {
        if (response.ok) {
            window.open('/login', '_self'); // Открыть страницу входа
        } else {
            console.error("Ошибка при выходе.");
            alert("Не удалось выйти. Попробуйте еще раз.");
        }
    })
    .catch(error => {
        console.error("Ошибка:", error);
        alert("Произошла ошибка при выходе. Попробуйте позже.");
    });
  }
  
  