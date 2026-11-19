import os

def _f(name, default): 
    v = os.environ.get(name); return float(v) if v not in (None, "") else default

MODE = os.environ.get("LLM_MODE", "azure")          # "azure" or "stub" (offline dry run)
AZURE_OPENAI_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT", "")
AZURE_OPENAI_API_KEY = os.environ.get("AZURE_OPENAI_API_KEY", "")
AZURE_OPENAI_API_VERSION = os.environ.get("AZURE_OPENAI_API_VERSION", "2025-04-01-preview")
CHAT_DEPLOYMENT = os.environ.get("AZURE_OPENAI_CHAT_DEPLOYMENT", "")
EMBED_DEPLOYMENT = os.environ.get("AZURE_OPENAI_EMBED_DEPLOYMENT", "")
TRAINING_API_KEY = os.environ.get("TRAINING_API_KEY", "")   # empty = no auth (local dev only)
DEFAULT_TEMPERATURE = _f("DEFAULT_TEMPERATURE", 0.2)
DEFAULT_TOP_P = _f("DEFAULT_TOP_P", 0.9)
DEFAULT_TOP_K = int(_f("DEFAULT_TOP_K", 4))
# Teaching switch for module M2.2: when "1", a drafted service request is created immediately
# (no code-level confirmation guard) so learners can see a prompt-only control fail.
UNSAFE_NO_CONFIRM_GUARD = os.environ.get("UNSAFE_NO_CONFIRM_GUARD", "0") == "1"

# Each learner brings their own chat model (sent in request headers). Set to "0" to fall back to the shared deployment.
REQUIRE_LEARNER_MODEL = os.environ.get("REQUIRE_LEARNER_MODEL", "1") == "1"
ALLOWED_HOST_SUFFIXES = (".openai.azure.com", ".services.ai.azure.com", ".cognitiveservices.azure.com")

# Application-level control for personal data: mask technician names, employee ids and mobile numbers in retrieved
# chunks BEFORE the model sees them. Off by default so learners can discover the leak (module M2.2, defence in depth).
REDACT_PERSONAL_DATA = os.environ.get("REDACT_PERSONAL_DATA", "0") == "1"

