"""Спільний код для генерації питань на відповідність (matching)."""
import json
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def q(level, text, left_label, right_label, pairs, distractors=None, note=""):
    if isinstance(distractors, str):
        distractors = [distractors]
    expl = "Правильно: " + "; ".join(f"{a} — {b}" for a, b in pairs) + "."
    if note:
        expl += " " + note
    meta = {"pairs": [list(p) for p in pairs], "leftLabels": [left_label], "rightLabels": [right_label]}
    if distractors:
        meta["distractors"] = distractors
    return {
        "text": text,
        "options": [],
        "correctIndex": 0,
        "explanation": expl,
        "testLevel": level,
        "questionType": "matching",
        "metadata": meta,
    }


def topic_name(subject_dir, prefix):
    for f in sorted(os.listdir(os.path.join(ROOT, "content", subject_dir))):
        if f.startswith(prefix) and f.endswith(".json"):
            with open(os.path.join(ROOT, "content", subject_dir, f), encoding="utf-8") as fh:
                d = json.load(fh)
            return d["subject"], d["topic"]
    raise SystemExit(f"no topic file for {subject_dir}/{prefix}")


def write(subject_dir, prefix, out_name, questions):
    subject, topic = topic_name(subject_dir, prefix)
    for item in questions:
        pairs = item["metadata"]["pairs"]
        rights = [p[1] for p in pairs] + item["metadata"].get("distractors", [])
        assert len(set(rights)) == len(rights), item["text"]
        assert len({p[0] for p in pairs}) == len(pairs), item["text"]
    path = os.path.join(ROOT, "content", subject_dir, out_name)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump({"subject": subject, "topic": topic, "cards": [], "questions": questions}, fh, ensure_ascii=False, indent=2)
    print(f"{path}: {len(questions)}")
