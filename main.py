from security_grader import (
    check_https, get_certificate, parse_certificate,
    check_tls_version, check_hsts, check_headers,
    check_csp, check_cookie_security, assign_grade
)
from urllib.parse import urlparse

url = input("Enter a website URL (e.g., https://example.com): ").strip()
hostname = urlparse(url).hostname

results = {}
results['https'] = check_https(url)

try:
    cert = get_certificate(hostname)
    cert_info = parse_certificate(cert)
    results['certificate_valid'] = True
except:
    results['certificate_valid'] = False

results['tls_version'] = check_tls_version(hostname)
results['hsts'] = check_hsts(url)
headers = check_headers(url)
results['secure_headers'] = all(headers.values())
results['csp'] = check_csp(url)
results['cookie_secure'] = check_cookie_security(url)

print("\n🔍 Security Details:")
print(f"🔐 HTTPS Supported: {results['https']}")
print(f"📜 TLS Version: {results['tls_version']}")
print(f"📅 Certificate Valid: {results['certificate_valid']}")
print(f"🛡️ HSTS Enabled: {results['hsts']}")
print(f"🔒 Secure Headers Present: {headers}")
print(f"📑 CSP Enabled: {results['csp']}")
print(f"🍪 All Cookies Secure: {results['cookie_secure']}")

final_grade = assign_grade(results)
print(f"\n✅ Final Security Grade: {final_grade}")