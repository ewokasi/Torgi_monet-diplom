const dashboardContent = document.getElementById("dashboard-content");
const auctionsTable = document.getElementById("auctionsTable");
const usersTable = document.getElementById("usersTable");
const activeClientsTable = document.getElementById("activeClientsTable");

function showAuctionsTable() {
    auctionsTable.style.display = "table";
    usersTable.style.display = "none";
    activeClientsTable.style.display = "none";
    document.getElementById("auctionSearchContainer").style.display = "block";
    document.getElementById("userSearchContainer").style.display = "none";
    document.getElementById("activeuserSearchContainer").style.display = "none";

    getAllAuctions(); 
}

function showUsersTable() {
    usersTable.style.display = "table";
    auctionsTable.style.display = "none";
    activeClientsTable.style.display = "none";
    document.getElementById("auctionSearchContainer").style.display = "none";
    document.getElementById("userSearchContainer").style.display = "block";
    document.getElementById("activeuserSearchContainer").style.display = "none";
    getAllClients(); 
}

async function showActiveClientsTable() {
    usersTable.style.display = "none";
    auctionsTable.style.display = "none";
    // Отправляем запрос к серверу, чтобы получить список активных пользователей
    const response = await fetch("/mongo/clients/active_clients", { method: "POST" });
    const activeClients = await response.json();
    document.getElementById("activeuserSearchContainer").style.display = "block";
    document.getElementById("userSearchContainer").style.display = "none";
    document.getElementById("auctionSearchContainer").style.display = "none";

    // Находим или создаем контейнер для таблицы активных пользователей
    const activeClientsTable = document.getElementById("activeClientsTableBody");
    activeClientsTable.innerHTML = ""; // Очищаем таблицу

    // Заполняем таблицу данными активных пользователей
    activeClients.forEach(client => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${client.id}</td>
            <td>${client.nickname}</td>
            <td>${client.email}</td>
            <td>${client.phone_number}</td>
            <td>${client.bet_count}</td>
        `;
        activeClientsTable.appendChild(row);
    });

    // Отображаем таблицу
    document.getElementById("activeClientsTable").style.display = "table";
}
// Filter auctions by search input
function filterAuctions() {
    const filter = document.getElementById("auctionSearchInput").value.toLowerCase();
    const rows = document.getElementById("auctionsTableBody").getElementsByTagName("tr");
    Array.from(rows).forEach(row => {
        const auctionName = row.cells[1].textContent.toLowerCase();
        row.style.display = auctionName.includes(filter) ? "" : "none";
    });
}

// Filter users by search input
function filterUsers() {
    const filter = document.getElementById("userSearchInput").value.toLowerCase();
    const rows = document.getElementById("usersTableBody").getElementsByTagName("tr");
    Array.from(rows).forEach(row => {
        const nickname = row.cells[1].textContent.toLowerCase();
        const email = row.cells[2].textContent.toLowerCase();
        const phone = row.cells[3].textContent.toLowerCase();
        row.style.display = nickname.includes(filter) || email.includes(filter) || email.includes(filter) ? "" : "none";
    });
}
// Filter active users by search input
function filterActiveUsers() {
    const filter = document.getElementById("activeuserSearchInput").value.toLowerCase();
    const rows = document.getElementById("activeClientsTableBody").getElementsByTagName("tr");
    Array.from(rows).forEach(row => {
        const nickname = row.cells[1].textContent.toLowerCase();
        row.style.display = nickname.includes(filter) ? "" : "none";
    });
}

// Отображение списка аукционов в таблице с вызовом deleteAuction
async function getAllAuctions() {
    const response = await fetch("/mongo/auction/short_get_all", { method: "GET" });
    const auctions = await response.json();
    const tableBody = document.getElementById("auctionsTableBody");
    tableBody.innerHTML = ""; // Очистка таблицы

    auctions.reverse().forEach(auction => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${auction.a_id}</td>
            <td>${auction.short_name}</td>
            <td><button onclick="editAuction('${auction.a_id}')">Edit</button></td>
            <td><button onclick="deleteAuction('${auction.a_id}', '${auction.short_name}')">Delete</button></td>
        `;
        tableBody.appendChild(row);
    });
}

// Функция для удаления аукциона с подтверждением
async function deleteAuction(id, auctionName) {
    // Создаем модальное окно подтверждения
    const confirmation = prompt(`Введите название аукциона "${auctionName}" для подтверждения удаления:`);

    // Проверяем, совпадает ли введенное значение с именем аукциона
    if (confirmation === auctionName) {
        const response = await fetch(`/mongo/auction/delete?a_id=${id}`, { method: "DELETE" });
        if (response.ok) {
            customAlert("Аукцион успешно удален.");
            getAllAuctions(); // Обновление списка после удаления
        } else {
            customAlert("Ошибка при удалении аукциона.");
        }
    } else {
        customAlert("Удаление отменено: имя аукциона не совпадает.");
    }
}

/// Функция для бана пользователя с подтверждением
async function banClient(id, clientNickname) {
    // Создаем модальное окно подтверждения
    const confirmation = prompt(`Введите никнейм пользователя "${clientNickname}" для подтверждения блокировки:`);

    // Проверяем, совпадает ли введенное значение с никнеймом пользователя
    if (confirmation === clientNickname) {
        const response = await fetch(`/mongo/clients/ban?id=${id}`, { method: "DELETE" });
        if (response.ok) {
            customAlert("Пользователь успешно заблокирован.");
            getAllClients(); // Обновление списка после блокировки
        } else {
            customAlert("Ошибка при блокировке пользователя.");
        }
    } else {
        customAlert("Блокировка отменена: введенный никнейм не совпадает.");
    }
}

// Отображение списка пользователей в таблице с вызовом banClient
async function getAllClients() {
    const response = await fetch("/mongo/clients/get_all", { method: "GET" });
    const clients = await response.json();
    const tableBody = document.getElementById("usersTableBody");
    tableBody.innerHTML = ""; // Очистка таблицы

    clients.reverse().forEach(client => {
        const row = document.createElement("tr");
       
        row.innerHTML = `
            <td>${client.id}</td>
            <td>${client.nickname}</td>
            <td>${client.email}</td>
            <td>${client.phone_number}</td>
            <td><button onclick="editClient('${client.id}')">Edit</button></td>
        `;
        if (client['status']=="banned"){
            row.innerHTML+=`<td><button onclick="unbanClient('${client.id}','${client.nickname}')">Unban</button></td>`
        }else{
            row.innerHTML+=`<td><button onclick="banClient('${client.id}','${client.nickname}')">Ban</button></td>`

        }
        tableBody.appendChild(row);
    });
}



// Функция для закрытия модального окна
function closeEditAuctionModal() {
    document.getElementById("editAuctionModal").style.display = "none";
}



// Показать модальное окно и загрузить данные пользователя
async function editClient(id) {
    // Получаем данные о конкретном пользователе
    const response = await fetch(`/mongo/clients/get?clients_id=${id}`, { method: "GET" });
    const client = await response.json();
    console.log(client);

    const container = document.getElementById("clientFieldsContainer");
    container.innerHTML = ""; // Очищаем контейнер перед добавлением новых полей

    // Проходим по всем полям пользователя и создаем для них инпуты
    for (const [key, value] of Object.entries(client)) {
        if (["c_id", "password", "get_mails"].includes(key)) continue; // Пропускаем ID и другие неизменяемые поля

        const fieldLabel = document.createElement("label");
        fieldLabel.setAttribute("for", `client_${key}`);
        fieldLabel.textContent = key.charAt(0).toUpperCase() + key.slice(1); // Форматируем имя поля

        // Проверяем, если поле должно быть чекбоксом
        if (["mail_receive_bet_beated", "mail_receive_auction_started", "email_verified"].includes(key)) {
            const fieldInput = document.createElement("input");
            fieldInput.setAttribute("type", "checkbox");
            fieldInput.setAttribute("id", `client_${key}`);
            fieldInput.setAttribute("name", key);
            fieldInput.checked = Boolean(value); // Устанавливаем состояние чекбокса на основе значения
            
            container.appendChild(fieldLabel);
            container.appendChild(fieldInput);
        } else {
            const fieldInput = document.createElement("input");
            fieldInput.setAttribute("type", "text");
            fieldInput.setAttribute("id", `client_${key}`);
            fieldInput.setAttribute("name", key);
            fieldInput.value = value || ""; // Устанавливаем текущее значение из данных пользователя
            
            container.appendChild(fieldLabel);
            container.appendChild(fieldInput);
        }
        container.appendChild(document.createElement("br"));
    }

    // Отображаем модальное окно
    const editClientModal = document.getElementById("editClientModal");
    editClientModal.style.display = "flex";

    // Сохраняем ID текущего пользователя, чтобы использовать при сохранении
    editClientModal.dataset.clientId = id;
}


// Функция для закрытия модального окна редактирования пользователя
function closeEditClientModal() {
    document.getElementById("editClientModal").style.display = "none";
}
// Функция для сохранения изменений пользователя
async function saveClientChanges() {
    const editClientModal = document.getElementById("editClientModal");
    const id = editClientModal.dataset.clientId;

    // Сбор данных из всех полей формы
    const fields = document.getElementById("clientFieldsContainer").getElementsByTagName("input");
    const updatedClient = {};

    for (let field of fields) {
        const fieldName = field.name;

        // Проверяем, является ли поле чекбоксом
        if (field.type === "checkbox") {
            updatedClient[fieldName] = field.checked; // Сохраняем значение чекбокса как true/false
        } else if (field.type === "text") {
            const fieldValue = field.value;
            if (fieldValue !== "") {
                updatedClient[fieldName] = fieldValue; // Сохраняем текстовые поля, если они не пустые
            }
        }
    }

    // Формируем JSON объект для отправки
    const payload = {
        id: id,
        ...updatedClient
    };

    // Отправка данных на сервер
    const response = await fetch(`/mongo/clients/edit?id=${id}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });

    if (response.ok) {
        customAlert("Client updated successfully");
        closeEditClientModal();
        getAllClients(); // Обновление списка пользователей
    } else {
        customAlert("Failed to update client");
    }
}




// Закрытие модального окна при нажатии на клавишу Esc
document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
        closeEditAuctionModal();
        closeEditClientModal();
    }
});

// Функция для разбана пользователя
async function unbanClient(id, clientNickname) {
     // Создаем модальное окно подтверждения
     const confirmation = prompt(`Введите никнейм пользователя "${clientNickname}" для подтверждения блокировки:`);

     // Проверяем, совпадает ли введенное значение с никнеймом пользователя
     if (confirmation === clientNickname) {
        try {
            // Отправляем запрос на сервер для разбана пользователя
            const response = await fetch(`/mongo/clients/unban?id=${id}`, {
                method: 'POST',  // POST запрос для разбана
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (response.ok) {
                // Успешный ответ
                const result = await response.json();
                customAlert(result.message); // Показать сообщение об успешном разбане
                getAllClients(); // Обновить список пользователей
            } else {
                // Ошибка от сервера
                const error = await response.json();
                customAlert(`Error: ${error.detail}`); // Показать ошибку
            }
        } catch (error) {
            // Ошибка на клиенте
            console.error('Error during unban:', error);
            customAlert('An error occurred while trying to unban the user.');
        }
    }
}
async function editAuction(id) {
    const response = await fetch(`/mongo/auction/get?a_id=${id}`, { method: "GET" });
    const auction = await response.json();

    const container = document.getElementById("auctionFieldsContainer");
    container.innerHTML = ""; // Очищаем контейнер перед добавлением новых полей

    // Добавляем поля для каждого свойства аукциона
    for (const [key, value] of Object.entries(auction)) {
        if (["a_id", "created_at", "is_active", "album"].includes(key)) continue;
        console.log(key, value)
        const fieldLabel = document.createElement("label");
        fieldLabel.setAttribute("for", `auction_${key}`);
        fieldLabel.textContent = key.charAt(0).toUpperCase() + key.slice(1); 

        if (key === "photo") {
            // Если поле - это фото, создаем элемент для загрузки файла и превью
            const fileInput = document.createElement("input");
            fileInput.type = "file";
            fileInput.id = "auction_photo";
            fileInput.name = "photo";
            fileInput.accept = "image/*";
            fileInput.onchange = handleImageUpload; // Добавляем обработчик загрузки

            const previewImg = document.createElement("img");
            previewImg.id = "previewImg";
            previewImg.style.maxWidth = "100px";
            previewImg.src = "data:image/jpeg;base64,"+value || ""; // Устанавливаем текущее изображение, если оно есть

            container.appendChild(fieldLabel);
            container.appendChild(fileInput);
            container.appendChild(previewImg);
        } 
        else if(key == "bets"){
            bvalue = JSON.stringify(auction['bets'], null, 2)
            const fieldInput = document.createElement("textarea");
            fieldInput.type = "text";
            fieldInput.id = `auction_${key}`;
            fieldInput.name = key;
            fieldInput.value = bvalue || ""; 

            container.appendChild(fieldLabel);
            container.appendChild(fieldInput); 
        }
        else {
            const fieldInput = document.createElement("input");
            fieldInput.type = "text";
            fieldInput.id = `auction_${key}`;
            fieldInput.name = key;
            fieldInput.value = value || ""; 

            container.appendChild(fieldLabel);
            container.appendChild(fieldInput);  
        }
        container.appendChild(document.createElement("br"));
    }

    document.getElementById("editAuctionModal").style.display = "flex";
    document.getElementById("editAuctionModal").dataset.auctionId = id;
}

// Обработчик загрузки изображения
function handleImageUpload(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            document.getElementById("previewImg").src = e.target.result;
        };
        reader.readAsDataURL(file);
    }
}

async function saveAuctionChanges() {
    const editAuctionModal = document.getElementById("editAuctionModal");
    const id = editAuctionModal.dataset.auctionId;

    // Сбор данных из всех полей формы
    const fields = document.getElementById("auctionFieldsContainer").getElementsByTagName("input");
    const bets = document.getElementById("auction_bets"); 
    const updatedAuction = {};

    // Обработка input полей
    for (let field of fields) {
        const fieldName = field.name;
        const fieldValue = field.value;

        // Заполняем только поля, которые были изменены
        if (fieldValue !== "") {
            updatedAuction[fieldName] = fieldValue;
        }
    }

    if (document.getElementById("auction_bets").value != "") {
        updatedAuction["bets"] = document.getElementById("auction_bets").value; // Добавляем в объект, если текст не пустой
      
    }
    
    console.log(updatedAuction)
    // Формируем JSON объект для отправки
    const payload = {
        a_id: id,
        ...updatedAuction
    };

    // Отправка данных на сервер
    const response = await fetch(`/mongo/auction/update_auction?a_id=${id}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });

    if (response.success) {
        customAlert(response.message);
        closeEditAuctionModal();
        getAllAuctions(); // Обновление списка аукционов
    } else {
        customAlert("Failed to update auction");
    }
}
async function saveAuctionChanges() {
    const editAuctionModal = document.getElementById("editAuctionModal");
    const id = editAuctionModal.dataset.auctionId;

    const fields = document.getElementById("auctionFieldsContainer").getElementsByTagName("input");
    const updatedAuction = {};

    for (let field of fields) {
        const fieldName = field.name;
        const fieldValue = field.value;
        if (fieldName === "photo" && field.files.length > 0) {
            const file = field.files[0];
            updatedAuction.photo = await convertFileToBase64(file); 
        } else {
            updatedAuction[fieldName] = fieldValue;
        }
    }
    
    if (document.getElementById("auction_bets").value != "") {
        updatedAuction["bets"] = document.getElementById("auction_bets").value; // Добавляем в объект, если текст не пустой
      
    }
    

    const payload = { a_id: id, ...updatedAuction };

    const response = await fetch(`/mongo/auction/update_auction?a_id=${id}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });
    
    const result = await response.json(); // Преобразуем ответ в JSON
    
    if (result.success) {
        customAlert("Auction updated successfully");
        closeEditAuctionModal();
        getAllAuctions();
    } else {
        customAlert("Error: " + result['message']);
    }
}


// Конвертация файла изображения в Base64
function convertFileToBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.onerror = error => reject(error);
        reader.readAsDataURL(file);
    });
}


getAllAuctions();
showAuctionsTable();


