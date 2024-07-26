import os
from dotenv import load_dotenv
from telegram import Update, ChatMember
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ChatMemberHandler, CallbackContext

# Cargar variables de entorno
load_dotenv()
TOKEN = os.getenv('TOKEN')

# Verificar si el token fue cargado correctamente
if not TOKEN:
    raise ValueError("No se ha encontrado el TOKEN en el archivo .env")

BANNER_PATH = 'ruta/a/tu/banner.jpg'  # Ruta a la imagen del banner
# o URL: BANNER_URL = 'http://example.com/banner.jpg'

# Mensajes de publicidad
publicidad = [
    "Publicidad 1: Visita nuestro sitio web en example.com",
    "Publicidad 2: Únete a nuestro canal en Telegram en t.me/example",
    "Publicidad 3: Síguenos en nuestras redes sociales @example",
    "Publicidad 4: Aprovecha nuestras ofertas especiales en example.com/ofertas"
]

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('¡Hola! Soy tu bot de Telegram.')

async def echo(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(update.message.text)

async def greet_new_member(update: Update, context: CallbackContext) -> None:
    for member in update.chat_member.new_chat_members:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f'¡Bienvenido, {member.full_name}!')

        # Enviar el banner
        if os.path.exists(BANNER_PATH):
            with open(BANNER_PATH, 'rb') as banner:
                await context.bot.send_photo(chat_id=update.effective_chat.id, photo=banner)
        # Si usas URL: await context.bot.send_photo(chat_id=update.effective_chat.id, photo=BANNER_URL)
        
        # Enviar publicidades de 2 en 2
        for i in range(0, len(publicidad), 2):
            await context.bot.send_message(chat_id=update.effective_chat.id, text='\n\n'.join(publicidad[i:i+2]))

async def unknown(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Lo siento, no entiendo ese comando.")

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(ChatMemberHandler(greet_new_member, ChatMemberHandler.CHAT_MEMBER))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))

    application.run_polling()

if __name__ == '__main__':
    main()
