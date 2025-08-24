# MethodHunter-v3-
MethodHunter v3 is a Python tool designed to detect and test for dangerous/misconfigured HTTP methods on web servers. It helps bug bounty hunters and security researchers quickly identify endpoints that may allow file uploads, modifications, or other insecure actions.


🚀 Features

Scans target URLs for common risky HTTP methods:

OPTIONS

PUT (file upload check included ✅)

DELETE

PATCH

TRACE

CONNECT

Automatically uploads a test file if PUT is allowed, and reports the URL.

Saves results into results.txt for later review.

Simple CLI usage for quick assessments.

🖥️ Usage

python3 method_hunter-v3.py -u http://target.com

-h, --help → show help message

python3 method_hunter-v3.py -u http://target.com

[*] Testing HTTP methods for: http://target.com
✅ OPTIONS: OPTIONS blocked (HTTP 501)
🚨 PUT: PUT confirmed exploitable at http://target/mhunter_b43de0bbbcc5465a8f9b1a7ba4cb635d.txt
✅ DELETE: DELETE blocked (HTTP 501)
✅ PATCH: PATCH blocked (HTTP 501)
✅ TRACE: TRACE blocked (HTTP 501)
✅ CONNECT: CONNECT blocked (HTTP 501)
[+] Results saved to results.txt

🧪 Testing Locally (Insecure Lab)

You can spin up a deliberately vulnerable server locally to test MethodHunter:

1. Download a file named as insecure_server.py
2. Run the server: sudo python3 insecure_server.py
3. Upload a file manually: curl -X PUT http://127.0.0.1:80/test.html -d '*h1>Hello, This is Mustafa-Almohsen</h1>'
4. Or test with the tool:

- python3 method_hunter-v3.py -u http://127.0.0.1:80

- OUTPUT:

[*] Testing HTTP methods for: http://127.0.0.1:80
✅ OPTIONS: OPTIONS blocked (HTTP 501)
🚨 PUT: PUT confirmed exploitable at http://127.0.0.1:80/mhunter_b43de0bbbcc5465a8f9b1a7ba4cb635d.txt
✅ DELETE: DELETE blocked (HTTP 501)
✅ PATCH: PATCH blocked (HTTP 501)
✅ TRACE: TRACE blocked (HTTP 501)
✅ CONNECT: CONNECT blocked (HTTP 501)
[+] Results saved to results.txt
