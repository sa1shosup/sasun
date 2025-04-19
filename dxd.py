import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Конфигурация
TOKEN = "7942282080:AAGYeFmFyLtibd4AB1rcLxMDqhNoq22_T4s"  # Замените на реальный токен
FONT_PATH = "arial.ttf"  # Путь к шрифту (можно использовать стандартный)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправляем инструкцию по использованию"""
    instructions = """
    Отправьте данные для выписки в следующем формате:
    
    1. Номер бронирования (например: АЗ34ВЕСF0368C)
    2. Пункт пропуска (например: Нур Жолы - Хоргос)
    3. Дата (например: 04.03.2025)
    4. Временной интервал (например: 21:00-22:00)
    5. Номер транспорта (например: ABC123)
    6. Номер прицепа (или 'нет')
    7. Страна регистрации (например: Казахстан)
    """
    await update.message.reply_text(instructions)

async def generate_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Разбираем ввод пользователя
        lines = [line.strip() for line in update.message.text.split('\n') if line.strip()]
        if len(lines) < 7:
            await update.message.reply_text("Ошибка: нужно ровно 7 строк данных!")
            return

        booking_num, checkpoint, date, time_range, vehicle, trailer, country = lines[:7]
        
        # Создаем изображение
        img = Image.new('RGB', (800, 1200), color='white')
        draw = ImageDraw.Draw(img)
        
        # Загружаем шрифты
        try:
            font_large_bold = ImageFont.truetype(FONT_PATH, 24)
            font_medium_bold = ImageFont.truetype(FONT_PATH, 20)
            font_regular = ImageFont.truetype(FONT_PATH, 18)
            font_bold = ImageFont.truetype(FONT_PATH, 18)
        except:
            # Fallback на стандартные шрифты
            font_large_bold = ImageFont.load_default(size=24)
            font_medium_bold = ImageFont.load_default(size=20)
            font_regular = ImageFont.load_default(size=18)
            font_bold = ImageFont.load_default(size=18)

        y_position = 50  # Стартовая позиция по вертикали

        # Заголовок
        draw.text((50, y_position), "1 of 1", fill="black", font=font_large_bold)
        y_position += 40

        # Основной заголовок
        draw.text((50, y_position), "ВЫПИСКА ИЗ СИСТЕМЫ ЭЛЕКТРОННОЙ ОЧЕРЕДИ", fill="black", font=font_medium_bold)
        y_position += 40

        # Дата и время
        print_time = datetime.now().strftime("%d.%m.%Y %H:%M")
        draw.text((50, y_position), f"Дата и время распечатки: {print_time}", fill="black", font=font_regular)
        y_position += 60

        # Секция бронирования
        draw.text((50, y_position), "БРОНИРОВАНИЕ", fill="black", font=font_medium_bold)
        y_position += 30
        for item in ["- Статус", "- № бронирования", "- Пункт пропуска", 
                    "- Дата", "- Ориентировочное время", "- Тип очереди"]:
            draw.text((70, y_position), item, fill="black", font=font_regular)
            y_position += 25
        y_position += 15

        # Разделительная линия
        draw.line([(50, y_position), (750, y_position)], fill="black", width=2)
        y_position += 20

        # Данные бронирования
        for text in [booking_num, checkpoint, date, time_range]:
            draw.text((50, y_position), text, fill="black", font=font_bold)
            y_position += 30
        y_position += 20

        # Разделительная линия
        draw.line([(50, y_position), (750, y_position)], fill="black", width=2)
        y_position += 20

        # Транспорт
        draw.text((50, y_position), "ТРАНСПОРТ", fill="black", font=font_medium_bold)
        y_position += 30
        for item in ["- Номерной знак транспорта", "- Номерной знак прицепа", 
                    "- Страна регистрации"]:
            draw.text((70, y_position), item, fill="black", font=font_regular)
            y_position += 25
        y_position += 15

        # Данные транспорта
        for text in [vehicle, trailer if trailer.lower() != 'нет' else "Нет", country]:
            draw.text((50, y_position), text, fill="black", font=font_bold)
            y_position += 30
        y_position += 20

        # Разделительная линия
        draw.line([(50, y_position), (750, y_position)], fill="black", width=2)
        y_position += 20

        # Фондация
        draw.text((50, y_position), "ФОНДАЦИЯ", fill="black", font=font_medium_bold)
        y_position += 30
        draw.text((70, y_position), "- Цифровая платформа для бизнеса", fill="black", font=font_regular)
        y_position += 50

        # Разделительная линия
        draw.line([(50, y_position), (750, y_position)], fill="black", width=2)
        y_position += 30

        # Подпись
        draw.text((50, y_position), "Для подтверждения бронирования предъявите QR для сканирования на пункте пропуска", 
                 fill="black", font=font_regular)
        y_position += 50

        # Финальная линия
        draw.line([(50, y_position), (750, y_position)], fill="black", width=2)
        y_position += 30

        # Логотип
        draw.text((300, y_position), "CARGO RUQSAT", fill="black", font=font_medium_bold)

        # Сохраняем изображение
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)

        # Отправляем пользователю
        await update.message.reply_photo(photo=img_byte_arr, caption="Ваша выписка готова!")

    except Exception as e:
        await update.message.reply_text(f"Произошла ошибка: {str(e)}")

def main():
    """Запуск бота"""
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_document))
    
    print("Бот запущен и ожидает сообщений...")
    app.run_polling()

if __name__ == '__main__':
    main()
