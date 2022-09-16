# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework import status
import logging
from rest_framework_jwt.settings import api_settings
from response import *
from services import *
from qpay import *
import time
from models import *

log_date = datetime.now().strftime('%Y-%m-%d')
log_file = '/home/ezen/kiosk/log/Log_{0}'.format(log_date)
logging.basicConfig(filename=log_file + '.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

# Create your views here.

@api_view(['POST'])
def jwt(request):
    logging.info("jwt")
    if request.method == 'POST':
        data = JSONParser().parse(request)
        device_id = data["device_id"]
        if Status.objects.filter(device_id=device_id).exists():
            kiosk = Status.objects.get(device_id=device_id)
            if Jwt.objects.filter(device_id=device_id).exists():
                jwt = Jwt.objects.get(device_id=device_id)
            else:
                jwt = Jwt()
                jwt.kiosk_id = kiosk.id
                jwt.username = kiosk.name
                jwt.device_id = kiosk.device_id
                jwt.save()
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

            payload = jwt_payload_handler(jwt)
            logging.info(payload)
            userJwt = jwt_encode_handler(payload)
            logging.info(userJwt)

            jwt.jwt = userJwt
            jwt.save()

            response = status_success(1, "Amjilttai", jwt.jwt)
        else:
            response = status_unsuccessful(1, None, "Burtgelgui kiosk baina jwt")
    else:
        response = status_unsuccessful(1, None, "Buruu method")

    return JsonResponse(response, status=status.HTTP_200_OK)


@api_view(['POST'])
def ads(request):
    logging.info("ads")
    # permission_classes = (IsAuthenticated,)
    if request.method == 'POST':
        ads = Ads.objects.filter(is_active=1)
        arr = []
        for i in range(len(ads)):
            arr.append({
                "id": ads[i].id,
                "url": ads[i].image
            })
        response = status_success(1, "ads", arr)
    else:
        response = status_unsuccessful(1, None, "Buruu method")

    return JsonResponse(response, status=status.HTTP_200_OK)


@api_view(['POST'])
def checkNumber(request):
    logging.info("checkNumber")
    # permission_classes = (IsAuthenticated,)
    if request.method == 'POST':
        data = JSONParser().parse(request)
        number = data["number"]
        turul = data["type"]
        jwtNew = data["jwt"]

        response = ""
        if Jwt.objects.filter(jwt=jwtNew).exists():
            kiosk_id = Jwt.objects.get(jwt=jwtNew).kiosk_id
            logging.info(kiosk_id)

            result = bankConnection(str(kiosk_id), "checkNumber", number, "", "", "", "")

            if len(result.content) > 128:
                result = DecodeProduct(result.content)
            else:
                result = Decode(result.content)
            # logging.info(result)
            result = json.loads(result)
            units = []
            datas = []
            honogtoi = []
            honoggui = []
            logging.info(result)
            if result["status"] == -1:
                message = ""
                if result["errors"] == "ER0001":
                    message = "Сервис нэр тохирохгүй байна"
                if result["errors"] == "ER0002":
                    message = "Урьдчилсан төлбөртөөр дараа төлбөрт дугаар орж ирсэн байна"
                if result["errors"] == "ER0003":
                    message = "Цэнэглэлт хийх боломжгүй утасны дугаар эсвэл дугаар олдоогүй"
                if result["errors"] == "ER0004":
                    message = "Цэнэглэгч карт тохирохгүй болон тохиролцсон утга зөрсөн"
                if result["errors"] == "ER0005":
                    message = "Цэнэглэлт амжилтгүй"
                if result["errors"] == "ER0006":
                    message = "Дараа төлбөртөөр урьдчилсан төлбөрт орж ирсэн"
                if result["errors"] == "ER0007":
                    message = "Ижил гүйлгээ дахин орж ирсэн"
                response = status_unsuccessful(1, None, message)
            else:
                if turul == "unit":
                    if result["status"] == 1:
                        message = "Таны оруулсан дугаар дараа төлбөрт дугаар тул нэгжээр цэнэглэх боломжгүй"
                        response = status_unsuccessful(1, None, message)
                    else:
                        for i in range(len(result["unit"])):
                            profile_code = str(result["unit"][i]["profile_code"])
                            if Unit.objects.filter(is_active=1, profile_id=profile_code, honog=0).exists():
                                unit = Unit.objects.get(is_active=1, profile_id=profile_code, honog=0)
                                honoggui.append({
                                    "profile_id": unit.profile_id,
                                    "url": unit.image,
                                    "price": unit.price
                                })
                        if len(honoggui) > 0:
                            units.append({
                                "name": "hyazgaargui",
                                "day": honoggui
                            })

                        for i in range(len(result["unit"])):
                            profile_code = str(result["unit"][i]["profile_code"])
                            if Unit.objects.filter(is_active=1, profile_id=profile_code, honog=1).exists():
                                unit = Unit.objects.get(is_active=1, profile_id=profile_code, honog=1)
                                honogtoi.append({
                                    "profile_id": unit.profile_id,
                                    "url": unit.image,
                                    "price": unit.price
                                })
                        if len(honogtoi) > 0:
                            units.append({
                                "name": "hyazgaartai",
                                "day": honogtoi
                            })
                        message = "amjilttai"
                        unitDataPost = {
                            "products": units
                        }
                        logging.info(unitDataPost)
                        response = status_success(0, message, unitDataPost)
                if turul == "data":
                    if result["status"] == 1:
                        message = "Таны оруулсан дугаар дараа төлбөрт дугаар тул нэгжээр цэнэглэх боломжгүй"
                        response = status_unsuccessful(1, None, message)
                    else:
                        if len(result["data"]) == 0:
                            logging.info(str(
                                number) + " дугаарын үйлчилгээний хугацаа дууссан байна. Та хоногтой картаар цэнэглэнэ үү! Line-231")
                            message = str(
                                number) + " дугаарын үйлчилгээний хугацаа дууссан байна. Та хоногтой картаар цэнэглэнэ үү!"
                            response = status_unsuccessful(1, "oneway", message)
                        else:
                            for i in range(len(result["data"])):
                                profile_code = str(result["data"][i]["profile_code"])
                                if Data.objects.filter(is_active=1, profile_id=profile_code, hyazgaar=1).exists():
                                    data = Data.objects.get(is_active=1, profile_id=profile_code, hyazgaar=1)
                                    honoggui.append({
                                        "profile_id": data.profile_id,
                                        "url": data.image,
                                        "price": data.price
                                    })
                            if len(honoggui) > 0:
                                datas.append({
                                    "name": "hyazgaargui",
                                    "day": honoggui
                                })
                            logging.info("datas hyazgaargui")
                            logging.info(datas)
                            for i in range(len(result["data"])):
                                profile_code = str(result["data"][i]["profile_code"])
                                if Data.objects.filter(is_active=1, profile_id=profile_code, hyazgaar=0).exists():
                                    data = Data.objects.get(is_active=1, profile_id=profile_code, hyazgaar=0)
                                    honogtoi.append({
                                        "profile_id": data.profile_id,
                                        "url": data.image,
                                        "price": data.price
                                    })
                            if len(honogtoi) > 0:
                                datas.append({
                                    "name": "hyazgaartai",
                                    "day": honogtoi
                                })
                            logging.info("datas hyazgaartai")
                            logging.info(datas)
                            message = "amjilttai"
                            unitDataPost = {
                                "products": datas
                            }
                            logging.info(unitDataPost)
                            response = status_success(0, message, unitDataPost)
                if turul == "post":
                    logging.info("post")
                    if result["status"] == 0:
                        message = "Таны оруулсан дугаар урьдчилсан төлбөрт дугаар байна"
                        response = status_unsuccessful(1, None, message)
                    else:
                        result = bankConnection(str(kiosk_id), "invoice", number, "", "", "", "")
                        if result.status_code == 404 or not result:
                            logging.error("Error: " + str(result.status_code) + ". Line-114")
                        result = Decode(result.content)
                        result = json.loads(result)
                        logging.info(result)
                        must_pay = int(result["value"])
                        register = checkRegister(number)
                        dat = {
                            "post": must_pay,
                            "register": register
                        }
                        message = "Таны оруулсан дугаар дараа төлбөрт дугаар тул нэгжээр цэнэглэх боломжгүй"
                        response = status_success(0, message, dat)
                elif turul == "restoresim":
                    register = checkRegister(number)
                    if result["status"] == -1:
                        err = "бүртгэлгүй буюу устсан дугаар тул сэргээх боломжгүй"
                        response = status_unsuccessful(1, None, err)
                    elif register == "Регистэрийн Дугааргүй хэрэглэгч" or register == "Регистэрийн Бүртгэлгүй хэрэглэгч":
                        err = "Регистэрийн Дугааргүй хэрэглэгч"
                        response = status_unsuccessful(1, None, err)
                    elif result["type"] == "CDMA":
                        err = "Таны сонгосон дугаарыг үүсгэх боломжгүй байна"
                        response = status_unsuccessful(1, None, err)
                    else:
                        if result["status"] == 0:
                            res = {
                                "register": register
                            }
                            response = status_success(1, None, res)
                        else:
                            result = bankConnection(str(kiosk_id), "invoice", number, "", "", "", "")
                            if result.status_code == 404 or not result:
                                logging.error("Error: " + str(result.status_code) + ". Line-114")
                                response = status_unsuccessful(1, None, str(result.status_code))
                            else:
                            # result = Decode(result.content)
                            # result = json.loads(result)
                            # logging.info(result)
                            # must_pay = int(result["value"])
                            # if must_pay <= 0:
                                res = {
                                    "register": register
                                }
                                response = status_success(1, None, res)
                            # else:
                            #     err = "төлбөрийн үлдэгдэлтэй тул сэргээх боломжгүй байна"
                            #     response = status_unsuccessful(1, None, err)
        else:
            response = status_unsuccessful(0, None, "Burtgelgui jwt baina checkNumber")
    else:
        response = status_unsuccessful(1, None, "Buruu method")

    return JsonResponse(response, status=status.HTTP_200_OK)


@api_view(['POST'])
def order(request):
    logging.info("order")
    if request.method == 'POST':
        data = JSONParser().parse(request)
        number = data["number"]
        turul = data["type"]
        profile_id = data["profile_id"]
        device_id = data["device_id"]
        payment = data["payment"]
        jwtNew = data["jwt"]
        logging.info(profile_id)
        if Jwt.objects.filter(jwt=jwtNew).exists():
            kiosk = Status.objects.get(device_id=device_id)
            order = Orders()
            if turul == "post":
                prepaid = 1
                order.product_name = "Дараа төлбөртийн төлөлт"
                order.must_pay = profile_id.split("-")[-1]
            else:
                prepaid = 0
                if turul == "unit":
                    unitData = Unit.objects.get(profile_id=profile_id, is_active=1)
                else:
                    unitData = Data.objects.get(profile_id=profile_id, is_active=1)
                order.product_name = unitData.name
                order.must_pay = unitData.price
            order.product_profile_id = profile_id
            order.number = number
            order.paid = "0"
            order.order_success = "0"
            order.kiosk_name = kiosk.name
            order.prepaid = prepaid
            order.save()
            order.trans_id = order.id
            order.save()

            q_pay = {}
            message = "Amjilttai"
            if payment == "qpay":
                invoice_response = invoice(str(order.id), order.product_name, order.must_pay)
                logging.info("invoice_response")
                logging.info(invoice_response)
                if 'error' in invoice_response:
                    message = invoice_response["message"]
                else:
                    logging.info("invoice_id")
                    logging.info(invoice_response["invoice_id"])
                    q_pay = {
                        "invoice_id": invoice_response["invoice_id"],
                        "qr_image": invoice_response["qr_image"]
                    }
            dat = {
                "order_id": order.id,
                "q_pay": q_pay
            }
            logging.info("dat")
            logging.info(dat)
            response = status_success(1, message, dat)
        else:
            logging.info("not exists jwt")
            message = "Burtgelgui jwt baina order"
            response = status_unsuccessful(1, None, message)
    else:
        response = status_unsuccessful(1, None, "Buruu method")

    return JsonResponse(response, status=status.HTTP_200_OK)


@api_view(['POST'])
def charge(request):
    logging.info("charge")
    if request.method == 'POST':
        data = JSONParser().parse(request)
        number = data["number"]
        turul = data["type"]
        paid = data["paid"]
        order_id = data["order_id"]
        payment = data["payment"]
        jwtNew = data["jwt"]
        logging.info(paid)
        # logging.info(int(paid))
        logging.info(order_id)
        if Jwt.objects.filter(jwt=jwtNew).exists():
            order = Orders.objects.get(id=order_id)
            kiosk = Status.objects.get(name=order.kiosk_name)

            if int(kiosk.id) > 2:
                order.paid = int(order.paid) + int(paid)
                order.save()
            logging.info("Хүлээж авсан мөнгө: " + str(order.must_pay) + "=" + str(order.paid))

            if int(order.must_pay) == int(order.paid):
                if turul == "unit" or turul == "data":
                    functionName = "setPrePaidCharge"
                else:
                    functionName = "setPostPaidCharge"
                addcashlog(kiosk.id, order.paid, order.product_name, payment, "1", order_id, "0")
                kiosk.cash_total = kiosk.cash_total + int(order.paid)
                kiosk.save()
                logging.info("Нийт бэлэн мөнгө=" + str(kiosk.cash_total))

                result = bankConnection(str(kiosk.id), functionName, number, str(order.paid), order.product_profile_id,
                                        "Киоск{0}_{1}".format(kiosk.id, payment), order.trans_id)
                if result.status_code == 404 or not result:
                    logging.error("Error: " + str(result.status_code) + ". Line-211")

                result = Decode(result.content)
                logging.info(result)
                if  "Success" in result:
                    order.order_success = 1
                    order.save()

                response = status_success(1, "amjilttai", order.id)
            else:
                message = "Mungun dun taarahgui baina"
                response = status_unsuccessful(1, None, message)
        else:
            message = "Burtgelgui jwt baina charge"
            response = status_unsuccessful(1, None, message)
    else:
        response = status_unsuccessful(1, None, "Buruu method")

    return JsonResponse(response, status=status.HTTP_200_OK)


@api_view(['POST'])
def prefix(request):
    logging.info("prefix")
    if request.method == 'POST':
        data = JSONParser().parse(request)
        numbertype = data["numbertype"]
        jwt = data["jwt"]
        if Jwt.objects.filter(jwt=jwt).exists():
            pre = Prefix.objects.filter(category=numbertype)
            prefix = []
            for i in range(len(pre)):
                prefix.append({
                    "prefix": str(pre[i].prefix)
                })
            response = status_success(1, "Prefix", prefix)
        else:
            response = status_unsuccessful(0, None, "Burtgelgui jwt prefix")
    else:
        response = status_unsuccessful(1, None, "Buruu method")

    return JsonResponse(response, status=status.HTTP_200_OK)


@api_view(['POST'])
def searchNumber(request):
    logging.info("searchNumber")
    if request.method == 'POST':
        data = JSONParser().parse(request)
        number = data["number"]
        az = data["az"]
        numbertype = data["numbertype"]
        jwt = data["jwt"]
        if Jwt.objects.filter(jwt=jwt).exists():
            result = getNumber(number, az, numbertype)
            logging.info(result)
            response = status_success(1, None, result)
        else:
            response = status_unsuccessful(0, None, "Burtgelgui jwt searchNumber")
    else:
        response = status_unsuccessful(1, None, "Buruu method")

    return JsonResponse(response, status=status.HTTP_200_OK)


@api_view(['POST'])
def blockUnblock(request):
    logging.info("blockUnblock")
    if request.method == 'POST':
        data = JSONParser().parse(request)
        number = data["number"]
        device_id = data["device_id"]
        block = data["block"]
        logging.info(block)
        bagts_id = data["bagts"]
        number_type = data["numbertype"]
        az = data["az"]
        jwt = data["jwt"]
        logging.info(bagts_id)
        user_ip = get_client_ip(request)
        logging.info("user_ip: " + str(user_ip))
        if Jwt.objects.filter(jwt=jwt).exists():
            kiosk = Status.objects.get(device_id=device_id)
            kiosk_name = "kiosk{0}".format(kiosk.id)
            socket_results = FilternumberBlockUnblock(block, "", number, "", kiosk_name, user_ip, kiosk.sales_id)
            if socket_results == "Success":
                if block == "block":
                    numbertype = Numbertype.objects.get(id=number_type)
                    aziinDugaar = AziinDugaar.objects.get(type=az)

                    # if bagts_id == "":
                    #     result = {
                    #         "negj": "",
                    #         "data": "",
                    #         "honog": "",
                    #         "nuhtsul": "",
                    #         "une": ""
                    #     }
                    # else:
                    if Bagts.objects.filter(id=bagts_id).exists():
                        bagts = Bagts.objects.get(id=bagts_id)
                        # bagts_une = bagts.une
                        number_price = numbertype.price + aziinDugaar.price + bagts.une

                        logging.info(number_price)
                        result = {
                            "negj": bagts.negj,
                            "data": bagts.data,
                            "honog": bagts.honog,
                            "nuhtsul": bagts.nuhtsul,
                            "price": number_price
                        }
                    else:
                        result = "Not found bagts id"
                else:
                    logging.info("unblock")
                    result = "Unblocked"

                logging.info(result)
                message = ""
                response = status_success(1, message, result)
            else:
                message = "Таны сонгосон дугаар захиалганд орсон байна"
                response = status_unsuccessful(1, None, message)
        else:
            response = status_unsuccessful(1, None, "Burtgelgui jwt blockUnblock")
    else:
        response = status_unsuccessful(1, None, "Buruu method")

    return JsonResponse(response, status=status.HTTP_200_OK)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@api_view(['POST'])
def userConfirmation(request):
    logging.info("userConfirmation")
    if request.method == 'POST':
        data = JSONParser().parse(request)
        device_id = data["device_id"]
        register = data["register"]
        number = data["number"]
        product_name = data["product_name"]
        state = data["state"]
        jwt = data["jwt"]
        if Jwt.objects.filter(jwt=jwt).exists():
            kiosk = Status.objects.get(device_id=device_id)
            kiosk_name = "kiosk{0}".format(kiosk.id)
            date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            logging.info(kiosk_name + "|" + register + "|" + number + "|" + product_name + "|" + state + "|" + date_now)
            user_confirmation = UserConfirmation()
            user_confirmation.kiosk_name = kiosk_name
            user_confirmation.register = register
            user_confirmation.number = number
            user_confirmation.product_name = product_name
            user_confirmation.state = state
            user_confirmation.date = date_now
            user_confirmation.save()
            response = status_success(1, None, "Success")
        else:
            response = status_unsuccessful(1, None, "Burtgelgui jwt hur")
    else:
        response = status_unsuccessful(1, None, "Buruu method")
    return JsonResponse(response, status=status.HTTP_200_OK)


@api_view(['POST'])
def hur(request):
    logging.info("hur")
    if request.method == 'POST':
        data = JSONParser().parse(request)
        register = data["register"]
        fingerprint = data["fingerprint"]
        number_type = data["numbertype"]
        az = data["az"]
        bagts_id = data["bagts"]
        turul = data["type"]
        jwt = data["jwt"]
        logging.info(number_type)
        logging.info(bagts_id)
        if Jwt.objects.filter(jwt=jwt).exists():
            h = huruuniiHee(register, fingerprint)
            if "return" in h:
                resultCode = h["return"]["resultCode"]
                if resultCode == "0":
                    if turul == "post":
                        result = {
                            "sim_id": "",
                            "price": ""
                        }
                    else:
                        number_price = ""
                        numbertype = Numbertype.objects.get(id=number_type)
                        tipo = ""
                        if turul == "newnumber":
                            tipo = u"Дугаарын үнэ"
                            aziinDugaar = AziinDugaar.objects.get(type=az)
                            bagts = Bagts.objects.get(id=bagts_id)
                            number_price = numbertype.price + aziinDugaar.price + bagts.une
                            logging.info(numbertype.price)
                            logging.info(aziinDugaar.price)
                            # if numbertype == "4":
                            #     if bagts == "1":
                            #         number_price = 10000 + aziinDugaar.price
                            #     if bagts == "2":
                            #         number_price = 10000 + aziinDugaar.price
                            #     if bagts == "3":
                            #         number_price = 120000 + aziinDugaar.price
                            # if number_type == "5":
                            #     if bagts == "1":
                            #         number_price = 10000 + aziinDugaar.price
                            #     if bagts == "2":
                            #         number_price = 20000 + aziinDugaar.price
                            #     if bagts == "3":
                            #         number_price = 40000 + aziinDugaar.price
                            #
                            # logging.info(number_price)

                        if turul == "restoresim":
                            tipo = u"Сим сэргээсэн"
                            number_price = numbertype.price

                        user = Users()
                        user.family_name = h["return"]["response"]["surname"]
                        user.last_name = h["return"]["response"]["lastname"]
                        user.first_name = h["return"]["response"]["firstname"]
                        if register[2:4] > datetime.now().strftime("%y"):
                            user.birthday = "19" + str(register[2:4]) + "/" + str(register[4:6]) + "/" + str(register[6:8])
                        else:
                            user.birthday = "20" + str(register[2:4]) + "/" + str(int(register[4:6]) - 20) + "/" + str(
                                register[6:8])
                        if int(register[8:9]) % 2 == 0:
                            huis = "Эм"
                        else:
                            huis = "Эр"
                        user.gender = huis
                        reg = h["return"]["response"]["regnum"]
                        user.register = reg.upper()
                        user.address = h["return"]["response"]["fullAddress"]
                        user.city = h["return"]["response"]["aimagCityName"]
                        user.soum = h["return"]["response"]["soumDistrictName"]
                        user.save()

                        sim = Sims()
                        sim.user = Users.objects.get(id=user.id)
                        sold_sim = Sims()
                        sold_sim.is_sold = 0
                        sold_sim.user = sim.user
                        sold_sim.number_price = number_price
                        sold_sim.paid = "0"
                        sold_sim.number_type = numbertype
                        sold_sim.tipo = tipo
                        sold_sim.save()
                        result = {
                            "sim_id": str(sold_sim.id),
                            "price": str(number_price)
                        }
                    response = status_success(1, None, result)
                else:
                    if resultCode == "1":
                        logging.error("олдсонгүй. Line-453")
                        result = "Хуруу хээ олдсонгүй"
                    elif resultCode == "2":
                        logging.error("дотоод алдаа. Line-465")
                        result = "ХУР системтэй холбогдоход алдаа гарлаа. Та холбогдох ажилтанд хандана уу"
                    elif resultCode == "3":
                        logging.error("сертификатын алдаа. Line-459")
                        result = "ХУР системтэй холбогдоход алдаа гарлаа. Та холбогдох ажилтанд хандана уу"
                    elif resultCode == "301":
                        logging.error("Иргэний хурууны хээ бүртгэлгүй байна. Line-462")
                        result = "Иргэний хурууны хээ бүртгэлгүй байна"
                    elif resultCode == "302":
                        logging.error("Хуруу хээ таарахгүй байна. Line-465")
                        result = "Хуруу хээ таарахгүй байна"
                    elif resultCode == "303":
                        logging.error("Хурууны хээ тулгах процесс хэт удаан байна. Line-468")
                        result = "Хурууны хээ тулгах процесс хэт удаан байна"
                    elif resultCode == "304":
                        logging.error("Хурууны хээ тулгах процессд алдаа гарлаа. Line-471")
                        result = "Хурууны хээ тулгах процессд алдаа гарлаа"
                    elif resultCode == "401":
                        logging.error("Бүргэлийн газарт очиж бүртгэлээ шалгуулах шаардлагатай. Line-474")
                        result = "Бүргэлийн газарт очиж бүртгэлээ шалгуулах шаардлагатай"
                    elif resultCode == "402":
                        logging.error("Эзэмшигч биш болно. Line-477")
                        result = "Эзэмшигч биш болно"
                    else:
                        result = ""
                    response = status_unsuccessful(1, None, result)
            else:
                logging.error("ХУР системтэй холбогдоход алдаа гарлаа. Line-470")
                err = "ХУР системтэй холбогдоход алдаа гарлаа."
                response = status_unsuccessful(1, None, err)
        else:
            response = status_unsuccessful(1, None, "Burtgelgui jwt hur")
    else:
        response = status_unsuccessful(1, None, "Buruu method")

    return JsonResponse(response, status=status.HTTP_200_OK)


@api_view(['POST'])
def createNumber(request):
    logging.info("createNumber")
    if request.method == 'POST':
        data = JSONParser().parse(request)
        number_type = data['numbertype']
        turul = data['type']
        number = data['number']
        bagts = data['bagts']
        device_id = data["device_id"]
        sim_id = data['sim_id']
        paid = data['paid']
        payment = data['payment']
        serial = data['serial']
        az = data['az']
        jwt = data["jwt"]
        logging.info(bagts)
        if Jwt.objects.filter(jwt=jwt).exists():
            price_plan_id = PricePlan.objects.get(bagts_id=bagts).id

            numbertype = Numbertype.objects.get(id=number_type)
            kiosk = Status.objects.get(device_id=device_id)

            logging.info("Serial=" + str(serial[0:20]))
            sold_sim = Sims.objects.get(id=sim_id)
            sold_sim.serial = serial[0:20]
            sold_sim.number = number
            sold_sim.is_sold = 1
            sold_sim.paid = paid
            sold_sim.kiosk_name = kiosk.name
            sold_sim.save()

            addcashlog(kiosk.id, sold_sim.paid, sold_sim.tipo, payment, "1", "0", sold_sim.id)
            kiosk.cash_total = int(kiosk.cash_total) + int(sold_sim.paid)
            kiosk.save()

            kiosk.sim_card_total = kiosk.sim_card_total - 1
            logging.info("Total sim=" + str(kiosk.sim_card_total))
            kiosk.save()

            if turul == "newnumber":
                socket_results = FilternumberBlockUnblock("unblock", "", number, "", "", "", "")
                logging.info(socket_results)

            h = simSergeehOrNewNumber(turul, sold_sim.id, price_plan_id, sold_sim.user_id, kiosk.id, numbertype.types_id, sold_sim.tipo)
            logging.info("Dugaar uusgelt: " + h)
            h = "Success"
            if h == "Success":
                is_number_created = 1
                if number_type == "5":
                    time.sleep(120)
                    res = juulchinDugaar(price_plan_id, number)
                    if res == "SUCCESS":
                        is_number_created = 1
                    else:
                        is_number_created = 2
                        logging.info("juulchin dugaariin nemelt bagts amjiltgui")
                sold_sim.is_number_created = is_number_created
                sold_sim.save()
                if az != "6":
                    aziin_dugaar = AziinDugaar.objects.get(id=az)
                    shivelt(sold_sim.id, kiosk.name, sold_sim.number, aziin_dugaar.price, "24", "-1", "0",
                            sold_sim.created_at.date(),
                            str(kiosk.name.encode('utf-8')) + str(sold_sim.tipo.encode('utf-8')), "-1")

                response = status_success(1, "amjilttai", sold_sim.id)
                return JsonResponse(response, status=status.HTTP_200_OK)
            else:
                sold_sim.save()
                logging.error("Серверээс хариу авахад алдаа гарлаа. Line-1664")
                message = "Серверээс хариу авахад алдаа гарлаа"
                response = status_unsuccessful(1, None, message)
        else:
            response = status_unsuccessful(1, None, "Burtgelgui jwt createNumber")
    else:
        response = status_unsuccessful(1, None, "Buruu method")

    return JsonResponse(response, status=status.HTTP_200_OK)


@api_view(['POST'])
def payment(request):
    logging.info("payment")
    if request.method == 'POST':
        data = JSONParser().parse(request)
        payment = data["payment"]
        sim_id = data["sim_id"]
        jwt = data["jwt"]
        if Jwt.objects.filter(jwt=jwt).exists():
            q_pay = {}
            message = "Amjilttai"
            sim = Sims.objects.get(id=sim_id)
            if payment == "qpay":
                invoice_response = invoice(str(sim.id), str(sim.tipo.encode('utf-8')), str(sim.number_price))
                logging.info(invoice_response)
                if 'error' in invoice_response:
                    message = invoice_response["message"]
                else:
                    logging.info("invoice_id")
                    logging.info(invoice_response["invoice_id"])
                    q_pay = {
                        "invoice_id": invoice_response["invoice_id"],
                        "qr_image": invoice_response["qr_image"]
                    }
            response = status_success(1, message, q_pay)
        else:
            message = "Burtgelgui jwt baina"
            response = status_unsuccessful(1, None, message)
    else:
        response = status_unsuccessful(1, None, "Buruu method")
    return JsonResponse(response, status=status.HTTP_200_OK)


@api_view(['POST'])
def checkPayment(request):
    logging.info("checkPayment")
    if request.method == 'POST':
        data = JSONParser().parse(request)
        invoice_id = data["invoice_id"]
        # access_token = data["access_token"]
        jwt = data["jwt"]
        if Jwt.objects.filter(jwt=jwt).exists():
            res = check_qpay(invoice_id)
            logging.info(res)
            if res["count"] > 0:
                payment_status = res["rows"][res["count"]-1]["payment_status"]
                logging.info(payment_status)
                if payment_status == "PAID":
                    response = status_success(1, "Tulbur tulult amjilttai", payment_status)
                else:
                    response = status_unsuccessful(1, None, payment_status)
            else:
                message = "Qpay-d burtgelgui guilgee baina"
                response = status_unsuccessful(1, None, message)
        else:
            message = "Burtgelgui jwt baina"
            logging.info(message)
            response = status_unsuccessful(1, None, message)
    else:
        response = status_unsuccessful(1, None, "Buruu method")
    return JsonResponse(response, status=status.HTTP_200_OK)


@api_view(['POST'])
def callBackUrl(request):
    logging.info("callBackUrl")
    data = JSONParser().parse(request)
    order_id = data["payment_id"]
    logging.info(order_id)
    # order = Order.objects.get(id=order_id)
    json = check_qpay(order.qpay_invoice_id)
    # print(json)
    if json["count"] > 0:
        payment_status = json["rows"][json["count"] - 1]["payment_status"]
        print(payment_status)
        if payment_status == "PAID":
            return status_success(0, None, payment_status)
        else:
            return status_unsuccessful(1, None, payment_status)
    else:
        message = "Qpay-d burtgelgui guilgee baina"
        return status_unsuccessful(1, None, message)
    # logging.info("SAVED")


@api_view(['POST'])
def barimt(request):
    logging.info("ebarimt")
    if request.method == 'POST':
        data = JSONParser().parse(request)
        turul = data["type"]
        order_id = data["order_id"]
        customerNo = data["customerNo"]
        billType = data["billType"]
        jwt = data["jwt"]
        logging.info(customerNo)
        logging.info(billType)
        if Jwt.objects.filter(jwt=jwt).exists():
            sim = ""
            order = ""
            kiosk_id = Jwt.objects.get(jwt=jwt).kiosk_id
            if turul == "newnumber" or turul == "restoresim":
                sim = Sims.objects.get(id=order_id)
                hariu = ebarimt(customerNo, billType, 0, sim.paid, sim.tipo)
            else:
                order = Orders.objects.get(id=order_id)
                hariu = ebarimt(customerNo, billType, 0, order.paid, order.product_name)

            hariu = json.dumps(hariu)
            hariu = json.loads(hariu)

            if (not hariu) or hariu["success"] == False:
                logging.error("Цэнэглэлт амжилттай, И-баримттай холбогдоход алдаа гарлаа. Line-459")
                message = "Цэнэглэлт амжилттай, И-баримттай холбогдоход алдаа гарлаа." # hariu["message"]
                logging.info(message)
                response = status_unsuccessful(1, None, message)
            else:
                success = hariu["success"]
                register_num = hariu["registerNo"]
                bill_id = hariu["billId"]
                fecha = hariu["date"]
                mac_address = hariu["macAddress"]
                internal_code = ""
                if "internalCode" in hariu:
                    internal_code = hariu["internalCode"]
                bill_type = hariu["billType"]
                qr_data = hariu["qrData"]
                lott = hariu["lottery"]
                vat = hariu["vat"]
                if turul == "newnumber" or turul == "restoresim":
                    addlottery(kiosk_id, success, register_num, bill_id, fecha, mac_address, internal_code, bill_type,
                           qr_data, lott, sim.paid, sim.number, sim.tipo, vat)

                    bill(bill_id, kiosk_id, sim.tipo, sim.number, int(sim.paid), lott, qr_data, vat)
                else:
                    addlottery(kiosk_id, success, register_num, bill_id, fecha, mac_address, internal_code, bill_type,
                           qr_data, lott, order.paid, order.number, order.product_name, vat)

                    bill(bill_id, kiosk_id, order.product_name, order.number, int(order.paid), lott, qr_data, vat)

                if int(kiosk_id) > 2:
                    kiosk = Status.objects.get(id=kiosk_id)
                    kiosk.printer_counter += 1
                    kiosk.save()
                message = "Created"
                ebarimt_image = "static/ebarimt/kiosk{0}/bill.bmp".format(kiosk_id)
                logging.info(ebarimt_image)
                response = status_success(1, message, ebarimt_image)
        else:
            message = "Burtgelgui jwt baina"
            logging.info(message)
            response = status_unsuccessful(1, None, message)
    else:
        response = status_unsuccessful(1, None, "Buruu method")
    return JsonResponse(response, status=status.HTTP_200_OK)


@api_view(['POST'])
def baiguullagaRegister(request):
    logging.info("baiguullagaRegister")
    if request.method == 'POST':
        data = JSONParser().parse(request)
        register = data["register"]
        jwt = data["jwt"]
        if Jwt.objects.filter(jwt=jwt).exists():
            res = checkBaiguullaga(register)
            logging.info("checkBaiguullaga")
            logging.info(res)
            name = "Таны оруулсан регистр " + res["name"] + " байгууллага дээр бүртгэлтэй байна."
            if res["found"]:
                response = status_success(1, "amjilttai", name)
            else:
                response = status_unsuccessful(1, None, name)
        else:
            message = "Burtgelgui jwt baina"
            logging.info(message)
            response = status_unsuccessful(1, None, message)
    else:
        response = status_unsuccessful(1, None, "Buruu method")
    return JsonResponse(response, status=status.HTTP_200_OK)


@api_view(['POST'])
def nubisoftLog(request):
    logging.info("nubisoftLog")
    if request.method == 'POST':
        data = JSONParser().parse(request)
        nubisoft_log = data["nubisoft_log"]
        jwt = data["jwt"]
        if Jwt.objects.filter(jwt=jwt).exists():
            logging.info("==================================================")
            logging.info(nubisoft_log)
            logging.info("==================================================")
            response = status_success(1, "amjilttai", name)
        else:
            message = "Burtgelgui jwt baina"
            logging.info(message)
            response = status_unsuccessful(1, None, message)
    else:
        response = status_unsuccessful(1, None, "Buruu method")
    return JsonResponse(response, status=status.HTTP_200_OK)