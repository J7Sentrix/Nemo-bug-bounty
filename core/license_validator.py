import os
import json
import base64
import hmac
import hashlib
from datetime import datetime
from functools import wraps
from pathlib import Path
from config.config import config

class LicenseValidator:
    def __init__(self):
        # Secure Master Secret Key used to verify integrity
        # In production, change this to a complex unique byte sequence
        self._SECRET_KEY = b"SECRET_PAYPAL_BACKEND_SIGNING_KEY_2026"
        self.is_premium_active = False
        self.license_data = {}

    def verify_license(self) -> bool:
        """Reads local license file and cryptographically checks expiration and validity."""
        license_path = config.get("LICENSE_PATH")
        
        if not os.path.exists(license_path):
            self.is_premium_active = False
            return False

        try:
            with open(license_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            payload_str = data.get("payload", "")
            signature_received = data.get("signature", "")

            if not payload_str or not signature_received:
                self.is_premium_active = False
                return False

            # Cryptographic Validation using SHA256 HMAC
            expected_signature = hmac.new(
                self._SECRET_KEY, 
                payload_str.encode("utf-8"), 
                hashlib.sha256
            ).hexdigest()

            if not hmac.compare_digest(expected_signature, signature_received):
                print("[!] Warning: Cryptographic signature mismatch! Premium disabled.")
                self.is_premium_active = False
                return False

            # Expiration Constraints Check
            payload = json.loads(payload_str)
            expires_at_str = payload.get("expires_at", "1970-01-01")
            expiration_date = datetime.strptime(expires_at_str, "%Y-%m-%d")

            if datetime.now() > expiration_date:
                print(f"[!] Subscription expired on {expires_at_str}. Please renew via PayPal.")
                self.is_premium_active = False
                return False

            # License Validated Successfully
            self.license_data = payload
            self.is_premium_active = True
            return True

        except Exception as e:
            print(f"[!] System Exception validating premium license data: {e}")
            self.is_premium_active = False
            return False

def requires_premium(func):
    """Decorator to securely gate premium orchestration routines."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        validator = LicenseValidator()
        if validator.verify_license():
            return func(*args, **kwargs)
        else:
            print("\n" + "="*60)
            print("[!] ACCESS DENIED: This feature requires an active premium subscription.")
            print("[+] Unlock premium features instantly by subscribing via PayPal.")
            print("="*60 + "\n")
            return None
    return wrapper
