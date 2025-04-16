async function fetchAuctionData() {
    try {
        const response = await fetch('/mongo/auction/get_all', {
            method: 'GET',
            headers: {
                'Accept': 'application/json'
            }
        });

        if (!response.ok) {
            customAlert('Network response was not ok ' + response.statusText);
            throw new Error('Network response was not ok ' + response.statusText);
        }

        const data = await response.json();
        displayAuctionData(data);
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
        customAlert(error);
    }
}

function displayAuctionData(data) {
    const activeAuctionGrid = document.getElementById('activeAuctions');
    const upcomingAuctionGrid = document.getElementById('upcomingAuctions');
    const completedAuctionGrid = document.getElementById('completedAuctions');

    activeAuctionGrid.innerHTML = ''; // Очистить существующие данные активных аукционов
    upcomingAuctionGrid.innerHTML = ''; // Очистить существующие данные предстоящих аукционов
    completedAuctionGrid.innerHTML = ''; // Очистить существующие данные завершенных аукционов
    document.getElementById('active-header').style.display="none";
    document.getElementById('upcoming-header').style.display="none";
    document.getElementById('finished-header').style.display="none";
    const now = new Date();

    data.forEach(auction => {
        const startTime = new Date(auction.start_datetime);
        const endTime = new Date(auction.end_datetime);
        
        const auctionCard = document.createElement('div');
        auctionCard.className = 'auction-card';
        auctionCard.innerHTML = `
            <div class="card-list">
                <article class="card">
                    <figure class="card-image">
                        <img src='data:image/jpeg;base64,${auction.photo}' />
                    </figure>
                    <div class="card-header">
                        <a href="#">${auction.short_name}</a>
                    </div>
                    <div class="card-footer">
                        <span><strong>От ${auction["start_price"]} ₽</strong></span>
                    </div>
                    <div class="card-meta card-meta--date">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <rect x="2" y="4" width="20" height="18" rx="4" />
                            <path d="M8 2v4" />
                            <path d="M16 2v4" />
                            <path d="M2 10h20" />
                        </svg>
                        ${new Date(auction.start_datetime).toLocaleString()}
                    </div>
                </article>
            </div>
        `;

        // Добавить событие клика на карточку
        auctionCard.addEventListener('click', () => {
            const auctionId = auction.a_id.a_id || auction.a_id; // Получить ID аукциона
            window.open(`alt_auction?a_id=${auctionId}`, '_self');
        });

        // Определяем, в какую секцию добавлять аукцион
        if (startTime <= now && now <= endTime) {
            // Активные аукционы
            activeAuctionGrid.appendChild(auctionCard);
            document.getElementById('active-header').style.display="none";
        } else if (startTime > now) {
            // Предстоящие аукционы
            upcomingAuctionGrid.appendChild(auctionCard);
            document.getElementById('upcoming-header').style.display="block";
        } else {
            // Завершенные аукционы
            completedAuctionGrid.appendChild(auctionCard);
            document.getElementById('finished-header').style.display="block";
        }
    });

    
    document.getElementById("loadingScreen").style.display = "none";
}


// Fetch auction data when the page loads
window.onload = fetchAuctionData;
