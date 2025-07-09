import random
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler

subjects = {
    "Придмети": ["Яйце", "Книга", "Компьютер", "Літак", "Автобус", "Гарбуз", "Диня", "Стул", "Хліб"],
    "Тварини": ["Кіт", "Собака", "Тигр", "Морский кінь", "Хом'ячок", "Морска свинка", "Кальмар", "Осменіг"],
    "Природа": ["Квітка", "Дерево", "Яблуня", "Камень", "Море", "Фрукти"],
    "Магічні створіння": ["Ангел", "Морське восьминоге чудовисько", "Людина-Солнце", "Черткик", "Ельф", "Дворф", "Вампир"]

}
Type = {
    "Придмети": ["потрісканний(а)", "намоченний(а)", "працюючий(а)", "здивованний(а)", "роздратованний(а)"],
    "Тварини": ["милий(а)", "здивованний(а)", "роздратованний(а)", "страашний(а)", "печальний(а)", "травмированний(а)"],
    "Природа": ["живий(а)", "ходящий(а)", "магічний(а)", "злий(а)", "красний(а)", "маринованний(а)"],
    "Магічні створіння": ["литающий(а)", "малюючий(а)", "злий(а)", "страшний(а)", "милий(а)", "працюючий(а)"]
}
Place = {
    "Місця": [
        "в воді", "на пляжі", "в морі", "на дереві", "під стілом", "в повітрі", "на люстрі", "в гаражі",
        "в дома", "в літаку", "в оффисі", "на роботі", "на полці", "на столі", "під вентилятором", "на стулі",
        "в ліфті", "в телефоні", "на балконі", "біля котика", "біля курятника", "біля мясної лавки"
        ]
}

difficulty = {
    "Легкий": "легко",
    "Середній": "середньо",
    "Складний": "складно"
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_message = (
        "Привіт! Я бот для челенджу по типу 3 слова \n"
        "Я даю тобі 3 слова з яких ти мусиш зробити картинку \n"
        "команди які ти можеш використовувати: \n"
        "/help - показує список команд \n"
        "/make_idea - даю 3 слова \n"
        "/difficalty - рівень складності \n"
        "/categories - показує які є категорії"
        )
    await update.message.reply_text(start_message)

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_message = (
        "В мене є такі команди: \n"
        "/help - показує список команд \n"
        "/make_idea - даю 3 слова \n"
        "/difficalty - рівень складності \n"
        "/categories - показує які є категорії"
    )
    await update.message.reply_text(help_message)

async def make_idea_message(category=None, difficulty=None):
    if category and category in subjects:
        subject = random.choice(subjects[category])

    else:
        subject = random.choice([item for sublist in subjects.values() for item in sublist])
    
    Type = random.choice([item for sublist in Type.values() for item in sublist])
    Place = random.choice([item for sublist in Place.values() for item in sublist])

    difficulty_text = f" ({difficulty[difficulty]})" if difficulty else ""

    return f"твої 3 слова: {subject} {Type} {Place} {difficulty_text}"

async def categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(category, callback_data= f"category_{category}")]
        for category in subjects.keys() and category in Type.keys():
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Оберіть категорію", reply_markup=reply_markup)

async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data.split("_")
    if data[0] == "category":
        context.user_data["category"] = data[1]
        await query.message.reply_text(f"Обрана категорія: {data[1]} \n Використайте команду /make_idea ")
    elif data[0] == "difficulty":
        context.user_data["difficulty"] = data[1]
        await query.message.reply_text(f"Обраний рівень складності: {data[1]} \n Використайте команду /make_idea ")

async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    category = context.user_data.get("category")
    difficulty = context.user_data.get("difficulty")
    art_idea = make_idea_message(category, difficulty)
    await update.message.reply_text(art_idea)