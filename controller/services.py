# -*- coding: utf-8 -*-

import socket
import json, requests
from updateTables import *
from ctypes import *
import logging
from models import *
from updateTables import *


def checkRegister(number):
    serverName = '10.10.10.173'
    serverPort = 8888
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    sentence = {
        "Action": "Check",
        "PhoneNumber": number
    }
    clientSocket.send(json.dumps(sentence))
    modifiedSentence = clientSocket.recv(20480)
    clientSocket.close()
    return modifiedSentence


def bankConnection(kiosk_id, functionName, number, paid, product_profile_id, cashOrCard, order_trans_id):
    logging.info("bankConnection")
    logging.info(kiosk_id)
    serviceName = ""
    if kiosk_id == "2":
        serviceName = "Kiosk"
    if kiosk_id == "1":
        serviceName = "Kiosk_2"
    if kiosk_id == "3":
        serviceName = "Kiosk_3"
    to_bill = dict()
    to_bill["serviceName"] = serviceName
    to_bill["phone_number"] = number
    if functionName != "invoice":
        to_bill["trans_id"] = order_trans_id
        to_bill["amount"] = str(paid)
        to_bill["card"] = product_profile_id
        to_bill["cashOrCard"] = cashOrCard
    data = Encode(to_bill)
    logging.info(to_bill)
    url = "https://banksystem.gmobile.mn/service.php/api_services/kiosk/socialPay/" + functionName + "/response"
    try:
        return requests.post(url=url, data=data)
    except get_errno() == 10060 or get_errno() == 10061:
        return False


def ebarimt(customerNo, billType, cashAmount, nonCashAmount, product_name):
    cashAmount = "%.2f" % float(cashAmount)
    nonCashAmount = "%.2f" % float(nonCashAmount)
    if cashAmount > nonCashAmount:
        vat = float(cashAmount) / 11
        amount = cashAmount
    else:
        vat = float(nonCashAmount) / 11
        amount = nonCashAmount
    vat = "%.2f" % vat
    code = sku(product_name)
    data = {
        "amount": amount,
        "vat": vat,
        "customerNo": customerNo,
        "billType": billType,
        "cashAmount": cashAmount,
        "nonCashAmount": nonCashAmount,
        "cityTax": "0.00",
        "districtCode": "35",
        "posNo": "",
        "returnBillId": "",
        "invoiceId": "",
        "reportMonth": "",
        "branchNo": "",
        "stocks": [
            {
                "code": product_name,
                "name": product_name,
                "measureUnit": "1",
                "qty": "1.00",
                "unitPrice": amount,
                "totalAmount": amount,
                "cityTax": "0.00",
                "vat": vat,
                "barCode": code
            }
        ],
        "bankTransactions": []
    }
    ilgeeh = json.dumps(data)
    logging.info("data")
    logging.info(ilgeeh)
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        soc.connect(('10.10.10.173', 8008))
        soc.send(ilgeeh)
        datas = soc.recv(10240)
        soc.close()
        datas = json.loads(datas)
        logging.info("datas")
        logging.info(datas)
        if "lotteryWarningMsg" in datas:
            return False
        return datas
    except soc.error, e:
        if e.errno == 10060 or e.errno == 10061:
            # except get_errno() == 10061 or get_errno() == 10060:
            soc.close()
            return False


# def getNumber(number, az, numbertype):
#     # if numbertype == "3":
#     numbertype = "2"
#
#     first4 = number[0:4]
#     last4 = number[4:8]
#
#     res = checkLast4(last4)
#     ontsgoiDugaar = "engiin"
#     if az == "5":
#         if last4 == "AAAA":
#             ontsgoiDugaar = "alt1"
#         last4 = "****"
#     if az == "7":
#         if last4 == "DEAB":
#             ontsgoiDugaar = "mungu1"
#         if last4 == "ABDE":
#             ontsgoiDugaar = "mungu2"
#         if last4 == "AABB":
#             ontsgoiDugaar = "mungu3"
#         last4 = "****"
#     if az == "9":
#         if last4 == "ABBA":
#             ontsgoiDugaar = "hurel1"
#         if last4 == "ABAB":
#             ontsgoiDugaar = "hurel2"
#         last4 = "****"
#     if az == "6":
#         if res == "alt1":
#             az = "5"
#             ontsgoiDugaar = "alt1"
#         if res == "mungu1" or res == "mungu2" or res == "mungu3":
#             az = "7"
#             ontsgoiDugaar = "mungu3"
#         if res == "hurel1":
#             az = "9"
#             ontsgoiDugaar = "hurel1"
#         if res == "hurel2":
#             az = "9"
#             ontsgoiDugaar = "hurel2"
#
#     prefixList = list(Prefix.objects.filter(is_active=1, prefix__contains=number[0:2], category=numbertype).order_by("prefix"))
#     i = 0
#     numbers = []
#
#     if numbertype == "2":
#         if number[2] == "*":
#             if number[3] == "*":
#                 if res == "engiin":
#                     if (number[4:6] != "**" and number[6:8] == "**") or (number[4] == "*" and number[5:7] != "**" and number[7] == "*") or (number[4] != "*" and number[5:7] == "**" and number[7] != "*") \
#                             or (number[4:6] == "**" and number[6:8] != "**") or (number[4] != "*" and number[5] == "*" and number[6] != "*" and number[7] == "*") \
#                             or (number[4] == "*" and number[5] != "*" and number[6] == "*" and number[7] != "*") or (number[2:8] == "******"):
#                         first4 = str(prefixList[i].prefix)
#                     else:
#                         first4 = first4
#                 else:
#                     if ontsgoiDugaar != "engiin":
#                         if az == "7" or az == "9":
#                             first4 = str(prefixList[i].prefix)
#             else:
#                 digit4 = []
#                 for j in range(0, len(prefixList)):
#                     if str(prefixList[j].prefix)[3] == number[3]:
#                         digit4.append(prefixList[j].prefix)
#                 first4 = str(digit4[i])
#         if number[2] == "1" and number[3] == "*":
#             first4 = str(prefixList[i].prefix)
#
#     start = first4 + last4
#     prefix = ''.join(str(k) for k in start)
#
#     socket_results = FilternumberBlockUnblock("filter", prefix, az, "", "", "")
#     # socket_results = FilternumberBlockUnblock("filter", "", utga, prefix, az, "")
#     if socket_results != "-1":
#         socket_results = socket_results.split('|')
#     else:
#         socket_results = None
#     if socket_results != None:
#         for number in socket_results:
#             data = number.split(":")
#             if data[1] == az:
#                 numbers.append(data[0])
#
#     tmp = []
#     i = 0
#     while (i < len(numbers)):
#         numero = numbers[i]
#         numero = numero[0:4]
#         if Prefix.objects.filter(is_active=1, prefix__contains=numero, category=numbertype).exists() and numero != "9811":
#             tmp.append(numbers[i])
#         i += 1
#     numbers = tmp
#
#     num = []
#     if numbers != None:
#         for number in numbers:
#             if checkDigit(number) == ontsgoiDugaar:
#                 # data_number[str(number)] = number
#                 num.append({
#                     "prefix": number
#                 })
#             # if len(numbers) >= 100:
#             #     break
#
#     result = num
#
#     return result

def getNumber(prefix, az, numbertype):
    # move = int(request.GET['move'])
    # prefix = request.GET["prefix"]
    # az = request.GET['az']
    # numbertype = "2"
    if numbertype == "3":
        numbertype = "2"
    logging.info(prefix)
    # if numbertype == "4":
    #     prefix[0:2] = "DE"

    first4 = prefix[0:4]
    last4 = prefix[4:8]

    logging.info(prefix)

    ontsgoiDugaar = "engiin"

    if az != "6":
        if prefix == "DEAAAAAA":
            ontsgoiDugaar = "brilliant"
        if prefix == "DEABCCCC":
            ontsgoiDugaar = "alt1"
        if prefix == "DEAAAADE":
            ontsgoiDugaar = "alt2"
        if prefix == "DEAADEAA":
            ontsgoiDugaar = "alt3"
        if prefix == "DEAABBAA":
            ontsgoiDugaar = "alt4"
        if prefix == "DEBBAAAA":
            ontsgoiDugaar = "alt5"
        if prefix == "DEAAAABB":
            ontsgoiDugaar = "alt6"
        if prefix == "DExxABAB":
            ontsgoiDugaar = "mungu1"
        if prefix == "DExxABBA":
            ontsgoiDugaar = "mungu2"
        if prefix == "DExxAABB":
            ontsgoiDugaar = "mungu3"
        if prefix == "DEAAABBB":
            ontsgoiDugaar = "mungu4"
        if prefix == "DEABDEAB":
            ontsgoiDugaar = "mungu5"
        if prefix == "DEABABDE":
            ontsgoiDugaar = "mungu6"
        if prefix == "DExx000B":
            ontsgoiDugaar = "hurel1"
        if prefix == "DExxB000":
            ontsgoiDugaar = "hurel2"
        if prefix == "DEABABED":
            ontsgoiDugaar = "hurel3"
        if prefix == "DEABBAED":
            ontsgoiDugaar = "hurel4"
        last4 = "****"
    logging.info(ontsgoiDugaar)

    if ontsgoiDugaar == "engiin":
        prefixList = list(Prefix.objects.filter(is_active=1, prefix__contains=prefix[0:2], category=numbertype).order_by("prefix"))
    else:
        prefixList = list(Prefix.objects.filter(is_active=1, category=numbertype).order_by("prefix"))
    logging.info(prefixList)
    i = 0
    numbers = []

    if numbertype == "2":
        if prefix[2] == "*":
            if prefix[3] == "*":
                if ontsgoiDugaar == "engiin":
                    if (prefix[4:6] != "**" and prefix[6:8] == "**") or (prefix[4] == "*" and prefix[5:7] != "**" and prefix[7] == "*") or (prefix[4] != "*" and prefix[5:7] == "**" and prefix[7] != "*") \
                            or (prefix[4:6] == "**" and prefix[6:8] != "**") or (prefix[4] != "*" and prefix[5] == "*" and prefix[6] != "*" and prefix[7] == "*") \
                            or (prefix[4] == "*" and prefix[5] != "*" and prefix[6] == "*" and prefix[7] != "*") or (prefix[2:8] == "******"):
                        first4 = str(prefixList[i].prefix)
                    else:
                        first4 = first4
                else:
                    if ontsgoiDugaar != "engiin":
                        if az == "7" or az == "9":
                            first4 = str(prefixList[i].prefix)
            else:
                digit4 = []
                for j in range(0, len(prefixList)):
                    if str(prefixList[j].prefix)[3] == prefix[3]:
                        digit4.append(prefixList[j].prefix)
                first4 = str(digit4[i])
        if prefix[2] == "1" and prefix[3] == "*":
            first4 = str(prefixList[i].prefix)

    # logging.info(first4)
    # logging.info(last4)
    d = 0
    if ontsgoiDugaar != "engiin":
        while len(numbers) < 132:
            first4 = str(prefixList[d].prefix)
            # logging.info(first4)
            # start = first4 + last4
            # prefix = ''.join(str(k) for k in start)

            socket_results = FilternumberBlockUnblock("filter", "1", first4, az, "", "", "")
            if socket_results != "-1":
                socket_results = socket_results.split('|')
            else:
                socket_results = None
            if socket_results != None:
                for number in socket_results:
                    data = number.split(":")
                    if data[1] == az:
                        numbers.append(data[0])
            # logging.info(numbers)
            d += 1
            if d == len(prefixList):
                break
    else:
        logging.info("ELSE")
        logging.info(first4)
        logging.info(last4)
        start = first4 + last4
        prefix = ''.join(str(k) for k in start)

        socket_results = FilternumberBlockUnblock("filter", "3", prefix, az, "", "", "")
        if socket_results != "-1":
            socket_results = socket_results.split('|')
        else:
            socket_results = None
        if socket_results != None:
            for number in socket_results:
                data = number.split(":")
                # logging.info(data[1])
                if data[1] == az:
                    numbers.append(data[0])

    logging.info("numbers")
    logging.info(numbers)
    tmp = []
    i = 0
    while (i < len(numbers)):
        numero = numbers[i]
        numero = numero[0:4]
        # logging.info(numero)
        if Prefix.objects.filter(is_active=1, prefix__contains=numero, category=numbertype).exists() and numero != "9811":
            tmp.append(numbers[i])
        i += 1
    logging.info("tmp")
    logging.info(tmp)
    numbers = tmp

    # if 'movedown' in request.GET:
    #     # if socket_results != None:
    #     if len(numbers) > move + 24:
    #         numbers = numbers[move:move + 24]
    #         move = move + 24
    #     elif len(numbers) - move > 0:
    #         numbers = numbers[move:len(numbers)]
    #         move = move + 24
    #     elif len(numbers) == 0:
    #         move = 24
    #         numbers = None
    #     else:
    #         move = len(numbers) - 24
    #         # else:
    #         #   numbers = None
    # else:
    #     # if socket_results != None:
    #     if len(numbers) != 0:
    #         if move > 24:
    #             numbers = numbers[move - 24:move + 23]
    #             move = move - 24
    #         elif move <= 24:
    #             numbers = numbers[0:24]
    #             move = 24
    #     else:
    #         numbers = None
    #         move = 24
    #         # else:
    #         #   numbers = None

    # result = []
    # data_number = dict()
    # if numbers != None:
    #     for number in numbers:
    #         if checkNumber(number) == ontsgoiDugaar:
    #             # logging.info("match")
    #             data_number[str(number)] = number
    # logging.info("data_number")
    # logging.info(data_number)
    # result.append(data_number)
    # result.append(move)
    # logging.info(result)
    # # result.append(res)
    #
    # return Response(result)
    num = []
    if numbers != None:
        for number in numbers:
            if checkNumber(number) == ontsgoiDugaar:
                # data_number[str(number)] = number
                num.append({
                    "prefix": number
                })
            # if len(numbers) >= 100:
            #     break

    result = num

    return result


# def checkLast4(last4):
#     oron5 = last4[0:1]
#     oron6 = last4[1:2]
#     oron7 = last4[2:3]
#     oron8 = last4[3:4]
#
#     if oron5 != "*" and oron6 != "*" and oron7 != "*" and oron8 != "*": # last4 != "****"
#         # golden shalgah DEABCCCC, DECBCCCC, DEACCCCC
#         if ((oron5 == oron6) and (oron6 == oron7) and (oron7 == oron8)):
#             return "alt1"
#         # silver shalgah DEABABDE, DExxAABB, DEABDEAB
#         # DEABDEAB
#         # if ((oron1 == oron5) and (oron2 == oron6) and (oron3 == oron7) and (oron4 == oron8)):
#         #     return "mungu1"
#         # # DEABABDE
#         # if ((oron1 == oron7) and (oron2 == oron8) and (oron3 == oron5) and (oron4 == oron6) and (oron3 != oron4)):
#         #     return "mungu2"
#         # DExxAABB
#         if ((oron5 == oron6) and (oron7 == oron8) and (oron6 != oron7)):
#             return "mungu3"
#
#         # hurel shalgah DExxABBA, DExxABAB
#         # DExxABBA
#         if ((oron5 == oron8) and (oron6 == oron7)):
#             return "hurel1"
#         # DExxABAB
#         if ((oron5 == oron7) and (oron6 == oron8)):
#             return "hurel2"
#         else:
#             return "engiin"
#     else:
#         return "engiin"


def FilternumberBlockUnblock(turul, search_type, number, az, user, user_ip, sales_id):
    soc = socket.socket()
    soc.connect(('10.10.10.173', 8088))
    if turul == "filter":
        request_string = "0003ACC_QUERY:0|{0}|100|{1}|{2}".format(search_type, number, az)
    elif turul == "block":
        request_string = "0003Block:{0}|{1}|0|{2}|{3}|Kiosk".format(number, "blockkiosk-" + str(user.encode('utf-8')), user_ip, sales_id)
        # request_string = "0003Block:{0}|{1}".format(number, user.encode('utf-8'))
    else:
        request_string = "0003Unblock:{0}|{1}|0|{2}|{3}|Kiosk".format(number, "unblockkiosk-" + str(user.encode('utf-8')),
                                                                    user_ip, sales_id)
        # request_string = "0003Unblock:{0}".format(number)
    soc.send(request_string)
    socket_results = soc.recv(2048)
    logging.info(socket_results)
    soc.close()
    return socket_results


def huruuniiHee(register, fingerprint):
    logging.info("huruuniiHee")
    data = {
        'service_name': 'WS100103_getCitizenAddressInfo',
        'request_data': {
            'auth': {
                'citizen': {
                    'regnum': register,
                    'fingerprint': fingerprint
                },
                'operator': {
                    'regnum': register,
                    'fingerprint': fingerprint
                }
            },
            'regnum': register
        }
    }
    url = "http://192.168.18.47/service.php/service_api/webserver/1/post_json/xyp/citizen/response"
    headers = {'content-type': 'application/json'}
    hariu = requests.post(url, data=json.dumps(data), headers=headers)
    logging.info("hariu")
    h = json.loads(hariu.text)
    logging.info(h)
    return h


def simSergeehOrNewNumber(turul, sold_sim_id, price_plan_id, user_id, kiosk_id, numbertype_types_id, tipo):
    sim = Sims.objects.get(id=sold_sim_id)
    price_plan = PricePlan.objects.get(id=price_plan_id)
    user = Users.objects.get(id=user_id)
    kiosk = Status.objects.get(id=kiosk_id)
    sales_id = kiosk.sales_id
    sales_location_id = kiosk.sales_location_id
    ruim_type = kiosk.ruim_type

    serverName = '10.10.10.173'
    serverPort = 8888
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))

    if turul == "restoresim":
        action = "Duplicate"
    else:
        action = "NewConnection"

    sentence = {
        "Action": action,
        "PhoneNumber": sim.number,
        "ICCID": sim.serial,
        "KioskID": sales_id,
        "KioskLocationID": sales_location_id,
        "RUIMType": ruim_type,
        "ProdType": "3",
        "Package": price_plan.code,
        "CustomerType": "%Хувь хүн",
        "Email": "mail",
        "OfficePhone": "phone_num",
        "HomePhone": "home_phone",
        "Credit_Limit": "0",
        "Sales_Branch": kiosk.address,
        "Sales_Name": kiosk.name,
        "Sales_User": "Kiosk",
        "Invoice_Type": "Өөрт нь өгөх",
        "Customer_Type": "Individual",
        "Enjoy_Invite": "",
        "ParentID": "",
        "Sector": "",
        "JobTitle": "",
        "JobName": "",
        "Pre_to_Post": "",
        "Zone": "",
        "Parameters": "",
        "Profile": [{
            "Customer_Name": user.last_name + " " + user.first_name,
            "Cert_type": "Регистер",
            "Cert_Number": user.register,
            "Address": user.address,
            "Gender": user.gender,
            "Birthday": user.birthday,
            "City": user.city,
            "Soum": user.soum
        }],
        "Price": sim.number_price
    }

    # if turul == "restoresim":
    #     sentence = {
    #         "Action": "Duplicate",
    #         "PhoneNumber": sim.number,
    #         "ICCID": sim.serial,
    #         "AgentID": sales_id,
    #         "KioskLocationID": sales_location_id,
    #         "RUIMType": ruim_type,
    #         "SoldPrice": sim.number_price
    #     }
    # else:
    #     sentence = {
    #         "Action": "NewConnection",
    #         "PhoneNumber": sim.number,
    #         "ICCID": sim.serial,
    #         "AgentID": sales_id,
    #         "KioskLocationID": sales_location_id,
    #         "RUIMType": ruim_type,
    #         "ProdType": "3",
    #         "Package": price_plan.code,
    #         "Profile": [
    #             {
    #                 "Customer_Name": user.first_name,
    #                 "Cert_type": "Регистер",
    #                 "Cert_Number": user.register,
    #                 "Address": user.address,
    #                 "Gender": user.gender,
    #                 "Birthday": user.birthday,
    #                 "City": user.city,
    #                 "Soum": user.soum
    #             }
    #         ],
    #         "SoldPrice": sim.number_price
    #     }
    logging.info(sentence)
    clientSocket.send(json.dumps(sentence))
    modifiedSentence = clientSocket.recv(20480)
    clientSocket.close()

    if modifiedSentence == "Success":
        shivelt(sim.id, kiosk.name, sim.number, sim.number_price,
                numbertype_types_id,
                price_plan.type_id, sim.serial[0:19], sim.created_at.date(),
                str(kiosk.name.encode('utf-8')) + str(tipo.encode('utf-8')), ruim_type)
    return modifiedSentence


def juulchinDugaar(price_plan_id, number):
    logging.info("juulchinDugaar")
    soc = socket.socket()
    soc.connect(('10.10.10.173', 8010))
    request_string = "0001ADD_TOURIST#976{0}#{1}".format(number, price_plan_id)
    logging.info(request_string)
    soc.send(request_string)
    socket_results = soc.recv(2048)
    logging.info(socket_results)
    soc.close()
    return socket_results


def shivelt(cashlog_id, kiosk_name, number, price, numbertype_types_id, price_plan_type_id, serial, date_time, comment, ruim_type):
    url = "http://192.168.18.232/SalesOnlineShiwelt/GAgentPrepaid.asmx/GAgentPrePaidServiceMothod"
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    da = {
        "access_from": "gagent",
        "transactionid": cashlog_id,
        "did": kiosk_name,
        "Phone": number,
        "TotalAmount": price,
        "TypesID": numbertype_types_id,
        "TypePricePlanID": price_plan_type_id,
        "serial": serial,
        "datetime": date_time,
        "Comment": comment,
        "cmb_paytype": "Борлуулалт",
        "ruimType": ruim_type,
    }
    hariu = requests.post(url, data=da, headers=headers)
    logging.info(hariu.text)


def checkBaiguullaga(register):
    url = "http://info.ebarimt.mn/rest/merchant/info?regno={0}".format(register)
    hariu = requests.get(url=url)
    return json.loads(hariu.text)