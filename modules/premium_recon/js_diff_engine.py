import os
import re
import difflib
import urllib.request
from pathlib import Path
from typing import Dict, List
from core.license_validator import requires_premium

class JSDiffEngine:
    def __init__(self):
        self.cache_dir = Path("cache/js_history")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        # Patterns for detecting modern API route patterns and potential configuration variables
        self.endpoint_pattern = re.compile(r'["\'](/api/v[0-9]/[a-zA-Z0-9_\-\.\/]+)["\']')
        self.keyword_pattern = re.compile(r'\b(secret|token|api_key|auth|staging|dev_env|bearer)\b\s*[:=]', re.IGNORECASE)

    def _sanitize_filename(self, url: str) -> str:
        """Converts a URL into a safe, valid local file name."""
        return re.sub(r'[^a-zA-Z0-9_\.-]', '_', url.replace("http://", "").replace("https://", "")) + ".js"

    def _fetch_remote_js(self, url: str) -> str:
        """Downloads remote textual assets securely using Python standard utilities."""
        try:
            req = urllib.request.Request(
                url, 
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Asset-Monitor/1.0'}
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                return response.read().decode('utf-8', errors='ignore')
        except Exception as e:
            print(f"[-] Fetch failed for {url}: {e}")
            return ""

    @requires_premium
    def monitor_and_diff(self, url: str) -> Dict[str, List[str]]:
        """Downloads live JS asset, compares to local history, and extracts actionable indicators."""
        print(f"[+] Running Premium JS Changelog Monitor for: {url}")
        
        live_content = self._fetch_remote_js(url)
        if not live_content:
            return {"new_endpoints": [], "suspicious_additions": []}

        filename = self._sanitize_filename(url)
        cache_path = self.cache_dir / filename
        
        findings = {"new_endpoints": [], "suspicious_additions": []}

        # If historical state does not exist, initialize cache and extract base baseline indicators
        if not cache_path.exists():
            with open(cache_path, "w", encoding="utf-8") as f:
                f.write(live_content)
            print(f"[+] Initialized history baseline tracking cache for: {filename}")
            return findings

        # Read historical textual data state
        with open(cache_path, "r", encoding="utf-8") as f:
            old_content = f.read()

        # Compute Unified Diff structural differences
        old_lines = old_content.splitlines()
        new_lines = live_content.splitlines()
        diff = list(difflib.unified_diff(old_lines, new_lines, n=0))

        # Filter and parse explicit additions (Lines prefixed with '+')
        additions = [line[1:].strip() for line in diff if line.startswith('+') and not line.startswith('+++')]

        for line in additions:
            # Detect newly appended relative endpoint links
            for endpoint in self.endpoint_pattern.findall(line):
                findings["new_endpoints"].append(endpoint)
            # Check for interesting administrative keywords matching the pattern matrix
            if self.keyword_pattern.search(line):
                findings["suspicious_additions"].append(line)

        # Update persistent cache snapshot with the latest iteration
        with open(cache_path, "w", encoding="utf-8") as f:
            f.write(live_content)

        return findings
