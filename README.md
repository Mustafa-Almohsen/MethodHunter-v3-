⚠️ Disclaimer

This tool is for educational and authorized security testing only. I am not responsible for misuse.
----

MethodHunter-v3-
MethodHunter v3 is a Python tool designed to detect and test for dangerous/misconfigured HTTP methods on web servers. It helps bug bounty hunters and security researchers quickly identify endpoints that may allow file uploads, modifications, or other insecure actions.

-------

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
------

python3 method_hunter-v3.py -u htt*://target.com

-h, --help → show help message

python3 method_hunter-v3.py -u htt*://target.com


----- 

🧪 Testing Locally (Insecure Lab)

You can spin up a deliberately vulnerable server locally to test MethodHunter:

1. Download a file named as insecure.py
2. Run the server: sudo python3 insecure.py
3. Upload a file manually: curl -X PUT htt*://127.0.0.1:80/test.txt -d '{"key": "Hello,This is Mustafa-Almohsn"}'
4. Or test with the tool:

- python3 method_hunter-v3.py -u htt*://127.0.0.1:80

  <img width="1269" height="323" alt="image" src="https://github.com/user-attachments/assets/a633b9a7-95e9-46ca-a9f4-e530691f6573" />

