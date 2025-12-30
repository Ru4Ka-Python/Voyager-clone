#!/usr/bin/env python3
"""Test script to verify the GUI fix for mixed model selection."""

import sys
import os

# Add the project directory to the path so we can import the GUI module
sys.path.insert(0, '/home/engine/project')

from gui import LEGACY_MODELS, model_support

def test_model_support():
    """Test the model_support function to understand what each model supports."""
    print("=== Model Support Analysis ===")
    
    test_models = [
        "gpt-3.5-turbo",  # Legacy
        "gpt-4",          # Legacy  
        "gpt-4.1",        # Legacy
        "gpt-5.2-pro",   # New
        "gpt-5.2",       # New (supports reasoning_effort, verbosity, xhigh)
        "o1",            # New (supports reasoning_effort only)
    ]
    
    for model in test_models:
        support = model_support(model)
        print(f"{model:15} -> reasoning: {support.reasoning_effort}, verbosity: {support.verbosity}, store: {support.store}, xhigh: {support.xhigh_reasoning}")
    
    print()

def test_mixed_scenarios():
    """Test different model selection scenarios."""
    print("=== Mixed Model Scenarios ===")
    
    scenarios = [
        # All legacy
        ["gpt-4", "gpt-4", "gpt-3.5-turbo", "gpt-4", "gpt-4"],
        
        # All new
        ["gpt-5.2", "gpt-5.2", "o1", "gpt-5.2-pro", "gpt-5.2"],
        
        # Mixed: mostly legacy with one new
        ["gpt-4", "gpt-4", "gpt-5.2", "gpt-4", "gpt-4"],
        
        # Mixed: mostly new with one legacy
        ["gpt-5.2", "gpt-5.2", "gpt-4", "gpt-5.2", "gpt-5.2"],
        
        # Mixed: equal mix
        ["gpt-4", "gpt-5.2", "gpt-4", "gpt-5.2", "o1"],
    ]
    
    for i, models in enumerate(scenarios, 1):
        print(f"Scenario {i}: {models}")
        
        all_legacy = all(m in LEGACY_MODELS for m in models)
        any_legacy = any(m in LEGACY_MODELS for m in models)
        
        supports = [model_support(m) for m in models]
        reasoning_ok = any(s.reasoning_effort for s in supports)
        verbosity_ok = any(s.verbosity for s in supports)
        store_ok = any(s.store for s in supports)
        
        print(f"  all_legacy: {all_legacy}, any_legacy: {any_legacy}")
        print(f"  Old settings enabled: {all_legacy}")
        print(f"  New settings enabled: {not all_legacy}")
        print(f"  Reasoning effort available: {reasoning_ok}")
        print(f"  Verbosity available: {verbosity_ok}")
        print(f"  Store available: {store_ok}")
        print()

if __name__ == "__main__":
    test_model_support()
    test_mixed_scenarios()