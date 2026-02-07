# GhostCrack ⚡  
**Fully Automated WPA/WPA2 Handshake Capture & Cracker** (Aircrack-ng on steroids)

[![Stars](https://img.shields.io/github/stars/yourusername/GhostCrack?style=social)](https://github.com/yourusername/GhostCrack)
[![Forks](https://img.shields.io/github/forks/yourusername/GhostCrack?style=social)](https://github.com/yourusername/GhostCrack)

## Features
- Fully automated (one command)
- Beautiful progress bars
- Auto deauth + handshake capture
- Success desktop notification
- Clean code + comments
- Works on Kali/Raspberry Pi/Parrot

## Demo
![demo](demo.gif)

## Installation & Run
```bash
sudo apt update && sudo apt install aircrack-ng python3-pip -y
pip3 install tqdm colorama pyfiglet

git clone https://github.com/yourusername/GhostCrack.git
cd GhostCrack
chmod +x ghostcrack.py
sudo python3 ghostcrack.py
