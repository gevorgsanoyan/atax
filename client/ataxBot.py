import telebot
from telebot import types
import datetime
import sqlite3
import os
import smtplib
from telegramcalendar import create_calendar


TOKEN = "XXXXX"
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

bot = telebot.TeleBot(TOKEN)


gmail_user = 'ataxcurrent@gmail.com'
gmail_password = 'Tax.123456'




def sendMailtoGmail(tSubject, tBody, eText, toAddres ):
    sent_from = gmail_user
    to = [toAddres]

    subject = tSubject
    body = tBody

    email_text = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (sent_from, ", ".join(to), subject, eText)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()

        print('Email sent!')
    except:
        print('Something went wrong...')




current_shown_dates={}

#current_shown_dates={}
@bot.message_handler(commands=['calendar'])
def get_calendar(message):
    now = datetime.datetime.now() #Current date
    chat_id = message.chat.id
    date = (now.year,now.month)
    current_shown_dates[chat_id] = date #Saving the current date in a dict
    markup= create_calendar(now.year,now.month)
    bot.reply_to(message, "Пожалуйста, выберите дату.", reply_markup=markup)



@bot.callback_query_handler(func=lambda call: call.data == 'next-month')
def next_month(call):
    chat_id = call.message.chat.id
    saved_date = current_shown_dates.get(chat_id)
    if(saved_date is not None):
        year,month = saved_date
        month+=1
        if month>12:
            month=1
            year+=1
        date = (year,month)
        current_shown_dates[chat_id] = date
        markup= create_calendar(year,month)
        bot.reply_to(call.message, "Пожалуйста, выберите дату.", reply_markup=markup)

        #bot.edit_message_text("Please, choose a date", call.from_user.id, call.message.message_id, reply_markup=markup)
        #bot.answer_callback_query(call.id, text="")


@bot.callback_query_handler(func=lambda call: call.data == 'previous-month')
def previous_month(call):
    chat_id = call.message.chat.id
    saved_date = current_shown_dates.get(chat_id)
    if(saved_date is not None):
        year,month = saved_date
        month-=1
        if month<1:
            month=12
            year-=1
        date = (year,month)
        current_shown_dates[chat_id] = date
        markup= create_calendar(year,month)
        bot.reply_to(call.message, "Пожалуйста, выберите дату.", reply_markup=markup)
        #bot.edit_message_text("Please, choose a date", call.from_user.id, call.message.message_id, reply_markup=markup)
        #bot.answer_callback_query(call.id, text="")
    #else:
        #Do something to inform of the error
        #pass





list_items = []
list_items.append("Ввод данных о пассажире и рейсе.")
list_items.append("Вернутся в начало.")
list_items.append("Отмена и выход.")




newclientReqDic = {}

class newClientReq:
    def __init__(self, cFname, cLname, cDocNumb, cEmail, cFlight, cFlAirport, cFlDate, cDest, cDestType):
        self.fName = cFname
        self.lName = cLname
        self.DocNumb = cDocNumb
        self.email = cEmail
        self.filghtNumb = cFlight
        self.airport = cFlAirport
        self.fldate = cFlDate
        self.Dest = cDest
        self.cDestType = cDestType

newDriverReqDic = {}
class newDriverReq:
    def __init__(self, dFname, dLname, dDocNumb, dPhone, dTlgMsg, dCarInfo):
        self.dFname = dFname
        self.dLname = dLname
        self.dDocNumb = dDocNumb
        self.dPhone = dPhone
        self.dTlgMsg = dTlgMsg
        self.dCarInfo = dCarInfo


@bot.message_handler(commands=['register'])
def driverRegisterStart(message):
    bot.send_message(message.chat.id, "Hello. Welcome to Atax Service registration portal.")
    bot.send_message(message.chat.id, "Fro registration, please enter Your name.")
    bot.register_next_step_handler(message, driverNameInput)

def driverNameInput(message):
    if message.text == "/register":
        driverRegisterStart(message)
    else:
        chatId = message.chat.id
        nd = newDriverReq(message.text, None, None, None, message.from_user.id, None)
        newDriverReqDic[chatId] = nd
        msg = bot.send_message(message.chat.id,
                               "Dear " + "<b>" + nd.dFname + "</b>. Please, enter Your last name.",
                               parse_mode='HTML')
        bot.register_next_step_handler(msg, driverLastNameInput)

def driverLastNameInput(message):
    if message.text == "/register":
        driverRegisterStart(message)
    else:
        nd = newDriverReqDic[message.chat.id]
        nd.dLname = message.text
        msg = bot.send_message(message.chat.id,
                               "Dear <b>" + nd.dFname + " " + nd.dLname + "</b>. Please, enter Your driving licence number.",
                               parse_mode='HTML')
        bot.register_next_step_handler(msg, driverDocNumbImput)


def driverDocNumbImput(message):
    if message.text == "/register":
        driverRegisterStart(message)
    else:
        nd = newDriverReqDic[message.chat.id]
        nd.dDocNumb = message.text
        msg = bot.send_message(message.chat.id,
                               "Dear <b>" + nd.dFname + " " + nd.dLname + "</b>. Please, enter contact phone.",
                               parse_mode='HTML')
        bot.register_next_step_handler(msg, driverPhoneImput)


def driverPhoneImput(message):
    if message.text == "/register":
        driverRegisterStart(message)
    else:
        nd = newDriverReqDic[message.chat.id]
        nd.dPhone = message.text
        msg = bot.send_message(message.chat.id,
                               "Dear <b>" + nd.dFname + " " + nd.dLname + "</b>. Please, enter Your car information (Make, model, year and etc.).",
                               parse_mode='HTML')
        bot.register_next_step_handler(msg, driverCarInfoImput)


def driverCarInfoImput(message):
    if message.text == "/register":
        driverRegisterStart(message)
    else:
        nd = newDriverReqDic[message.chat.id]
        nd.dCarInfo = message.text
        msg = bot.send_message(message.chat.id,
                               "Dear <b>" + nd.dFname + " " + nd.dLname + "</b>. Please, confirm inputed information.Driving licence <b>"
                               + str(nd.dDocNumb) + "</b>, phone: <b>" + str(nd.dPhone) + "</b>.",
                               parse_mode='HTML')


        markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add("Confirm!")
        markup.add("Discard!")

        msg = bot.reply_to(msg, "Confirm, or type command 'register' for new input.", reply_markup=markup)

        bot.register_next_step_handler(msg, driverImputConfirm)


def driverImputConfirm(message):
    if message.text == "/register":
        driverRegisterStart(message)
    else:
        if message.text == "Confirm!":
            nd = newDriverReqDic[message.chat.id]
            conn = sqlite3.connect(os.path.join(BASE_DIR, "db.sqlite3"))
            curs = conn.cursor()
            sqlStm = "INSERT INTO tdrivers_tdriver(dFirstName, dLastName, dDocNumber, dPhone, dTlgMsg, dCarInfo, iUser_id, isActive, isReviewed) VALUES('" + str(
                nd.dFname) + "', '" + str(nd.dLname) + "', '" + str(nd.dDocNumb) + "', '" + str(nd.dPhone) + "', '" + str(nd.dTlgMsg) + \
                     "', '" + nd.dCarInfo + "' , '2', '0', '0')"
            curs.execute(sqlStm)
            conn.commit()

            bot.send_message(message.chat.id,
                             "Dear <b>" + nd.dFname + " " + nd.dLname + "</b>. Your information is registered in our database. We will contact You, as soon, as possible. Thank You for Your patient.",
                             parse_mode='HTML')

            sendMailtoGmail('New driver registered', nd.dDocNumb, nd.dFname + " " + nd.dLname + " " + nd.dPhone, 'gevorgsanoyan@gmail.com')





@bot.message_handler(commands=['flight'])
def filghtInputStart(message):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

    for item in list_items:
        markup.add(item)

    bot.send_message(message.chat.id, "Добро пожаловать!")
    bot.send_message(message.chat.id, "Просим ввести Ваши данные.")
    msg = bot.reply_to(message, "Выберите комманду для продолжения ввода, или комнаду /flight", reply_markup=markup)
    bot.register_next_step_handler(msg, finputMenuChoose)


def finputMenuChoose(message):
    if message.text == list_items[0]:
        msg = bot.send_message(message.chat.id, "Пожалуйста, введите Ваше имя.")
        bot.register_next_step_handler(msg, clientNameInput)
    else:
        if message.text == list_items[1]:
            filghtInputStart(message)


def clientNameInput(message):
    if message.text == "/flight" or message.text == list_items[1] or message.text == list_items[2]:
        filghtInputStart(message)
    else:
        chatId = message.chat.id
        nc = newClientReq(message.text, "", "", "", "", "", "", "", "")
        newclientReqDic[chatId] = nc
        msg = bot.send_message(message.chat.id, "Уважамемый(-ая) " + "<b>"+ nc.fName +  "</b>. Пожалуйста, введите фамилию.", parse_mode='HTML')
        bot.register_next_step_handler(msg, clientLastNameInput)


def clientLastNameInput(message):
    if message.text == "/flight":
        filghtInputStart(message)
    else:
        nc = newclientReqDic[message.chat.id]
        nc.lName = message.text
        msg = bot.send_message(message.chat.id, "Уважамемый(-ая) <b>" + nc.fName + " " + nc.lName + "</b>. Пожалуйста, введите номер документа (паспорт).", parse_mode='HTML')
        bot.register_next_step_handler(msg, clientDocNumbImput)



def clientDocNumbImput(message):
    if message.text == "/flight":
        filghtInputStart(message)
    else:
        nc = newclientReqDic[message.chat.id]
        nc.DocNumb = message.text
        msg = bot.send_message(message.chat.id,
                               "Уважамемый(-ая) <b>" + nc.fName + " " + nc.lName + "</b>. Пожалуйста, введите номер рейса.", parse_mode='HTML')
        bot.register_next_step_handler(msg, flightNumberInput)


def flightNumberInput(message):
    if message.text == "/flight":
        filghtInputStart(message)
    else:
        nc = newclientReqDic[message.chat.id]
        nc.cFlight = message.text
        msg = bot.send_message(message.chat.id,
                               "Уважамемый(-ая) <b>" + nc.fName + " " + nc.lName + "</b>. Пожалуйста, введите дату рейса.", parse_mode='HTML')
        get_calendar(message)

@bot.callback_query_handler(func=lambda call: call.data[0:13] == 'calendar-day-')
def flDateInput(call):
    message = call.message
    if message.text == "/flight":
        filghtInputStart(message)
    else:
        nc = newclientReqDic[message.chat.id]

        chat_id = call.message.chat.id
        saved_date = current_shown_dates.get(chat_id)
        if (saved_date is not None):
            day = call.data[13:]
            date = datetime.datetime(int(saved_date[0]), int(saved_date[1]), int(day))
            nc.cFlDate = date

            msg = bot.send_message(message.chat.id, "Введите пожалуйста приблизительное время посадки в 24 часовом формате(ЧЧ:ММ).")

            bot.register_next_step_handler(msg, timeInput)



def timeInput(message):
    if message.text == "/flight":
        filghtInputStart(message)
    else:
        nc = newclientReqDic[message.chat.id]
        inputTime = message.text

        try:
            hr = int(inputTime[0:2])
            mnt = int(inputTime[3:])

            nc.cFlDate = nc.cFlDate.replace(minute=mnt, hour=hr)
        except:
            pass

        conn = sqlite3.connect(os.path.join(BASE_DIR, "db.sqlite3"))
        curs = conn.cursor()

        u = curs.execute("SELECT apName FROM client_airports ORDER BY id")

        markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        for itrm in u:
            markup.add(str(itrm[0]))

        msg = bot.reply_to(message, "Пожалуйста, выберите аэропорт.",
                           reply_markup=markup)

        bot.register_next_step_handler(msg, airportInput)


def airportInput(message):
    if message.text == "/flight":
        filghtInputStart(message)
    else:
        nc = newclientReqDic[message.chat.id]
        nc.cFlAirport = message.text
        conn = sqlite3.connect(os.path.join(BASE_DIR, "db.sqlite3"))
        curs = conn.cursor()

        u = curs.execute("SELECT dName, dCity AS destin FROM client_destination ORDER BY id")

        markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        for itrm in u:
            markup.add(str(itrm[0]))

        #markup.add("Отель")
        markup.add("Другое")

        msg = bot.reply_to(message, "Пожалуйста, выберите конечний пункт.",
                           reply_markup=markup)

        bot.register_next_step_handler(msg, destinationInput)




def destinationInput(message):
    if message.text == "/flight":
        filghtInputStart(message)
    else:
        nc = newclientReqDic[message.chat.id]
        nc.Dest = message.text
        if nc.Dest == "Другое":
            nc.cDestType = 2
            msg = bot.send_message(message.chat.id, "Введите наименование и адрес пункта назначения.")
            bot.register_next_step_handler(message, inputConfirmation)
        else:
            nc.cDestType = 1
            inputConfirmation(message)




def inputConfirmation(message):
    if message.text == "/flight":
        filghtInputStart(message)
    else:
        nc = newclientReqDic[message.chat.id]
        nc.Dest = message.text
        #conn = sqlite3.connect(os.path.join(BASE_DIR, "db.sqlite3"))
        #curs = conn.cursor()
        msg = bot.send_message(message.chat.id,
                               "Уважамемый(-ая) <b>" + nc.fName + " " + nc.lName + "!</b> номер Вашего рейса #<b>" + nc.cFlight + "</b>, на " + str(
                                   nc.cFlDate) +" в аэропорт <b>" + nc.cFlAirport + "</b>. Пункт назначения - <b>" + nc.Dest + "</b>" , parse_mode='HTML')

        markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add("Подтверждаю!")
        markup.add("Отмена и ввод заново.")

        msg = bot.reply_to(msg, "Пожалуйста, подтвердите введенные данные.",
                           reply_markup=markup)

        bot.register_next_step_handler(msg, ConfirmAndInput)


def ConfirmAndInput(message):
    if message.text == "/flight":
        filghtInputStart(message)
    else:
        nc = newclientReqDic[message.chat.id]
        tlgMsg = message.from_user.id

        if message.text == "Подтверждаю!":
            conn = sqlite3.connect(os.path.join(BASE_DIR, "db.sqlite3"))
            curs = conn.cursor()

            try:
                clientId = curs.execute("SELECT id FROM client_client WHERE cDocNumber = '" + nc.DocNumb + "'").fetchall()[0][0]
            except:
                clientId = 0

            print(clientId)


            if clientId < 1:
                sqlStm = "INSERT INTO client_client(cFirstName, cLastName, cDocNumber, cTlgMsg, iUser_id) VALUES('" + str(nc.fName) + "', '" + str(nc.lName) + "', '" + str(nc.DocNumb) + "', '" + str(tlgMsg) + "', '2')"
                curs.execute(sqlStm)
                conn.commit()
                clientId = curs.execute("SELECT id FROM client_client WHERE cDocNumber = '" + nc.DocNumb + "'").lastrowid


            apId = curs.execute("SELECT id FROM client_airports WHERE apName = '" + nc.cFlAirport + "'").fetchone()[0]

            if nc.cDestType == 1:
                destId = curs.execute("SELECT id FROM client_destination WHERE dName = '" + nc.Dest + "'").fetchone()[0]
            else:
                destId = 0


            sqlStm = "INSERT INTO client_clientflight(fClient_id, fAirport_id, flNumber, flDate, flDestination_id, flDestOther, isAccepted, accpDriver_id) VALUES('" + str(clientId) + "', '"+ str(apId) +"', '"+ str(nc.cFlight) + "', '"+ \
                     str(nc.cFlDate)+"', '"+ str(destId) +"', '" + str(nc.Dest) +"', '0', '0')"
            curs.execute(sqlStm)
            conn.commit()

            msg = bot.send_message(message.chat.id, "Уважамемый(-ая) <b>" + nc.fName + " " + nc.lName +
                               "!</b> Ваши данные введени в систему. Наш представитель будет ждать Вас в аэропорту <b>" + nc.cFlAirport + "</b> Желаем мягкой посадки.", parse_mode='HTML')

            sendMailtoGmail('New filght registered', nc.DocNumb, nc.fName + " " + nc.lName + " " + str(nc.cFlight) + " " + str(nc.cFlDate),
                            'gevorgsanoyan@gmail.com')
        else:
            filghtInputStart(message)


@bot.message_handler(commands=['getorders'])
def getOrderStart(message):
    conn = sqlite3.connect(os.path.join(BASE_DIR, "db.sqlite3"))
    curs = conn.cursor()
    sqlStm = "SELECT client_clientflight.id, fAirport_id, client_airports.apName, client_airports.apShortName, fClient_id, cFirstName, cLastName, " +\
                                "flNumber, flDate, flDestOther " +\
                                "FROM client_clientflight " +\
                                "INNER JOIN client_airports On client_clientflight.fAirport_id = client_airports.id " +\
                                "INNER JOIN client_client ON client_clientflight.fClient_id = client_client.id " +\
                                "WHERE isAccepted  = 0"
    orders = curs.execute(sqlStm)

    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

    for ord in orders:
        msgText = str(ord[7]) + "_date:" + str(ord[8]) + " " + str(ord[2])
        markup.add(msgText)

    msg = bot.reply_to(message, "Current orders list.",
                       reply_markup=markup)

    bot.register_next_step_handler(msg, orderGetByDriver)


def orderGetByDriver(message):
    fnIndex = message.text.find("_date")
    flNumb = message.text[:fnIndex]
    conn = sqlite3.connect(os.path.join(BASE_DIR, "db.sqlite3"))
    curs = conn.cursor()
    sqlStm = "SELECT client_clientflight.id, fAirport_id, client_airports.apName, client_airports.apShortName, fClient_id, cFirstName, cLastName, " + \
             "flNumber, flDate, flDestOther, isAccepted " + \
             "FROM client_clientflight " + \
             "INNER JOIN client_airports On client_clientflight.fAirport_id = client_airports.id " + \
             "INNER JOIN client_client ON client_clientflight.fClient_id = client_client.id " + \
             "WHERE flNumber = '" + flNumb + "'"
    orders = curs.execute(sqlStm)

    for order in orders:
        if order[10] == 0:
            confText = "Dear colleague. Your selectet order details is: Flight number <b>" + str(order[7]) + "</b>, flight date:<b>" + str(order[8]) +\
                             "</b>, airport - <b>" + str(order[2]) + "</b>, client: <b>" + str(order[5]) + " " + str(order[6]) + "</b>."

            bot.send_message(message.chat.id, confText, parse_mode='HTML')

            driverId = curs.execute("SELECT id FROM tdrivers_tdriver WHERE dTlgMsg = '" + str(message.from_user.id) + "'").fetchall()[0][0]

            curs.execute("UPDATE client_clientflight SET isAccepted = 1,accDate = ' " + str(datetime.datetime.now()) + "', accpDriver_id = '" + str(driverId) + "' WHERE flNumber = '" + str(order[7]) + "'")
            conn.commit()

        else:
            bot.send_message(message.chat.id, "Dear colleague. We are sorry, but this order is not longer available.",parse_mode='HTML')




if __name__ == '__main__':
    print("Bot Running")
    bot.polling(none_stop=True)
