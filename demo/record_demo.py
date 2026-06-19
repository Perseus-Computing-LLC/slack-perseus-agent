#!/usr/bin/env python3
"""Record Perseus for Slack demo video.
Usage: python3 record_demo.py [--duration 165]
"""

import http.server
import socketserver
import threading
import time
import sys
import os

# Config
PROJECT_ROOT = '/opt/data/webui/minions/.minions-data/workspace/slack-perseus-agent'
DEMO_DIR = os.path.join(PROJECT_ROOT, 'demo')
HTML_FILE = os.path.join(DEMO_DIR, 'demo_terminal.html')
OUTPUT_DIR = os.path.join(DEMO_DIR, 'video_output')
DURATION = int(sys.argv[1]) if len(sys.argv) > 1 else 165  # ~2:45

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Start HTTP server in demo directory
os.chdir(DEMO_DIR)
httpd = socketserver.TCPServer(("127.0.0.1", 9876), http.server.SimpleHTTPRequestHandler)
t = threading.Thread(target=httpd.serve_forever, daemon=True)
t.start()
print(f"HTTP server started on http://127.0.0.1:9876")

try:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 1280, 'height': 720},
            record_video_dir=OUTPUT_DIR,
            record_video_size={'width': 1280, 'height': 720},
        )
        page = context.new_page()

        print("Navigating to demo terminal...")
        page.goto('http://127.0.0.1:9876/demo_terminal.html',
                  wait_until='domcontentloaded', timeout=15000)

        # Verify JS is running
        time.sleep(4)
        screen_text = page.inner_text('#screen')
        print(f"Screen has content: {len(screen_text)} chars")
        if len(screen_text) < 10:
            errors = []
            page.on('pageerror', lambda err: errors.append(str(err)))
            time.sleep(2)
            print(f"WARNING: Screen appears empty! JS errors: {errors}")

        # Wait for demo to complete
        print(f"Recording for {DURATION}s...")
        time.sleep(DURATION)

        context.close()
        browser.close()
        print("Recording complete!")

        # Find the WebM file
        webm_files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith('.webm')]
        if webm_files:
            webm_path = os.path.join(OUTPUT_DIR, webm_files[0])
            print(f"WebM saved: {webm_path}")
        else:
            print("ERROR: No WebM file found in output directory")

except Exception as e:
    print(f"Recording failed: {e}")
    import traceback
    traceback.print_exc()
finally:
    httpd.shutdown()
    print("HTTP server stopped")
