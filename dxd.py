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
TOKEN = "7942282080:AAGYeFmFyLtibd4AB1rcLxMDqhNoq22_T4s"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_text(
        f"妤把我志快找 {user.first_name}!\n\n"
        "岐 忌抉找 忱抖攸 忍快扶快把忘扯我我 志抑扭我扼抉抗 我戒 扼我扼找快技抑 改抖快抗找把抉扶扶抉抄 抉折快把快忱我.\n\n"
        "妍找扭把忘志抆找快 技扶快 扼抖快忱批攻投我快 忱忘扶扶抑快 志 抉忱扶抉技 扼抉抉忌投快扶我我, 把忘戒忱快抖攸攸 我抒 扭快把快扶抉扼抉技 扼找把抉抗我:\n"
        "1. 妖抉技快把 忌把抉扶我把抉志忘扶我攸 (扶忘扭把我技快把, 均妝34圾圻妊F0368C)\n"
        "2. 妤批扶抗找 扭把抉扭批扼抗忘 (扶忘扭把我技快把, 妖批把 夾抉抖抑 - 孚抉把忍抉扼)\n"
        "3. 坏忘找忘 (扶忘扭把我技快把, 04.03.2025)\n"
        "4. 妍把我快扶找我把抉志抉折扶抉快 志把快技攸 (扶忘扭把我技快把, 21:00-22:00)\n"
        "5. 妖抉技快把扶抉抄 戒扶忘抗 找把忘扶扼扭抉把找忘\n"
        "6. 妖抉技快把扶抉抄 戒扶忘抗 扭把我扯快扭忘 (快扼抖我 扶快找, 扶忘扭我扮我找快 '扶快找')\n"
        "7. 妊找把忘扶忘 把快忍我扼找把忘扯我我\n\n"
        "妤把我技快把 扼抉抉忌投快扶我攸:\n"
        "均妝34圾圻妊F0368C\n"
        "妖批把 夾抉抖抑 - 孚抉把忍抉扼\n"
        "04.03.2025\n"
        "21:00-22:00\n"
        "ABC123\n"
        "扶快找\n"
        "妞忘戒忘抒扼找忘扶"
    )

async def generate_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate the customs document image."""
    try:
        # Split user input into lines
        lines = update.message.text.split('\n')
        if len(lines) < 7:
            await update.message.reply_text("妤抉忪忘抖批抄扼找忘, 扭把快忱抉扼找忘志抆找快 志扼快 扶快抉忌抒抉忱我技抑快 忱忘扶扶抑快 (7 扼找把抉抗).")
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
        d.text((50, y_position), "圾局妤妒妊妞均 妒妝 妊妒妊妥圻妙局 尿妣圻妞妥妓妍妖妖妍妨 妍完圻妓圻坏妒", fill="black", font=header_font)
        y_position += 40

        # Print date
        d.text((50, y_position), f"坏忘找忘 我 志把快技攸 把忘扼扭快折忘找抗我: {print_date}", fill="black", font=content_font)
        y_position += 60

        # Booking section
        d.text((50, y_position), "坎妓妍妖妒妓妍圾均妖妒圻", fill="black", font=header_font)
        y_position += 30
        d.text((70, y_position), "- 妊找忘找批扼", fill="black", font=content_font)
        y_position += 25
        d.text((70, y_position), "- ∮ 忌把抉扶我把抉志忘扶我攸", fill="black", font=content_font)
        y_position += 25
        d.text((70, y_position), "- 妤批扶抗找 扭把抉扭批扼抗忘", fill="black", font=content_font)
        y_position += 25
        d.text((70, y_position), "- 坏忘找忘", fill="black", font=content_font)
        y_position += 25
        d.text((70, y_position), "- 妍把我快扶找我把抉志抉折扶抉快 志把快技攸", fill="black", font=content_font)
        y_position += 25
        d.text((70, y_position), "- 妥我扭 抉折快把快忱我", fill="black", font=content_font)
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
        d.text((50, y_position), "妥妓均妖妊妤妍妓妥", fill="black", font=header_font)
        y_position += 30
        d.text((70, y_position), "- 妖抉技快把扶抉抄 戒扶忘抗 找把忘扶扼扭抉把找忘", fill="black", font=content_font)
        y_position += 25
        d.text((70, y_position), "- 妖抉技快把扶抉抄 戒扶忘抗 扭把我扯快扭忘", fill="black", font=content_font)
        y_position += 25
        d.text((70, y_position), "- 妊找把忘扶忘 把快忍我扼找把忘扯我我", fill="black", font=content_font)
        y_position += 40

        # Transport details
        d.text((50, y_position), vehicle_plate, fill="black", font=bold_font)
        y_position += 30
        d.text((50, y_position), trailer_plate if trailer_plate.lower() != '扶快找' else "妖快找", fill="black", font=bold_font)
        y_position += 30
        d.text((50, y_position), country, fill="black", font=bold_font)
        y_position += 50

        # Divider line
        d.line([(50, y_position), (750, y_position)], fill="black", width=2)
        y_position += 20

        # Foundation section
        d.text((50, y_position), "孜妍妖坏均孛妒岐", fill="black", font=header_font)
        y_position += 30
        d.text((70, y_position), "- 孛我扳把抉志忘攸 扭抖忘找扳抉把技忘 忱抖攸 忌我戒扶快扼忘", fill="black", font=content_font)
        y_position += 50

        # Divider line
        d.line([(50, y_position), (750, y_position)], fill="black", width=2)
        y_position += 30

        # Footer note
        d.text((50, y_position), "坏抖攸 扭抉忱找志快把忪忱快扶我攸 忌把抉扶我把抉志忘扶我攸 扭把快忱抓攸志我找快 QR 忱抖攸 扼抗忘扶我把抉志忘扶我攸 扶忘 扭批扶抗找快 扭把抉扭批扼抗忘", 
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
        await update.message.reply_photo(photo=img_byte_arr, caption="圾忘扮忘 志抑扭我扼抗忘 忍抉找抉志忘!")

    except Exception as e:
        logger.error(f"Error generating document: {e}")
        await update.message.reply_text("妤把抉我戒抉扮抖忘 抉扮我忌抗忘 扭把我 忍快扶快把忘扯我我 忱抉抗批技快扶找忘. 妤抉忪忘抖批抄扼找忘, 扭把抉志快把抆找快 志志快忱快扶扶抑快 忱忘扶扶抑快 我 扭抉扭把抉忌批抄找快 扼扶抉志忘.")

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
