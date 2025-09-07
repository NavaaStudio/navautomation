from navautomation.client import SyncClient

c = SyncClient()
# ورود
resp = c.auth_login("alice", "s3cr3t")
print(resp)
# ارسال پیام به user id = 42
r = c.msg_send("user", 42, "Navautomation | نواتومیشن\nکتابخانه رسمی برای پیام‌رسان نوا")
print(r)
# ذخیرهٔ سشن رمزنگاری‌شده
c.sess_save("strong-passphrase")
