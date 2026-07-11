"""
Test suite for parameter consistency validation.
Task T8.2: Regression tests for critical parameters per Rule 8.
"""

import yaml
import pytest
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
LEDGER_PATH = REPO_ROOT / "PARAMETER_LEDGER.yaml"


class TestParameterLedger:
    """Validate PARAMETER_LEDGER.yaml structure and content."""

    @pytest.fixture
    def ledger(self):
        """Load parameter ledger."""
        with open(LEDGER_PATH, 'r') as f:
            return yaml.safe_load(f)

    def test_ledger_exists(self):
        """Verify PARAMETER_LEDGER.yaml exists."""
        assert LEDGER_PATH.exists(), "PARAMETER_LEDGER.yaml not found"

    def test_ledger_valid_yaml(self, ledger):
        """Verify PARAMETER_LEDGER is valid YAML."""
        assert ledger is not None, "PARAMETER_LEDGER.yaml is empty or invalid"

    def test_ledger_has_parameters_section(self, ledger):
        """Verify ledger has parameters section."""
        assert "parameters" in ledger, "PARAMETER_LEDGER.yaml missing 'parameters' section"

    def test_cosmological_parameters(self, ledger):
        """Verify critical cosmological parameters are defined."""
        params = ledger["parameters"]

        expected = {
            "w_0": {"value": -0.5485, "tag": "[FITTED]"},
            "w_a": {"value": -0.3968, "tag": "[FITTED]"},
            "H_0": {"value": 71.92, "tag": "[FITTED]"},
            "epsilon": {"value": 0.02511, "tag": "[FITTED]"},
        }

        for param_name, expected_values in expected.items():
            assert param_name in params, f"Missing parameter: {param_name}"
            param = params[param_name]
            assert "value" in param, f"{param_name} missing 'value' field"
            assert "tag" in param, f"{param_name} missing 'tag' field"
            assert "source" in param, f"{param_name} missing 'source' field"

            # Check values match (within tolerance for floats)
            if isinstance(expected_values["value"], float):
                assert abs(param["value"] - expected_values["value"]) < 1e-4, \
                    f"{param_name} value mismatch: {param['value']} vs {expected_values['value']}"

    def test_stiffness_parameters(self, ledger):
        """Verify K3 stiffness parameters."""
        params = ledger["parameters"]

        assert "stiffness_S12" in params, "Missing stiffness_S12"
        assert params["stiffness_S12"]["value"] == 1014, "stiffness_S12 should be 1014"

        assert "stiffness_S21" in params, "Missing stiffness_S21"
        assert params["stiffness_S21"]["value"] == 336, "stiffness_S21 should be 336"

    def test_axion_mass_parameters(self, ledger):
        """Verify axion mass predictions."""
        params = ledger["parameters"]

        assert "axion_mass_S12" in params, "Missing axion_mass_S12"
        assert params["axion_mass_S12"]["value"] == 3.18e-21, "axion_mass_S12 mismatch"

        assert "axion_mass_S21" in params, "Missing axion_mass_S21"
        assert params["axion_mass_S21"]["value"] == 1.83e-21, "axion_mass_S21 mismatch"

    def test_alpha_eff_parameters(self, ledger):
        """Verify superradiance coupling parameters."""
        params = ledger["parameters"]

        assert "alpha_eff_S12" in params, "Missing alpha_eff_S12"
        assert params["alpha_eff_S12"]["value"] == 1.55, "alpha_eff_S12 mismatch"

        assert "alpha_eff_S21" in params, "Missing alpha_eff_S21"
        assert params["alpha_eff_S21"]["value"] == 0.89, "alpha_eff_S21 mismatch"

    def test_pta_parameters(self, ledger):
        """Verify PTA prediction parameters."""
        params = ledger["parameters"]

        assert "pta_period_S12" in params, "Missing pta_period_S12"
        assert params["pta_period_S12"]["value"] == 7.52, "pta_period_S12 mismatch"

        assert "pta_period_S21" in params, "Missing pta_period_S21"
        assert params["pta_period_S21"]["value"] == 13.08, "pta_period_S21 mismatch"

        # Verify frequency ratio bounds
        assert "pta_frequency_ratio_lower" in params, "Missing pta_frequency_ratio_lower"
        assert params["pta_frequency_ratio_lower"]["value"] == 1.73, "PTA ratio lower mismatch"

        assert "pta_frequency_ratio_upper" in params, "Missing pta_frequency_ratio_upper"
        assert params["pta_frequency_ratio_upper"]["value"] == 1.75, "PTA ratio upper mismatch"

    def test_all_parameters_have_source(self, ledger):
        """Verify all parameters cite their source (Rule 8)."""
        params = ledger["parameters"]

        for param_name, param in params.items():
            assert "source" in param, f"{param_name} missing 'source' field"
            assert len(param["source"]) > 0, f"{param_name} has empty 'source'"

    def test_all_parameters_have_tag(self, ledger):
        """Verify all parameters have a tag ([VERIFIED], [FITTED], or [PREDICTED])."""
        params = ledger["parameters"]
        valid_tags = {"[VERIFIED]", "[FITTED]", "[PREDICTED]"}

        for param_name, param in params.items():
            assert "tag" in param, f"{param_name} missing 'tag'"
            assert param["tag"] in valid_tags, \
                f"{param_name} has invalid tag '{param['tag']}'. Must be one of {valid_tags}"

    def test_caveats_section_exists(self, ledger):
        """Verify caveats are documented in ledger."""
        assert "caveats" in ledger, "PARAMETER_LEDGER.yaml missing 'caveats' section"

    def test_all_gaps_documented(self, ledger):
        """Verify all 6 referee-identified gaps are documented."""
        caveats = ledger.get("caveats", {})
        expected_gaps = {"GAP-1", "GAP-2", "GAP-3", "GAP-4", "GAP-5", "GAP-6"}

        documented_gaps = {c["id"] for c in caveats if isinstance(c, dict) and "id" in c}

        missing = expected_gaps - documented_gaps
        assert len(missing) == 0, f"Missing gap documentation: {missing}"


class TestStiffnessValues:
    """Regression tests for K3 stiffness values (Task T2.1)."""

    def test_stiffness_ratio_reduced_form(self):
        """Verify stiffness ratio reduces to 169/56."""
        numerator = 1014
        denominator = 336

        # Find GCD
        from math import gcd
        g = gcd(numerator, denominator)
        reduced_num = numerator // g
        reduced_den = denominator // g

        assert reduced_num == 169, f"Reduced numerator should be 169, got {reduced_num}"
        assert reduced_den == 56, f"Reduced denominator should be 56, got {reduced_den}"

    def test_frequency_ratio_bounds(self):
        """Verify √(1014/336) lies in (1.73, 1.75)."""
        import math

        ratio = math.sqrt(1014 / 336)

        assert 1.73 < ratio < 1.75, \
            f"√(1014/336) = {ratio:.6f} should lie in (1.73, 1.75)"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
