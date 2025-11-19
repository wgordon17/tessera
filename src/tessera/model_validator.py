"""
Model validation utilities for verifying available models from LLM providers.
"""

import sys
from typing import List, Optional, Dict, Any
import requests
from .config import LLMConfig


class ModelValidator:
    """Validate configured models against provider's available models."""

    @staticmethod
    def fetch_available_models(base_url: str, api_key: str, timeout: float = 10.0) -> Optional[List[str]]:
        """
        Fetch available models from the /v1/models endpoint.

        Args:
            base_url: Base URL for the API (e.g., "http://localhost:3000/v1")
            api_key: API key for authentication
            timeout: Request timeout in seconds

        Returns:
            List of available model IDs, or None if request fails
        """
        try:
            # Ensure base_url ends with /v1
            if not base_url.endswith('/v1'):
                base_url = base_url.rstrip('/') + '/v1'

            models_url = f"{base_url}/models"

            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }

            response = requests.get(models_url, headers=headers, timeout=timeout)

            if response.status_code == 200:
                data = response.json()
                # OpenAI-compatible response format
                if "data" in data:
                    return [model["id"] for model in data["data"]]
                else:
                    print(f"Warning: Unexpected response format from {models_url}")
                    print(f"Response: {data}")
                    return None
            else:
                print(f"Error: Failed to fetch models from {models_url}")
                print(f"Status code: {response.status_code}")
                print(f"Response: {response.text[:200]}")
                return None

        except requests.exceptions.Timeout:
            print(f"Error: Timeout fetching models from {base_url}")
            return None
        except requests.exceptions.ConnectionError:
            print(f"Error: Could not connect to {base_url}")
            print("Make sure the Copilot proxy is running if using OPENAI_BASE_URL")
            return None
        except Exception as e:
            print(f"Error: Failed to fetch models: {e}")
            return None

    @staticmethod
    def validate_models(config: LLMConfig, strict: bool = True) -> bool:
        """
        Validate that configured models are available.

        Args:
            config: LLM configuration to validate
            strict: If True, exit on validation failure. If False, just warn.

        Returns:
            True if validation passed, False otherwise
        """
        # Only validate if using a proxy (base_url is set)
        if not config.base_url:
            print("Skipping model validation (not using proxy)")
            return True

        # If no models configured, this is an error
        if not config.models:
            print("\n" + "=" * 80)
            print("ERROR: No models configured!")
            print("=" * 80)
            print("\nPlease configure models in your .env file using:")
            print("  OPENAI_MODELS=model1,model2,model3")
            print("\nExample:")
            print("  OPENAI_MODELS=gpt-4,gpt-3.5-turbo,o1-preview")
            print("\n" + "=" * 80)

            # Fetch and display available models
            available = ModelValidator.fetch_available_models(config.base_url, config.api_key)
            if available:
                print("\nAvailable models from proxy:")
                print("=" * 80)
                for i, model in enumerate(available, 1):
                    print(f"{i:2}. {model}")
                print("=" * 80)
                print(f"\nTo use these models, add to your .env file:")
                print(f"OPENAI_MODELS={','.join(available[:3])}")  # Show first 3 as example
                print()

            if strict:
                sys.exit(1)
            return False

        # Fetch available models
        print(f"Validating configured models against {config.base_url}...")
        available_models = ModelValidator.fetch_available_models(config.base_url, config.api_key)

        if available_models is None:
            print("Warning: Could not fetch available models for validation")
            if strict:
                print("\nPlease ensure the proxy is running before starting agents.")
                sys.exit(1)
            return False

        # Check each configured model
        print(f"\nConfigured models: {', '.join(config.models)}")
        print(f"Available models: {len(available_models)} total")

        invalid_models = []
        valid_models = []

        for model in config.models:
            if model in available_models:
                valid_models.append(model)
                print(f"  ✓ {model}")
            else:
                invalid_models.append(model)
                print(f"  ✗ {model} (NOT AVAILABLE)")

        if invalid_models:
            print("\n" + "=" * 80)
            print(f"ERROR: {len(invalid_models)} configured model(s) not available!")
            print("=" * 80)
            print(f"\nInvalid models: {', '.join(invalid_models)}")
            print(f"\nAvailable models from proxy:")
            for i, model in enumerate(available_models, 1):
                print(f"{i:2}. {model}")
            print("\n" + "=" * 80)
            print(f"\nUpdate your .env file to use available models:")
            print(f"OPENAI_MODELS={','.join(available_models[:3])}")
            print("=" * 80)

            if strict:
                sys.exit(1)
            return False

        print(f"\n✓ All {len(valid_models)} configured model(s) are available!")
        return True

    @staticmethod
    def display_available_models(base_url: str, api_key: str) -> None:
        """
        Display all available models from the provider.

        Args:
            base_url: Base URL for the API
            api_key: API key for authentication
        """
        print("\n" + "=" * 80)
        print("FETCHING AVAILABLE MODELS")
        print("=" * 80)

        models = ModelValidator.fetch_available_models(base_url, api_key)

        if models:
            print(f"\nFound {len(models)} available models:")
            print("-" * 80)
            for i, model in enumerate(models, 1):
                print(f"{i:2}. {model}")
            print("-" * 80)
            print(f"\nTo use these models, add to your .env file:")
            print(f"OPENAI_MODELS={','.join(models[:3])}")  # Show first 3 as example
            if len(models) > 3:
                print(f"# ... and {len(models) - 3} more")
        else:
            print("\n✗ Could not fetch models. Check proxy connection.")

        print("=" * 80 + "\n")


def validate_config_models(config: LLMConfig, strict: bool = True) -> bool:
    """
    Convenience function to validate models in an LLMConfig.

    Args:
        config: Configuration to validate
        strict: If True, exit on failure. If False, just warn.

    Returns:
        True if validation passed
    """
    return ModelValidator.validate_models(config, strict=strict)


def list_available_models(base_url: str = "http://localhost:3000/v1", api_key: str = "dummy") -> None:
    """
    Convenience function to list available models.

    Args:
        base_url: Base URL for the API
        api_key: API key for authentication
    """
    ModelValidator.display_available_models(base_url, api_key)
