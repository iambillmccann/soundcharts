import hashlib
import hmac

secret_key = '1234567890'  # Replace with your actual payload

data = '{"status": "success"}'  # Replace with your actual secret key

# Compute HMAC
signature = hmac.new(bytes(secret_key , 'latin-1'), msg = bytes(data , 'latin-1'), digestmod = hashlib.sha256).hexdigest()

print(signature)
