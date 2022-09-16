# -*- coding: utf-8 -*-

import json, base64
from Crypto.Hash import MD5
from Crypto.Cipher import DES3
import logging
from models import *
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from datetime import datetime
import qrcode
from services import *
from models import *


def Encode(mongolia):
    data = json.dumps(mongolia)
    key = "KIosk2018&#_B0rl4ul@lt"
    key = MD5.new(key)
    key = key.hexdigest()[0:24]

    cipher = DES3.new(key, DES3.MODE_ECB)
    pad_len = 8 - len(data) % 8
    padding = chr(pad_len) * pad_len
    data += padding
    print data
    result = cipher.encrypt(data)
    result = base64.b64encode(result)
    return result


def DecodeProduct(mongolia):
    key = "KIosk2018&#_B0rl4ul@lt"
    key = MD5.new(key)
    key = key.hexdigest()[0:24]
    cipher = DES3.new(key, DES3.MODE_ECB)
    result = base64.b64decode(mongolia)
    result = cipher.decrypt(result)
    # logging.info(result)
    a = result.index("]}")
    result = result[:a + 2]
    return result


def Decode(mongolia):
    key = "KIosk2018&#_B0rl4ul@lt"
    key = MD5.new(key)
    key = key.hexdigest()[0:24]

    cipher = DES3.new(key, DES3.MODE_ECB)
    result = base64.b64decode(mongolia)
    result = cipher.decrypt(result)
    a = result.index("}")
    result = result[:a + 1]
    return result


def addcashlog(kiosk_id, money, order_name, payment, mungu_tatsan, order_id, sim_id):
    kiosk = Status.objects.get(id=kiosk_id)
    cash = Cashlog()
    cash.money = money
    cash.kiosk = kiosk
    if Orders.objects.filter(id=order_id).exists():
        order = Orders.objects.get(id=order_id)
    else:
        order = Orders()
        order == "0"
    cash.order_id = order.id
    if Sims.objects.filter(id=sim_id).exists():
        sim = Sims.objects.get(id=sim_id)
    else:
        sim = Sims()
        sim == "0"
    cash.sim_id = sim.id
    cash.orders = order_name
    cash.payment = payment
    cash.money_charged = mungu_tatsan
    cash.save()


def sku(product_name):
    if product_name == "1000 нэгжийн карт" or product_name == "2000 нэгжийн карт" or product_name == "5000 нэгжийн карт" or product_name == "10000 нэгжийн карт" or product_name == "30000 нэгжийн карт" \
            or product_name == "30/30 үйлчилгээний 30 хоногтой карт" or product_name == "50/50 үйлчилгээний 60 хоногтой карт" or product_name == "0/30 үйлчилгээний 30 хоногтой карт" \
            or product_name == "0/50 үйлчилгээний 180 хоногтой карт" or product_name == "0/50 үйлчилгээний 30 хоногтой карт" or product_name == "0/50 үйлчилгээний 365 хоногтой карт":
        return "8413"
    if product_name == "Дараа төлбөртийн төлбөр" or product_name == "Шинэ дугаар":
        return "8413"
    else:
        return "8422"


def bill(bill_id, kiosk_id, name, number, price, lott, qr_data, vat):
    kiosk = Status.objects.get(id=kiosk_id)
    img_h = 790
    img_w = 540

    img = Image.new("RGBA", (img_w, img_h), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    text_font_20 = ImageFont.truetype("arial.ttf", 20, encoding="unic")
    text_font_22 = ImageFont.truetype("arial.ttf", 22, encoding="unic")
    text_font_24 = ImageFont.truetype("arial.ttf", 24, encoding="unic")
    text_font_39 = ImageFont.truetype("arial.ttf", 39, encoding="unic")

    txt_x = 40
    txt_y = 20
    txt_a = 40

    text = u"Хэрэглэгчийн хувь"
    txt_w, txt_h = draw.textsize(text, font=text_font_20)
    draw.text((img_w - txt_w - txt_a, txt_y), text, (0, 0, 0), font=text_font_20)

    txt_y += 20
    text = u"\"ЖИ-МОБАЙЛ\" ХХК"
    txt_w, txt_h = draw.textsize(text, font=text_font_39)
    draw.text(((img_w / 2) - (txt_w / 2) + 20, txt_y), text, (0, 0, 0), font=text_font_39)

    txt_y += 50
    text = u"ҮҮРЭН ХОЛБОНЫ ҮНДЭСНИЙ ОПЕРАТОР"
    txt_w, txt_h = draw.textsize(text, font=text_font_22)
    draw.text(((img_w / 2) - (txt_w / 2) + 20, txt_y), text, (0, 0, 0), font=text_font_22)

    txt_y += 30
    text = u"БЭЛЭН МӨНГӨНИЙ ТООЦООНЫ ХУУДАС"
    txt_w, txt_h = draw.textsize(text, font=text_font_20)
    draw.text(((img_w / 2) - (txt_w / 2) + 20, txt_y), text, (0, 0, 0), font=text_font_20)

    txt_y += 50
    text = u"Баримтын №:"
    draw.text((txt_x, txt_y), text, (0, 0, 0), font=text_font_20)
    text = bill_id

    txt_y += 30
    txt_w, txt_h = draw.textsize(text, font=text_font_20)
    draw.text((img_w - txt_w - txt_a, txt_y), text, (0, 0, 0), font=text_font_20)

    txt_y += 30
    text = u"Хэвлэсэн огноо:"
    draw.text((txt_x, txt_y), text, (0, 0, 0), font=text_font_22)
    text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    txt_w, txt_h = draw.textsize(text, font=text_font_22)
    draw.text((img_w - txt_w - txt_a, txt_y), text, (0, 0, 0), font=text_font_22)

    txt_y += 30
    text = u"Салбар:"
    draw.text((txt_x, txt_y), text, (0, 0, 0), font=text_font_22)
    text = u"Салбар №03"
    txt_w, txt_h = draw.textsize(text, font=text_font_22)
    draw.text((img_w - txt_w - txt_a, txt_y), text, (0, 0, 0), font=text_font_22)

    txt_y += 30
    text = u"Киоскын дугаар:"
    draw.text((txt_x, txt_y), text, (0, 0, 0), font=text_font_22)
    text = kiosk.name

    txt_w, txt_h = draw.textsize(text, font=text_font_22)
    draw.text((img_w - txt_w - txt_a, txt_y), text, (0, 0, 0), font=text_font_22)

    txt_y += 25
    draw.line((txt_x, txt_y, img_w - txt_a, txt_y), fill=0, width=2)

    txt_y += 20
    text = u"ТӨРӨЛ"
    draw.text((txt_x, txt_y), text, (0, 0, 0), font=text_font_24)
    text = u"ДУГААР"
    txt_w, txt_h = draw.textsize(text, font=text_font_24)
    draw.text(((img_w - 40) / 3 + 100, txt_y), text, (0, 0, 0), font=text_font_24)
    text = u"ҮНЭ"
    txt_w, txt_h = draw.textsize(text, font=text_font_24)
    draw.text((img_w - txt_w - txt_a, txt_y), text, (0, 0, 0), font=text_font_24)

    txt_y += 50
    text = name

    draw.text((txt_x, txt_y), text, (0, 0, 0), font=text_font_20)
    text = str(number)

    txt_w, txt_h = draw.textsize(text, font=text_font_20)
    draw.text(((img_w - 40) / 3 + 100, txt_y), text, (0, 0, 0), font=text_font_20)
    text = str(price)

    txt_w, txt_h = draw.textsize(text, font=text_font_20)
    draw.text((img_w - txt_w - txt_a, txt_y), text, (0, 0, 0), font=text_font_20)

    txt_y += 25
    draw.line((txt_x, txt_y, img_w - txt_a, txt_y), fill=0, width=2)

    txt_y += 30
    text = lott
    txt_w, txt_h = draw.textsize(text, font=text_font_24)
    draw.text(((img_w / 3) * 2, txt_y), text, (0, 0, 0), font=text_font_24)

    qr = qrcode.QRCode(version=1, border=0, box_size=4)
    qr.add_data(qr_data)
    qr.make(fit=True)
    qr_img = qr.make_image()
    img.paste(qr_img, (txt_x + 10, txt_y))

    txt_y += 80
    text = u"НӨАТ 10%"
    draw.text(((img_w / 2), txt_y), text, (0, 0, 0), font=text_font_22)
    text = str(vat)
    txt_w, txt_h = draw.textsize(text, font=text_font_22)
    draw.text((img_w - txt_w - txt_a, txt_y), text, (0, 0, 0), font=text_font_22)
    txt_y += 30
    text = u"НИЙТ ДҮН"
    draw.text(((img_w / 2), txt_y), text, (0, 0, 0), font=text_font_22)
    text = str(price)
    txt_w, txt_h = draw.textsize(text, font=text_font_22)
    draw.text((img_w - txt_w - txt_a, txt_y), text, (0, 0, 0), font=text_font_22)

    txt_y += 120
    text = u"Та төлбөрийн баримтаа хадгална уу"
    txt_w, txt_h = draw.textsize(text, font=text_font_20)
    draw.text(((img_w / 2) - (txt_w / 2) + 20, txt_y), text, (0, 0, 0), font=text_font_20)

    txt_y += 30
    text = u"ЖИМОБАЙЛ ХХК-Р ҮЙЛЧЛҮҮЛСЭН"
    txt_w, txt_h = draw.textsize(text, font=text_font_22)
    draw.text(((img_w / 2) - (txt_w / 2) + 20, txt_y), text, (0, 0, 0), font=text_font_22)
    txt_y += 20
    text = u"ТАНД БАЯРЛАЛАА"
    txt_w, txt_h = draw.textsize(text, font=text_font_22)
    draw.text(((img_w / 2) - (txt_w / 2) + 20, txt_y), text, (0, 0, 0), font=text_font_22)

    txt_y += 30
    text = u"Утас: 98103636"
    draw.text((txt_x, txt_y), text, (0, 0, 0), font=text_font_20)
    text = u"Лавлах: 3636"
    txt_w, txt_h = draw.textsize(text, font=text_font_20)
    draw.text(((img_w - 40) / 3 + 50, txt_y), text, (0, 0, 0), font=text_font_20)
    text = u"Факс: 311195"
    txt_w, txt_h = draw.textsize(text, font=text_font_20)
    draw.text((img_w - txt_w - 40, txt_y), text, (0, 0, 0), font=text_font_20)

    # logging.info(kiosk_name.encode("utf-8").decode("utf-8"))
    img.save("/home/ezen/kiosk/static/ebarimt/kiosk{0}/bill.bmp".format(kiosk.id))

    # os.system("D:\\Printer\\Printer\\bin\\Debug\\Printer.exe")


def addlottery(kiosk_id, success, register_num, bill_id, fe, mac_address, internal_code, bill_type, qr_data, lott, amount, number,
               order, vat):
    logging.info("ADDLOTTERY")
    kiosk = Status.objects.get(id=kiosk_id)
    sugalaa = Lottery()
    sugalaa.success = success
    # logging.info(sugalaa.success)
    sugalaa.billid = bill_id
    sugalaa.date = fe
    sugalaa.mac_address = mac_address
    sugalaa.kiosk = kiosk
    sugalaa.register_number = register_num
    sugalaa.internal_code = internal_code
    sugalaa.bill_type = bill_type
    sugalaa.qr_data = qr_data
    sugalaa.lottery = lott
    sugalaa.paid = amount
    sugalaa.number = number
    sugalaa.order = order
    sugalaa.vat = vat
    sugalaa.save()


# def checkDigit(number):
#     # logging.info(number)
#     oron1 = number[0:1]
#     oron2 = number[1:2]
#     oron3 = number[2:3]
#     oron4 = number[3:4]
#     oron5 = number[4:5]
#     oron6 = number[5:6]
#     oron7 = number[6:7]
#     oron8 = number[7:8]
# 
#     # golden shalgah DEABCCCC, DECBCCCC, DEACCCCC
#     if (((oron3 != oron4) and (oron4 != oron5) and (oron5 == oron6) and (oron6 == oron7) and (oron7 == oron8)) or (
#                                 (oron3 != oron4) and (oron3 == oron5) and (oron4 != oron5) and (oron5 == oron6) and (
#                             oron6 == oron7) and (oron7 == oron8)) or (
#                             (oron3 != oron4) and (oron4 == oron5) and (oron5 == oron6) and (oron6 == oron7) and (
#                         oron7 == oron8))):
#         return "alt1"
# 
#     # silvershalgah DEABABDE, DExxAABB, DEABDEAB
#     # DEABDEAB
#     if ((oron1 == oron5) and (oron2 == oron6) and (oron3 == oron7) and (oron4 == oron8)):
#         return "mungu1"
#     # DEABABDE
#     if ((oron1 == oron7) and (oron2 == oron8) and (oron3 == oron5) and (oron4 == oron6) and (oron3 != oron4)):
#         return "mungu2"
#     # DExxAABB
#     if (((oron5 == oron6) and (oron7 == oron8) and (oron6 != oron7)) or (
#                             (oron5 == oron6) and (oron7 == oron8) and (oron6 != oron7) and (oron2 != oron5) and (
#                         oron2 != oron7))):
#         return "mungu3"
# 
#     # hurel shalgah DExxABBA, DExxABAB
#     # DExxABBA
#     if ((oron1 != oron2) and (oron5 == oron8) and (oron6 == oron7)):
#         return "hurel1"
#     # DExxABAB
#     if ((oron5 == oron7) and (oron6 == oron8)):
#         return "hurel2"
#     else:
#         return "engiin"

def checkNumber(number):
    oron1 = number[0:1]
    oron2 = number[1:2]
    oron3 = number[2:3]
    oron4 = number[3:4]
    oron5 = number[4:5]
    oron6 = number[5:6]
    oron7 = number[6:7]
    oron8 = number[7:8]

    # brilliant shalgah DEAAAAAA
    if ((oron3 == oron4) and (oron3 == oron5) and (oron3 == oron6) and (oron3 == oron7) and (oron3 == oron8) and
        (oron4 == oron5) and (oron4 == oron6) and (oron4 == oron7) and (oron4 == oron8) and
        (oron5 == oron6) and (oron5 == oron7) and (oron5 == oron8) and
        (oron6 == oron7) and (oron6 == oron8) and
        (oron7 == oron8)):
        return "brilliant"

    # golden shalgah DEABCCCC, DECBCCCC, DEACCCCC
    # DEABCCCC
    if (((oron3 != oron4)) and
        ((oron5 == oron6) and (oron5 == oron7) and (oron5 == oron8) and
         (oron6 == oron7) and (oron6 == oron8) and (oron7 == oron8))):
        return "alt1"
    # DEAAAADE
    if (((oron1 == oron7) and (oron2 == oron8)) and
            ((oron3 == oron4) and (oron3 == oron5) and (oron3 == oron6)) and
            ((oron4 == oron5) and (oron4 == oron6)) and ((oron5 == oron6))):
        return "alt2"
    # DEAADEAA
    if (((oron1 == oron5) and (oron2 == oron6)) and
            ((oron3 == oron4) and (oron3 == oron7) and (oron3 == oron8)) and
            ((oron4 == oron7) and (oron4 == oron8)) and ((oron7 == oron8))):
        return "alt3"
    # DEAABBAA
    if (((oron3 == oron4) and (oron3 == oron7) and (oron3 == oron8) and (oron4 == oron7) and (oron4 == oron8) and
         (oron7 == oron8)) and ((oron5 == oron6)) and
            ((oron5 != oron3) and (oron5 != oron4) and (oron5 != oron7) and (oron5 != oron8)) and
            ((oron6 != oron3) and (oron6 != oron4) and (oron6 != oron7) and (oron6 != oron8))):
        return "alt4"
    # DEBBAAAA
    if (((oron3 == oron4)) and ((oron3 != oron5) and (oron3 != oron6) and (oron3 != oron7) and (oron3 != oron8)) and
            ((oron4 != oron5) and (oron4 != oron6) and (oron4 != oron7) and (oron4 != oron8)) and
            ((oron5 == oron6) and (oron5 == oron7) and (oron5 == oron8)) and ((oron6 == oron7) and oron6 == oron8) and
            (oron7 == oron8)):
        return "alt5"
    # DEAAAABB
    if (((oron3 == oron4) and (oron3 == oron5) and (oron3 == oron6) and (oron4 == oron5) and (oron4 == oron6) and
         (oron5 == oron6)) and ((oron7 == oron8)) and ((oron7 != oron3) and (oron7 != oron4) and (oron7 != oron5) and
                                                       (oron7 != oron6) and (oron8 != oron3) and (oron8 != oron4) and
                                                       (oron8 != oron5) and (oron8 != oron6))):
        return "alt6"

    # if (((oron3 != oron4) and (oron4 != oron5) and (oron5 == oron6) and (oron6 == oron7) and (oron7 == oron8)) or (
    #                     (oron3 != oron4) and (oron3 == oron5) and (oron4 != oron5) and (oron5 == oron6) and (
    #         oron6 == oron7) and (oron7 == oron8)) or (
    #                 (oron3 != oron4) and (oron4 == oron5) and (oron5 == oron6) and (oron6 == oron7) and (
    #     oron7 == oron8))):
    #     return "alt1"

    # silver shalgah DEABABDE, DExxAABB, DEABDEAB
    # DExxABAB
    if (((oron5 == oron7) and (oron6 == oron8)) and
            ((oron5 != oron6) and (oron5 != oron8) and (oron6 != oron7) and (oron7 != oron8))):
        return "mungu1"
    # DExxABBA
    if (((oron5 == oron8) and (oron6 == oron7)) and
            ((oron5 != oron6) and (oron5 != oron7) and (oron6 != oron8) and (oron7 != oron8))):
        return "mungu2"
    # DExxAABB
    if (((oron5 == oron6) and (oron7 == oron8)) and
            ((oron5 != oron7) and (oron5 != oron8)) and ((oron6 != oron7) and (oron6 != oron8))):
        return "mungu3"
    # DEAAABBB
    if (((oron3 == oron4) and (oron3 == oron5) and (oron4 == oron5)) and
            ((oron6 == oron7) and (oron6 == oron8) and (oron7 == oron8)) and
            ((oron3 != oron6) and (oron3 != oron7) and (oron3 != oron8) and (oron4 != oron6) and (oron4 != oron7) and
             (oron4 != oron8)) and ((oron5 != oron6) and (oron5 != oron7) and (oron5 != oron8))):
        return "mungu4"
    # DEABDEAB
    if (((oron1 == oron5) and (oron2 == oron6) and (oron3 == oron7) and (oron4 == oron8)) and
            ((oron3 != oron4) and (oron3 != oron8) and (oron4 != oron7) and (oron7 != oron8))):
        return "mungu5"
    # DEABABDE
    if ((oron1 == oron7) and (oron2 == oron8) and (oron3 == oron5) and (oron4 == oron6) and
            ((oron3 != oron4) and (oron3 != oron6) and (oron4 != oron5) and (oron5 != oron6))):
        return "mungu6"

    # # DEABDEAB
    # if ((oron1 == oron5) and (oron2 == oron6) and (oron3 == oron7) and (oron4 == oron8)):
    #     return "mungu1"
    # # DEABABDE
    # if ((oron1 == oron7) and (oron2 == oron8) and (oron3 == oron5) and (oron4 == oron6) and (oron3 != oron4)):
    #     return "mungu2"
    # # DExxAABB
    # if (((oron5 == oron6) and (oron7 == oron8) and (oron6 != oron7)) or (
    #                 (oron5 == oron6) and (oron7 == oron8) and (oron6 != oron7) and (oron2 != oron5) and (
    #     oron2 != oron7))):
    #     return "mungu3"

    # hurel shalgah DExxABBA, DExxABAB
    #DExx000B
    if (((oron5 == "0") and (oron6 == "0") and (oron7 == "0")) and (oron8 != "0")):
        return "hurel1"
    # DExxB000
    if ((oron5 != "0") and ((oron6 == "0") and (oron7 == "0") and (oron8 == "0"))):
        return "hurel2"
    # DEABABED
    if (((oron1 == oron8) and (oron2 == oron7)) and ((oron3 == oron5) and (oron4 == oron6)) and
            ((oron3 != oron4) and (oron3 != oron6) and (oron4 != oron5) and (oron5 != oron6))):
        return "hurel3"
    # DEABBAED
    if (((oron1 == oron8) and (oron2 == oron7)) and ((oron3 == oron6) and (oron4 == oron5)) and
            ((oron3 != oron4) and (oron3 != oron5) and (oron4 != oron6) and (oron5 != oron6))):
        return "hurel4"

    # # DExxABBA
    # if ((oron1 != oron2) and (oron5 == oron8) and (oron6 == oron7)):
    #     return "hurel1"
    # # DExxABAB
    # if ((oron5 == oron7) and (oron6 == oron8)):
    #     return "hurel2"
    else:
        return "engiin"
