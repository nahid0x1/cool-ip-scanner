import socket
import threading
from termcolor import colored
from concurrent.futures import ThreadPoolExecutor
import ipaddress

def scan_ports(ip, ports):
    open_ports = []
    try:
        for port in ports:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)
                result = sock.connect_ex((ip, port))
                if result == 0:
                    open_ports.append(port)
    except Exception as e:
        pass
    return open_ports

def scan_and_store(ip, ports, port_filename):
    open_ports = scan_ports(ip, ports)
    num_found = len(open_ports)
    num_not_found = len(ports) - num_found
    
    
    if num_found > 0:
        open_ports = list(set(open_ports))  # Remove duplicates
        with open(port_filename, 'a') as file:
            file.write(f"{ip}\n")
        print(colored(f"IP : {ip} : {open_ports}", 'green'))
    else:
        print(colored(f"IP : {ip} : [No Port] ", 'red'))



def main():
    filename = input("Range File~# ")
    port_input = input("Ports~# ")
    num_threads = int(input("Thread~# "))

    ip_ranges = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                ip_range = line.strip()
                ip_ranges.append(ip_range)
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return

    ports = [int(port.strip()) for port in port_input.split(",")]

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        for ip_range in ip_ranges:
            start_ip, end_ip = ip_range.split('-')
            start_ip = ipaddress.ip_address(start_ip)
            end_ip = ipaddress.ip_address(end_ip)
            
            for ip in range(int(start_ip), int(end_ip)+1):
                ip_str = str(ipaddress.ip_address(ip))
                for port in ports:
                    port_filename = f"{port}.txt"
                    executor.submit(scan_and_store, ip_str, [port], port_filename)

if __name__ == "__main__":
    main()
