
var end_datetime; 
// Функция для загрузки данных аукциона
function loadAuctionDetails(auctionId) {
    fetch(`/mongo/auction/get?a_id=${auctionId}`)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            end_datetime = new Date(data.end_datetime);

            // Заполняем данные аукциона
            document.querySelector("#auction-datetime").textContent = new Date(data.start_datetime).toLocaleString();
            document.querySelector("#auction-datetime-end").textContent = new Date(data.end_datetime).toLocaleString() + " UTC+" + new Date().getTimezoneOffset() / -60;
            document.querySelector("#coin-name").textContent = data.short_name;
            document.querySelector("#starting-price").textContent = data.start_price;
            document.querySelector("#min-bid-step").textContent = data.min_bid_step;
            document.querySelector("#description").textContent = data.description;
            document.querySelector("#status-button").textContent = data.is_active ? "Идут торги..." : "Неактивно";

            if ("bank" in data) {
                const coinUrl = document.querySelector("#coin-url");
                coinUrl.href = data['bank'];
                coinUrl.innerHTML = "Подробнее на Банк России...";
            }

            // Создаем карусель
            const carouselContainer = document.querySelector("#carousel-container");
            carouselContainer.innerHTML = ""; // Очищаем предыдущие данные

            const images = [];

            // Добавляем главное фото
            if (data.photo) {
                images.push(`data:image/jpeg;base64,${data.photo}`);
            }

            // Добавляем фото из альбома
            if (data.album && Array.isArray(data.album)) {
                data.album.forEach(photo => {
                    images.push(`data:image/jpeg;base64,${photo}`);
                });
            }

            // Если есть изображения, создаем карусель
            if (images.length > 0) {
                const track = document.createElement("div");
                track.className = "carousel-track";

                images.forEach((src, index) => {
                    const slide = document.createElement("div");
                    slide.className = "carousel-slide";
                    const img = document.createElement("img");
                    img.src = src;
                    img.alt = `Изображение ${index + 1}`;                    
                    slide.appendChild(img);
                    track.appendChild(slide);
                });

                carouselContainer.appendChild(track);

                // Добавляем кнопки управления
                const prevButton = document.createElement("button");
                prevButton.className = "carousel-button prev";
                prevButton.textContent = "❮";
                const nextButton = document.createElement("button");
                nextButton.className = "carousel-button next";
                nextButton.textContent = "❯";
                
                carouselContainer.appendChild(prevButton);
                carouselContainer.appendChild(nextButton);

                if (images.length ==1){
                    prevButton.style.display = "None";
                    nextButton.style.display = "None";
                }

                // Добавляем логику для карусели
                const slides = Array.from(track.children);
                let currentSlide = 0;

                const updateCarousel = () => {
                    const slideWidth = slides[0].getBoundingClientRect().width;
                    track.style.transform = `translateX(-${currentSlide * slideWidth}px)`;
                };

                prevButton.addEventListener("click", () => {
                    currentSlide = (currentSlide - 1 + slides.length) % slides.length;
                    updateCarousel();
                });

                nextButton.addEventListener("click", () => {
                    currentSlide = (currentSlide + 1) % slides.length;
                    updateCarousel();
                });
                window.addEventListener("resize", updateCarousel);

                // Инициализация карусели
                updateCarousel();
            } else {
                // Если нет фото, показываем сообщение
                carouselContainer.textContent = "Изображения отсутствуют";
            }

            // Заполняем таблицу ставок
            const bidTable = document.querySelector("#bid-table tbody");
            bidTable.innerHTML = ""; // Очищаем предыдущие данные

            document.getElementById("time").textContent = "Время UTC+" + new Date().getTimezoneOffset() / -60;

            if (data.bets && data.bets.length > 0) {
                data.bets.slice().reverse().forEach(bet => {
                    const row = document.createElement("tr");

                    const userNameCell = document.createElement("td");
                    userNameCell.textContent = bet.nickname;
                    row.appendChild(userNameCell);

                    const betAmountCell = document.createElement("td");
                    betAmountCell.textContent = bet.bet_cost + ' ₽';
                    row.appendChild(betAmountCell);

                    const betTimeCell = document.createElement("td");
                    console.log(bet.created_at);
                    betTimeCell.textContent = new Date(bet.created_at + "+00:00").toLocaleString();

                    row.appendChild(betTimeCell);

                    bidTable.appendChild(row);
                });
            } else {
                // Если ставок нет, показываем сообщение
                const noBetsRow = document.createElement("tr");
                const noBetsCell = document.createElement("td");
                noBetsCell.colSpan = 3; // Чтобы объединить ячейки в строке
                noBetsCell.textContent = "Ставок пока нет";
                noBetsRow.appendChild(noBetsCell);
                bidTable.appendChild(noBetsRow);
            }
        })
        .catch(error => {
            console.error("Ошибка при загрузке данных:", error);
        });
}


// Функция для отправки ставки
document.getElementById("place-bid").addEventListener("click", function() {
    const bidInput = document.querySelector(".bid-input");
    const bidAmount = bidInput.value;
    if (bidAmount < 1) {
        customAlert("Ставка должна быть больше 0.");
        return;
    }

    const auctionId = new URLSearchParams(window.location.search).get("a_id");
    fetch(`/mongo/auction/add_bet_to_auction?a_id=${auctionId}&bet_cost=${bidAmount}`, {
        method: 'POST',
        headers: {
            'accept': 'application/json',
            'content-type': 'application/x-www-form-urlencoded'
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        if(data["detail"]=="Invalid credentials"){
            customAlert("Сначала авторизируйтесь");
            return;
        }
        if (data["status"]!='error') {
            customAlert("Ставка успешно сделана!");
            loadAuctionDetails(auctionId); // Обновляем данные аукциона
        } else {
            customAlert("Ошибка при размещении ставки. "+ data["message"]);
        }
    })
    .catch(error => {
        console.error("Ошибка при размещении ставки:", error);
    });
});

// Функция для выхода из аккаунта
function logout() {
    localStorage.removeItem("authToken");
    customAlert("Вы вышли из аккаунта");
    window.location.href = "login";
}

document.addEventListener("DOMContentLoaded", function () {
    const zoomContainer = document.querySelector(".zoom-container");
    const coinImage = document.querySelector("#coin-image");
    const zoomLens = document.createElement("div");
    const zoomedImage = document.createElement("img");

    zoomLens.className = "zoom-lens";
    zoomContainer.appendChild(zoomLens);

    zoomedImage.className = "zoom-image";
    zoomContainer.appendChild(zoomedImage);

    // Обработчик события наведения мыши
    zoomContainer.addEventListener("mousemove", (e) => {
        const { left, top, width, height } = zoomContainer.getBoundingClientRect();

        // Вычисляем координаты курсора относительно контейнера
        const lensX = e.clientX - left;
        const lensY = e.clientY - top;

        // Установка позиции лупы
        zoomLens.style.left = `${lensX - zoomLens.offsetWidth / 2}px`; // Центрирование лупы по курсору
        zoomLens.style.top = `${lensY - zoomLens.offsetHeight / 2}px`; // Центрирование лупы по курсору

        // Установка позиции увеличенного изображения
        zoomedImage.src = coinImage.src; // Ссылка на исходное изображение
        zoomedImage.style.display = "block"; // Показываем увеличенное изображение
        // Центрируем увеличенное изображение относительно курсора
        zoomedImage.style.left = `${lensX}px`;
        zoomedImage.style.top = `${lensY}px`;
        zoomedImage.style.transform = `translate(-${lensX * 2}px, -${lensY * 2}px)`; // Увеличиваем изображение с учетом положения курсора
    });

    // Обработчик события покидания мыши
    zoomContainer.addEventListener("mouseleave", () => {
        zoomedImage.style.display = "none"; // Скрываем увеличенное изображение при выходе
        zoomLens.style.display = "none"; // Скрываем лупу
    });

    // Обработчик события наведения на изображение
    coinImage.addEventListener("load", () => {
        zoomLens.style.display = "block"; // Показываем лупу при загрузке изображения
    });
});

// Функция для загрузки и обновления данных ставок
function loadAndUpdateBets(auctionId) {
    fetch(`/mongo/auction/get_bets?a_id=${auctionId}`)
        .then(response => response.json())
        .then(data => {
            console.log(data);

            // Заполняем таблицу ставок
            const bidTable = document.querySelector("#bid-table tbody");
            bidTable.innerHTML = ""; // Очищаем предыдущие данные

            if (data && data.length > 0) {
                data.slice().reverse().forEach(bet => {
                    const row = document.createElement("tr");

                    const userNameCell = document.createElement("td");
                    userNameCell.textContent = bet.nickname;
                    row.appendChild(userNameCell);

                    const betAmountCell = document.createElement("td");
                    betAmountCell.textContent = bet.bet_cost + ' ₽';
                    row.appendChild(betAmountCell);

                    const betTimeCell = document.createElement("td");
                    betTimeCell.textContent = new Date(bet.created_at+"+00:00").toLocaleString();
                    row.appendChild(betTimeCell);

                    bidTable.appendChild(row);
                });
            } else {
                // Если ставок нет, показываем сообщение
                const noBetsRow = document.createElement("tr");
                const noBetsCell = document.createElement("td");
                noBetsCell.colSpan = 3; // Чтобы объединить ячейки в строке
                noBetsCell.textContent = "Ставок пока нет";
                noBetsRow.appendChild(noBetsCell);
                bidTable.appendChild(noBetsRow);
            }
        })
        .catch(error => {
            console.error("Ошибка при загрузке данных:", error);
        });
}


// Загружаем данные аукциона при загрузке страницы
document.addEventListener("DOMContentLoaded", function () {
    const urlParams = new URLSearchParams(window.location.search);
    const auctionId = urlParams.get("a_id");
    if (auctionId) {
        loadAuctionDetails(auctionId); // Загружаем данные аукциона
    } else {
        customAlert("ID аукциона не найден. Перейдите на страницу с аукционами.");
        window.location.href = "/";
    }
     // Вызываем функцию для обновления ставок каждую секунду
    setInterval(() => {
        loadAndUpdateBets(auctionId); // Обновляем таблицу ставок
    }, 2000); // Каждую 2 секунды


});

