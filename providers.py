"""
AI provider layer.

A small abstraction so the app is not hard-coded to any one model:

- Claude is the preferred/default provider (Anthropic SDK).
- Gemini is an optional alternative (google-generativeai).
- A Demo (mock) provider runs with no API key so the app always works.

Selection is driven by environment variables (overridable per call):

    AI_PROVIDER=claude        # claude | gemini | demo   (default: claude)
    ANTHROPIC_API_KEY=...      # required for Claude mode
    GEMINI_API_KEY=...         # required for Gemini mode (GENAI_API_KEY also accepted)
    ANTHROPIC_MODEL=...        # optional, default claude-opus-4-8
    GEMINI_MODEL=...           # optional, default gemini-2.0-flash-exp

If the selected provider has no usable API key, the app falls back to Demo Mode
rather than failing.

Imports of the heavy SDKs are lazy, so neither `anthropic` nor
`google-generativeai` needs to be installed for Demo Mode to run.
"""

from __future__ import annotations

import importlib.util
import os
import re
from typing import Optional

# Load a local .env as early as possible so the key is visible to EVERY entry
# point (Strategy Studio page, brochure page, and the CLI) — not just the
# brochure path. Safe no-op if python-dotenv or .env is absent.
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

DEFAULT_ANTHROPIC_MODEL = "claude-opus-4-8"
DEFAULT_GEMINI_MODEL = "gemini-2.0-flash-exp"

# Defense-in-depth: never let anything that looks like a secret reach a log,
# the UI, a traceback, or a generated file. Apply redact() to any message that
# could conceivably contain key material before it is shown or stored.
_SECRET_RE = re.compile(
    r"(sk-ant-[A-Za-z0-9_\-]{6,}|AIza[A-Za-z0-9_\-]{10,}|sk-[A-Za-z0-9]{20,})"
)


def redact(text) -> str:
    """Mask anything resembling an Anthropic/Gemini API key."""
    return _SECRET_RE.sub("***redacted***", str(text))

# Canonical provider keys
CLAUDE = "claude"
GEMINI = "gemini"
DEMO = "demo"


class ProviderError(RuntimeError):
    """Raised when a provider cannot be constructed (missing key/SDK) or a call fails."""


# ---------------------------------------------------------------------------
# Key helpers
# ---------------------------------------------------------------------------

def _clean_key(value: Optional[str]) -> Optional[str]:
    """Trim whitespace and strip stray surrounding <...> (a common paste/templating artifact)."""
    if value is None:
        return None
    value = value.strip()
    if len(value) >= 2 and value[0] == "<" and value[-1] == ">":
        value = value[1:-1].strip()
    return value or None


def anthropic_key(explicit: str = None) -> Optional[str]:
    return _clean_key(explicit) or _clean_key(os.getenv("ANTHROPIC_API_KEY"))


def gemini_key(explicit: str = None) -> Optional[str]:
    # Accept the new GEMINI_API_KEY and the legacy GENAI_API_KEY.
    return (
        _clean_key(explicit)
        or _clean_key(os.getenv("GEMINI_API_KEY"))
        or _clean_key(os.getenv("GENAI_API_KEY"))
    )


def resolve_provider_name(preferred: str = None) -> str:
    name = (preferred or os.getenv("AI_PROVIDER") or CLAUDE).strip().lower()
    if name in ("anthropic", "claude"):
        return CLAUDE
    if name in ("gemini", "google", "genai"):
        return GEMINI
    if name in ("demo", "mock", "offline", "none"):
        return DEMO
    return CLAUDE


# ---------------------------------------------------------------------------
# Providers
# ---------------------------------------------------------------------------

class BaseProvider:
    name = "base"
    label = "Base"
    is_mock = False

    def generate(self, system: str, prompt: str) -> str:
        raise NotImplementedError


class ClaudeProvider(BaseProvider):
    name = CLAUDE
    label = "Claude"

    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = anthropic_key(api_key)
        self.model = model or os.getenv("ANTHROPIC_MODEL") or DEFAULT_ANTHROPIC_MODEL
        if not self.api_key:
            raise ProviderError("ANTHROPIC_API_KEY not set for Claude mode.")
        try:
            import anthropic  # lazy
        except ImportError as e:
            raise ProviderError("The 'anthropic' package is not installed.") from e
        self._anthropic = anthropic
        self._client = anthropic.Anthropic(api_key=self.api_key)

    def generate(self, system: str, prompt: str) -> str:
        try:
            # Stream to avoid HTTP timeouts on longer briefs; adaptive thinking
            # lets Claude decide how much to reason for this creative task.
            with self._client.messages.stream(
                model=self.model,
                max_tokens=16000,
                thinking={"type": "adaptive"},
                system=system,
                messages=[{"role": "user", "content": prompt}],
            ) as stream:
                message = stream.get_final_message()
        except self._anthropic.APIStatusError as e:
            raise ProviderError(f"Claude API error: {getattr(e, 'message', e)}") from e
        except Exception as e:  # network etc.
            raise ProviderError(f"Claude request failed: {e}") from e

        text = "".join(
            b.text for b in message.content if getattr(b, "type", None) == "text"
        ).strip()
        if not text:
            raise ProviderError("Claude returned an empty response.")
        return text


class GeminiProvider(BaseProvider):
    name = GEMINI
    label = "Gemini"

    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = gemini_key(api_key)
        self.model = model or os.getenv("GEMINI_MODEL") or DEFAULT_GEMINI_MODEL
        if not self.api_key:
            raise ProviderError("GEMINI_API_KEY not set for Gemini mode.")
        try:
            import google.generativeai as genai  # lazy
        except ImportError as e:
            raise ProviderError("The 'google-generativeai' package is not installed.") from e
        self._genai = genai
        genai.configure(api_key=self.api_key)

    def generate(self, system: str, prompt: str) -> str:
        try:
            model = self._genai.GenerativeModel(
                model_name=self.model, system_instruction=system
            )
            response = model.generate_content(prompt)
        except Exception as e:
            raise ProviderError(f"Gemini request failed: {e}") from e
        text = (getattr(response, "text", None) or "").strip()
        if not text:
            raise ProviderError("Gemini returned an empty response.")
        return text


class MockProvider(BaseProvider):
    name = DEMO
    label = "Demo"
    is_mock = True

    def __init__(self, reason: str = None):
        # Why we're in demo mode (e.g. "no API key found"), surfaced in the UI.
        self.reason = reason or "No API key configured"

    def generate(self, system: str, prompt: str) -> str:
        # The engine routes to rich, intake-aware demo builders before reaching
        # here; this is only a generic fallback.
        return (
            "# Demo Output\n\n"
            "_Running in Demo Mode — no API key configured._\n\n"
            "Add an `ANTHROPIC_API_KEY` (Claude) or `GEMINI_API_KEY` (Gemini) to "
            "generate live, tailored content."
        )


# ---------------------------------------------------------------------------
# Factory + status
# ---------------------------------------------------------------------------

def get_provider(preferred: str = None, api_key: str = None) -> BaseProvider:
    """
    Build the active provider. Falls back to Demo Mode when the selected
    provider has no usable API key or its SDK is unavailable.
    """
    name = resolve_provider_name(preferred)

    if name == DEMO:
        return MockProvider(reason="Demo Mode selected")

    try:
        if name == GEMINI:
            return GeminiProvider(api_key=api_key)
        return ClaudeProvider(api_key=api_key)
    except ProviderError as e:
        return MockProvider(reason=str(e))


def provider_status(api_key: str = None) -> dict:
    """A small summary for the UI: selected provider, keys present, effective mode."""
    selected = resolve_provider_name()
    has_anthropic = bool(anthropic_key(api_key if selected == CLAUDE else None))
    has_gemini = bool(gemini_key(api_key if selected == GEMINI else None))
    if selected == CLAUDE and has_anthropic:
        effective = CLAUDE
    elif selected == GEMINI and has_gemini:
        effective = GEMINI
    elif selected == DEMO:
        effective = DEMO
    else:
        effective = DEMO
    return {
        "selected": selected,
        "effective": effective,
        "has_anthropic_key": has_anthropic,
        "has_gemini_key": has_gemini,
        "anthropic_model": os.getenv("ANTHROPIC_MODEL") or DEFAULT_ANTHROPIC_MODEL,
        "gemini_model": os.getenv("GEMINI_MODEL") or DEFAULT_GEMINI_MODEL,
    }


def sdk_available(name: str) -> bool:
    """Whether the SDK package for a provider is importable (no key needed)."""
    module = {CLAUDE: "anthropic", GEMINI: "google.generativeai"}.get(name)
    if not module:
        return True
    try:
        return importlib.util.find_spec(module) is not None
    except (ImportError, ValueError):
        return False


def readiness(preferred: str = None, api_key: str = None) -> dict:
    """
    Zero-cost check of whether Live Mode is ready (no API call, no key value
    returned). Useful for surfacing 'ready for live' status in the UI.
    """
    name = resolve_provider_name(preferred)
    if name == CLAUDE:
        has_key = bool(anthropic_key(api_key))
        sdk = sdk_available(CLAUDE)
        return {
            "provider": CLAUDE,
            "has_key": has_key,
            "sdk_installed": sdk,
            "ready": has_key and sdk,
            "model": os.getenv("ANTHROPIC_MODEL") or DEFAULT_ANTHROPIC_MODEL,
        }
    if name == GEMINI:
        has_key = bool(gemini_key(api_key))
        sdk = sdk_available(GEMINI)
        return {
            "provider": GEMINI,
            "has_key": has_key,
            "sdk_installed": sdk,
            "ready": has_key and sdk,
            "model": os.getenv("GEMINI_MODEL") or DEFAULT_GEMINI_MODEL,
        }
    return {"provider": DEMO, "has_key": False, "sdk_installed": True, "ready": True, "model": "—"}


def health_check(provider=None) -> tuple:
    """
    Verify the active provider can actually generate, without ever exposing the
    key. Returns (ok: bool, message: str). In Demo Mode no live call is made.
    The message is always redacted.
    """
    prov = provider if provider is not None else get_provider()
    if getattr(prov, "is_mock", False):
        return True, f"Demo Mode active ({prov.reason}). No live API call made."
    try:
        prov.generate(
            "You are a connectivity probe. Reply with exactly: OK",
            "Reply with exactly: OK",
        )
        model = getattr(prov, "model", "?")
        return True, f"{prov.label} connection OK (model {model})."
    except Exception as e:  # never surface key material
        return False, redact(f"{prov.label} connection failed: {e}")
