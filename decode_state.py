import zlib
import base64

s = input("Enter the state:") #zlib un base64 kodētais URL state daļa
s += "=" * (-len(s) % 4) #atjauno trūkstošos '=' simbolus, lai padarītu to derīgu base64
compressed =  base64.urlsafe_b64decode(s) # base64 uz baitiem
json_bytes = zlib.decompress(compressed) # baiti un json baitiem
text = json_bytes.decode('utf-8') # json baitiem uz tekstu
print(text) #izvada json tekstu