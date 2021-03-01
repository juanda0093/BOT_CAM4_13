import MySQLdb
from random import SystemRandom


class Conexion:
    def connect(self, query):
        db = MySQLdb.connect(
            user="root",
            password="12345",
            host="127.0.0.1",
            port=3306,
            database="telegram",
        )
        cur = db.cursor()
        try:
            cur.execute(query)
            db.commit()
            return True
        except MySQLdb.Error as e:
            print(f"Error connecting to MySQLdb Platform: {e}")
            return False

    def connectReturn(self, query):
        db = MySQLdb.connect(
            user="root",
            password="12345",
            host="127.0.0.1",
            port=3306,
            database="cam4bot",
        )
        cur = db.cursor()
        try:
            cur.execute(query)
            result = cur.fetchall()
            if result is not None:
                return result
            result = None
        except MySQLdb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
        db.close()

    def obtenerCodigoRf(self, i):
        query = "SELECT codigotelegram FROM cam4bot.referidos WHERE idreferido = '{id}'"
        return self.connectReturn(query.format(id=i))

    def obtenerIdRefiere(self, c):
        query = "SELECT idtelegram FROM cam4bot.telegrams WHERE codigo = '{code}'"
        return self.connectReturn(query.format(code=c))
        
    def obtenerTotalRf(self, c):
        query = "SELECT COUNT(codigotelegram) FROM cam4bot.referidos WHERE codigotelegram = '{code}'"
        return self.connectReturn(query.format(code=c))
        
    def obtenerTReferidos(self, id):
        query = "(SELECT noreferidos FROM cam4bot.referidos WHERE idreferido = '{i}') union (SELECT 0) LIMIT 1"
        return self.connectReturn(query.format(i=id))

    def insertatCuentaC4(self, update):
        query = "INSERT INTO cam4bot.cam4users (idtelegram, cam4user)VALUES ('{id}', '{c4u}')"
        return self.connect(query.format(id=update.message.chat.id,c4u=update.message.text.upper()))

    def insertTelegram(self, update):
        query = "SELECT nombre FROM cam4bot.telegrams WHERE codigo = '{codigo}'"
        code = self.generarCodigo()
        while len(self.connectReturn(query.format(codigo=code))) != 0:
            code = self.generarCodigo()
        query = "INSERT INTO cam4bot.telegrams (idtelegram, usuario, nombre, apellido, codigo) VALUES ({id}, '{usuario}', '{nombre}', '{apellido}', '{codigo}')"
        return self.connect(
            query.format(
                id=update.message.chat.id,
                usuario=update.message.chat.username,
                nombre=update.message.chat.first_name,
                apellido=update.message.chat.last_name,
                codigo=code,
            )
        )

    def insertReferido(self, update):
        query = "INSERT INTO cam4bot.referidos (idreferido, codigotelegram) VALUES ('{id}', '{codigo}')"
        return self.connect(query.format(id=update.message.chat.id,codigo=update.message.text.upper()))

    def generarCodigo(self):
        longitud = 5
        valores = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        cryptogen = SystemRandom()
        c = ""
        while longitud > 0:
            c = c + cryptogen.choice(valores)
            longitud = longitud - 1
        return c.upper()

    def selectTelegram(self, update):
        query = "SELECT nombre FROM cam4bot.telegrams WHERE UPPER(codigo) = UPPER('{codigo}') AND idtelegram <> {id}"
        result = self.connectReturn(
            query.format(codigo=update.message.text.upper(), id=update.message.chat.id)
        )
        if len(result) == 0:
            return False
        else:
            return True

    def modificarTelegram(self, update):
        query = (
            "UPDATE cam4bot.telegrams SET usuario = '{user}' WHERE idtelegram = '{id}'"
        )
        return self.connect(
            query.format(id=update.message.chat.id, user=update.message.chat.username)
        )

    def obtenerIDCam4User(self, usuario):
        query = "SELECT t.idtelegram, t.nombre, t.codigo FROM cam4bot.cam4users AS c JOIN cam4bot.telegrams AS t ON t.idtelegram = c.idtelegram WHERE c.cam4user = '{user}'"
        return self.connectReturn(query.format(user=usuario[1]))

    def modificarCuentaC4(self, u):
        query = "UPDATE cam4bot.cam4users SET estado = 'T' WHERE cam4user = '{usuario}'"
        return self.connect(query.format(usuario=u[1]))

    def VerificacionEstadoC4(self, update):
        query = "SELECT cam4user FROM cam4bot.cam4users WHERE idtelegram = '{id}' AND estado = 'T'"
        return self.connectReturn(query.format(id=update.message.chat.id))

    def verificarUsuario(self, update):
        query = "SELECT nombre FROM cam4bot.telegrams WHERE idtelegram = '{id}'"
        result = self.connectReturn(query.format(id=update.message.chat.id))
        if len(result) != 0:
            query = "SELECT nombre FROM cam4bot.telegrams WHERE idtelegram = '{id}' AND UPPER(usuario) = UPPER('{user}')"
            result = self.connectReturn(query.format(id=update.message.chat.id, user=update.message.chat.username)
            )
            if len(result) == 0:
                return self.modificarTelegram(update)
