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

addressList = list(csv.reader(open("Tokens.csv"))) 
addressList=sorted(addressList, key=lambda x: x[0])

address = None
contract = None
API_KEY = os.getenv('API_KEY')

def getContract(address):
    
    global contract
    
    url = "https://api.etherscan.io/api?module=contract&action=getabi&address="+address+"&apikey="+API_KEY

    response = urlopen(url)
    abi=json.loads(response.read())["result"]
    contract = web3.eth.contract(address=address, abi=abi) 

# Sets up GUI    
window = tk.Tk()
window.title("ERC-20 Balance")
window.geometry("350x250")

# Allows the esc key to be used to close the GUI
window.bind('<Escape>', lambda e: window.quit())

nameList = []
for i in range(len(addressList)):
    nameList.append(addressList[i][0])

name = StringVar(window)
name.set(nameList[0]) # default value

drop = OptionMenu(window, name, *nameList)
drop.pack()

symbol=None
inAddress=None
userInfo=None
infoLabel=None

def getInfo():
    
    global name
    global symbol
    global inAddress
    global userInfo
    global infoLabel
    
    name = name.get()
    for i in range(len(addressList)):
        if name == addressList[i][0]:
            contractAddress = addressList[i][1]
    getContract(Web3.toChecksumAddress(contractAddress))
                
    info.destroy()
    drop.destroy()
        
    totalSupplyWei = contract.functions.totalSupply().call()
    totalSupply = web3.fromWei(totalSupplyWei, 'ether')
    symbol = contract.functions.symbol().call()
    infoLabel = Label(window, text = f"Total Supply: {round(totalSupply)} {symbol} ")
    infoLabel.pack()
    inAddress= Entry(window, width= 25)
    inAddress.pack()
    userInfo = tk.Button(window, text="Get address Info", height = 2, width = 15, command = getBalance)
    userInfo.pack()
    
def getBalance():
    
    infoLabel.destroy()
    
    checkSumAddress = Web3.toChecksumAddress(inAddress.get())
    balanceWei = contract.functions.balanceOf(checkSumAddress).call()
    balance = web3.fromWei(balanceWei, 'ether')
    addressLabel = Label(window, text = checkSumAddress, font='Helvetica 13 bold')
    addressLabel.pack()
    
    inAddress.destroy()
    userInfo.destroy()
    
    balanceLabel = Label(window, text = f"Your Balance: {balance} {symbol}")
    balanceLabel.pack()

info = tk.Button(window,text="Get Info", height = 2, width = 10, command = getInfo)
info.pack()

tk.mainloop()