# Импорт модулей (разрешено на ПР1)
from datetime import datetime

# ==========================================
# ФУНКЦИИ (не менее 3-х по заданию)
# ==========================================

# Функция 1: Проверка и публикация новости
def publish_news(title: str, text: str, author: str) -> str:
    if len(title) == 0:
        return "Ошибка: Заголовок не может быть пустым. Публикация отменена."
    if len(text) == 0:
        return "Ошибка: Текст новости не может быть пустым. Публикация отменена."
    if len(author) == 0:
        return "Ошибка: Не указан автор. Публикация отменена."
    return f"Новость успешно опубликована автором {author}."

# Функция 2: Назначение категории
def assign_category(category: str) -> str:
    allowed_categories = "Технологии, Спорт, Политика, Культура"
    if category in allowed_categories:
        return category
    return "Разное"

# Функция 3: Добавление комментария
def add_comment(comment_text: str, commenter_name: str) -> str:
    if len(comment_text) == 0:
        return "Комментариев пока нет."
    if len(commenter_name) == 0:
        return f"Аноним: {comment_text}"
    return f"{commenter_name}: {comment_text}"

# Функция 4: Оценка популярности новости
def rate_popularity(views: int) -> str:
    if views >= 1000:
        return "ВИРУСНАЯ (очень популярная)"
    elif views >= 100:
        return "ПОПУЛЯРНАЯ"
    else:
        return "НОВАЯ (мало просмотров)"

# Функция 5: Полный вывод новости (как в новостной ленте)
def display_full_news(title, author, category, text, views, popularity, comment, pub_date):
    print("                НОВОСТНАЯ ЛЕНТА")
    print(f"ЗАГОЛОВОК : {title}")
    print(f"АВТОР     : {author}")
    print(f"КАТЕГОРИЯ : {category}")
    print(f"ДАТА      : {pub_date}")
    print(f"ПРОСМОТРЫ : {views} ({popularity})")
    print("ТЕКСТ НОВОСТИ:")
    print(text)
    print("КОММЕНТАРИЙ:")
    print(comment)


print("       СИСТЕМА ПУБЛИКАЦИИ НОВОСТЕЙ")

title = input("Введите заголовок новости: ")
text = input("Введите текст новости: ")
author = input("Введите имя автора: ")
category = input("Введите категорию (Технологии/Спорт/Политика/Культура): ")

views_str = input("Введите количество просмотров (только цифры): ")
views = int(views_str)   # преобразование типов

comment_text = input("Введите текст комментария: ")
commenter_name = input("Введите имя комментатора: ")

status_publish = publish_news(title, text, author)
final_category = assign_category(category)
final_comment = add_comment(comment_text, commenter_name)
popularity = rate_popularity(views)
pub_date = datetime.now().strftime('%d.%m.%Y %H:%M')

print("\n" + status_publish)

if "Ошибка" not in status_publish:
    display_full_news(
        title,
        author,
        final_category,
        text,
        views,
        popularity,
        final_comment,
        pub_date
    )
else:
    print("Новость не была опубликована из-за ошибки ввода.")