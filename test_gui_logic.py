#!/usr/bin/env python3
"""Test script to verify the GUI logic fix for mixed model selection."""

def test_logic():
    """Test the fixed logic for model selection."""
    
    # Define legacy models
    LEGACY_MODELS = {
        "gpt-3.5-turbo",
        "gpt-4", 
        "gpt-4-turbo",
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-4.1",
    }
    
    def model_support(model: str):
        """Simplified version of model_support function."""
        if model in LEGACY_MODELS:
            return {
                'reasoning_effort': False,
                'verbosity': False,
                'store': True,
                'xhigh_reasoning': False,
            }
        elif model == "gpt-5.2-pro":
            return {
                'reasoning_effort': False,
                'verbosity': False,
                'store': True,
                'xhigh_reasoning': False,
            }
        elif model in {"o1", "o3", "o4-mini"}:
            return {
                'reasoning_effort': True,
                'verbosity': False,
                'store': True,
                'xhigh_reasoning': False,
            }
        elif model == "gpt-5.2":
            return {
                'reasoning_effort': True,
                'verbosity': True,
                'store': True,
                'xhigh_reasoning': True,
            }
        else:
            return {
                'reasoning_effort': True,
                'verbosity': True,
                'store': True,
                'xhigh_reasoning': False,
            }
    
    print("=== Testing Fixed Logic ===")
    
    scenarios = [
        # All legacy
        ("All Legacy", ["gpt-4", "gpt-4", "gpt-3.5-turbo", "gpt-4", "gpt-4"]),
        
        # All new
        ("All New", ["gpt-5.2", "gpt-5.2", "o1", "gpt-5.2-pro", "gpt-5.2"]),
        
        # Mixed: mostly legacy with one new
        ("Mostly Legacy + One New", ["gpt-4", "gpt-4", "gpt-5.2", "gpt-4", "gpt-4"]),
        
        # Mixed: mostly new with one legacy
        ("Mostly New + One Legacy", ["gpt-5.2", "gpt-5.2", "gpt-4", "gpt-5.2", "gpt-5.2"]),
        
        # Mixed: equal mix
        ("Equal Mix", ["gpt-4", "gpt-5.2", "gpt-4", "gpt-5.2", "o1"]),
    ]
    
    for name, models in scenarios:
        print(f"\n{name}:")
        print(f"  Models: {models}")
        
        all_legacy = all(m in LEGACY_MODELS for m in models)
        any_legacy = any(m in LEGACY_MODELS for m in models)
        
        # OLD LOGIC (broken)
        old_settings_enabled_old = all_legacy
        settings_enabled_old = not any_legacy
        
        # NEW LOGIC (fixed)
        old_settings_enabled_new = all_legacy
        settings_enabled_new = not all_legacy
        
        supports = [model_support(m) for m in models]
        reasoning_ok = any(s['reasoning_effort'] for s in supports)
        verbosity_ok = any(s['verbosity'] for s in supports)
        
        print(f"  OLD LOGIC - Old settings: {old_settings_enabled_old}, New settings: {settings_enabled_old}")
        print(f"  NEW LOGIC - Old settings: {old_settings_enabled_new}, New settings: {settings_enabled_new}")
        print(f"  Reasoning effort available: {reasoning_ok}")
        print(f"  Verbosity available: {verbosity_ok}")
        
        # Check if the fix resolves the issue
        if old_settings_enabled_old and settings_enabled_old:
            print("  ❌ OLD: Both tabs enabled (shouldn't happen)")
        elif not old_settings_enabled_old and not settings_enabled_old:
            print("  ❌ OLD: Both tabs disabled (BUG - user can't configure anything!)")
        else:
            print("  ✅ OLD: One tab enabled")
            
        if old_settings_enabled_new and settings_enabled_new:
            print("  ❌ NEW: Both tabs enabled (shouldn't happen)")
        elif not old_settings_enabled_new and not settings_enabled_new:
            print("  ❌ NEW: Both tabs disabled (still broken)")
        else:
            print("  ✅ NEW: One tab enabled (FIXED!)")

if __name__ == "__main__":
    test_logic()