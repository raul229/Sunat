import requests
import hashlib
import base64
import os
import uuid
import re

# ---------------- CONFIG ----------------
TENANT_ID = "5936fc44-399a-4904-b3e2-dfbc9d8577d8"
CLIENT_ID = "3e62f81e-590b-425b-9531-cad6683656cf"
REDIRECT_URI = "https://apps.powerapps.com/auth/v2"
SCOPE = "https://service.powerapps.com//.default openid profile offline_access"

EMAIL = ""


# ---------------- PKCE ----------------
def generate_pkce():
    code_verifier = base64.urlsafe_b64encode(os.urandom(40)).decode().rstrip("=")
    challenge = hashlib.sha256(code_verifier.encode()).digest()
    code_challenge = base64.urlsafe_b64encode(challenge).decode().rstrip("=")
    return code_verifier, code_challenge


# ---------------- INICIO ----------------
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0",
})

code_verifier, code_challenge = generate_pkce()

state = base64.urlsafe_b64encode(uuid.uuid4().bytes).decode().rstrip("=")
nonce = str(uuid.uuid4())

authorize_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/authorize"

params = {
    "client_id": CLIENT_ID,
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    "response_mode": "fragment",
    "code_challenge": code_challenge,
    "code_challenge_method": "S256",
    "state": state,
    "nonce": nonce
}

r1 = session.get(authorize_url, params=params)
print("Authorize status:", r1.status_code)

html = r1.text

# ---------------- EXTRAER TOKENS DINÁMICOS ----------------
def extract(pattern, text):
    match = re.search(pattern, text)
    return match.group(1) if match else None

sFT = extract(r'"sFT":"(.*?)"', html)
sCtx = extract(r'"sCtx":"(.*?)"', html)
canary = extract(r'"canary":"(.*?)"', html)
hpgid = extract(r'"hpgid":(\d+)', html)
hpgact = extract(r'"hpgact":(\d+)', html)

print("sFT:", bool(sFT))
print("sCtx:", bool(sCtx))
print("canary:", bool(canary))
print("hpgid:", hpgid)
print("hpgact:", hpgact)

# ---------------- PASO 2: ENVIAR USERNAME ----------------
login_url = f"https://login.microsoftonline.com/{TENANT_ID}/login"

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "canary": canary,
    "client-request-id": str(uuid.uuid4()),
    "hpgid": hpgid,
    "hpgact": hpgact,
    "Origin": "https://login.microsoftonline.com",
    "Referer": r1.url
}

payload = {
    "login": EMAIL,
    "loginfmt": EMAIL,
    "type": "11",
    "LoginOptions": "3",
    "flowToken": sFT,
    "ctx": sCtx
}

r2 = session.post(login_url, headers=headers, data=payload)

print("Username POST status:", r2.status_code)

# Guardamos respuesta para inspección
with open("after_username.html", "w", encoding="utf-8") as f:
    f.write(r2.text)

print("Respuesta guardada en after_username.html")