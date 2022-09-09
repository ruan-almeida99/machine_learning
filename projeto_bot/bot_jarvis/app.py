######## IMPORT LIBS ########

from asyncio import QueueEmpty
import datetime
import os
import time

import requests
from requests import Session
from zabbix_api import ZabbixAPI

import mysql.connector
from mysql.connector import Error

######## GLOBAL VARIABLES ########

token = '1647952364:AAESG2R78CLdgfwTmX0PGrftOCCTUKaUSBo'
message_id_global = int()
chat_id = '-616559508'

url_zabbix = 'https://zbx.dz7telecom.com.br/index.php'

login_data = {
    'name': 'ruan.almeida',
    'password': 'Dz7!4267@',
    'enter': 'Conectar-Se',
}

hostname_db_mysql = '10.76.1.33'
user_db_mysql = 'bot_api'
passwd_db_mysql = 'Skynet321@'
name_db_mysql = 'mapa_gpon'

get_rota_liberdade = []
get_rota_miguel_couto = []
timestamp_today = int()
global_json_result = []

s = requests.Session()
r = s.post(url_zabbix, data=login_data)

signal_dwdm_pta = 'https://zbx.dz7telecom.com.br/chart2.php?graphid=2385&from=now-3h&to=now&height=201&width=1717&profileIdx=web.charts.filter&_=vm0joqqo.png'

transit_ntt = 'https://zbx.dz7telecom.com.br/chart2.php?graphid=17971&from=now-2d&to=now&height=201&width=1734&profileIdx=web.charts.filter&_=vluurfej.png'
transit_redfox_pta = 'https://zbx.dz7telecom.com.br/chart2.php?graphid=19252&from=now-2d&to=now&height=201&width=1734&profileIdx=web.charts.filter&_=vluux3tw.png'
transit_redfox_eqx = 'https://zbx.dz7telecom.com.br/chart2.php?graphid=19204&from=now-2d&to=now&height=201&width=1734&profileIdx=web.charts.filter&_=vluusm49.png'

ptt_ixbr_pta = 'https://zbx.dz7telecom.com.br/chart2.php?graphid=2792&from=now-2d&to=now&height=201&width=1734&profileIdx=web.charts.filter&_=vluv0qeg.png'
ptt_ixbr_eqx = 'https://zbx.dz7telecom.com.br/chart2.php?graphid=17885&from=now-2d&to=now&height=201&width=1734&profileIdx=web.charts.filter&_=vluuvcc3.png'
ptt_privado_eqx = 'https://zbx.dz7telecom.com.br/chart2.php?graphid=17972&from=now-2d&to=now&height=201&width=1734&profileIdx=web.charts.filter&_=vluuu6gl.png'

pni_meta1 = 'https://zbx.dz7telecom.com.br/chart2.php?graphid=2808&from=now-2d&to=now&height=201&width=1734&profileIdx=web.charts.filter&_=vluv2a7b.png'
pni_meta2 = ' https://zbx.dz7telecom.com.br/chart2.php?graphid=2809&from=now-2d&to=now&height=201&width=1734&profileIdx=web.charts.filter&_=vluv2a7b.png'
pni_google = 'https://zbx.dz7telecom.com.br/chart2.php?graphid=2807&from=now-2d&to=now&height=201&width=1734&profileIdx=web.charts.filter&_=vluv1ie0.png'

cdn_oca1 = 'https://zbx.dz7telecom.com.br/chart2.php?graphid=2736&from=now-2d&to=now&height=201&width=1734&profileIdx=web.charts.filter&_=vluv7qms.png'
cdn_oca2 = 'https://zbx.dz7telecom.com.br/chart2.php?graphid=2737&from=now-2d&to=now&height=201&width=1734&profileIdx=web.charts.filter&_=vluv9xg1.png'
cdn_ggc1 = 'https://zbx.dz7telecom.com.br/chart2.php?graphid=2732&from=now-2d&to=now&height=201&width=1734&profileIdx=web.charts.filter&_=vluvc3fn.png'
cdn_ggc2 = 'https://zbx.dz7telecom.com.br/chart2.php?graphid=2735&from=now-2d&to=now&height=201&width=1734&profileIdx=web.charts.filter&_=vluvd4gt.png'
cdn_fna = 'https://zbx.dz7telecom.com.br/chart2.php?graphid=2731&from=now-2d&to=now&height=201&width=1734&profileIdx=web.charts.filter&_=vluv6mjg.png'

########################################

####### TELEGRAM API ########


class api_telegram:

    # Get telegram chat id.
    def last_chat_id(token):
        try:
            url = 'https://api.telegram.org/bot{}/getUpdates'.format(token)
            response = requests.get(url)
            if response.status_code == 200:
                json_msg = response.json()
                for json_result in reversed(json_msg['result']):
                    return json_result['message']['chat']['id']
                print('Nenhum grupo encontrado')
            else:
                print(
                    'A resposta falhou, código de status: {}'.format(
                        response.status_code
                    )
                )
        except Exception as e:
            print('Erro no getUpdates:', e)

    # Send messages through specific chat.
    def send_message(token, chat_id, message):
        try:
            data = {'chat_id': chat_id, 'text': message}
            url = 'https://api.telegram.org/bot{}/sendMessage'.format(token)
            requests.post(url, data)
        except Exception as e:
            print('Erro no sendMessage:', e)

    # Send images through specific chat. 
    def send_image(file_path):
        body = {
            'chat_id': chat_id,
        }
        files = {'photo': open(file_path, 'rb')}
        r = requests.post(
            'https://api.telegram.org/bot{}/sendPhoto'.format(token),
            data=body,
            files=files,
        )
        if r.status_code >= 400:
            print(
                'Houve um erro ao enviar mensagem. Detalhe: {}'.format(r.text)
            )
        else:
            print('Mensagem enviada com sucesso.')


######## BOT API ########


class bot_api:

    # Download zabbix hosts graphs through the web.
    def download_graph(graph_url, name_file):
        with open('{}.png'.format(name_file), 'wb') as imagem:
            s = requests.Session()
            r = s.post(url_zabbix, data=login_data)
            resposta = s.get(graph_url, stream=True)
            if not resposta.ok:
                print('Ocorreu um erro, status:', resposta.status_code)
            else:
                for dado in resposta.iter_content(1024):
                    if not dado:
                        break
                    imagem.write(dado)

    # Remove file on directory.
    def remove_file(file_name):
        os.remove(file_name)

    # Convert date today to timestamp.
    def convert_date_to_datime():
        global timestamp_today
        today_hour = str(datetime.date.today())
        today_hour_convert = datetime.datetime.strptime(today_hour, '%Y-%m-%d')
        timestamp_today = datetime.datetime.timestamp(today_hour_convert)

    def process_download_and_send_graph(url_image, name_img):
        global message_id_global
        bot_api.download_graph(url_image, name_img),
        api_telegram.send_image('{}.png'.format(name_img)),
        bot_api.remove_file('{}.png'.format(name_img)),

######## ZABBIX API ########


class zabbix_bot_api:
    def __init__(self):
        pass

    # Search signal on route Liberdade Zabbix.
    def signal_liberdade():
        global get_rota_liberdade

        try:
            zbx = ZabbixAPI(server='https://zbx.dz7telecom.com.br/')
            login = zbx.login('dz7bot', '965&tx5siKN!')

            get_rota_liberdade = zbx.item.get(
                {
                    'output': ['itemid', 'name', 'units', 'lastvalue'],
                    'hostids': '10647',
                    'filter': {'itemid': ['40832', '40831', '40830', '40829']},
                }
            )
        except Exception as e:
            print('Erro:', e)

    # Search signal on route Miguel Couto Zabbix.
    def signal_miguel_couto():
        global get_rota_miguel_couto

        try:
            zbx = ZabbixAPI(server='https://zbx.dz7telecom.com.br/')
            login = zbx.login('dz7bot', '965&tx5siKN!')

            get_rota_miguel_couto = zbx.item.get(
                {
                    'output': ['itemid', 'name', 'units', 'lastvalue'],
                    'hostids': '10647',
                    'filter': {'itemid': ['40803', '40820', '40834', '40833']},
                }
            )
        except Exception as e:
            print('Erro:', e)

######## MySQL API ########

class mysql_api:

    def __init__(self):
        
        pass

    def create_server_connection(host_name, user_name, user_password, name_db):
        connection = None
        try:
            connection = mysql.connector.connect(
                host=host_name,
                user=user_name,
                passwd=user_password,
                database=name_db
            )
            print("MySQL Database connection successful")
        except Error as err:
            print(f"Error: '{err}'")

        return connection

    def read_query(connection, query):
        cursor = connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as err:
            print(f"Error: '{err}'")


######## APP ########

# Get updade chat, search last message on chat and make decision.
def get_update_chat(token):
    try:
        url = 'https://api.telegram.org/bot{}/getUpdates'.format(token)
        global message_id_global
        global global_json_result
        response = requests.get(url)
        if response.status_code == 200:
            json_msg = response.json()
            for json_result in reversed(json_msg['result']):
                global_json_result = json_result
                if len(json_result['message'].keys()) == 6:
                    if (
                        json_result['message']['entities'][0]['type']
                        == 'bot_command'
                        and json_result['message']['message_id']
                        != message_id_global
                    ):
                        if (
                            json_result['message']['text'] == '/getmap'
                            or json_result['message']['text']
                            == '/getmap@Dz7Telecom_bot'
                        ):
                            api_telegram.send_image(
                                '/home/recruta/projeto_bot/bot_jarvis/archives/backbone_map.png'
                            ),
                            message_id_global = int(
                                json_result['message']['message_id']
                            )
                            break

                        elif (
                            json_result['message']['text']
                            == '/getmap_telefonia'
                            or json_result['message']['text']
                            == '/getmap_telefonia@Dz7Telecom_bot'
                        ):
                            api_telegram.send_image(
                                '/home/recruta/projeto_bot/bot_jarvis/archives/telefonia_map.png'
                            ),
                            message_id_global = int(
                                json_result['message']['message_id']
                            )
                            break

                        elif (
                            json_result['message']['text'] == '/transit_ntt'
                            or json_result['message']['text']
                            == '/transit_ntt@Dz7Telecom_bot'
                        ):
                            name_img = ('ntt',)
                            bot_api.process_download_and_send_graph(transit_ntt,name_img)
                            message_id_global = int(
                                json_result['message']['message_id']
                                )
                            break

                        elif (
                            json_result['message']['text']
                            == '/transit_redfox_pta'
                            or json_result['message']['text']
                            == '/transit_redfox_pta@Dz7Telecom_bot'
                        ):
                            name_img = ('redfox_pta',)
                            bot_api.process_download_and_send_graph(transit_redfox_pta,name_img)
                            message_id_global = int(
                                json_result['message']['message_id']
                                )
                            break

                        elif (
                            json_result['message']['text']
                            == '/transit_redfox_eqx'
                            or json_result['message']['text']
                            == '/transit_redfox_eqx@Dz7Telecom_bot'
                        ):
                            name_img = ('redfox_eqx',)
                            bot_api.process_download_and_send_graph(transit_redfox_eqx,name_img)
                            message_id_global = int(
                                json_result['message']['message_id']
                                )
                            break

                        elif (
                            json_result['message']['text'] == '/ptt_ixbr_pta'
                            or json_result['message']['text']
                            == '/ptt_ixbr_pta@Dz7Telecom_bot'
                        ):
                            name_img = ('ixbr_pta',)
                            bot_api.process_download_and_send_graph(ptt_ixbr_pta,name_img)
                            message_id_global = int(
                                json_result['message']['message_id']
                                )
                            break

                        elif (
                            json_result['message']['text'] == '/ptt_ixbr_eqx'
                            or json_result['message']['text']
                            == '/ptt_ixbr_eqx@Dz7Telecom_bot'
                        ):
                            name_img = ('ixbr_eqx',)
                            bot_api.process_download_and_send_graph(ptt_ixbr_eqx,name_img)
                            message_id_global = int(
                                json_result['message']['message_id']
                                )
                            break

                        elif (
                            json_result['message']['text']
                            == '/ptt_privado_eqx'
                            or json_result['message']['text']
                            == '/ptt_privado_eqx@Dz7Telecom_bot'
                        ):
                            name_img = ('ptt_privado_eqx',)
                            bot_api.process_download_and_send_graph(ptt_privado_eqx,name_img)
                            message_id_global = int(
                                json_result['message']['message_id']
                                )
                            break

                        elif (
                            json_result['message']['text'] == '/pni_meta1'
                            or json_result['message']['text']
                            == '/pni_meta1@Dz7Telecom_bot'
                        ):
                            name_img = ('pni_meta1',)
                            bot_api.process_download_and_send_graph(pni_meta1,name_img)
                            message_id_global = int(
                                json_result['message']['message_id']
                                )
                            break

                        elif (
                            json_result['message']['text'] == '/pni_meta2'
                            or json_result['message']['text']
                            == '/pni_meta2@Dz7Telecom_bot'
                        ):
                            name_img = ('pni_meta2',)
                            bot_api.process_download_and_send_graph(pni_meta2,name_img)
                            message_id_global = int(
                                json_result['message']['message_id']
                                )
                            break

                        elif (
                            json_result['message']['text'] == '/pni_google'
                            or json_result['message']['text']
                            == '/pni_google@Dz7Telecom_bot'
                        ):
                            name_img = ('pni_google',)
                            bot_api.process_download_and_send_graph(pni_google,name_img)
                            message_id_global = int(
                                json_result['message']['message_id']
                                )
                            break

                        elif (
                            json_result['message']['text'] == '/cdn_oca1'
                            or json_result['message']['text']
                            == '/cdn_oca1@Dz7Telecom_bot'
                        ):
                            name_img = ('cdn_oca1',)
                            bot_api.process_download_and_send_graph(cdn_oca1,name_img)
                            message_id_global = int(
                                json_result['message']['message_id']
                                )
                            break

                        elif (
                            json_result['message']['text'] == '/cdn_oca2'
                            or json_result['message']['text']
                            == '/cdn_oca2@Dz7Telecom_bot'
                        ):
                            name_img = ('cdn_oca2',)
                            bot_api.process_download_and_send_graph(cdn_oca2,name_img)
                            message_id_global = int(
                                json_result['message']['message_id']
                                )
                            break

                        elif (
                            json_result['message']['text'] == '/cdn_ggc1'
                            or json_result['message']['text']
                            == '/cdn_ggc1@Dz7Telecom_bot'
                        ):
                            name_img = ('cdn_ggc1',)
                            bot_api.process_download_and_send_graph(cdn_ggc1,name_img)
                            message_id_global = int(
                                json_result['message']['message_id']
                                )
                            break

                        elif (
                            json_result['message']['text'] == '/cdn_ggc2'
                            or json_result['message']['text']
                            == '/cdn_ggc2@Dz7Telecom_bot'
                        ):
                            name_img = ('cdn_ggc2',)
                            bot_api.process_download_and_send_graph(cdn_ggc2,name_img)
                            message_id_global = int(
                                json_result['message']['message_id']
                                )
                            break

                        elif (
                            json_result['message']['text'] == '/cdn_fna'
                            or json_result['message']['text']
                            == '/cdn_fna@Dz7Telecom_bot'
                        ):
                            name_img = ('cdn_fna',)
                            bot_api.process_download_and_send_graph(cdn_fna,name_img)
                            message_id_global = int(
                                json_result['message']['message_id']
                                )
                            break

                        elif (
                            json_result['message']['text'] == '/manual'
                            or json_result['message']['text']
                            == '/manual@Dz7Telecom_bot'
                        ):
                            manual = [
                                '======================== \n'
                                'COMANDOS: \n \n'
                                '/getmap \n'
                                '/getmap_telefonia \n'
                                '/liberdade \n'
                                '/incidentes_1d \n'
                                '/miguel_couto \n'
                                '/transit_ntt \n'
                                '/transit_redfox_pta \n'
                                '/transit_redfox_eqx \n'
                                '/ptt_ixbr_pta \n'
                                '/ptt_ixbr_eqx \n'
                                '/ptt_privado_eqx \n'
                                '/pni_meta1 \n'
                                '/pni_meta2 \n'
                                '/pni_google \n'
                                '/cdn_oca1 \n'
                                '/cdn_oca2 \n'
                                '/cdn_ggc1 \n'
                                '/cdn_ggc2 \n'
                                '/cdn_fna \n'
                                '======================== \n'
                            ]
                            api_telegram.send_message(token, chat_id, manual)
                            message_id_global = int(
                                json_result['message']['message_id']
                            )
                            break

                        elif (
                            json_result['message']['text'] == '/liberdade'
                            or json_result['message']['text']
                            == '/liberdade@Dz7Telecom_bot'
                        ):
                            # Send image.
                            name_img = ('signal_dwdm_pta',)
                            bot_api.process_download_and_send_graph(signal_dwdm_pta,name_img)

                            # Get signal ports on zabbix api.
                            zabbix_bot_api.signal_liberdade(),
                            rota_liberdade = (
                                [
                                    '========================== \n'
                                    'SINAL ROTA LIBERDADE: \n'
                                    '\n'
                                    'Transceiver XGE0/0/5: \n'
                                    '{}{}'.format(
                                        get_rota_liberdade[3]['lastvalue'],
                                        (get_rota_liberdade[3]['units']),
                                    )
                                    + '\n'
                                    '\n'
                                    'Transceiver XGE0/0/6: \n'
                                    '{}{}'.format(
                                        get_rota_liberdade[2]['lastvalue'],
                                        (get_rota_liberdade[2]['units']),
                                    )
                                    + '\n'
                                    '\n'
                                    'Transceiver XGE0/0/7: \n'
                                    '{}{}'.format(
                                        get_rota_liberdade[1]['lastvalue'],
                                        (get_rota_liberdade[1]['units']),
                                    )
                                    + '\n'
                                    '\n'
                                    'Transceiver XGE0/0/8: \n'
                                    '{}{}'.format(
                                        get_rota_liberdade[0]['lastvalue'],
                                        (get_rota_liberdade[0]['units']),
                                    )
                                    + '\n'
                                    '=========================='
                                ],
                            )

                            # Send message to telegram.
                            api_telegram.send_message(
                                token, chat_id, rota_liberdade
                            ),
                            message_id_global = int(
                                json_result['message']['message_id']
                            )
                            break

                        elif (
                            json_result['message']['text'] == '/miguel_couto'
                            or json_result['message']['text']
                            == '/miguel_couto@Dz7Telecom_bot'
                        ):
                            # send image.
                            name_img = ('signal_dwdm_pta',)
                            bot_api.process_download_and_send_graph(signal_dwdm_pta,name_img)

                            # send text.
                            zabbix_bot_api.signal_miguel_couto(),

                            print(get_rota_miguel_couto),

                            rota_miguel_couto = (
                                [
                                    '========================== \n'
                                    'SINAL ROTA MIGUEL COUTO: \n'
                                    '\n'
                                    'Transceiver XGE0/0/1: \n'
                                    '{}{}'.format(
                                        get_rota_miguel_couto[0]['lastvalue'],
                                        (get_rota_miguel_couto[0]['units']),
                                    )
                                    + '\n'
                                    '\n'
                                    'Transceiver XGE0/0/2: \n'
                                    '{}{}'.format(
                                        get_rota_miguel_couto[1]['lastvalue'],
                                        (get_rota_miguel_couto[1]['units']),
                                    )
                                    + '\n'
                                    '\n'
                                    'Transceiver XGE0/0/3: \n'
                                    '{}{}'.format(
                                        get_rota_miguel_couto[3]['lastvalue'],
                                        (get_rota_miguel_couto[3]['units']),
                                    )
                                    + '\n'
                                    '\n'
                                    'Transceiver XGE0/0/4: \n'
                                    '{}{}'.format(
                                        get_rota_miguel_couto[2]['lastvalue'],
                                        (get_rota_miguel_couto[2]['units']),
                                    )
                                    + '\n'
                                    '=========================='
                                ],
                            )
                            api_telegram.send_message(
                                token, chat_id, rota_miguel_couto
                            ),
                            message_id_global = int(
                                json_result['message']['message_id']
                            )
                            break

                        elif (
                            json_result['message']['text'] == '/incidentes_1d'
                            or json_result['message']['text']
                            == '/incidentes_1d@Dz7Telecom_bot'
                        ):
                            global timestamp_today
                            message = []

                            zbx = ZabbixAPI(
                                server='https://zbx.dz7telecom.com.br/'
                            )
                            login = zbx.login('dz7bot', '965&tx5siKN!')

                            bot_api.convert_date_to_datime()

                            get_problem = zbx.problem.get(
                                {
                                    'output': 'extend',
                                    'time_from': timestamp_today,
                                    'sortfield': ['eventid'],
                                }
                            )

                            # envia problema por problema.
                            for i in range(len(get_problem)):
                                message = (
                                    10 * '=='
                                    + '\n'
                                    + '{}'.format([i])
                                    + '- '
                                    + get_problem[i]['name']
                                    + '\n'
                                    + 10 * '=='
                                )
                                api_telegram.send_message(
                                    token, chat_id, message
                                )

                            message_id_global = int(
                                json_result['message']['message_id']
                            )
                            break

                        elif (
                            json_result['message']['text'][:9] == '/consulta'
                            or json_result['message']['text'][:25]
                            == '/consulta@Dz7Telecom_bot'
                        ):
                            global hostname_db_mysql
                            global user_db_mysql
                            global passwd_db_mysql
                            global name_db_mysql
                            
                            msg_split = json_result['message']['text'].split()

                            if msg_split[1] == 'olt':
                                OLT = "'"+msg_split[2]+"'"
                                PLACA = "'"+msg_split[4]+"'"
                                PON = "'"+msg_split[6]+"'"

                                try:

                                    connection = mysql_api.create_server_connection(hostname_db_mysql, user_db_mysql, passwd_db_mysql, name_db_mysql)
                                    query = "SELECT * FROM olt WHERE sigla={}".format(OLT)+" AND"+" placa={}".format(PLACA)+" AND"+" pon={}".format(PON)+";"
                                    result = mysql_api.read_query(connection, query)

                                    msg_format= ['OLT : {}'.format(result[0][1])+'\n'
                                                 'PLACA: {}'.format(result[0][2])+'\n'
                                                 'PON: {}'.format(result[0][3])+'\n'
                                                 'HUB: {}'.format(result[0][4])+2*'\n'+
                                                 'NAP: {}'.format(result[0][5])+2*'\n'+
                                                 'ENDEREÇOS: {}'.format(result[0][6])+2*'\n'+
                                                 'LOC_HUB: https://www.google.com.br/maps/place/{},{}'.format(result[0][7],result[0][8])]

                                    api_telegram.send_message(token,chat_id,msg_format),
                            
                                    message_id_global = int(
                                        json_result['message']['message_id']
                                    )
                                    break

                                except Exception as e:
                                    print('Erro', e),
                                    message = ['Desculpa eu não entendi! =)']
                                    api_telegram.send_message(token,chat_id,message),
                                    message_id_global = int(
                                        json_result['message']['message_id']
                                    )
                                    break

                            elif msg_split[1] == 'nap':
                                NAP = msg_split[2]

                                try:

                                    connection = mysql_api.create_server_connection(hostname_db_mysql, user_db_mysql, passwd_db_mysql, name_db_mysql)
                                    query = "SELECT * FROM olt WHERE nap LIKE "+"'%{}%'".format(NAP)+";"
                                    result = mysql_api.read_query(connection, query)

                                    msg_format= ['OLT : {}'.format(result[0][1])+'\n'
                                                 'PLACA: {}'.format(result[0][2])+'\n'
                                                 'PON: {}'.format(result[0][3])+'\n'
                                                 'HUB: {}'.format(result[0][4])+2*'\n'+
                                                 'NAP: {}'.format(result[0][5])+2*'\n'+
                                                 'ENDEREÇOS: {}'.format(result[0][6])+2*'\n'+
                                                 'LOC_HUB: https://www.google.com.br/maps/place/{},{}'.format(result[0][7],result[0][8])]

                                    api_telegram.send_message(token,chat_id,msg_format),
                            
                                    message_id_global = int(
                                        json_result['message']['message_id']
                                    )
                                    break
                                
                                except Exception as e:
                                    print('Erro', e),
                                    message = ['Desculpa eu não entendi! =)']
                                    api_telegram.send_message(token,chat_id,message),
                                    message_id_global = int(
                                        json_result['message']['message_id']
                                    )
                                    break

                            elif msg_split[1] == 'hub':
                                HUB = msg_split[2]

                                try:

                                    connection = mysql_api.create_server_connection(hostname_db_mysql, user_db_mysql, passwd_db_mysql, name_db_mysql)
                                    query = "SELECT * FROM olt WHERE hub LIKE "+"'%{}%'".format(HUB)+";"
                                    print(query)
                                    result = mysql_api.read_query(connection, query)

                                    msg_format= ['OLT : {}'.format(result[0][1])+'\n'
                                                 'PLACA: {}'.format(result[0][2])+'\n'
                                                 'PON: {}'.format(result[0][3])+'\n'
                                                 'HUB: {}'.format(result[0][4])+2*'\n'+
                                                 'NAP: {}'.format(result[0][5])+2*'\n'+
                                                 'ENDEREÇOS: {}'.format(result[0][6])+2*'\n'+
                                                 'LOC_HUB: https://www.google.com.br/maps/place/{},{}'.format(result[0][7],result[0][8])]

                                    api_telegram.send_message(token,chat_id,msg_format),
                            
                                    message_id_global = int(
                                        json_result['message']['message_id']
                                    )
                                    break
                                
                                except Exception as e:
                                    print('Erro', e),
                                    message = ['Desculpa eu não entendi! =)']
                                    api_telegram.send_message(token,chat_id,message),
                                    message_id_global = int(
                                        json_result['message']['message_id']
                                    )
                                    break
                            
                        else:
                            break
                    break
                else:
                    pass   # return print('Não é bot command')
        else:
            return print(
                'A resposta falhou, código de status: {}'.format(
                    response.status_code
                )
            )
    except Exception as e:
        print('Erro no getUpdates:', e),
        message_id_global = int(
                                    json_result['message']['message_id']
                                )


x = 0

while x == 0:
    get_update_chat(token)
    time.sleep(2)
