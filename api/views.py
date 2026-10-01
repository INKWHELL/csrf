import json

from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST


def csrf_failure_view(request, reason=""):

    return JsonResponse({"detail": f"CSRF Failed: {reason}"}, status=403)



@require_POST
def login_view(request):

    data = json.loads(request.body or "{}")
    user = authenticate(
        request, username=data.get("username"), password=data.get("password")
    )
    if user is None:
        return JsonResponse({"detail": "Invalid credentials."}, status=401)
    login(request, user)
    return JsonResponse({"detail": "Logged in.", "username": user.username})


@ensure_csrf_cookie
@require_GET
def csrf_view(request):

    return JsonResponse({"csrfToken": get_token(request)})


# ---------------------------------------------------------------------------
# VULNERABLE STATE (default): @csrf_exempt disables Django's CsrfViewMiddleware
# check for this endpoint — this is the misconfiguration under test in 5.4.
#
# FIX: delete the @csrf_exempt line below and restart the server. With it
# removed, CsrfViewMiddleware will reject any POST to this endpoint that
# does not carry a valid, matching CSRF token.

@require_POST
def change_email_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({"detail": "Authentication required."}, status=401)
    new_email = request.POST.get("email", "")
    request.user.email = new_email
    request.user.save(update_fields=["email"])
    return JsonResponse({"detail": "Email updated.", "email": new_email})
