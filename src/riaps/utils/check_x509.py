'''
Created on Nov 26, 2024

@author: riaps
'''
from cryptography import x509
from cryptography.hazmat.backends import default_backend
import datetime

def check_x509_validity(cert_path):
    try:
        with open(cert_path, 'rb') as cert_file:
            cert_data = cert_file.read()
            cert = x509.load_pem_x509_certificate(cert_data, default_backend())

        # Check if the certificate is valid at the current time
        now = datetime.datetime.utcnow()
        if cert.not_valid_before <= now <= cert.not_valid_after:
            return True
        else:
            return False

    except Exception as e:
        print(f"Error checking certificate: {e}")
        return False
