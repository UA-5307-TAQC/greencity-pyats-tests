"""Utility functions for loading test data from YAML files."""
import yaml


def load_test_data(path):
    """Load test data from a YAML file."""
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}
