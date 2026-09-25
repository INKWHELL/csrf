# 5.4 CSRF — Evidence Project

Reproduces Build, Break, Fix and Evaluation for the missing/misconfigured
CSRF protection vulnerability, so you can capture real screenshots instead
of describing the expected output.

## Layout

```
csrf-demo/
├── manage.py
├── requirements.txt
├── config/          Django settings + urls
├── api/             /api/login/, /api/csrf/, /api/account/email/
├── frontend/         legit.html — trusted frontend (port 5501)
└── attacker/         attacker.html — bare auto-submitting form (port 5500)
```

## One-time setup

```bash
cd csrf-demo
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo_user   # creates joe / testpass123
```

Use Chrome. Run three servers, each in its own terminal:

```bash
# Terminal 1 — Django API
python manage.py runserver 7999

# Terminal 2 — trusted frontend
cd frontend && python -m http.server 5501

# Terminal 3 — attacker page
cd attacker && python -m http.server 5500
```

`api/views.py` has `@csrf_exempt` on `change_email_view` by default — this
is the vulnerable state.

## Capturing the Build evidence (safe baseline)

1. Go to `http://localhost:5501/legit.html`, click **Log in as joe**.
2. Click **Change email (legitimate request)**.
3. Screenshot the output showing `{"detail": "Email updated.", "email": "joe-updated@example.com"}`.

This proves the endpoint works correctly for its intended purpose before
the vulnerability is introduced.

## Capturing the Break evidence (vulnerable state)

4. With `@csrf_exempt` still in place, open `http://localhost:5500/attacker.html`.
   It submits itself on load — no click needed.
5. Screenshot the Network tab's `/api/account/email/` request/response:
   the request carries the victim's `sessionid` cookie and no CSRF token,
   and the response is `200 OK` with `{"detail": "Email updated.", "email": "attackersemail@gmail.com"}`.
6. Reload `legit.html` and check the account's email now shows the
   attacker's address — confirms the change was real, not just a response body.

## Capturing the Fix / Evaluation evidence (fixed state)

7. In `api/views.py`, delete the `@csrf_exempt` line directly above
   `def change_email_view(request):`. Save.
8. Restart the Django server (Ctrl+C, then `python manage.py runserver 7999` again).
9. Reload `http://localhost:5500/attacker.html`.
10. Screenshot the Network tab response: now `403 Forbidden`, with a JSON
    body starting `"CSRF Failed: ..."`.
11. Go back to `legit.html`, log in again if needed, and click
    **Change email**. Screenshot the successful `200 OK` response —
    confirms the fix didn't break the legitimate flow.

## Note on the exact failure message

Django checks the `Origin` header before it checks for a CSRF token. Since
the attacker's origin (`5500`) is not in `CSRF_TRUSTED_ORIGINS`, the actual
response you'll see is:

```json
{"detail": "CSRF Failed: Origin checking failed - http://localhost:5500 does not match any trusted origins."}
```

rather than a "token missing" message — Django rejects it at the origin
check, before it would even get to checking for a token. This is expected
and still confirms the fix: the request is blocked either way, and this
matches your Fix section's point that only Django's own middleware, not a
manually reimplemented check, determines the outcome.

## Resetting between attempts

```bash
rm db.sqlite3
python manage.py migrate
python manage.py seed_demo_user
```
