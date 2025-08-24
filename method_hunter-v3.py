#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MethodHunter v3 - Advanced HTTP Method Misconfiguration Scanner
"""

import requests
import argparse
import sys
import os
import uuid
from urllib.parse import urljoin
from colorama import Fore, Style, init as colorama_init

# Init color support
colorama_init(autoreset=True)

# Icons
ICONS = {
    "ok": "✅",
    "warn": "⚠️",
    "critical": "🚨",
    "info": "ℹ️",
    "test": "[*]",
    "target": "[+]"
}


def print_colored(msg, color=Fore.WHITE, emoji=""):
    print(f"{color}{emoji} {msg}{Style.RESET_ALL}")


def check_options(url, session):
    try:
        r = session.options(url, timeout=8)
        allow = r.headers.get("Allow")
        if allow:
            return True, f"Allowed methods: {allow}"
        elif r.status_code == 200:
            return False, "OPTIONS allowed but no 'Allow' header (suspicious)"
        else:
            return False, f"OPTIONS blocked (HTTP {r.status_code})"
    except Exception as e:
        return False, f"OPTIONS request failed: {e}"


def check_put(url, session):
    try:
        filename = f"mhunter_{uuid.uuid4().hex}.txt"
        test_url = urljoin(url + "/", filename)
        content = b"mhunter_put_test"

        # Try upload
        r = session.put(test_url, data=content, timeout=8)
        if r.status_code in [200, 201, 204]:
            # Try fetch
            fetch = session.get(test_url, timeout=8)
            if fetch.status_code == 200 and content in fetch.content:
                # Cleanup
                session.delete(test_url, timeout=5)
                return True, f"PUT confirmed exploitable at {test_url}"
            else:
                return False, "PUT might be allowed (200 OK) but file not retrievable"
        else:
            return False, f"PUT blocked (HTTP {r.status_code})"
    except Exception as e:
        return False, f"PUT request failed: {e}"


def check_delete(url, session):
    try:
        filename = f"mhunter_{uuid.uuid4().hex}.txt"
        test_url = urljoin(url + "/", filename)
        content = b"mhunter_delete_test"

        # Upload file first
        put_resp = session.put(test_url, data=content, timeout=8)
        if put_resp.status_code not in [200, 201, 204]:
            return False, "DELETE test skipped (PUT not allowed to create file)"

        # Try delete
        del_resp = session.delete(test_url, timeout=8)
        if del_resp.status_code in [200, 202, 204]:
            check = session.get(test_url, timeout=8)
            if check.status_code == 404:
                return True, f"DELETE confirmed exploitable at {test_url}"
            else:
                return False, "DELETE returned success but file still accessible"
        else:
            return False, f"DELETE blocked (HTTP {del_resp.status_code})"
    except Exception as e:
        return False, f"DELETE request failed: {e}"


def check_patch(url, session):
    try:
        r = session.patch(url, json={"mhunter": "test"}, timeout=8)
        if r.status_code < 400:
            return False, f"PATCH allowed (HTTP {r.status_code})"
        else:
            return False, f"PATCH blocked (HTTP {r.status_code})"
    except Exception as e:
        return False, f"PATCH request failed: {e}"


def check_trace(url, session):
    try:
        r = session.request("TRACE", url, timeout=8)
        if r.status_code < 400 and "TRACE" in r.text:
            return True, "TRACE confirmed enabled (echoed input)"
        elif r.status_code < 400:
            return False, f"TRACE might be enabled (HTTP {r.status_code})"
        else:
            return False, f"TRACE blocked (HTTP {r.status_code})"
    except Exception as e:
        return False, f"TRACE request failed: {e}"


def check_connect(url, session):
    try:
        r = session.request("CONNECT", url, timeout=8)
        if r.status_code < 400:
            return False, f"CONNECT might be allowed (HTTP {r.status_code})"
        else:
            return False, f"CONNECT blocked (HTTP {r.status_code})"
    except Exception as e:
        return False, f"CONNECT request failed: {e}"


def test_target(url, args):
    session = requests.Session()
    results = []
    print_colored(f"Testing HTTP methods for: {url}", Fore.CYAN, ICONS["test"])

    # OPTIONS
    allowed, msg = check_options(url, session)
    results.append((url, "OPTIONS", allowed, msg))

    # PUT
    allowed, msg = check_put(url, session)
    results.append((url, "PUT", allowed, msg))

    # DELETE
    allowed, msg = check_delete(url, session)
    results.append((url, "DELETE", allowed, msg))

    # PATCH
    allowed, msg = check_patch(url, session)
    results.append((url, "PATCH", allowed, msg))

    # TRACE
    allowed, msg = check_trace(url, session)
    results.append((url, "TRACE", allowed, msg))

    # CONNECT
    allowed, msg = check_connect(url, session)
    results.append((url, "CONNECT", allowed, msg))

    # Print results
    for u, method, confirmed, msg in results:
        if confirmed:
            print_colored(f"{method}: {msg}", Fore.RED, ICONS["critical"])
        elif "allowed" in msg.lower() or "enabled" in msg.lower():
            print_colored(f"{method}: {msg}", Fore.YELLOW, ICONS["warn"])
        else:
            print_colored(f"{method}: {msg}", Fore.GREEN, ICONS["ok"])

    # Save to file
    with open(args.output, "a", encoding="utf-8") as f:
        f.write(f"\n--- {url} ---\n")
        for u, method, confirmed, msg in results:
            status = "CONFIRMED" if confirmed else "INFO"
            f.write(f"[{method}] {status}: {msg}\n")
    print_colored(f"Results saved to {args.output}", Fore.CYAN, ICONS["target"])


def main():
    parser = argparse.ArgumentParser(description="MethodHunter v3 - HTTP Method Misconfiguration Scanner")
    parser.add_argument("-u", "--url", help="Target URL")
    parser.add_argument("-l", "--list", help="File with list of target URLs")
    parser.add_argument("-o", "--output", default="results.txt", help="Output file")
    args = parser.parse_args()

    if not args.url and not args.list:
        print("Usage: python3 methodhunter.py -u https://target.com OR -l urls.txt")
        sys.exit(1)

    targets = []
    if args.url:
        targets.append(args.url.strip())
    if args.list:
        with open(args.list, "r", encoding="utf-8") as f:
            targets.extend([line.strip() for line in f if line.strip()])

    for t in targets:
        test_target(t, args)


if __name__ == "__main__":
    main()
