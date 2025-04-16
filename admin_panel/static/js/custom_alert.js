function customAlert(message, options = {}) {
    // Создаём затемнённый фон и контейнер
    const overlay = document.createElement("div");
    overlay.classList.add("alert-overlay");

    const alertBox = document.createElement("div");
    alertBox.classList.add("alert-box");

    // Настраиваем заголовок и текст сообщения
    const alertMessage = document.createElement("p");
    alertMessage.classList.add("alert-message");
    alertMessage.innerText = message;

    // Создаем кнопку закрытия
    const closeButton = document.createElement("button");
    closeButton.classList.add("alert-button");
    closeButton.innerText = "OK";

    // Добавляем элементы в контейнер
    alertBox.appendChild(alertMessage);
    alertBox.appendChild(closeButton);
    overlay.appendChild(alertBox);
    document.body.appendChild(overlay);

    // Закрытие при нажатии на кнопку, вне окна или клавишу Esc
    closeButton.onclick = closeAlert;
    overlay.onclick = (e) => {
        if (e.target === overlay) closeAlert();
    };

    function closeAlert() {
        overlay.classList.add("alert-overlay-hide");
        alertBox.classList.add("alert-box-hide");

        // Удаляем обработчик событий после закрытия
        document.removeEventListener("keydown", handleKeyDown);

        setTimeout(() => {
            document.body.removeChild(overlay);
        }, 300);
    }

    function handleKeyDown(event) {
        if (event.key === "Escape") {
            closeAlert();
        }
    }

    // Добавляем обработчик для клавиши Esc
    document.addEventListener("keydown", handleKeyDown);
}
