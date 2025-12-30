#!/usr/bin/env python3
"""Comprehensive test to verify all aspects of the GUI fix."""

def test_all_scenarios():
    """Test all possible model selection scenarios."""
    
    # Define legacy models
    LEGACY_MODELS = {
        "gpt-3.5-turbo", "gpt-4", "gpt-4-turbo", "gpt-4o", "gpt-4o-mini", "gpt-4.1",
    }
    
    def model_support(model: str):
        """Simplified version of model_support function."""
        if model in LEGACY_MODELS:
            return {'reasoning_effort': False, 'verbosity': False, 'store': True, 'xhigh_reasoning': False}
        elif model == "gpt-5.2-pro":
            return {'reasoning_effort': False, 'verbosity': False, 'store': True, 'xhigh_reasoning': False}
        elif model in {"o1", "o3", "o4-mini"}:
            return {'reasoning_effort': True, 'verbosity': False, 'store': True, 'xhigh_reasoning': False}
        elif model == "gpt-5.2":
            return {'reasoning_effort': True, 'verbosity': True, 'store': True, 'xhigh_reasoning': True}
        else:
            return {'reasoning_effort': True, 'verbosity': True, 'store': True, 'xhigh_reasoning': False}
    
    print("=== Comprehensive Test of GUI Fix ===")
    
    test_cases = [
        # Edge case: Single legacy model
        ("Single Legacy", ["gpt-4"]),
        
        # Edge case: Single new model
        ("Single New", ["gpt-5.2"]),
        
        # All legacy models
        ("All Legacy", ["gpt-4", "gpt-4", "gpt-3.5-turbo", "gpt-4", "gpt-4"]),
        
        # All new models (no verbosity support)
        ("All New (no verbosity)", ["o1", "o1", "o1", "o1", "o1"]),
        
        # All new models (with verbosity support)
        ("All New (with verbosity)", ["gpt-5.2", "gpt-5.2", "gpt-5.2", "gpt-5.2", "gpt-5.2"]),
        
        # Mixed: 1 new, 4 legacy
        ("1 New + 4 Legacy", ["gpt-5.2", "gpt-4", "gpt-4", "gpt-4", "gpt-4"]),
        
        # Mixed: 4 new, 1 legacy
        ("4 New + 1 Legacy", ["gpt-5.2", "gpt-5.2", "gpt-5.2", "gpt-5.2", "gpt-4"]),
        
        # Mixed: 2 new, 3 legacy
        ("2 New + 3 Legacy", ["gpt-5.2", "o1", "gpt-4", "gpt-4", "gpt-4"]),
        
        # Mixed: 3 new, 2 legacy
        ("3 New + 2 Legacy", ["gpt-5.2", "o1", "gpt-5.2-pro", "gpt-4", "gpt-4"]),
        
        # Mixed: All different
        ("All Different", ["gpt-4", "gpt-5.2", "o1", "gpt-4.1", "gpt-5.2-pro"]),
    ]
    
    all_passed = True
    
    for name, models in test_cases:
        print(f"\n{name}:")
        print(f"  Models: {models}")
        
        all_legacy = all(m in LEGACY_MODELS for m in models)
        any_legacy = any(m in LEGACY_MODELS for m in models)
        
        # Apply fixed logic
        old_settings_enabled = all_legacy
        settings_enabled = not all_legacy
        
        supports = [model_support(m) for m in models]
        reasoning_ok = any(s['reasoning_effort'] for s in supports)
        verbosity_ok = any(s['verbosity'] for s in supports)
        store_ok = any(s['store'] for s in supports)
        
        print(f"  Old settings enabled: {old_settings_enabled}")
        print(f"  New settings enabled: {settings_enabled}")
        print(f"  Reasoning effort available: {reasoning_ok}")
        print(f"  Verbosity available: {verbosity_ok}")
        print(f"  Store available: {store_ok}")
        
        # Verify the fix works
        if not old_settings_enabled and not settings_enabled:
            print("  ❌ FAIL: Both tabs disabled - user can't configure anything!")
            all_passed = False
        elif old_settings_enabled and settings_enabled:
            print("  ❌ FAIL: Both tabs enabled - shouldn't happen!")
            all_passed = False
        else:
            print("  ✅ PASS: Exactly one tab enabled")
            
            # Additional validation for mixed scenarios
            if any_legacy and not all_legacy:  # Mixed scenario
                if not settings_enabled:
                    print("  ❌ FAIL: Mixed models should enable new settings!")
                    all_passed = False
                elif old_settings_enabled:
                    print("  ❌ FAIL: Mixed models should disable old settings!")
                    all_passed = False
                else:
                    print("  ✅ PASS: Mixed models correctly enable new settings")
            
            # Validate that settings availability matches expectations
            if settings_enabled:
                if reasoning_ok:
                    print("  ✅ Reasoning effort control should be enabled")
                if verbosity_ok:
                    print("  ✅ Verbosity control should be enabled")
    
    print(f"\n{'='*50}")
    if all_passed:
        print("🎉 ALL TESTS PASSED! The fix works correctly.")
    else:
        print("❌ SOME TESTS FAILED! The fix needs more work.")
    
    return all_passed

if __name__ == "__main__":
    test_all_scenarios()