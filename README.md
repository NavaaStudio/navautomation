# Navautomation — کلاینت رسمی اتوماسیون برای پیام‌رسان نوا

> **دو زبانه (فارسی ↔ English)** — هر بخش به‌صورت دوگانه ارائه شده است: ابتدا فارسی، سپس متن معادل انگلیسی. این فایل برای قرارگیری در ریشهٔ مخزن گیت‌هاب و استفادهٔ رسمی به‌عنوان README طراحی شده است.

---

# مروری کوتاه

**فارسی**

Navautomation یک کتابخانهٔ پایتون رسمی و سبک برای تعامل برنامه‌محور با سرور پیام‌رسان «نوا» است. این پروژه با هدف فراهم کردن رابطی واضح، امن و قابل تست برای عملیات رایج (ورود، ثبت‌نام، مدیریت نشست رمزگذاری‌شده، ارسال/دریافت پیام، آپلود فایل و امور مدیریتی پایه) طراحی شده است.

**English**

Navautomation is a compact, production-oriented Python client library to interact programmatically with a Nava messenger server. It aims to provide a clear, secure and testable interface for common operations (login, signup, encrypted session management, send/receive messages, uploads, and basic administrative actions).

---

# اهداف و اصول طراحی

**فارسی**

* **شفافیت و سادگی API**: توابع با نام‌های کوتاه و قابل فهم طراحی شده‌اند تا استفادهٔ روزمره و نوشتن اسکریپت را تسهیل کنند.
* **امنیت**: ذخیرهٔ نشست به‌صورت رمزنگاری‌شده، مدیریت خطاهای سرور با ساختار مشخص، و رعایت اصول حداقلی در تعامل با سرور.
* **قابلیت تست و توسعه**: جداکردن منطق شبکه، نگاشت خطاها و تاریخچهٔ لاگ مناسب برای تست و توسعه در محیط CI.

**English**

* **API clarity**: Short, predictable function names to simplify scripting and automation tasks.
* **Security**: Encrypted session storage, structured server error handling, and minimal safe defaults when interacting with the server.
* **Testability**: Network logic separated from business logic, consistent error types, and clear points for unit / integration testing.

---

# ویژگی‌های کلیدی / Key features

**فارسی**

* پشتیبانی از عملیات پایهٔ کاربر: ثبت‌نام، ورود (پسورد و OTP)
* ارسال، ویرایش، حذف پیام؛ واکنش (reaction)؛ علامت‌گذاری خوانده‌شده
* ارسال فایل (آپلود) با پشتیبانی multipart
* مدیریت گروه و کانال (ایجاد، پیوستن)
* ذخیره/بارگذاری نشست رمزنگاری‌شده (`session.nava`)
* خطاهای استاندارد شده (`NavaErr`) برای هندلینگ پیوسته

**English**

* User operations: signup, login (password and OTP)
* Message operations: send, edit, delete, react, mark-read
* File upload (multipart)
* Group and channel management (create, join)
* Encrypted session persistence (`session.nava`)
* Standardized errors (`NavaErr`) for consistent handling

---

# نصب / Installation

**فارسی**

پیشنهاد می‌شود بسته را از PyPI نصب کنید:

```bash
pip install navautomation
```

برای نصب از سورس (در حالت توسعه):

```bash
git clone https://github.com/<your-repo>/navautomation.git
cd navautomation
python -m pip install -e .
```

**English**

Install from PyPI:

```bash
pip install navautomation
```

For editable installation from source (development):

```bash
git clone https://github.com/<your-repo>/navautomation.git
cd navautomation
python -m pip install -e .
```

---

# شروع سریع — Quickstart

**فارسی**

مثال کوتاه برای ورود، ارسال پیام و ذخیرهٔ سشن:

```python
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
```

**English**

Minimal example showing login, send message and save encrypted session:

```python
from navautomation.client import SyncClient

c = SyncClient()
# login
resp = c.auth_login("alice", "s3cr3t")
print(resp)
# send message to user id = 42
r = c.msg_send("user", 42, "Navautomation | NavaAutomation\nOfficial client for Nava messenger")
print(r)
# save encrypted session
c.sess_save("strong-passphrase")
```

---

# مروری بر API (خلاصه) / API reference (summary)

**فارسی**

توابع مهم کلاس `SyncClient`:

* `otp_send(email)` — ارسال کد OTP به ایمیل
* `otp_ver(email, code)` — تایید کد OTP
* `otp_login(email, code)` — ورود با OTP
* `auth_login(user, pwd)` — ورود با نام‌کاربری/رمز
* `auth_signup(user, email, pwd)` — ثبت‌نام کاربر
* `msg_send(tt, id, body)` — ارسال پیام؛ `tt` یکی از `user|group|channel`
* `msg_fetch(tt, id)` — واکشی پیام‌ها برای هدف مشخص
* `msg_edit(mid, body)` — ویرایش پیام
* `msg_del(mid)` — حذف پیام (soft delete)
* `react(mid, emoji, remove=False)` — واکنش به پیام
* `mark_read(from_user)` — علامت‌گذاری خوانده‌شده
* `upload(filepath)` — آپلود فایل (multipart)
* `join_group(gid)` — پیوستن به گروه
* `create_group(name, privacy)` — ایجاد گروه
* `create_channel(name, broadcast=False)` — ایجاد کانال
* `report(type, target_id, reason)` — ثبت گزارش
* `sess_save(passphrase)` / `sess_load(passphrase)` / `sess_rm()` — مدیریت نشست رمزنگاری‌شده

توابع بیشتر و جزئیات خطاها در داکیومنت کد و docstrings قرار دارد.

**English**

Key methods of `SyncClient`:

* `otp_send(email)` — send OTP email
* `otp_ver(email, code)` — verify OTP
* `otp_login(email, code)` — login using OTP
* `auth_login(user, pwd)` — login via username/password
* `auth_signup(user, email, pwd)` — signup
* `msg_send(tt, id, body)` — send message (tt ∈ `user|group|channel`)
* `msg_fetch(tt, id)` — fetch messages
* `msg_edit(mid, body)` — edit message
* `msg_del(mid)` — soft-delete message
* `react(mid, emoji, remove=False)` — add/remove reaction
* `mark_read(from_user)` — mark messages read
* `upload(filepath)` — file upload (multipart)
* `join_group(gid)`, `create_group(name, privacy)`, `create_channel(name, broadcast=False)`
* `report(type, target_id, reason)` — append report
* `sess_save(passphrase)`, `sess_load(passphrase)`, `sess_rm()` — encrypted session helpers

Detailed signatures and possible error responses are described in the package docstrings.

---

# مدیریت نشست رمزنگاری‌شده (`session.nava`) / Encrypted session storage

**فارسی**

* نشست‌ها به‌صورت یک فایل رمزنگاری‌شده محلی ذخیره می‌شوند (پیش‌فرض: `session.nava`).
* پیاده‌سازی توصیه‌شده: استفاده از AES-GCM با یک `passphrase` قوی برای رمزنگاری محتوا. فایل نباید در کنترل نسخه قرار گیرد.
* توابع مرتبط: `sess_save(passphrase)`, `sess_load(passphrase)`, `sess_rm()`.

**English**

* Sessions are persisted as a local encrypted file (default: `session.nava`).
* Recommended implementation: AES-GCM with a strong passphrase. Never commit the session file to version control.
* Methods: `sess_save(passphrase)`, `sess_load(passphrase)`, `sess_rm()`.

---

# نکات امنیتی و رعایت سیاست استفاده / Security & usage policy

**فارسی**

1. هرگونه ارسال گروهی یا خودکار پیام باید با رعایت قوانین محلی و سیاست‌های سرویس انجام شود. حتی در محیط تست از rate-limit و dry-run استفاده کنید.
2. اطلاعات حساس (رمز، توکن، passphrase) را در مخزن کد قرار ندهید؛ از متغیرهای محیطی یا secret store استفاده کنید.
3. لاگ‌ها را طوری بنویسید که اطلاعات حساس در آنها ثبت نشود.

**English**

1. Any automated or bulk messaging must comply with local laws and the platform policy. Always use rate-limiting and dry-run for tests.
2. Do not commit secrets (passwords, tokens, passphrases) to the repository — use environment variables or secret management.
3. Do not log sensitive material.

---

# بسته‌بندی و انتشار / Packaging & publishing (short)

**فارسی**

* از `pyproject.toml` با backendِ `setuptools` یا `flit` استفاده کنید.
* برای ساخت و تست بسته: `python -m build` سپس `twine` برای آپلود به TestPyPI و پس از آزمایش به PyPI اصلی.
* همواره از API token استفاده کنید و آن را در متغیرهای امن CI (مثل GitHub Actions secrets) ذخیره نمایید.

**English**

* Use `pyproject.toml` and build with `python -m build`.
* Upload to TestPyPI first via `twine`, verify, then upload to PyPI production.
* Use API tokens stored securely in CI.

---

# مشارکت / Contributing

**فارسی**

* Issues و Pull Requestها خوش‌آمد گفته می‌شوند. لطفاً قبل از ارسال PR، تست‌ها را اجرا و قالب‌بندی کد را رعایت کنید (`black`, `flake8`).
* برای تغییر API یا افزودن قابلیت بزرگ، ابتدا یک Issue باز کنید و طرح پیشنهادی را ارائه دهید.

**English**

* Issues and PRs are welcome. Run tests and format code before submitting a PR (`black`, `flake8`).
* For large API changes open an Issue first to discuss the design.

---

# لایسنس / License

**فارسی**

این پروژه تحت مجوز MIT منتشر می‌شود. متن کامل مجوز در فایل `LICENSE` قرار دارد.

**English**

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

# تماس / Contact

**فارسی**

برای گزارش باگ یا درخواست ویژگی از بخش Issues در مخزن استفاده کنید.

**English**

Use repository Issues to report bugs or request features.

---

*Document prepared for repository use. For additional assets (examples, CI workflows, or English-only readme) request a separate file.*
