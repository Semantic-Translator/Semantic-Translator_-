"""Simple domain detector placeholder."""


KEYWORDS = {
    "biology": {"cell", "dna", "protein", "membrane", "клетка", "днк", "белок"},
    "medicine": {"patient", "diagnosis", "therapy", "пациент", "диагноз", "терапия"},
    "chemistry": {"molecule", "reaction", "atom", "молекула", "реакция", "атом"},
}


def detect_domain(text: str) -> str:
    normalized = text.lower()
    scores = {
        domain: sum(1 for keyword in keywords if keyword in normalized)
        for domain, keywords in KEYWORDS.items()
    }
    best_domain = max(scores, key=scores.get)
    return best_domain if scores[best_domain] > 0 else "common"
