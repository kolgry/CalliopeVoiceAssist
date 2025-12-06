import webbrowser as wb
import os
import platform


class BrowserManager:

    def __init__(self):
        self.system = platform.system()
        self.available_browsers = []
        self.detect_browsers()

    def detect_browsers(self):
        if self.system == "Windows":
            browser_paths = {
                'chrome': r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                'chrome_x86': r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
                'edge': r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
                'firefox': r'C:\Program Files\Mozilla Firefox\firefox.exe',
                'firefox_x86': r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe',
                'vivaldi': r'C:\Users\{}\AppData\Local\Vivaldi\Application\vivaldi.exe'.format(os.getenv('USERNAME')),
                'brave': r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe',
                'opera': r'C:\Users\{}\AppData\Local\Programs\Opera\opera.exe'.format(os.getenv('USERNAME')),
            }
        elif self.system == "Darwin":
            browser_paths = {
                'chrome': '/Applications/Google Chrome.app',
                'firefox': '/Applications/Firefox.app',
                'safari': '/Applications/Safari.app',
                'edge': '/Applications/Microsoft Edge.app',
                'vivaldi': '/Applications/Vivaldi.app',
                'brave': '/Applications/Brave Browser.app',
                'opera': '/Applications/Opera.app',
            }
        else:
            browser_paths = {
                'chrome': '/usr/bin/google-chrome',
                'chromium': '/usr/bin/chromium-browser',
                'firefox': '/usr/bin/firefox',
                'vivaldi': '/usr/bin/vivaldi',
                'brave': '/usr/bin/brave-browser',
                'opera': '/usr/bin/opera',
            }

        for name, path in browser_paths.items():
            if os.path.exists(path):
                self.available_browsers.append((name, path))
                print(f"[INFO] Found browser: {name}")

        if not self.available_browsers:
            print("[WARNING] No specific browsers found, will use system default")

    def get_browser(self):
        """Get a browser controller with fallback support"""
        if not self.available_browsers:
            return wb.get()

        for name, path in self.available_browsers:
            try:
                if self.system == "Windows":
                    return wb.get(f'"{path}" %s')
                elif self.system == "Darwin":
                    return wb.get(f'open -a "{path}" %s')
                else:
                    return wb.get(f'{path} %s')
            except Exception as e:
                print(f"[WARNING] Could not register {name}: {e}")
                continue

        return wb.get()

    def open_url(self, url):
        """Open URL with the best available browser"""
        try:
            browser = self.get_browser()
            browser.open(url)
            return True
        except Exception as e:
            print(f"[ERROR] Could not open browser: {e}")
            try:
                wb.open(url)
                return True
            except:
                return False