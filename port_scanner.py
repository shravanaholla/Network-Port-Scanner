import socket
import sys
from datetime import datetime


def scan_port(target_host, port, timeout=1.0):
    """Try connecting to a single TCP port. Returns True if open, False if closed."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        result = s.connect_ex((target_host, port))
        s.close()
        return result == 0
    except socket.gaierror:
        raise
    except socket.error:
        raise


def scan_ports(target, ports, timeout=1.0):
    """Resolve target and scan a list of ports.

    Returns a dictionary: { 'target': str, 'target_ip': str, 'results': {port: 'open'|'closed'|error} }
    """
    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        raise

    results = {}
    for port in ports:
        try:
            is_open = scan_port(target_ip, int(port), timeout)
            results[int(port)] = 'open' if is_open else 'closed'
        except Exception as e:
            results[int(port)] = f'error: {e}'

    return {'target': target, 'target_ip': target_ip, 'results': results}


def main():
    target = input("Enter target website or IP (e.g., scanme.nmap.org): ")
    target = target.replace("https://", "").replace("http://", "").strip("/")

    try:
        scan_info = scan_ports(target, [21, 22, 23, 25, 80, 443, 8080])
    except socket.gaierror:
        print(f"\n[!] Error: Cannot resolve '{target}'.")
        return
    except Exception as e:
        print(f"\n[!] Error during scan: {e}")
        return

    print("-" * 50)
    print(f"Scanning Target: {scan_info['target_ip']} ({scan_info['target']})")
    print(f"Time Started   : {str(datetime.now())}")
    print("-" * 50)

    for port, status in scan_info['results'].items():
        if status == 'open':
            print(f"[+] Port {port}: OPEN")
        else:
            print(f"[-] Port {port}: {status}")

    print("-" * 50)
    print("Scan complete.")


if __name__ == "__main__":
    main()