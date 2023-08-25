import hashlib
import hmac

# Your request payload
data = 'YOUR_PAYLOAD_HERE'  # Replace with your actual payload

# The shared secret key from Veriff
secret_key = 'YOUR_SECRET_KEY_HERE'  # Replace with your actual secret key

# Compute HMAC
signature = hmac.new(bytes(secret_key , 'latin-1'), msg = bytes(data , 'latin-1'), digestmod = hashlib.sha256).hexdigest()

print(signature)
