import os
import logging
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token from BotFather
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_text(
        f"§±§â§Ú§Ó§Ö§ä {user.first_name}!\n\n"
        "§Á §Ò§à§ä §Õ§Ý§ñ §Ô§Ö§ß§Ö§â§Ñ§è§Ú§Ú §Ó§í§á§Ú§ã§à§Ü §Ú§Ù §ã§Ú§ã§ä§Ö§Þ§í §ï§Ý§Ö§Ü§ä§â§à§ß§ß§à§Û §à§é§Ö§â§Ö§Õ§Ú.\n\n"
        "§°§ä§á§â§Ñ§Ó§î§ä§Ö §Þ§ß§Ö §ã§Ý§Ö§Õ§å§ð§ë§Ú§Ö §Õ§Ñ§ß§ß§í§Ö §Ó §à§Õ§ß§à§Þ §ã§à§à§Ò§ë§Ö§ß§Ú§Ú, §â§Ñ§Ù§Õ§Ö§Ý§ñ§ñ §Ú§ç §á§Ö§â§Ö§ß§à§ã§à§Þ §ã§ä§â§à§Ü§Ú:\n"
        "1. §¯§à§Þ§Ö§â §Ò§â§à§ß§Ú§â§à§Ó§Ñ§ß§Ú§ñ (§ß§Ñ§á§â§Ú§Þ§Ö§â, §¡§©34§£§¦§³F0368C)\n"
        "2. §±§å§ß§Ü§ä §á§â§à§á§å§ã§Ü§Ñ (§ß§Ñ§á§â§Ú§Þ§Ö§â, §¯§å§â §¨§à§Ý§í - §·§à§â§Ô§à§ã)\n"
        "3. §¥§Ñ§ä§Ñ (§ß§Ñ§á§â§Ú§Þ§Ö§â, 04.03.2025)\n"
        "4. §°§â§Ú§Ö§ß§ä§Ú§â§à§Ó§à§é§ß§à§Ö §Ó§â§Ö§Þ§ñ (§ß§Ñ§á§â§Ú§Þ§Ö§â, 21:00-22:00)\n"
        "5. §¯§à§Þ§Ö§â§ß§à§Û §Ù§ß§Ñ§Ü §ä§â§Ñ§ß§ã§á§à§â§ä§Ñ\n"
        "6. §¯§à§Þ§Ö§â§ß§à§Û §Ù§ß§Ñ§Ü §á§â§Ú§è§Ö§á§Ñ (§Ö§ã§Ý§Ú §ß§Ö§ä, §ß§Ñ§á§Ú§ê§Ú§ä§Ö '§ß§Ö§ä')\n"
        "7. §³§ä§â§Ñ§ß§Ñ §â§Ö§Ô§Ú§ã§ä§â§Ñ§è§Ú§Ú\n\n"
        "§±§â§Ú§Þ§Ö§â §ã§à§à§Ò§ë§Ö§ß§Ú§ñ:\n"
        "§¡§©34§£§¦§³F0368C\n"
        "§¯§å§â §¨§à§Ý§í - §·§à§â§Ô§à§ã\n"
        "04.03.2025\n"
        "21:00-22:00\n"
        "ABC123\n"
        "§ß§Ö§ä\n"
        "§¬§Ñ§Ù§Ñ§ç§ã§ä§Ñ§ß"
    )

async def generate_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate the customs document image."""
    try:
        # Split user input into lines
        lines = update.message.text.split('\n')
        if len(lines) < 7:
            await update.message.reply_text("§±§à§Ø§Ñ§Ý§å§Û§ã§ä§Ñ, §á§â§Ö§Õ§à§ã§ä§Ñ§Ó§î§ä§Ö §Ó§ã§Ö §ß§Ö§à§Ò§ç§à§Õ§Ú§Þ§í§Ö §Õ§Ñ§ß§ß§í§Ö (7 §ã§ä§â§à§Ü).")
            return

        # Extract data from user input
        booking_number = lines[0].strip()
        checkpoint = lines[1].strip()
        date = lines[2].strip()
        time_range = lines[3].strip()
        vehicle_plate = lines[4].strip()
        trailer_plate = lines[5].strip()
        country = lines[6].strip()

        # Create a blank image (white background)
        img = Image.new('RGB', (800, 1200), color='white')
        d = ImageDraw.Draw(img)

        # Load fonts (you'll need to have these font files or use default ones)
        try:
            title_font = ImageFont.truetype("arialbd.ttf", 24)
            header_font = ImageFont.truetype("arialbd.ttf", 20)
            content_font = ImageFont.truetype("arial.ttf", 18)
            bold_font = ImageFont.truetype("arialbd.ttf", 18)
        except:
            # Fallback to default fonts if specified fonts not available
            title_font = ImageFont.load_default()
            header_font = ImageFont.load_default()
            content_font = ImageFont.load_default()
            bold_font = ImageFont.load_default()

        # Current date and time for the print stamp
        print_date = datetime.now().strftime("%d.%m.%Y %H:%M")

        # Draw the document content
        y_position = 50

        # Title
        d.text((50, y_position), "1 of 1", fill="black", font=title_font)
        y_position += 40

        # Header
        d.text((50, y_position), "§£§½§±§ª§³§¬§¡ §ª§© §³§ª§³§´§¦§®§½ §¿§­§¦§¬§´§²§°§¯§¯§°§« §°§¹§¦§²§¦§¥§ª", fill="black", font=header_font)
        y_position += 40

        # Print date
        d.text((50, y_position), f"§¥§Ñ§ä§Ñ §Ú §Ó§â§Ö§Þ§ñ §â§Ñ§ã§á§Ö§é§Ñ§ä§Ü§Ú: {print_date}", fill="black", font=content_font)
        y_position += 60

        # Booking section
        d.text((50, y_position), "§¢§²§°§¯§ª§²§°§£§¡§¯§ª§¦", fill="black", font=header_font)
        y_position += 30
        d.text((70, y_position), "- §³§ä§Ñ§ä§å§ã", fill="black", font=content_font)
        y_position += 25
        d.text((70, y_position), "- ¡í §Ò§â§à§ß§Ú§â§à§Ó§Ñ§ß§Ú§ñ", fill="black", font=content_font)
        y_position += 25
        d.text((70, y_position), "- §±§å§ß§Ü§ä §á§â§à§á§å§ã§Ü§Ñ", fill="black", font=content_font)
        y_position += 25
        d.text((70, y_position), "- §¥§Ñ§ä§Ñ", fill="black", font=content_font)
        y_position += 25
        d.text((70, y_position), "- §°§â§Ú§Ö§ß§ä§Ú§â§à§Ó§à§é§ß§à§Ö §Ó§â§Ö§Þ§ñ", fill="black", font=content_font)
        y_position += 25
        d.text((70, y_position), "- §´§Ú§á §à§é§Ö§â§Ö§Õ§Ú", fill="black", font=content_font)
        y_position += 40

        # Divider line
        d.line([(50, y_position), (750, y_position)], fill="black", width=2)
        y_position += 20

        # Booking details
        d.text((50, y_position), booking_number, fill="black", font=bold_font)
        y_position += 30
        d.text((50, y_position), checkpoint, fill="black", font=bold_font)
        y_position += 30
        d.text((50, y_position), date, fill="black", font=bold_font)
        y_position += 30
        d.text((50, y_position), time_range, fill="black", font=bold_font)
        y_position += 50

        # Divider line
        d.line([(50, y_position), (750, y_position)], fill="black", width=2)
        y_position += 20

        # Transport section
        d.text((50, y_position), "§´§²§¡§¯§³§±§°§²§´", fill="black", font=header_font)
        y_position += 30
        d.text((70, y_position), "- §¯§à§Þ§Ö§â§ß§à§Û §Ù§ß§Ñ§Ü §ä§â§Ñ§ß§ã§á§à§â§ä§Ñ", fill="black", font=content_font)
        y_position += 25
        d.text((70, y_position), "- §¯§à§Þ§Ö§â§ß§à§Û §Ù§ß§Ñ§Ü §á§â§Ú§è§Ö§á§Ñ", fill="black", font=content_font)
        y_position += 25
        d.text((70, y_position), "- §³§ä§â§Ñ§ß§Ñ §â§Ö§Ô§Ú§ã§ä§â§Ñ§è§Ú§Ú", fill="black", font=content_font)
        y_position += 40

        # Transport details
        d.text((50, y_position), vehicle_plate, fill="black", font=bold_font)
        y_position += 30
        d.text((50, y_position), trailer_plate if trailer_plate.lower() != '§ß§Ö§ä' else "§¯§Ö§ä", fill="black", font=bold_font)
        y_position += 30
        d.text((50, y_position), country, fill="black", font=bold_font)
        y_position += 50

        # Divider line
        d.line([(50, y_position), (750, y_position)], fill="black", width=2)
        y_position += 20

        # Foundation section
        d.text((50, y_position), "§¶§°§¯§¥§¡§¸§ª§Á", fill="black", font=header_font)
        y_position += 30
        d.text((70, y_position), "- §¸§Ú§æ§â§à§Ó§Ñ§ñ §á§Ý§Ñ§ä§æ§à§â§Þ§Ñ §Õ§Ý§ñ §Ò§Ú§Ù§ß§Ö§ã§Ñ", fill="black", font=content_font)
        y_position += 50

        # Divider line
        d.line([(50, y_position), (750, y_position)], fill="black", width=2)
        y_position += 30

        # Footer note
        d.text((50, y_position), "§¥§Ý§ñ §á§à§Õ§ä§Ó§Ö§â§Ø§Õ§Ö§ß§Ú§ñ §Ò§â§à§ß§Ú§â§à§Ó§Ñ§ß§Ú§ñ §á§â§Ö§Õ§ì§ñ§Ó§Ú§ä§Ö QR §Õ§Ý§ñ §ã§Ü§Ñ§ß§Ú§â§à§Ó§Ñ§ß§Ú§ñ §ß§Ñ §á§å§ß§Ü§ä§Ö §á§â§à§á§å§ã§Ü§Ñ", 
              fill="black", font=content_font)
        y_position += 50

        # Final line
        d.line([(50, y_position), (750, y_position)], fill="black", width=2)
        y_position += 30

        # CARGO RUQSAT
        d.text((300, y_position), "CARGO RUQSAT", fill="black", font=header_font)

        # Save image to bytes
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)

        # Send the image to user
        await update.message.reply_photo(photo=img_byte_arr, caption="§£§Ñ§ê§Ñ §Ó§í§á§Ú§ã§Ü§Ñ §Ô§à§ä§à§Ó§Ñ!")

    except Exception as e:
        logger.error(f"Error generating document: {e}")
        await update.message.reply_text("§±§â§à§Ú§Ù§à§ê§Ý§Ñ §à§ê§Ú§Ò§Ü§Ñ §á§â§Ú §Ô§Ö§ß§Ö§â§Ñ§è§Ú§Ú §Õ§à§Ü§å§Þ§Ö§ß§ä§Ñ. §±§à§Ø§Ñ§Ý§å§Û§ã§ä§Ñ, §á§â§à§Ó§Ö§â§î§ä§Ö §Ó§Ó§Ö§Õ§Ö§ß§ß§í§Ö §Õ§Ñ§ß§ß§í§Ö §Ú §á§à§á§â§à§Ò§å§Û§ä§Ö §ã§ß§à§Ó§Ñ.")

def main():
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))

    # on non command i.e message - generate document
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_document))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
