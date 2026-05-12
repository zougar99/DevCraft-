import subprocess
import os
import json
from colorama import Fore
from time import sleep, gmtime
import calendar

# Decoration for colored output
POSITIVE = f"[{Fore.GREEN}+{Fore.RESET}]"
NEGATIVE = f"[{Fore.RED}-{Fore.RESET}]"
PURPLE = Fore.MAGENTA
RED = Fore.RED
GREEN = Fore.GREEN
RESET = Fore.RESET

def me():
    print(f"{RED}--------------------")
    print(f"{RED}BY ZAKARIA ATERTOUR ")
    print(f"{RED}--------------------{RESET}")

def time_seconds():  # Current time in seconds
    current_time = gmtime()
    current_time = calendar.timegm(current_time)  # Current time in seconds
    return current_time

# Check if the device is rooted
def is_rooted():
    try:
        adb_output = subprocess.check_output("adb shell su -c 'whoami'", shell=True).decode('utf-8')
        if "root" in adb_output:
            print(f"{POSITIVE} The device is rooted.")
            return True
        else:
            print(f"{NEGATIVE} The device is not rooted.")
            return False
    except subprocess.CalledProcessError:
        print(f"{NEGATIVE} Unable to access root privileges.")
        return False

# Start
os.system("cls")
file_path = r"countries.json"
with open(file_path, 'r') as file:
    data = json.load(file)
countries = data["countries"]
cmnd1 = data["cmnd1"]
cmnd2 = data["cmnd2"]
cmnd3 = data["cmnd3"]
cmnd4 = data["cmnd4"]
cmnd5 = data["cmnd5"]
cmnd6 = data["cmnd6"]
cmnd7 = data["cmnd7"]
cmnd8 = data["cmnd8"]

# Check if the device is rooted
if not is_rooted():
    print(f"{NEGATIVE} Cannot proceed because the device is not rooted.")
    exit()

# If the device is rooted, proceed
country_length = len(countries) - 1
while True:
    me()
    print(f"{POSITIVE} Choose the country you want to use:")
    for i, country in enumerate(countries):
        print(f"{GREEN}{i}{RESET} => {PURPLE}{country['name']}{RESET}")
    select = input(f"{RED}=> {RESET}")
    if select.isdigit():
        if int(select) > int(country_length):
            os.system("cls")
        else:
            break
    else:
        os.system("cls")

os.system("cls")
print(f"{NEGATIVE} WAIT ...", end="\r")

# Build ADB commands
adb_command = "adb shell"
root_commands = [
    "su",
    f"{cmnd1} {countries[int(select)]['code']}",
    f"{cmnd2} {countries[int(select)]['code']}",
    f"{cmnd3} {countries[int(select)]['operator']}",
    f"{cmnd4} {countries[int(select)]['operator']}",
    f"{cmnd5} {countries[int(select)]['operator']}",
    f"{cmnd6} {countries[int(select)]['o_code']}",
    f"{cmnd7} {countries[int(select)]['o_code']}",
    f"{cmnd8} {countries[int(select)]['o_code']}",
    "exit",
]

# Run ADB commands
adb_process = subprocess.Popen(adb_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
sleep(1)
for command in root_commands:
    adb_process.stdin.write(command + '\n')
    adb_process.stdin.flush()
adb_process.stdin.close()
adb_process.wait()

me()
print(f"{POSITIVE} The process for {countries[int(select)]['name']} is done :)")
sleep(20)

'''
References:
https://xphone24.com/operator-codes.php
https://www.iban.com/country-codes
'''
