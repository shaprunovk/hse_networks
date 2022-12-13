import argparse
import subprocess
import ipaddress

def ping(host, packet_size):
    process = subprocess.run(
        ["ping", host, "-M", "do", "-s", packet_size, "-c", "1"],
        stdout=subprocess.DEVNULL
    )
    return process.returncode == 0


def find_mtu(host):
    min_mtu = 1
    max_mtu = 10000
    while max_mtu - min_mtu > 1:
        mtu = (min_mtu + max_mtu) // 2
        print(f'Current check MTU: {mtu}')
        if ping(host, str(mtu)):
            min_mtu = mtu
        else:
            max_mtu = mtu
    return min_mtu

def check_domain(domain):
    alph = 'abcdefghijklmnopqrstuvwxyz'
    alph += alph.upper()
    alph += '1234567890'
    for ch in domain:
        if alph.find(ch) == -1:
            return False
    return True

def check_literal_host(host):
    domains = host.split('.')
    for domain in domains:
        if not check_domain(domain):
            return False
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('host')

    args = parser.parse_args()
    host = args.host

    try:
        ipaddress.ip_address(host)
    except:
        if not check_literal_host(host):
            print(f'Incorrect hostname: {host}')
            exit(1)

    try:
        ping(host, "1")
    except:
        print(f'Host error for {host}')
        exit(1)

    mtu = find_mtu(host)
    print(f'MTU = {mtu}')

if __name__ == '__main__':
    main()