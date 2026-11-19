"""Model access. 'azure' uses Azure OpenAI; 'stub' is an offline extractive stand-in for dry runs only."""
import hashlib, math, re
import numpy as np
from . import config as C

TOOLS = [{
    "type": "function",
    "function": {
        "name": "create_service_request",
        "description": "Draft a service request for a pump asset. This only DRAFTS the request: the application itself asks the user to confirm before anything is submitted. Call it as soon as the user asks to raise a service request, with the asset id and a short issue description.",
        "parameters": {"type": "object",
                       "properties": {"asset_id": {"type": "string", "description": "e.g. PX100-L3-007"},
                                      "issue": {"type": "string"}},
                       "required": ["asset_id", "issue"]},
    },
}]

_clients = {}
def client(endpoint=None, key=None, api_version=None):
    """Shared client (embeddings) when called without arguments; learner client otherwise."""
    from openai import AzureOpenAI
    endpoint = endpoint or C.AZURE_OPENAI_ENDPOINT
    key = key or C.AZURE_OPENAI_API_KEY
    api_version = api_version or C.AZURE_OPENAI_API_VERSION
    k = (endpoint, hash(key), api_version)          # key itself is never stored as a dict key
    if k not in _clients:
        if len(_clients) > 200: _clients.clear()
        _clients[k] = AzureOpenAI(azure_endpoint=endpoint, api_key=key, api_version=api_version, max_retries=2)
    return _clients[k]

# ---- embeddings
def _hash_embed(text, dim=256):
    v = np.zeros(dim, dtype=np.float32)
    for w in re.findall(r"[a-z0-9\-\.]+", text.lower()):
        h = int(hashlib.md5(w.encode()).hexdigest(), 16)
        v[h % dim] += 1.0
    n = np.linalg.norm(v)
    return v / n if n else v

def embed(texts):
    if C.MODE == "stub":
        return np.vstack([_hash_embed(t) for t in texts])
    out = []
    for i in range(0, len(texts), 64):
        r = client().embeddings.create(model=C.EMBED_DEPLOYMENT, input=texts[i:i + 64])
        out += [d.embedding for d in r.data]
    m = np.array(out, dtype=np.float32)
    return m / np.linalg.norm(m, axis=1, keepdims=True)

# ---- chat
def chat(system, history, user, temperature, top_p, seed, model=None):
    """Returns (text, tool_calls, ignored_params, usage) where tool_calls = [{"name", "args"}]."""
    if C.MODE == "stub":
        text, calls = _stub_chat(user)
        usage = {"prompt_tokens": (len(system) + len(user)) // 4, "completion_tokens": len(text) // 4}
        return text, calls, [], usage
    msgs = [{"role": "system", "content": system}] + history + [{"role": "user", "content": user}]
    import json
    ignored = []
    params = {"temperature": temperature, "top_p": top_p}
    if seed is not None: params["seed"] = seed
    while True:
        try:
            m_ = model or {}
            r = client(m_.get("endpoint"), m_.get("key"), m_.get("api_version")).chat.completions.create(
                model=m_.get("deployment") or C.CHAT_DEPLOYMENT, messages=msgs, tools=TOOLS, **params)
            break
        except Exception as e:
            # newer models reject some sampling settings; drop the named one and retry, and tell the caller
            msg = str(e).lower()
            bad = [p for p in list(params) if p in msg and ("unsupported" in msg or "not supported" in msg or "invalid" in msg)]
            if not bad: raise
            for p in bad: params.pop(p); ignored.append(p)
    m = r.choices[0].message
    calls = []
    for tc in (m.tool_calls or []):
        try: args = json.loads(tc.function.arguments)
        except Exception: args = {}
        calls.append({"name": tc.function.name, "args": args})
    u = getattr(r, "usage", None)
    usage = {"prompt_tokens": getattr(u, "prompt_tokens", 0) or 0, "completion_tokens": getattr(u, "completion_tokens", 0) or 0}
    return (m.content or ""), calls, ignored, usage

def _stub_chat(user):
    q = user.split("Question:")[-1].strip()
    m = re.search(r"(PX\d{3}-L\d-\d{3})", q)
    if re.search(r"service request|raise a request", q, re.I) and m:
        return "I have drafted a service request. Please confirm to submit it.", [
            {"name": "create_service_request", "args": {"asset_id": m.group(1), "issue": q[:120]}}]
    docs = re.findall(r"\[([^\]]+)\] (.+)", user.split("Question:")[0])
    if not docs: return "The documents provided do not state that.", []
    return f"{docs[0][1][:240]} [{docs[0][0]}]", []
