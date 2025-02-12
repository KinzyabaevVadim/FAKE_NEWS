from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # Отправляем index.html при запросе к корню

@app.route('/generate_news', methods=['POST'])
def generate_news():
    try:
        data = request.json  # Получаем данные из запроса
        title = data.get('title')
        description = data.get('description')
        journalist = data.get('journalist')
        site_name = data.get('siteName', "Новостной портал")
        article_date = data.get('articleDate', "Сегодня")
        related_news = [
            data.get('relatedNews1', "Новость 1: Что-то интересное"),
            data.get('relatedNews2', "Новость 2: Еще что-то важное"),
            data.get('relatedNews3', "Новость 3: Срочные новости")
        ]
        ad_banner1 = data.get('adBanner1', 'https://via.placeholder.com/728x90')
        ad_banner2 = data.get('adBanner2', 'https://via.placeholder.com/728x90')
        photos = data.get('photos', [])

        # Генерация HTML-кода для новостей
        news_html = f"""
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title} | {site_name}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #f9f9f9;
                    color: #333;
                }}
                .header {{
                    background-color: #333;
                    color: #fff;
                    padding: 10px 20px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }}
                .header .logo {{
                    font-size: 24px;
                    font-weight: bold;
                }}
                .header nav a {{
                    color: #fff;
                    text-decoration: none;
                    margin-left: 20px;
                    font-size: 16px;
                }}
                .header nav a:hover {{
                    text-decoration: underline;
                }}
                .news-container {{
                    max-width: 1200px;
                    margin: 20px auto;
                    padding: 20px;
                    background-color: #fff;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }}
                h1 {{
                    font-size: 2.5em;
                    margin-bottom: 20px;
                    color: #222;
                }}
                .news-meta {{
                    font-size: 0.9em;
                    color: #777;
                    margin-bottom: 20px;
                }}
                .news-content {{
                    font-size: 1.1em;
                    line-height: 1.6;
                    margin-bottom: 30px;
                    white-space: pre-wrap; /* Сохраняет пробелы и переносы строк */
                }}
                .news-photos {{
                    position: relative;
                    margin-bottom: 30px;
                }}
                .news-photos img {{
                    width: 600px; /* Установите фиксированную ширину для фотографий */
                    height: auto; /* Автоматическая высота для сохранения пропорций */
                    border-radius: 8px;
                    box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
                }}
                .navigation-buttons {{
                    display: flex;
                    justify-content: space-between;
                    margin-top: 10px;
                }}
                .navigation-buttons button {{
                    padding: 10px 15px;
                    font-size: 16px;
                    cursor: pointer;
                }}
                .journalist {{
                    font-style: italic;
                    color: #555;
                    margin-top: 20px;
                }}
                .related-news {{
                    margin-top: 40px;
                    padding: 20px;
                    background-color: #f1f1f1;
                    border-radius: 8px;
                }}
                .related-news h2 {{
                    font-size: 1.5em;
                    margin-bottom: 15px;
                }}
                .related-news ul {{
                    list-style: none;
                    padding: 0;
                }}
                .related-news ul li {{
                    margin-bottom: 10px;
                }}
                .related-news ul li a {{
                    color: #007BFF;
                    text-decoration: none;
                }}
                .related-news ul li a:hover {{
                    text-decoration: underline;
                }}
                .footer {{
                    background-color: #333;
                    color: #fff;
                    padding: 20px;
                    text-align: center;
                    margin-top: 40px;
                }}
                .footer a {{
                    color: #fff;
                    text-decoration: none;
                    margin: 0 10px;
                }}
                .footer a:hover {{
                    text-decoration: underline;
                }}
                .ad-banner {{
                    margin: 10px 0;
                    text-align: center;
                    background-color: #f1f1f1;
                    padding: 5px;
                    border-radius: 8px;
                }}
                .ad-banner img {{
                    max-width: 100%;
                    height: auto;
                    max-height: 100px;
                }}
            </style>
        </head>
        <body>
            <header class="header">
                <div class="logo">{site_name}</div>
                <nav>
                    <a href="#">Главная</a>
                    <a href="#">Политика</a>
                    <a href="#">Экономика</a>
                    <a href="#">Спорт</a>
                </nav>
            </header>
        
            <div class="news-container">
                <h1>{title}</h1>
                <div class="news-meta">
                    Опубликовано: {article_date} | Автор: {journalist}
                </div>
        
                <div class="ad-banner">
                    <img src="{ad_banner1}" alt="Реклама">
                </div>
        
                <div class="news-content">
                    {description}
                </div>
        
                <div class="news-photos">
                    <img id="currentPhoto" src="{photos[0]}" alt="Фото">
                    <div class="navigation-buttons">
                        <button id="prevButton" onclick="changePhoto(-1)">&#60; Предыдущее</button>
                        <button id="nextButton" onclick="changePhoto(1)">Следующее &#62;</button>
                    </div>
                </div>
        
                <div class="ad-banner">
                    <img src="{ad_banner2}" alt="Реклама">
                </div>
        
                <div class="related-news">
                    <h2>Читайте также:</h2>
                    <ul>
                        <li><a href="#">{related_news[0]}</a></li>
                        <li><a href="#">{related_news[1]}</a></li>
                        <li><a href="#">{related_news[2]}</a></li>
                    </ul>
                </div>
            </div>
        
            <footer class="footer">
                <p>&copy; {site_name}. Все права защищены.</p>
                <a href="#">Политика конфиденциальности</a>
                <a href="#">Контакты</a>
            </footer>
        
            <script>
                const photos = {json.dumps(photos)};
                let currentIndex = 0;
        
                function changePhoto(direction) {{
                    currentIndex += direction;
                    if (currentIndex < 0) {{
                        currentIndex = photos.length - 1; // Перейти к последнему фото
                    }} else if (currentIndex >= photos.length) {{
                        currentIndex = 0; // Перейти к первому фото
                    }}
                    document.getElementById('currentPhoto').src = photos[currentIndex];
                }}
            </script>
        </body>
        </html>
        """

        return jsonify({'html': news_html})

    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Возвращаем ошибку в формате JSON

if __name__ == '__main__':
    app.run(debug=True)