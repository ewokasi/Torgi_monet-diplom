document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("createAuctionForm");
    const fileInput = document.getElementById("coin-photo");
    const previewImage = document.getElementById("preview-image");
    let base64Image = ""; // Variable to store the Base64 of the main image
    let albumImages = []; // Array to store additional images' Base64

    // Function to convert an image to Base64
    function convertImageToBase64(file) {
        return new Promise((resolve) => {
            const reader = new FileReader();
            reader.onloadend = () => {
                const base64 = reader.result.split(",")[1]; // Extract Base64 string
                resolve(base64); // Resolve promise with Base64 string
            };
            reader.readAsDataURL(file); // Read file as Data URL
        });
    }

    // Обработка выбора главного фото
    fileInput.addEventListener("change", function (event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onloadend = () => {
                previewImage.src = reader.result; // Устанавливаем изображение в элемент превью
                previewImage.style.display = "block"; // Показываем превью
                convertImageToBase64(file).then((base64) => {
                    base64Image = base64; // Сохраняем Base64 изображения
                });
            };
            reader.readAsDataURL(file); // Преобразуем файл в Data URL
        }
    });

    // Handle form submission
    form.addEventListener("submit", function (e) {
        e.preventDefault(); // Prevent default form submission

        // Check and validate the start and end date-time fields
        const startDateTime = document.getElementById("start_datetime").value;
        const endDateTime = document.getElementById("end_datetime").value;

        if (!isValidDateTime(startDateTime)) {
            customAlert("Неверный формат даты начала! Используйте формат: дд.мм.гггг чч:мм");
            return;
        }

        if (!isValidDateTime(endDateTime)) {
            customAlert("Неверный формат даты окончания! Используйте формат: дд.мм.гггг чч:мм");
            return;
        }

        // Check and validate the price fields
        const startPrice = document.getElementById("start_price").value;
        const minBidStep = document.getElementById("min_bid_step").value;

        if (!isPositiveNumber(startPrice)) {
            customAlert("Начальная цена должна быть числом больше 0!");
            return;
        }

        if (!isPositiveNumber(minBidStep)) {
            customAlert("Минимальный шаг ставки должен быть числом больше 0!");
            return;
        }

        // Collect additional images from the album inputs
        let albumInputs = document.querySelectorAll('#album input[type="file"]'); // Find all file inputs in the album container
        let albumPromises = []; // To hold promises for each image conversion

        albumInputs.forEach((input) => {
            let file = input.files[0];
            if (file) {
                albumPromises.push(convertImageToBase64(file)); // Add conversion promise to the array
            }
        });

        // Wait for all Base64 conversions to complete
        Promise.all(albumPromises).then((albumBase64Images) => {
            albumImages = albumBase64Images; // Store all album images' Base64 in the array

            // Prepare data to send
            let auctionData = {
                short_name: document.getElementById("short_name").value,
                start_datetime: startDateTime,
                end_datetime: endDateTime,
                start_price: startPrice,
                min_bid_step: minBidStep,
                description: document.getElementById("description").value,
                bank: document.getElementById("bank").value,
                photo: base64Image, // Main image in Base64
                album: albumImages // Additional images in Base64
            };

            console.log(auctionData); // Check data before sending it

            // Send data via fetch
            fetch("/mongo/auction/add", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(auctionData),
            })
            .then(response => response.json())
            .then(data => {
                if (data) {
                    customAlert("Аукцион успешно создан!");
                    // Uncomment the following line for redirection after successful auction creation
                    // window.location.href = `alt_auction?a_id=${data.a_id}`;
                } else {
                    customAlert("Ошибка при создании аукциона. Попробуйте снова.");
                }
            })
            .catch(error => {
                console.error("Ошибка при создании аукциона:", error);
            });
        });
    });
});

// Функция для добавления поля загрузки дополнительного фото
function addAlbumPhotoInput() {
    // Получаем контейнер для альбома
    const album = document.getElementById('album');

    // Создаем новый input для загрузки фотографии
    const inp = document.createElement('input');
    inp.type = 'file';
    inp.classList.add('coin-album'); // Добавляем класс для идентификации
    inp.accept = 'image/*'; // Только изображения

    // Создаем элемент для превью изображения
    const previewContainer = document.createElement('div');
    previewContainer.classList.add('photo-preview');
    const img = document.createElement('img');
    img.style.display = "none"; // Скрываем изображение по умолчанию
    previewContainer.appendChild(img);
    
    // Добавляем контейнер с input и превью в альбом
    album.appendChild(inp);
    album.appendChild(previewContainer);

    // Обработка выбора дополнительного фото
    inp.addEventListener("change", function (event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onloadend = () => {
                // Отображаем изображение в превью
                img.src = reader.result;
                img.style.display = "block"; // Показываем изображение
            };
            reader.readAsDataURL(file); // Преобразуем файл в Data URL
        }
    });
}

// Функция проверки формата даты
function isValidDateTime(dateTime) {
    const dateTimeRegex = /^(\d{2}).(\d{2}).(\d{4}) (\d{2}):(\d{2})$/; // Регулярное выражение для дд.мм.гггг чч:мм
    const match = dateTime.match(dateTimeRegex);
    if (!match) return false;

    const day = parseInt(match[1], 10);
    const month = parseInt(match[2], 10);
    const year = parseInt(match[3], 10);
    const hours = parseInt(match[4], 10);
    const minutes = parseInt(match[5], 10);

    // Проверяем корректность значений даты и времени
    if (day < 1 || day > 31 || month < 1 || month > 12 || year < 1900 || year > 2100) return false;
    if (hours < 0 || hours > 23 || minutes < 0 || minutes > 59) return false;

    return true;
}

// Проверка числовых полей
function isPositiveNumber(value) {
    return !isNaN(value) && Number(value) > 0;
}

document.addEventListener("DOMContentLoaded", function () {
    // Инициализация Flatpickr на полях выбора даты и времени
    flatpickr("#start_datetime", {
        enableTime: true, // Включить выбор времени
        dateFormat: "d.m.Y H:i", // Формат даты и времени
        time_24hr: true, // Формат времени 24 часа
        locale: "ru", // Локализация на русский язык
        minDate: "today", // Минимальная дата — сегодня
    });

    flatpickr("#end_datetime", {
        enableTime: true,
        dateFormat: "d.m.Y H:i",
        time_24hr: true,
        locale: "ru",
        minDate: "today",
    });
});
