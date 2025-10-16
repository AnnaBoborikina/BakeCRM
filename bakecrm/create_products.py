import os
import sys
import django
from django.core.files.base import ContentFile
import requests

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bakecrm.settings')
django.setup()

from bakery.models import Product

# Данные товаров
PRODUCTS = [
    {"name": "Багет", "description": "Хрустящая французская булка с воздушной сердцевиной", "price": 120, "category": "bread"},
    {"name": "Круассан", "description": "Слоёный, маслянистый круассан ручной работы", "price": 85, "category": "pastry"},
    {"name": "Чизкейк Нью-Йорк", "description": "Классический чизкейк с нежной текстурой и ягодным соусом", "price": 280, "category": "cake"},
    {"name": "Капкейк Ванильный", "description": "Воздушный капкейк с ванильной начинкой и кремом", "price": 95, "category": "cupcake"},
    {"name": "Капкейк Шоколадный", "description": "Богатый шоколадный капкейк с глазурью", "price": 100, "category": "cupcake"},
    {"name": "Булочка с маком", "description": "Сдобная булочка с маком и сахарной посыпкой", "price": 70, "category": "bun"},
    {"name": "Пирожок с яблоком", "description": "Домашний пирожок с корицей и яблочной начинкой", "price": 65, "category": "pie"},
    {"name": "Пирожок с вишней", "description": "Сочный пирожок с вишневой начинкой", "price": 65, "category": "pie"},
    {"name": "Пирожок с капустой", "description": "Традиционный пирожок с тушёной капустой", "price": 60, "category": "pie"},
    {"name": "Пирожок с картошкой", "description": "Сытный пирожок с картофельным пюре и зеленью", "price": 60, "category": "pie"},
    {"name": "Булочка с изюмом", "description": "Сладкая булочка с изюмом и корицей", "price": 75, "category": "bun"},
    {"name": "Булочка с корицей", "description": "Ароматная булочка с коричной начинкой", "price": 80, "category": "bun"},
    {"name": "Медовик", "description": "Слоёный медовик с нежным сметанным кремом", "price": 260, "category": "cake"},
    {"name": "Наполеон", "description": "Хрустящие коржи с заварным кремом", "price": 240, "category": "cake"},
    {"name": "Эклер", "description": "Воздушное заварное пирожное с шоколадным кремом", "price": 90, "category": "pastry"},
    {"name": "Профитроли", "description": "Мини-эклеры с ванильным кремом (3 шт.)", "price": 150, "category": "pastry"},
    {"name": "Пончик классический", "description": "Пышный пончик с сахарной пудрой", "price": 65, "category": "donut"},
    {"name": "Пончик с глазурью", "description": "Пончик с шоколадной глазурью", "price": 70, "category": "donut"},
    {"name": "Брауни", "description": "Плотный шоколадный брауни с грецкими орехами", "price": 110, "category": "brownie"},
    {"name": "Маффин Шоколадный", "description": "Влажный маффин с кусочками шоколада", "price": 85, "category": "muffin"},
    {"name": "Маффин Банановый", "description": "Маффин с бананом и грецкими орехами", "price": 85, "category": "muffin"},
    {"name": "Маффин Морковный", "description": "Полезный маффин с морковью и специями", "price": 85, "category": "muffin"},
    {"name": "Печенье Овсяное", "description": "Хрустящее овсяное печенье с изюмом", "price": 50, "category": "cookie"},
    {"name": "Печенье Шоколадное", "description": "Мягкое печенье с кусочками тёмного шоколада", "price": 55, "category": "cookie"},
    {"name": "Пряник", "description": "Домашний пряник с мёдом и специями", "price": 60, "category": "gingerbread"},
    {"name": "Бублик классический", "description": "Отварной и запечённый бублик", "price": 45, "category": "bagel"},
    {"name": "Бублик с маком", "description": "Бублик с маковой посыпкой", "price": 50, "category": "bagel"},
    {"name": "Бублик с кунжутом", "description": "Бублик с кунжутной посыпкой", "price": 50, "category": "bagel"},
    {"name": "Лепёшка чесночная", "description": "Свежая лепёшка с чесноком и зеленью", "price": 90, "category": "flatbread"},
    {"name": "Фокачча", "description": "Итальянский хлеб с оливковым маслом и травами", "price": 140, "category": "bread"},
    {"name": "Ржаной хлеб", "description": "Плотный ржаной хлеб на закваске", "price": 130, "category": "bread"},
    {"name": "Бородинский хлеб", "description": "Традиционный русский хлеб с тмином", "price": 120, "category": "bread"},
    {"name": "Пшеничный хлеб", "description": "Мягкий пшеничный хлеб из муки высшего сорта", "price": 100, "category": "bread"},
    {"name": "Булочка для бургера", "description": "Свежая булочка с кунжутом", "price": 55, "category": "bun"},
    {"name": "Булочка для хот-дога", "description": "Длинная булочка для хот-дога", "price": 50, "category": "bun"},
    {"name": "Торт «Сникерс»", "description": "Торт с арахисом, карамелью и шоколадом", "price": 290, "category": "cake"},
    {"name": "Торт «Птичье молоко»", "description": "Нежный торт с зефирным слоем и шоколадной глазурью", "price": 270, "category": "cake"},
    {"name": "Тирамису", "description": "Итальянский десерт с кофе и маскарпоне", "price": 300, "category": "cake"},
    {"name": "Пирожное Картошка", "description": "Советское пирожное из крошек и какао", "price": 75, "category": "pastry"},
    {"name": "Ватрушка", "description": "Творожная ватрушка с изюмом", "price": 70, "category": "pastry"},
    {"name": "Слойка с творогом", "description": "Слоёное тесто с нежной творожной начинкой", "price": 85, "category": "pastry"},
    {"name": "Слойка с яблоком", "description": "Слоёное тесто с яблочной начинкой и корицей", "price": 80, "category": "pastry"},
    {"name": "Пирог с яблоками", "description": "Домашний яблочный пирог", "price": 220, "category": "pie"},
    {"name": "Пирог с творогом", "description": "Нежный творожный пирог", "price": 230, "category": "pie"},
    {"name": "Круассан с шоколадом", "description": "Круассан с вкладкой из тёмного шоколада", "price": 95, "category": "pastry"},
    {"name": "Круассан с миндалем", "description": "Круассан с миндальной посыпкой", "price": 100, "category": "pastry"},
    {"name": "Булочка «Хала»", "description": "Еврейская праздничная булочка", "price": 110, "category": "bun"},
    {"name": "Пицца-хлеб", "description": "Хрустящий хлеб с томатами и сыром", "price": 160, "category": "bread"},
    {"name": "Багет с сыром", "description": "Багет с начинкой из плавленого сыра", "price": 150, "category": "bread"},
    {"name": "Мини-багеты (3 шт.)", "description": "Удобные мини-багеты для перекуса", "price": 180, "category": "bread"},
]

def download_image(url, name):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return ContentFile(response.content, name=f"{name.replace(' ', '_')}.jpg")
    except Exception as e:
        print(f"Ошибка загрузки изображения для {name}: {e}")
    return None

def create_products():
    # Product.objects.all().delete()  # Опционально: очистить перед добавлением
    print("Добавление 50 товаров...")
    
    for i, item in enumerate(PRODUCTS, 1):
        # Генерация URL изображения
        category_map = {
            "bread": "bread,crusty",
            "pastry": "pastry",
            "cake": "cake",
            "cupcake": "cupcake",
            "bun": "bun",
            "pie": "pie",
            "donut": "donut",
            "brownie": "brownie",
            "muffin": "muffin",
            "cookie": "cookie",
            "gingerbread": "gingerbread",
            "bagel": "bagel",
            "flatbread": "flatbread"
        }
        query = category_map.get(item["category"], "food")
        image_url = f"https://source.unsplash.com/300x300/?{query}"
        
        product = Product(
            name=item["name"],
            description=item["description"],
            price=item["price"]
        )
        
        # Загружаем и сохраняем изображение
        image = download_image(image_url, item["name"])
        if image:
            product.image.save(image.name, image, save=False)
        
        product.save()
        print(f"{i}/50: {item['name']}")

if __name__ == "__main__":
    create_products()
    print("✅ Все товары добавлены!")