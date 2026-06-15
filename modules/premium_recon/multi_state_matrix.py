import urllib.request
import urllib.error
from typing import Dict, Any, List
from core.license_validator import requires_premium

class MultiStateMatrix:
    """
    Automated Access Control Matrix Tester. Replays transactions across multiple
    session states (e.g., Admin, User B, Anonymous) to map authorization anomalies.
    """
    def __init__(self):
        pass

    def _dispatch(self, url: str, headers: Dict[str, str]) -> Dict[str, Any]:
        """Internal helper to dispatch requests safely and capture response matrices."""
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=7) as response:
                body = response.read().decode('utf-8', errors='ignore')
                return {"status": response.status, "length": len(body)}
        except urllib.error.HTTPError as e:
            return {"status": e.code, "length": 0}
        except Exception as e:
            return {"status": 0, "length": 0}

    @requires_premium
    def run_matrix_analysis(self, target_url: str, admin_auth: str, user_auth: str) -> Dict[str, Dict[str, Any]]:
        """
        Executes structural differential analysis across three isolated authorization boundaries.
        """
        print(f"[+] Launching Multi-State Authorization Matrix for: {target_url}")
        
        # Define standard profiling header maps
        states = {
            "privileged_state": {"Authorization": admin_auth, "User-Agent": "Matrix Engine/1.0"},
            "low_privilege_state": {"Authorization": user_auth, "User-Agent": "Matrix Engine/1.0"},
            "unauthenticated_state": {"User-Agent": "Matrix Engine/1.0"}
        }

        matrix_results = {}

        for state_name, header_payload in states.items():
            matrix_results[state_name] = self._dispatch(target_url, header_payload)
            
        # Analyze and format findings into terminal output logs
        print("\n" + "="*50)
        print(f"DIFFERENTIAL MATRIX RESULTS FOR: {target_url}")
        print("="*50)
        for state, metrics in matrix_results.items():
            print(f" State: {state.upper():<25} | Status: {metrics['status']} | Length: {metrics['length']} bytes")
        print("="*50 + "\n")

        return matrix_results
