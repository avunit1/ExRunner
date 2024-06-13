import hashlib

# Open the file to calculate the hash of
with open('ExRunner.exe', 'rb') as f:
    data = f.read()

# Calculate the SHA256 hash
hash_object = hashlib.sha256()
hash_object.update(data)
hex_dig = hash_object.hexdigest()

# Save the hash to the hash.md5 file
with open('hash/hash_exe.md5', 'w') as f:
    f.write(hex_dig)
