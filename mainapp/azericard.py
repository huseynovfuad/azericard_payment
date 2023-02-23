import requests
import hashlib
import hmac
import random
import time


class Azericard:

    TERMINAL = "" # your terminal id
    PAYMENT_URL = "https://testmpi.3dsecure.az/cgi-bin/cgi_link" # payment url
    TRTYPE = "1"
    KEY_FOR_SIGN = "" # your key for sign
    MERCH_NAME = ""
    MERCH_URL = ""
    EMAIL = ""
    COUNTRY = "AZ"
    MERCH_GMT = "+4"
    BACKREF = "" # callback url

    @staticmethod
    def gmdate(str_formate, int_timestamp=None):
        if int_timestamp == None:
            return time.strftime(str_formate, time.gmtime())

        else:
            return time.strftime(str_formate, time.gmtime(int_timestamp))


    @staticmethod
    def substr(string, start, length=None):
        if start < 0:
            start = start + len(string)
        if not length:
            return string[start:]
        elif length > 0:
            return string[start:start + length]
        else:
            return string[start:length]

    @staticmethod
    def hash_hmac(algo, data, key):
        res = hmac.new(key, data.encode(), algo).hexdigest()
        return res


    @classmethod
    def hex2bin(cls, hexdata):
        bindata = ""

        i = 0

        while i < len(str(hexdata)):
            try:
                string = cls.substr(hexdata, i, 2)
                hexdec = int(bin(int(string, 16)), 2)

                bindata += chr(hexdec)

                i += 2
            except:
                pass

        return bindata.encode('latin-1')

    @classmethod
    def prepare_payment(cls, total_price, order_id, description="", currency="AZN"):

        irand = random.randint(1, 10000000)

        NONCE = cls.substr(hashlib.md5(str(irand).encode('utf-8')).hexdigest(), 0, 16)
        OPER_TIME = cls.gmdate("%Y%m%d%H%I%S")
        AMOUNT = f'{total_price}'
        RRN = ""
        INT_REF = ""

        to_sign = str(len(AMOUNT)) + AMOUNT + str(len(currency)) + currency + str(
            len(order_id)) + order_id + str(len(description)) + description + str(len(cls.MERCH_NAME)) + cls.MERCH_NAME + str(
            len(cls.MERCH_URL)) + cls.MERCH_URL + str(len(cls.TERMINAL)) + cls.TERMINAL + str(
            len(cls.EMAIL)) + cls.EMAIL + str(len(cls.TRTYPE)) + cls.TRTYPE + str(len(cls.COUNTRY)) + cls.COUNTRY + str(
            len(cls.MERCH_GMT)) + cls.MERCH_GMT + str(len(OPER_TIME)) + str(OPER_TIME) + str(len(NONCE)) + str(NONCE) + str(
            len(cls.BACKREF)) + cls.BACKREF

        res = cls.hex2bin(cls.KEY_FOR_SIGN)

        P_SIGN = cls.hash_hmac('sha1', to_sign, res)

        return {
            'AMOUNT': AMOUNT,
            'CURRENCY': currency,
            'ORDER': order_id,
            'DESC': description,
            'MERCH_NAME': cls.MERCH_NAME,
            'MERCH_URL': cls.MERCH_URL,
            'TERMINAL': cls.TERMINAL,
            'EMAIL': cls.EMAIL,
            'TRTYPE': cls.TRTYPE,
            'COUNTRY': cls.COUNTRY,
            'MERCH_GMT': cls.MERCH_GMT,
            'TIMESTAMP': OPER_TIME,
            'NONCE': NONCE,
            'BACKREF': cls.BACKREF,
            'P_SIGN': P_SIGN,
        }

    def get_payment_page(self, total_price, order_id, description="", currency="AZN"):
        response = requests.post(
            url=self.PAYMENT_URL,
            data=self.prepare_payment(
                total_price=total_price, order_id=order_id, description=description,
                currency=currency
            )
        )
        return response.text.replace("/simple", "https://testmpi.3dsecure.az/simple").replace("/cgi-bin/cgi_link", "https://testmpi.3dsecure.az/cgi-bin/cgi_link")