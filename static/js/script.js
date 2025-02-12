const maxPhotos = 5;
let photoCount = 0;
let photoFiles = []; // Массив для хранения загруженных изображений
let adBanner1File = null;
let adBanner2File = null;

// Обработчик для загрузки первого рекламного баннера
document.getElementById('adBanner1').addEventListener('change', function(event) {
    const file = event.target.files[0];
    const reader = new FileReader();
    reader.onload = function(e) {
        adBanner1File = e.target.result; // Сохраняем изображение в переменной
    };
    reader.readAsDataURL(file);
});

// Обработчик для загрузки второго рекламного баннера
document.getElementById('adBanner2').addEventListener('change', function(event) {
    const file = event.target.files[0];
    const reader = new FileReader();
    reader.onload = function(e) {
        adBanner2File = e.target.result; // Сохраняем изображение в переменной
    };
    reader.readAsDataURL(file);
});
document.getElementById('addPhotoButton').addEventListener('click', function() {
    if (photoCount < maxPhotos) {
        document.getElementById('photoInput').click();
    } else {
        alert('Вы можете добавить не более 5 фотографий.');
    }
});

document.getElementById('photoInput').addEventListener('change', function(event) {
    const files = event.target.files;
    for (let i = 0; i < files.length; i++) {
        if (photoCount < maxPhotos) {
            const file = files[i];
            const reader = new FileReader();
            reader.onload = function(e) {
                const photoItem = document.createElement('div');
                photoItem.className = 'photo-item';
                photoItem.innerHTML = `
                    <img src="${e.target.result}" style="width: 100px; margin: 5px;">
                    <span class="delete-photo">×</span>
                `;
                document.getElementById('photoList').appendChild(photoItem);

                // Добавляем обработчик для удаления фотографии
                photoItem.querySelector('.delete-photo').addEventListener('click', function() {
                    photoItem.remove();
                    photoCount--;
                    photoFiles = photoFiles.filter((photo, index) => index !== photoFiles.indexOf(e.target.result));
                });

                photoFiles.push(e.target.result); // Сохраняем изображение в массив
                photoCount++;
            };
            reader.readAsDataURL(file);
        }
    }
});

document.getElementById('createNewsButton').addEventListener('click', function() {
    const editSiteModal = document.getElementById('editSiteModal');
    editSiteModal.style.display = 'block';
});

document.querySelectorAll('.close').forEach(closeButton => {
    closeButton.addEventListener('click', function() {
        const modal = this.closest('.modal');
        modal.style.display = 'none';
    });
});



document.getElementById('generateRandomNews').addEventListener('click', function() {
    const currentDate = new Date().toLocaleDateString('ru-RU'); // Получаем текущую дату в формате "дд.мм.гггг"
    
    const randomNews = [
        `Курс рубля на ${currentDate}`,
        `Краткая сводка новостей на ${currentDate}`,
        `Почему не стоит верить всему в интернете`
    ];

    document.getElementById('relatedNews1').value = randomNews[0];
    document.getElementById('relatedNews2').value = randomNews[1];
    document.getElementById('relatedNews3').value = randomNews[2];
});

document.getElementById('saveSiteSettings').addEventListener('click', function() {
    const editSiteModal = document.getElementById('editSiteModal');
    editSiteModal.style.display = 'none';

    const downloadModal = document.getElementById('downloadModal');
    downloadModal.style.display = 'block';
});

// Обновленная функция для скачивания HTML
document.getElementById('downloadHTML').addEventListener('click', function() {
    const title = document.getElementById('title').value;
    const description = document.getElementById('description').value;
    const journalist = document.getElementById('journalist').value;

    const siteName = document.getElementById('siteName').value || "Новостной портал";
    const articleDate = document.getElementById('articleDate').value || new Date().toLocaleDateString('ru-RU');
    const relatedNews1 = document.getElementById('relatedNews1').value || "Новость 1: Что-то интересное";
    const relatedNews2 = document.getElementById('relatedNews2').value || "Новость 2: Еще что-то важное";
    const relatedNews3 = document.getElementById('relatedNews3').value || "Новость 3: Срочные новости";

    // Собираем данные для отправки на сервер
    const data = {
        title: title,
        description: description,
        journalist: journalist,
        siteName: siteName,
        articleDate: articleDate,
        relatedNews1: relatedNews1,
        relatedNews2: relatedNews2,
        relatedNews3: relatedNews3,
        adBanner1: adBanner1File || 'https://via.placeholder.com/728x90',
        adBanner2: adBanner2File || 'https://via.placeholder.com/728x90',
        photos: photoFiles
    };

    // Отправляем данные на сервер
    fetch('/generate_news', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        const blob = new Blob([result.html], { type: 'text/html' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'news.html';
        a.click();
        URL.revokeObjectURL(url);
    })
    .catch(error => {
        console.error("Ошибка при генерации HTML:", error);
    });
});