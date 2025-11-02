from cryptography.fernet import Fernet
print("Sikahkan copy encrypt key ini, dan simpan ke config.\nCatatan:\nJangan sampe hilang, jika hikang maka database gabisa di buka!")
print(f"\n\nKey:\n{Fernet.generate_key().decode()}")