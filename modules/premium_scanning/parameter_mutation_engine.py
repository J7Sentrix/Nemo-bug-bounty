import itertools
from typing import List, Iterator, Set, Dict
from core.license_validator import requires_premium

class ParameterMutationEngine:
    """
    Optimizes and expands a list of target endpoint parameters to identify
    potential hidden configurations or variables during local differential analysis.
    """
    def __init__(self):
        self.suffixes: List[str] = [
            '_id', 'Id', 'ID', '_num', 'Num', 
            '_debug', '_v', '_testing', '_old', '_new', '_bkp'
        ]
        self.prefixes: List[str] = [
            'user_', 'admin_', 'test_', 'debug_', 'api_', 'req_'
        ]
        self.replacements: Dict[str, List[str]] = {
            'id': ['user_id', 'admin_id', 'account_id', 'uuid', 'guid', 'uid'],
            'user': ['username', 'userid', 'user_id', 'account', 'member'],
            'debug': ['debug_mode', 'testing', 'v', 'verbose', 'trace'],
            'file': ['filepath', 'path', 'dir', 'folder', 'doc'],
            'email': ['email_address', 'mail', 'contact'],
            'config': ['cfg', 'settings', 'options', 'conf']
        }

    @requires_premium
    def mutate_parameters(self, base_parameters: List[str]) -> Iterator[str]:
        """
        Takes known base parameters and generates logical variants via memory-efficient yielding.
        """
        seen: Set[str] = set()

        for param in base_parameters:
            if not param:
                continue
                
            param_lower = param.lower()

            if param not in seen:
                seen.add(param)
                yield param

            # Process system dictionary expansion synonym matches
            if param_lower in self.replacements:
                for replacement in self.replacements[param_lower]:
                    if replacement not in seen:
                        seen.add(replacement)
                        yield replacement

            # Apply trailing contextual additions
            for suffix in self.suffixes:
                mutated_suffix = f"{param}{suffix}"
                if mutated_suffix not in seen:
                    seen.add(mutated_suffix)
                    yield mutated_suffix

            # Apply leading contextual additions
            for prefix in self.prefixes:
                mutated_prefix = f"{prefix}{param}"
                if mutated_prefix not in seen:
                    seen.add(mutated_prefix)
                    yield mutated_prefix
                    
            # Handle standard structural formatting swaps (snake <-> camel)
            if "_" in param:
                parts = param.split('_')
                camel_case = parts[0] + ''.join(word.capitalize() for word in parts[1:])
                if camel_case not in seen:
                    seen.add(camel_case)
                    yield camel_case
            else:
                lower_case = param.lower()
                if lower_case != param and lower_case not in seen:
                    seen.add(lower_case)
                    yield lower_case
