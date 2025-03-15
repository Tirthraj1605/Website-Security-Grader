import ssl
import socket
import requests
from urllib.parse import urlparse


def get_certificate(hostname, port=443):
    context = ssl.create_default_context()
    conn = context.wrap_socket(socket.socket(), server_hostname=hostname)
    conn.settimeout(5)
    conn.connect((hostname, port))
    cert = conn.getpeercert()
    conn.close()
    return cert


def parse_certificate(cert):
    return {
        'subject': dict(x[0] for x in cert['subject']),
        'issuer': dict(x[0] for x in cert['issuer']),
        'valid_from': cert['notBefore'],
        'valid_to': cert['notAfter']
    }


def check_https(url):
    return url.lower().startswith('https')


def check_tls_version(hostname):
    context = ssl.create_default_context()
    with context.wrap_socket(socket.socket(), server_hostname=hostname) as s:
        s.connect((hostname, 443))
        return s.version()


def check_hsts(url):
    try:
        response = requests.get(url, timeout=5)
        return 'strict-transport-security' in response.headers
    except:
        return False


def check_headers(url):
    try:
        response = requests.get(url, timeout=5)
        headers = response.headers
        return {
            'X-Frame-Options': headers.get('X-Frame-Options', None),
            'X-Content-Type-Options': headers.get('X-Content-Type-Options', None),
            'X-XSS-Protection': headers.get('X-XSS-Protection', None)
        }
    except:
        return {}


def check_csp(url):
    try:
        response = requests.get(url, timeout=5)
        return 'content-security-policy' in response.headers
    except:
        return False


def check_cookie_security(url):
    try:
        response = requests.get(url, timeout=5)
        cookies = response.cookies
        secure_flags = [cookie.secure for cookie in cookies]
        return all(secure_flags) if secure_flags else False
    except:
        return False