# Navautomation

**کتابخانهٔ رسمی خودکارسازی برای پیام‌رسان نوا**

> نسخه: رسمی | زبان‌ها: فارسی / English

---

## خلاصه — فارسی

Navautomation یک کتابخانهٔ پایتون برای خودکارسازی و تعامل با API پیام‌رسان `nava.bolino.ir` است. این بسته کلاینت‌های همگام (`SyncClient`) و ناهمگام (`AsyncClient`)، مکانیزم امن ذخیرهٔ سشن (`session.nava`) و توابع کمکی رایج (ورود، ارسال پیام، آپلود، مدیریت گروه/کانال، OTP و غیره) را فراهم می‌کند.

این README به‌صورت رسمی و حرفه‌ای نوشته شده و راهنمای نصب فوری، مثال‌های کاربردی، و نکات امنیتی را در خود دارد.

---

## Summary — English

Navautomation is a Python automation library for interacting with the Nava messaging platform API at `nava.bolino.ir`. It provides synchronous (`SyncClient`) and asynchronous (`AsyncClient`) clients, secure encrypted session persistence (`session.nava`) and utility helpers for common operations (auth, messaging, uploads, group/channel management, OTP, etc.).

This README contains installation, quickstart examples, security notes and publishing guidance.

---

# Table of contents / فهرست محتوا

1. Installation / نصب
2. Quickstart examples / نمونهٔ سریع
3. Sessions (encrypted) / سشن‌ها (رمزگذاری‌شده)
4. API surface / قابلیت‌ها
5. Admin usage & caution / استفادهٔ مدیریتی و هشدار
6. Packaging & publish / بسته‌بندی و انتشار
7. Contributing / مشارکت
8. License / مجوز
9. FAQ / عیب‌یابی مختصر

---

## 1) Installation / نصب (فوری)

> نصب آخرین کد از شاخهٔ `main` (فوری):

```bash
pip install git+https://github.com/NavaaStudio/navautomation.git@main
```

برای توسعه محلی (editable):

```bash
git clone https://github.com/NavaaStudio/navautomation.git
cd navautomation
pip install -e .
```

پیش‌نیازهای پایه (در `requirements.txt`):

```
requests>=2.28
aiohttp>=3.8
cryptography>=40
```

---

## 2) Quickstart / نمونهٔ سریع

### Sync client (همگام)

```py
from navautomation.client import SyncClient

c = SyncClient()  # base و api_path از config پیش‌فرض استفاده می‌کنند
# ورود با نام کاربری
c.auth_login('username', 'password')
# ارسال پیام
c.msg_send('user', 42, 'سلام از Navautomation')
# ذخیرهٔ سشن به فایل session.nava (رمزنگاری‌شده)
c.sess_save('my passphrase')
```

### Async client (ناهمگام)

```py
import asyncio
from navautomation.async_client import AsyncClient

async def main():
    c = AsyncClient()
    await c.auth_login('username', 'password')
    await c.msg_send('user', 42, 'پیام ناهمگام')
    await c.close()

asyncio.run(main())
```

---

## 3) Sessions: `session.nava` (رمزگذاری‌شده)

* فایل سشن به شکل `session.nava` در همان فولدری که اسکریپت اجرا می‌شود ذخیره می‌گردد (یا مسیر مشخص‌شده توسط کاربر).
* محتوای فایل با `cryptography.Fernet` رمزگذاری می‌شود — برای بارگزاری مجدد باید همان passphrase را وارد کنید.
* نکتهٔ امنیتی: عبارت عبور را امن نگهداری کنید؛ اگر فراموش شود، سشن قابل بازیابی نیست.

---

## 4) امکانات کلی / API surface

کوتاه و مفید (توابع کلیدی):

* احراز هویت:

  * `otp_send(email)`
  * `otp_ver(email, code)`
  * `otp_login(email, code)`
  * `auth_login(username, password)`
  * `auth_signup(username, email, password)`
* پیام‌رسانی:

  * `msg_send(target_type, target_id, body)`
  * `msg_fetch(target_type, target_id)`
  * `msg_edit(message_id, body)`
  * `msg_del(message_id)`
  * `react(message_id, emoji, remove=False)`
  * `mark_read(from_user)`
* فایل و آپلود:

  * `upload(filepath)` (multipart)
* گروه/کانال:

  * `join_group(group_id)`, `create_group(name, privacy)`
  * `create_channel(name, is_broadcast)`
* Session helpers:

  * `sess_save(passphrase)`, `sess_load(passphrase)`, `sess_rm()`

---

## 5) Administrative use, announcements and safety

* اگر شما مالک سرور و ادمین هستید؛ می‌توانید ابزارهای عمومی/اعلانی را اجرا کنید. قبل از ارسال پیام انبوه:

  * سقف ریت-لیمیت سرور را بررسی کنید.
  * بین ارسال‌ها تأخیر منطقی (`sleep`) قرار دهید.
  * گزارش و لاگ ایجاد کنید تا در صورت نیاز بتوانید پیام‌ها را ردیابی کنید.
* مثال اعلان تک‌بار برای شناسه‌های کاربری 1..20:

```py
from time import sleep
from navautomation.client import SyncClient

c = SyncClient()
c.auth_login('NavautomationGlobalAnnouncements', '3vdifji449')
text = 'Navautomation | نواتومیشن\nکتابخانه سلف برای پیامرسان نوا'
for uid in range(1,21):
    c.msg_send('user', uid, text)
    sleep(0.5)  # تأخیر کوچک برای احترام به محدودیت‌ها
```

> هشدار: استفادهٔ نابجا یا ارسال مکرر می‌تواند موجب مسدودسازی حساب‌ها شود. از این قابلیت تنها در شرایط مجاز و با اطلاع کاربران استفاده کنید.

---

## 6) Packaging & publish (خلاصه)

1. نسخهٔ جدید را در `pyproject.toml` یا `setup.cfg` به‌روزرسانی کنید.
2. بسته‌بندی:

   ```bash
   python -m build
   ```
3. بارگذاری به PyPI (نیاز به حساب PyPI):

   ```bash
   pip install twine
   twine upload dist/*
   ```
4. پس از انتشار، نصب با `pip install navautomation` امکان‌پذیر است.

نکته: در زمان انتشار عمومی، نام پکیج و وابستگی‌ها را با دقت بررسی کنید.

---

## 7) Contributing / مشارکت

* برای مشارکت: fork کنید، شاخهٔ feature بسازید، تغییرات را در branch خود انجام دهید و pull request ارسال کنید.
* از linters و قالب‌بندی (Black, flake8) استفاده کنید و تست‌های واحد اضافه کنید.

---

## 8) License / مجوز

پروژه تحت مجوز **MIT** منتشر می‌شود. لطفاً فایل `LICENSE` را در repo قرار دهید.

---

## 9) FAQ / Troubleshooting (مختصر)

* `ModuleNotFoundError: async_client` → اگر این خطا را دارید، نسخهٔ نصب‌شده ناقص است؛ دستور نصب از گیت را اجرا کنید:

```bash
pip install --upgrade git+https://github.com/NavaaStudio/navautomation.git@main
```

* مشکل بارگذاری/ذخیرهٔ session → بررسی کنید `cryptography` نصب شده و از همان passphrase استفاده می‌کنید.

---

## Contact / تماس

برای گزارش باگ یا درخواست ویژگی از بخش Issues در گیت‌هاب استفاده کنید.

---
