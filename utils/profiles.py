from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml

PROFILES_DIR = Path(__file__).resolve().parent.parent / "ats_profiles"


class ProfileError(RuntimeError):
    """ATS profile load/save error."""


def safe_profile_name(name: str) -> str:
    """Normalize a profile name to a safe filename stem."""
    name = (name or "").strip().lower()
    name = name.replace(" ", "_")
    name = re.sub(r"[^a-z0-9_\-]", "", name)
    name = re.sub(r"_+", "_", name).strip("_")
    return name or "custom_profile"


def profile_path(profile_name: str) -> Path:
    stem = safe_profile_name(profile_name)
    return PROFILES_DIR / f"{stem}.yaml"


def list_profiles() -> List[str]:
    """Return available profile stems."""
    if not PROFILES_DIR.exists():
        return []
    profiles: List[str] = []
    for p in sorted(PROFILES_DIR.glob("*.yaml")):
        profiles.append(p.stem)
    return profiles


def load_profile(profile_name: str) -> Dict[str, Any]:
    """Load a YAML profile. Raises ProfileError if invalid."""
    path = profile_path(profile_name)
    if not path.exists():
        raise ProfileError(f"Profile not found: {path.name}")

    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ProfileError(f"Failed to parse {path.name}: {exc}") from exc

    if not isinstance(data, dict):
        raise ProfileError(f"Invalid profile format in {path.name} (expected a mapping).")

    # basic normalization so components can rely on fields existing
    data.setdefault("job_titles", [])
    data.setdefault("keywords", {})
    data.setdefault("action_verbs", [])
    data.setdefault("metrics", {})
    data.setdefault("bullet_templates", [])
    data.setdefault("section_priority", [])
    return data


def save_profile(profile_name: str, yaml_text: str) -> Tuple[str, Dict[str, Any]]:
    """Validate + save profile YAML text.

    Returns (saved_stem, parsed_profile).
    """
    PROFILES_DIR.mkdir(parents=True, exist_ok=True)

    try:
        parsed = yaml.safe_load(yaml_text)
    except Exception as exc:
        raise ProfileError(f"YAML parse error: {exc}") from exc

    if not isinstance(parsed, dict):
        raise ProfileError("Profile YAML must define a mapping (top-level keys).")

    stem = safe_profile_name(profile_name)
    path = profile_path(stem)
    path.write_text(yaml.safe_dump(parsed, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return stem, load_profile(stem)
