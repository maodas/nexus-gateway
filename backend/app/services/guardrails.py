"""
Hybrid Enterprise Intent Policy Guardrails Engine for NexusGateway.
Pre-Check: Explicit Technical Allowlist for coding, software engineering & architecture.
Layer 1: Pre-compiled typo-tolerant regex pre-check (sub-1ms).
Layer 2: Lightweight semantic intent judge via Groq llama-3.1-8b-instant (non-blocking).
"""
import logging
import re
from typing import Tuple, Dict, List
import httpx
from app.core.config import settings

logger = logging.getLogger(__name__)

# Pre-Check: Technical Allowlist Regex (Software Engineering & Architecture Terms)
EXPLICIT_ALLOWED_PATTERNS = re.compile(
    r"\b(code|coding|debug|debugging|script|python|javascript|typescript|repo|api|sql|bug|fix|function|class|git|docker|fastapi|nextjs|react|html|css|json|finops|architecture|llm|gateway|router|redis|database|server)\b",
    re.IGNORECASE
)

# Layer 1: Pre-compiled Typo-Tolerant Regex Patterns
COMPILED_PATTERNS: Dict[str, List[re.Pattern]] = {
    "Cooking/Recipes": [
        re.compile(r"\b" + kw + r"\b", re.IGNORECASE) for kw in [
            "recipe", "receipe", "recipie", "recpie", "cook", "cooking", "bake", "baking",
            "ingredient", "dinner", "dish", "pasta", "cake", "cookie", "flavor", "cuisine",
            "chef", "food", "kitchen"
        ]
    ],
    "Gaming/Esports": [
        re.compile(r"\b" + kw + r"\b", re.IGNORECASE) for kw in [
            "gameplay", "cheat code", "playstation", "xbox", "nintendo",
            "fortnite", "call of duty", "esports", "video game", "gaming", "game"
        ]
    ],
    "Sports/Athletics": [
        re.compile(r"\b" + kw + r"\b", re.IGNORECASE) for kw in [
            "football", "soccer", "basketball", "nba", "nfl",
            "baseball", "world cup", "super bowl", "tournament", "sports"
        ]
    ],
    "Entertainment/Gossip": [
        re.compile(r"\b" + kw + r"\b", re.IGNORECASE) for kw in [
            "celebrity", "movie plot", "horoscope", "gossip", "hollywood", "movie", "film"
        ]
    ],
    "Personal Advice/Fiction": [
        re.compile(r"\b" + kw + r"\b", re.IGNORECASE) for kw in [
            "relationship advice", "fantasy story", "dating advice"
        ]
    ]
}

GROQ_JUDGE_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_JUDGE_MODEL = "llama-3.1-8b-instant"


async def validate_enterprise_policy(prompt_text: str) -> Tuple[bool, str, str]:
    """
    Async hybrid validation of user prompt against corporate Enterprise Intent Guardrails.

    Step 0: Immediate pass for technical / software engineering vocabulary.
    Layer 1: Sub-1ms typo-tolerant regex rules.
    Layer 2: Lightweight LLM semantic judge (Groq llama-3.1-8b-instant) with graceful try/except fallback.

    Args:
        prompt_text (str): User prompt string.

    Returns:
        Tuple[bool, str, str]: (is_allowed, category_name, detail_message)
    """
    if not prompt_text:
        return True, "Allowed", ""

    prompt_clean = prompt_text.lower().strip()

    # --- STEP 0: Explicit Technical Allowlist Pre-Check ---
    if EXPLICIT_ALLOWED_PATTERNS.search(prompt_clean):
        logger.info("✅ GUARDRAIL ALLOWED: Matched technical engineering allowlist pattern.")
        return True, "Allowed", ""

    # --- LAYER 1: Sub-1ms Typo-Tolerant Regex Pre-Check ---
    for category, compiled_regexes in COMPILED_PATTERNS.items():
        for compiled_re in compiled_regexes:
            if compiled_re.search(prompt_clean):
                logger.warning(
                    f"🛡️ GUARDRAIL LAYER 1 INTERCEPTED: Matched category '{category}' (Typo-Tolerant Regex)"
                )
                detail = (
                    f"🚫 PROMPT BLOCKED: Enterprise Policy restricts non-business topics ({category}) "
                    f"on corporate gateway channels."
                )
                return False, category, detail

    # --- LAYER 2: Lightweight Semantic Intent Judge (Groq llama-3.1-8b-instant) ---
    api_key = settings.GROQ_API_KEY
    if not api_key or api_key.startswith("gsk_your_"):
        return True, "Allowed", ""

    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        judge_payload = {
            "model": GROQ_JUDGE_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are an enterprise compliance classifier. Is the user prompt related to corporate business, "
                        "software engineering, finance, legal, project management, or operational automation? "
                        "Answer ONLY 'YES' or 'NO: [Category]'."
                    )
                },
                {"role": "user", "content": prompt_text[:500]}
            ],
            "temperature": 0.0,
            "max_tokens": 20,
        }

        async with httpx.AsyncClient(timeout=2.0) as client:
            response = await client.post(GROQ_JUDGE_URL, json=judge_payload, headers=headers)
            if response.status_code == 200:
                judge_out = response.json().get("choices", [{}])[0].get("message", {}).get("content", "").strip()
                if judge_out.startswith("NO"):
                    cat_detected = judge_out.replace("NO:", "").strip() or "Off-Topic Intent"
                    logger.warning(f"🛡️ GUARDRAIL LAYER 2 INTERCEPTED: Semantic judge flagged '{cat_detected}'")
                    detail = (
                        f"🚫 PROMPT BLOCKED: Enterprise Policy restricts non-business topics ({cat_detected}) "
                        f"on corporate gateway channels."
                    )
                    return False, cat_detected, detail
    except Exception as e:
        logger.debug(f"Layer 2 Semantic Judge skipped or timed out gracefully: {e}")

    return True, "Allowed", ""