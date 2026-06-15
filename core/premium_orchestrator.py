import os
from typing import Dict, Any, List, Optional
from core.license_validator import LicenseValidator, requires_premium
from modules.premium_recon.js_diff_engine import JSDiffEngine
from modules.premium_recon.multi_state_matrix import MultiStateMatrix
from modules.premium_scanning.network_compliance_router import NetworkComplianceRouter
from modules.premium_scanning.parameter_mutation_engine import ParameterMutationEngine
from modules.premium_vulnerability.smart_oob_correlator import SmartOOBCorrelator
from modules.premium_vulnerability.local_sast_scanner import LocalSASTScanner
from modules.premium_exploitation.custom_template_factory import CustomTemplateFactory
from modules.premium_exploitation.visual_evidence_builder import VisualEvidenceBuilder

class PremiumOrchestrator:
    """
    Centralized Premium Control Engine. Validates product access state entries
    and handles unified parameter processing distribution out to sub-module dependencies.
    """
    def __init__(self):
        self.license_manager = LicenseValidator()
        # Initialize instances directly into framework runtime boundaries
        self.js_diff = JSDiffEngine()
        self.auth_matrix = MultiStateMatrix()
        self.network_router = NetworkComplianceRouter()
        self.param_mutator = ParameterMutationEngine()
        self.sast_scanner = LocalSASTScanner()
        self.template_factory = CustomTemplateFactory()
        self.report_packager = VisualEvidenceBuilder()

    def check_premium_status(self) -> bool:
        """Exposes raw confirmation metrics detailing local licensing tier constraints."""
        return self.license_manager.verify_license()

    @requires_premium
    def run_premium_recon_pipeline(self, target_url: str, js_links: List[str]):
        """Orchestrates high-value advanced reconnaissance tracking cycles."""
        print(f"[*] Starting Premium Deep Recon Pipeline wrapper context for target mapping...")
        for link in js_links:
            diff_results = self.js_diff.monitor_and_diff(link)
            if diff_results.get("new_endpoints") or diff_results.get("suspicious_additions"):
                print(f"[!] Target Delta Updates Found inside source code maps: {link}")

    @requires_premium
    def run_premium_code_review(self, target_directory: str) -> List[Dict[str, Any]]:
        """Orchestrates code compliance analysis workflows over identified exposed leak vectors."""
        return self.sast_scanner.scan_directory(target_directory)
