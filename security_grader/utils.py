def assign_grade(results):
    score = 0

    if results.get('https'): score += 2
    if results.get('tls_version') in ['TLSv1.3', 'TLSv1.2']: score += 2
    if results.get('certificate_valid'): score += 2
    if results.get('hsts'): score += 2
    if results.get('secure_headers'): score += 2
    if results.get('csp'): score += 2
    if results.get('cookie_secure'): score += 2

    if score >= 12:
        return 'A+'
    elif score >= 10:
        return 'A'
    elif score >= 8:
        return 'B'
    elif score >= 6:
        return 'C'
    else:
        return 'D'