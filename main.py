import logging, metodo

from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    Filters,
)

meto = metodo.Metodos()
optio = 0
v = True

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def start(update, context):
    global optio
    global v
    optio = 0
    if meto.tieneUsuario(update):
        meto.verificaUsuario(update)
        if meto.registrarUsuario(update):
            saludo = "Hola! {nombre}, Bienvenid@ a Cam4Bot, el Bot con el que puedes ganar dinero fácilmente mediante referidos"
            update.message.reply_text(
                saludo.format(nombre=update.message.chat.first_name)
            )
            update.message.reply_text("Ingresa el código de referencia.")
            v = False
        else:
            result = meto.verificaEstadoC4(update)
            if len(result) == 0:
                update.message.reply_text("Espera Verificacion")
            else:
                text = "Numero Total de Referidos: {n}"
                result = meto.obtenerTReferido(update)
                update.message.reply_text(text.format(n=result[0][0]))
            optio = 2
    else:
        nombre = update.message.chat.first_name
        saludo = "Hola! {name}, para poder sar este Bot, debes crear tu propio Nombre de Usuario, aprende cómo crearlo viendo el siguiente video."
        update.message.reply_text(saludo.format(name=nombre))
        text = "Cuando lo crees escribe Ok"
        dirr = ".\source\deo_1.mp4"
        meto.sendVideo(update, text.format(name=nombre), dirr)
        v = True

def responderMensaje(update, context):
    global optio
    global v
    if meto.tieneUsuario(update):
        meto.verificaUsuario(update)
        if optio == 2:
            print("___")
        if optio == 1:
            meto.registrarCuentaC4(update)
            update.message.reply_text("Espera Verificacion")
            optio = 2
        if optio == 0:
            if meto.tieneUsuario(update):
                meto.registrarUsuario(update)
                optio, v = meto.verificaCodigo(update, v)
            else:
                nombre = update.message.chat.first_name
                saludo = "{name}, Aun no has creado tu Nombre de Usuario, Mira el video para aprender a crearlo."
                update.message.reply_text(saludo.format(name=nombre))
                text = "Cuando lo crees escribe Ok"
                dirr = ".\source\deo_1.mp4"
                meto.sendVideo(update, text.format(name=nombre), dirr)
                v = True
    else:
        nombre = update.message.chat.first_name
        saludo = "{name}, has eliminado tu Nombre de Usuario, para seguir usando este Bot, siempre debes tener un Nombre de Usuario.\n\nEscribelo de nuevo, si no recuerdas como, mira el video."
        update.message.reply_text(saludo.format(name=nombre))
        text = "Cuando establescas el Nombre de Usuario, escribe Ok"
        dirr = ".\source\deo_1.mp4"
        meto.sendVideo(update, text.format(name=nombre), dirr)
        v = True


def accionBotones(update, context):
    query = update.callback_query
    logger.info(
        'TELEGRAM query data: "%s" type: "%s"'
        % (str(query.data), str(type(query.data)))
    )
    if query.data == "1":
        print("Boton 1")


def start2(update, context):
    print("")

def responderMensaje2(update, context):
    print("")

def accionBotones2(update, context):
    query = update.callback_query
    txt = update.callback_query.message.text
    u = txt.split(": ")
    i = txt.split("| ")
    logger.info(
        'TELEGRAM query data: "%s" type: "%s"'
        % (str(query.data), str(type(query.data)))
    )
    if query.data == "1":
        bool = meto.totalAfiliado(i[1])
        if bool:
            meto.verificarCuentaC4(u)
                    
def main():
        """Start the bot."""
        # Create the Updater and pass it your bot's token.
        # Make sure to set use_context=True to use the new context based callbacks
        # Post version 12 this will no longer be necessary
        updater = Updater(
            "1648966134:AAHx-qSTyHAbek-ShU6XJ942npwYeFbRT8U", use_context=True
        )

        updater2 = Updater(
            "1679535422:AAGkx_4iJ5qavz_EgrEu6RePwU3c7KAIm3E", use_context=True
        )

        dp = updater.dispatcher
        dp2 = updater2.dispatcher

        dp.add_handler(CommandHandler("start", start))
        dp2.add_handler(CommandHandler("start", start2))

        dp.add_handler(MessageHandler(Filters.text, responderMensaje))
        dp2.add_handler(MessageHandler(Filters.text, responderMensaje2))

        dp.add_handler(CallbackQueryHandler(accionBotones))
        dp2.add_handler(CallbackQueryHandler(accionBotones2))

        dp.add_error_handler(error)
        dp2.add_error_handler(error)

        updater.start_polling()
        updater2.start_polling()

        updater.idle()
        updater2.idle()

if __name__ == "__main__":
    main()