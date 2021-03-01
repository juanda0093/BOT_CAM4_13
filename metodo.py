from typing import cast

import telegram
import dao, requests, time, json
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

conne = dao.Conexion()


class Metodos:
    def sendMessangeT(self, telegrams):
        text = "{nombre}, tu cuenta esta verificada\n\nAhora comparte el siguiente mensaje con todos tus usuario, grupos y canales de Telegram"
        url = "https://api.telegram.org/bot1648966134:AAHx-qSTyHAbek-ShU6XJ942npwYeFbRT8U/sendMessage"
        dato = {"chat_id": telegrams[0][0], "text": text.format(nombre=telegrams[0][1])}
        requests.post(url, data=dato)
    
    def sendMessange(self, text):
        url = "https://api.telegram.org/bot1679535422:AAGkx_4iJ5qavz_EgrEu6RePwU3c7KAIm3E/sendMessage"
        dato = {"chat_id": '1166478986', "text": text}
        requests.post(url, data=dato)
    
    def sendMessangeRespuesta(self, id, no):
        text = "Numero Total de Referidos: {nu}"
        url = "https://api.telegram.org/bot1648966134:AAHx-qSTyHAbek-ShU6XJ942npwYeFbRT8U/sendMessage"
        dato = {"chat_id": id, "text": text.format(nu=no)}
        requests.post(url, data=dato)

    def sendVideo(self, update, text, dirr):
        url = "https://api.telegram.org/bot1648966134:AAHx-qSTyHAbek-ShU6XJ942npwYeFbRT8U/sendVideo"
        file = {"video": (dirr, open(dirr, "rb"))}
        dato = {"chat_id": update.message.chat.id, "caption": text, "duration": 21}
        requests.post(url, files=file, data=dato)

    def sendMessangeBotones(self, text, update):
        keyboard = [
            [
                InlineKeyboardButton(
                    "Verificar C4: " + update.message.text.upper(), callback_data="1"
                )
            ],
            [
                InlineKeyboardButton(
                    "Chat con " + update.message.chat.first_name,
                    url="t.me/" + update.message.chat.username,
                )
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        url = "https://api.telegram.org/bot1679535422:AAGkx_4iJ5qavz_EgrEu6RePwU3c7KAIm3E/sendMessage"
        dato = {
            "chat_id": "1166478986",
            "text": text,
            "reply_markup": json.dumps(reply_markup.to_dict()),
        }
        requests.post(url, data=dato)

    def sendMessageBotonUs(self, telegrams):
        keyboard = [
            [InlineKeyboardButton("Boton 1", callback_data="1")],
            [InlineKeyboardButton("Boton 2", url="t.me/")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = "Hola, ___________________\n\nCódigo de Verificación: {code}"
        url = "https://api.telegram.org/bot1648966134:AAHx-qSTyHAbek-ShU6XJ942npwYeFbRT8U/sendMessage"
        dato = {
            "chat_id": telegrams[0][0],
            "text": text.format(code=telegrams[0][2]),
            "reply_markup": json.dumps(reply_markup.to_dict()),
        }
        requests.post(url, data=dato)

    def registrarCuentaC4(self, update):
        text = (
            "Hola, {name} | {id} | solicita la verificacion de existencia del Usuario: {c4user}"
        )
        self.sendMessangeBotones(
            text.format(
                name=update.message.chat.first_name, c4user=update.message.text.upper(), id=update.message.chat.id
            ),
            update,
        )
        return conne.insertatCuentaC4(update)

    def verificarCuentaC4(self, u):
        bool = conne.modificarCuentaC4(u)
        if bool:
            try:
                text = 'La Cuenta {user} Esta Verificada'
                self.sendMessange(text.format(user=u[1]))
                telegrams = conne.obtenerIDCam4User(u)
                self.sendMessangeT(telegrams)
                self.sendMessageBotonUs(telegrams)
            except Exception as e: 
                print(f"Exeption: {e}")
    
    def totalAfiliado(self, id):
        result = conne.obtenerCodigoRf(id)
        c = result[0][0]
        result = conne.obtenerIdRefiere(c)
        i = result[0][0]
        result = conne.obtenerTotalRf(c)
        t = result[0][0]
        self.sendMessangeRespuesta(i, t)
        self.sendMessangeRespuesta(id, 0)
        query = "UPDATE cam4bot.referidos SET noreferidos = '{to}' WHERE idreferido = '{id}'"
        return conne.connect(query.format(id=i, to=t))

    def obtenerTReferido(self, update):
        return conne.obtenerTReferidos(update.message.chat.id)

    def tieneUsuario(self, update):
        if update.message.chat.username is None:
            return False
        else:
            return True

    def verificaEstadoC4(self, update):
        return conne.VerificacionEstadoC4(update)

    def verificaUsuario(self, update):
        if conne.verificarUsuario(update):
            print("Telegram modificado")
        else:
            print("Telegram no modificado")

    def registrarUsuario(self, update):
        if conne.insertTelegram(update):
            return True
        else:
            return False

    def insertarReferido(self, update):
        return conne.insertReferido(update)

    def verificaCodigo(self, update, v):
        if conne.selectTelegram(update):
            self.insertarReferido(update)
            optio = self.instrucionRegistro(update)
            return optio, v
        else:
            if v:
                saludo = "{nombre}, Bienvenid@ a Cam4Bot, el Bot con el que puedes Ganar Dinero fácilmente Mediante Referidos"
                update.message.reply_text(
                    saludo.format(nombre=update.message.chat.first_name)
                )
                update.message.reply_text("Ingresa el Código de Referencia.")
                v = False
            else:
                update.message.reply_text(
                    "El Código "
                    + update.message.text.upper()
                    + " No es válido.\n\nIntenta Ingresar un Código de Referencia Valido."
                )
        return 0, v

    def instrucionRegistro(self, update):
        mej = "{nombre}, Para empezar a Ganar Dinero, Primero debes Registrarte a la Página"
        update.message.reply_text(mej.format(nombre=update.message.chat.first_name))
        text = ""
        dirr = ".\source\deo_1.mp4"
        self.sendVideo(update, text, dirr)
        keyboard = [
            [InlineKeyboardButton("Boton 1", url="t.me/juanda0093")],
            [InlineKeyboardButton("BOton 2", callback_data="2")],
            [InlineKeyboardButton("Boton 3", callback_data="3")],
            [InlineKeyboardButton("Boton 4", callback_data="4")],
            [InlineKeyboardButton("Boton 5", callback_data="5")],
            [InlineKeyboardButton("OpenVPN", url="t.me/juanda0093")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            "Mira___________________________________________________________________",
            reply_markup=reply_markup,
        )
        time.sleep(5)
        update.message.reply_text("Ingresa el Usuario Creado En Cam4")
        return 1