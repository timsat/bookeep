# -*- coding: utf-8 -*-
from decimal import Decimal
from datetime import date
import locale


def totalinwords(totals: Decimal):
    DP0_2 = ["", "одна ", "две "]

    D0_19 = ["", "один ", "два ", "три ", "четыре ", "пять ", "шесть ", "семь ", "восемь ", "девять ", "десять ", "одиннацать ", "двенадцать ", "тринадцать ",
             "четырнадцать ", "пятнадцать ", "шестнадцать ", "семнадцать ", "восемнадцать ", "девятнадцать "]

    D1 = ["", "", "двадцать ", "тридцать ", "сорок ", "пятьдесят ", "шестьдесят ", "семьдесят ", "восемьдесят ", "девяносто "]

    D2 = ["", "сто ", "двести ", "триста ", "четыреста ", "пятьсот ", "шестьсот ", "семьсот ", "восемьсот ", "девятьсот "]

    DN = [["рубль ", "рубля ", "рублей "],
          ["тысяча ", "тысячи ", "тысяч "],
          ["миллион ", "миллиона ", "миллионов "],
          ["миллиард ", "миллиарда ", "миллиардов "],
          ["триллион ", "триллиона ", "триллионов "],
          ["копейка", "копейки", "копеек"]]

    def getd0(n, i):
        return DP0_2[n] if (i == 1) and (n < 3) else D0_19[n]

    def getdn(d0, i):
        DNH = [2, 0, 1, 1, 1]
        k = DNH[d0] if d0 < 5 else 2
        return DN[i][k]

    s = ""
    num = int(totals)
    cents = int((totals - num) * 100)
    for i in range(len(DN) - 1):
        if num == 0:
            break
        triplet = num % 1000
        if triplet != 0 or i == 0:
            d0 = triplet % 10
            d02 = triplet % 100
            d1 = triplet % 100 // 10
            d2 = triplet // 100
            if d02 < 20:
                s = getd0(d02, i) + getdn(d02, i) + s
            else:
                s = D1[d1] + getd0(d0, i) + getdn(d0, i) + s
            s = D2[d2] + s
        num //= 1000
    s = '%s%02d %s' % (s, cents, getdn(cents if cents < 20 else cents % 10, -1))
    return s


def decimaltostr(d):
    return locale.format('%0.2f', d)


def localizedate(d: date):
    months = [u'января', u'февраля', u'марта', u'апреля', u'мая', u'июня', u'июля', u'августа', u'сентября', u'октября', u'ноября', u'декабря']
    return "%d %s %d" % (d.day, months[d.month - 1], d.year)