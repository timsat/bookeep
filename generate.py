# -*- coding: utf-8 -*-

from flask import Flask, render_template, redirect, url_for
import functools
import subprocess
from decimal import *
from datetime import date, datetime
import locale
import pystache
import misc
from entities import *

app = Flask(__name__)
locale.setlocale(locale.LC_ALL, 'ru_RU.utf8')
getcontext().rounding = ROUND_HALF_EVEN

@app.route('/')
def home():
    return render_template('index.html')

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def inputformat(prompt, func=None, default=None):
    while True:
        try:
            strval = input(bcolors.OKGREEN + prompt + bcolors.ENDC + '\n>> ')
            if len(strval) == 0 and default is not None:
                return default
            return func(strval) if func is not None else strval
        except Exception as ex:
            print(ex)


def inputint(prompt):
    return inputformat(prompt, lambda x: int(x))


def inputdec(prompt):
    return inputformat(prompt, lambda x: Decimal(x).quantize(Decimal('0.01')))


def inputdate(prompt, default=None):
    return inputformat(prompt, lambda x: datetime.strptime(x, '%Y-%m-%d').date(), default)


session = Session()
me = session.query(Agent).filter_by(id=1).first()
if me == None :
    name = inputformat('Enter your name:')
    me = Agent(name=name)
    session.add(me)
    session.commit()

myAccounts = session.query(BankAccount).filter_by(agentId=1).all()
if len(myAccounts) == 0 :
    bik = inputformat('Enter BIK:')
    bname = inputformat('Enter bank name:')
    accNum = inputformat('Enter account number:')
    kpp = inputformat('Enter KPP:')
    acc = BankAccount(bik = bik, bname = bname, num = accNum, agentId = 1)
    session.add(acc)
    session.commit()
    myAccounts = session.query(BankAccount).filter_by(agentId=1).all()

'''
data = {}
items = []
doctype = inputint('Doc type\n 1: invoice\n 2: job')
data['docnum'] = inputint('Doc number:')
docdate = inputdate('Doc date (%s):' % date.today().strftime('%Y-%m-%d'), date.today())
data['docdate'] = misc.localizedate(docdate)
print(data['docdate'])
i = 0
while True:
    i += 1
    item = {}
    s = inputformat('Service/product item (empty string to finish):', None)
    if len(s) == 0:
        break
    item['idx'] = i
    item['name'] = s
    item['unit'] = inputformat('Units:', None)
    item['count'] = inputint('Count:')
    unitPrice = inputdec('Unit price:')
    item['unitPrice'] = unitPrice
    item['unitPriceStr'] = misc.decimaltostr(unitPrice)
    itemTotal = item['unitPrice'] * item['count']
    item['itemTotal'] = itemTotal
    item['itemTotalStr'] = misc.decimaltostr(itemTotal)

    items.append(item)

data['items'] = items
data['total'] = functools.reduce(lambda x, y: x['itemTotal'] + y['itemTotal'], items, {'itemTotal': Decimal('0.00')})
data['totalStr'] = misc.decimaltostr(data['total'])
data['totalInWords'] = misc.totalinwords(data['total'])

if doctype == 1: 
    with open('invoice.tex.tpl', 'rb', buffering=0) as f:
        tmpl = f.readall().decode()
        output = pystache.render(tmpl, data)
        outputFile = 'invoice_%s_%s_.tex' % (data['docnum'], docdate.strftime('%Y-%m-%d'))
        with open(outputFile, 'w', encoding='utf-8') as ofile:
            ofile.write(output)
else:
    with open('act.tex.tpl', 'rb', buffering=0) as f:
        tmpl = f.readall().decode()
        output = pystache.render(tmpl, data)
        outputFile = 'act_%s_%s_.tex' % (data['docnum'], docdate.strftime('%Y-%m-%d'))
        with open(outputFile, 'w', encoding='utf-8') as ofile:
            ofile.write(output)


subprocess.call(['xelatex', './'+outputFile])
'''
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')