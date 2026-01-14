import re
from pathlib import Path
import streamlit as st

ATS_DIR = Path("ats_profiles")
DEFAULT_PROFILE = "cyber_security"


def _safe_name(name: str) -> str:
    name = (name or "").strip().lower()
    name = re.sub(r"[^a-z0-9_\-]+", "_", name)
    name = re.sub(r"_+", "_", name).strip("_")
    return name or DEFAULT_PROFILE


def _list_profiles():
    ATS_DIR.mkdir(parents=True, exist_ok=True)
    return sorted([p.stem for p in ATS_DIR.glob("*.yaml")])


def _profile_file(name: str) -> Path:
    ATS_DIR.mkdir(parents=True, exist_ok=True)
    return ATS_DIR / f"{_safe_name(name)}.yaml"


def render_profile_manager(cv: dict):
    """
    UI: select profile, preview YAML, edit YAML, save / save-as.
    Robust if cv['ats_profile'] missing.
    """
    if not isinstance(cv, dict):
        return None

    cv.setdefault("ats_profile", DEFAULT_PROFILE)

    profiles = _list_profiles()
    if DEFAULT_PROFILE not in profiles:
        profiles = [DEFAULT_PROFILE] + profiles

    current = cv.get("ats_profile", DEFAULT_PROFILE)
    if current not in profiles:
        current = DEFAULT_PROFILE
        cv["ats_profile"] = DEFAULT_PROFILE

    selected = st.selectbox(
        "Select ATS profile",
        options=profiles,
        index=profiles.index(current),
        key="ats_profile_selectbox",
    )

    if selected != cv.get("ats_profile"):
        cv["ats_profile"] = selected
        st.rerun()

    path = _profile_file(cv.get("ats_profile", DEFAULT_PROFILE))
    if not path.exists():
        # create empty stub if missing
        path.write_text("job_titles: []\nkeywords: {}\naction_verbs: []\nmetrics: {}\nsection_priority: []\n", encoding="utf-8")

    yaml_text = path.read_text(encoding="utf-8")

    st.caption(f"Profile file: {path.name}")

    edited = st.text_area(
        "Edit YAML (user-editable)",
        value=yaml_text,
        height=360,
        key="ats_profile_yaml_editor",
    )

    c1, c2 = st.columns([1, 1.3])
    with c1:
        if st.button("Save", use_container_width=True):
            try:
                path.write_text(edited, encoding="utf-8")
                st.success("Saved.")
            except Exception as e:
                st.error(f"Save failed: {e}")

    with c2:
        new_name = st.text_input("Save as (name)", value="", key="ats_profile_saveas_name")
        if st.button("Save as new profile", use_container_width=True):
            nn = _safe_name(new_name)
            try:
                new_path = _profile_file(nn)
                new_path.write_text(edited, encoding="utf-8")
                cv["ats_profile"] = nn
                st.success(f"Saved as {nn}.yaml")
                st.rerun()
            except Exception as e:
                st.error(f"Save-as failed: {e}")

    # Return nothing (optional). Caller can load profile separately.
    return None