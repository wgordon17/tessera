"""
Tessera configuration module.
"""

# XDG helpers
from .xdg import (
    get_xdg_config_home,
    get_xdg_cache_home,
    get_xdg_data_home,
    get_tessera_config_dir,
    get_tessera_cache_dir,
    ensure_directories,
    get_config_file_path,
    get_metrics_db_path,
)

# Unified config schema
from .schema import TesseraSettings

# Re-export original config classes for backward compatibility
from ..legacy_config import (
    LLMConfig,
    ScoringWeights,
    FrameworkConfig,
    SUPERVISOR_PROMPT,
    INTERVIEWER_PROMPT,
)

__all__ = [
    # XDG
    "get_xdg_config_home",
    "get_xdg_cache_home",
    "get_xdg_data_home",
    "get_tessera_config_dir",
    "get_tessera_cache_dir",
    "ensure_directories",
    "get_config_file_path",
    "get_metrics_db_path",
    # Schemas
    "TesseraSettings",
    # Legacy (backward compat)
    "LLMConfig",
    "ScoringWeights",
    "FrameworkConfig",
    "SUPERVISOR_PROMPT",
    "INTERVIEWER_PROMPT",
]
