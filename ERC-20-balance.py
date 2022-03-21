"""ERC-20 Balance"""
import tkinter as tk
from tkinter import *
from web3 import Web3
from urllib.request import urlopen
from dotenv import load_dotenv
import os
import json
import csv

load_dotenv()

w3 = os.getenv('ETH_URL')
web3 = Web3(Web3.HTTPProvider(w3))

address_list = list(csv.reader(open("Tokens.csv")))
address_list = sorted(address_list, key=lambda x: x[0])

address = None
contract = None
API_KEY = os.getenv('API_KEY')


def get_contract(address):
    """Get Contract"""
    global contract

    url = "https://api.etherscan.io/api?module=contract&action=getabi&address=" + \
        address+"&apikey="+API_KEY

    response = urlopen(url)
    abi = json.loads(response.read())["result"]
    contract = web3.eth.contract(address=address, abi=abi)


# Sets up GUI
window = tk.Tk()
window.title("ERC-20 Balance")
window.geometry("350x250")

# Allows the esc key to be used to close the GUI
window.bind('<Escape>', lambda e: window.quit())

name_list = []
for i in range(len(address_list)):
    name_list.append(address_list[i][0])

name = StringVar(window)
name.set(name_list[0])  # default value

drop = OptionMenu(window, name, *name_list)
drop.pack()

symbol = None
in_address = None
user_info = None
info_label = None


def getInfo():

    global name
    global symbol
    global in_address
    global user_info
    global info_label

    name = name.get()
    contract_address = None
    for i in range(len(address_list)):
        if name == address_list[i][0]:
            contract_address = address_list[i][1]
    get_contract(Web3.toChecksumAddress(contract_address))

    info.destroy()
    drop.destroy()

    total_supply_wei = contract.functions.total_supply().call()
    total_supply = web3.fromWei(total_supply_wei, 'ether')
    symbol = contract.functions.symbol().call()
    info_label = Label(
        window, text=f"Total Supply: {round(total_supply)} {symbol} ")
    info_label.pack()
    in_address = Entry(window, width=25)
    in_address.pack()
    user_info = tk.Button(window, text="Get address Info",
                          height=2, width=15, command=get_balance)
    user_info.pack()


def get_balance():
    """Get Balance"""

    info_label.destroy()

    check_sum_address = Web3.toChecksumAddress(in_address.get())
    balance_wei = contract.functions.balanceOf(check_sum_address).call()
    balance = web3.fromWei(balance_wei, 'ether')
    address_label = Label(window, text=check_sum_address,
                          font='Helvetica 13 bold')
    address_label.pack()

    in_address.destroy()
    user_info.destroy()

    balance_label = Label(window, text=f"Your Balance: {balance} {symbol}")
    balance_label.pack()


info = tk.Button(window, text="Get Info", height=2, width=10, command=getInfo)
info.pack()

tk.mainloop()
