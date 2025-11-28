# tasks/scoring.py
from datetime import datetime, date
from copy import deepcopy
from typing import List, Dict, Any, Set
import math

# Helper: parse date string (ISO) safely
def parse_date(s):
    if not s:
        return None
    if isinstance(s, date):
        return s
    try:
        return datetime.fromisoformat(s).date()
    except Exception:
        return None

def detect_cycles(tasks_by_id: Dict[int, Dict[str, Any]]):
    """
    Detect cycles in dependency graph.
    Returns set of node ids involved in any cycle.
    """
    graph = {}
    for tid, t in tasks_by_id.items():
        deps = t.get("dependencies") or []
        # dependencies indicate tasks this task depends on. We want edges t -> dep
        graph[tid] = [d for d in deps if d in tasks_by_id]

    visited = set()
    recstack = set()
    cycles = set()

    def dfs(node, path):
        if node in recstack:
            # cycle found: mark all nodes on path from the repeated node
            try:
                idx = path.index(node)
                cycles.update(path[idx:])
            except ValueError:
                cycles.add(node)
            return
        if node in visited:
            return
        visited.add(node)
        recstack.add(node)
        path.append(node)
        for nxt in graph.get(node, []):
            dfs(nxt, path)
        path.pop()
        recstack.remove(node)

    for n in list(graph.keys()):
        if n not in visited:
            dfs(n, [])
    return cycles

def normalize(value, min_v, max_v):
    if max_v - min_v <= 0:
        return 0.0
    return (value - min_v) / (max_v - min_v)

def safe_div(a, b):
    try:
        return a / b
    except Exception:
        return 0.0

def compute_scores(tasks: List[Dict[str, Any]], strategy: str = "smart_balance"):
    """
    Compute score components and final score (0-10) per task.
    strategy in ['fastest', 'high_impact', 'deadline', 'smart_balance']
    """
    # deep copy to avoid mutating input
    tasks = deepcopy(tasks)

    # assign IDs if missing (use index+1)
    for i, t in enumerate(tasks):
        if "id" not in t or t.get("id") is None:
            t["id"] = i + 1
    # map by id
    tasks_by_id = { t["id"]: t for t in tasks }

    # sanitize dependencies: keep only IDs that exist
    for t in tasks:
        deps = t.get("dependencies") or []
        t["dependencies"] = [int(d) for d in deps if (isinstance(d, int) or (isinstance(d, str) and d.isdigit()))]
        t["dependencies"] = [d for d in t["dependencies"] if d in tasks_by_id]

    # detect cycles
    cycles = detect_cycles(tasks_by_id)

    # compute dependents count (how many tasks depend on this task)
    dependents_count = {tid: 0 for tid in tasks_by_id}
    for t in tasks:
        for d in t.get("dependencies", []):
            if d in dependents_count:
                dependents_count[d] += 1

    # prepare component raw values for normalization
    today = date.today()
    urgency_days = {}
    importance_vals = []
    effort_vals = []
    dependents_vals = []

    for t in tasks:
        due = parse_date(t.get("due_date"))
        if due:
            days_left = (due - today).days
        else:
            # use a neutral large value (not urgent)
            days_left = 30  # treat unspecified due as 30 days away for normalization
        # Negative days for past-due -> high urgency
        urgency_days[t["id"]] = days_left
        importance_vals.append(t.get("importance", 5))
        effort_vals.append(float(t.get("estimated_hours", 1.0)))
        dependents_vals.append(dependents_count.get(t["id"], 0))

    # For urgency: smaller days_left -> higher urgency score
    # We will invert days_left into urgency raw: urgency_raw = -days_left (so smaller days -> bigger)
    urgency_raws = {tid: -d for tid, d in urgency_days.items()}

    # normalize into 0..1
    urg_min = min(urgency_raws.values()) if urgency_raws else 0
    urg_max = max(urgency_raws.values()) if urgency_raws else 0

    imp_min, imp_max = (min(importance_vals), max(importance_vals)) if importance_vals else (1,10)
    eff_min, eff_max = (min(effort_vals), max(effort_vals)) if effort_vals else (1.0, 8.0)
    dep_min, dep_max = (min(dependents_vals), max(dependents_vals)) if dependents_vals else (0,1)

    # compute normalized component 0..1 (higher = better)
    components = {}
    for t in tasks:
        tid = t["id"]
        # urgency_norm: 0..1 where 1 means most urgent (past due)
        urgency_norm = normalize(urgency_raws[tid], urg_min, urg_max) if urg_max - urg_min != 0 else 0.5

        # importance_norm: importance 1..10 -> 0..1
        importance_norm = normalize(t.get("importance", 5), imp_min, imp_max) if imp_max - imp_min !=0 else 0.5

        # effort: we want low estimated_hours to be better (quick wins).
        # So invert normalized effort: effort_norm = 1 - norm(est_hours)
        est = float(t.get("estimated_hours", 1.0))
        effort_norm = 1.0 - (normalize(est, eff_min, eff_max) if eff_max - eff_min != 0 else 0.5)

        # dependencies: tasks that unblock many (high dependents_count) are higher priority
        dep_norm = normalize(dependents_count.get(tid,0), dep_min, dep_max) if dep_max - dep_min != 0 else 0.0

        # if task is in cycle -> strong penalty on priority ability; keep component but mark later
        components[tid] = {
            "urgency": urgency_norm,
            "importance": importance_norm,
            "effort": effort_norm,
            "dependents": dep_norm
        }

    # strategy weights
    strategy = (strategy or "smart_balance").lower()
    if strategy == "fastest":
        weights = {"urgency": 0.2, "importance": 0.2, "effort": 0.5, "dependents": 0.1}
    elif strategy == "high_impact":
        weights = {"urgency": 0.2, "importance": 0.6, "effort": 0.1, "dependents": 0.1}
    elif strategy == "deadline":
        weights = {"urgency": 0.6, "importance": 0.2, "effort": 0.1, "dependents": 0.1}
    else:  # smart_balance
        weights = {"urgency": 0.35, "importance": 0.35, "effort": 0.15, "dependents": 0.15}

    # compute final scores 0..10
    results = []
    for t in tasks:
        tid = t["id"]
        comp = components[tid]
        raw_score = 0.0
        for k,w in weights.items():
            raw_score += comp.get(k,0.0) * w
        # scale 0..1 to 0..10
        score = raw_score * 10.0

        explanation_parts = []
        # create explanation: show dominant factors
        # pick top 2 components by contribution
        contributions = {k: comp[k] * weights[k] for k in weights}
        sorted_contrib = sorted(contributions.items(), key=lambda x: x[1], reverse=True)
        for key, val in sorted_contrib[:2]:
            if key == "urgency":
                days_left = urgency_days[tid]
                if days_left < 0:
                    explanation_parts.append("Past due")
                elif days_left == 0:
                    explanation_parts.append("Due today")
                else:
                    explanation_parts.append(f"Due in {days_left}d")
            elif key == "importance":
                explanation_parts.append(f"Importance {t.get('importance')}")
            elif key == "effort":
                explanation_parts.append(f"Quick win" if comp["effort"]>0.6 else "High effort")
            elif key == "dependents":
                cnt = dependents_count.get(tid,0)
                if cnt>0:
                    explanation_parts.append(f"Unblocks {cnt} task(s)")
        # circular dependency note
        if tid in cycles:
            explanation_parts.append("Circular dependency detected")

        # invalid/missing data warnings
        if parse_date(t.get("due_date")) is None and t.get("due_date"):
            # string present but couldn't parse
            explanation_parts.append("Invalid due date format")

        # final assembly
        explanation = "; ".join(explanation_parts) if explanation_parts else "No special factors"

        results.append({
            "id": tid,
            "title": t.get("title"),
            "due_date": t.get("due_date"),
            "estimated_hours": t.get("estimated_hours"),
            "importance": t.get("importance"),
            "dependencies": t.get("dependencies", []),
            "score": round(score, 4),
            "explanation": explanation,
            "in_cycle": (tid in cycles)
        })

    # sort descending by score
    results.sort(key=lambda x: x["score"], reverse=True)
    return results

# One public function
def score_tasks(tasks_input: List[Dict[str, Any]], strategy: str = "smart_balance"):
    """
    Wrapper that validates input minimally and returns scored tasks.
    """
    if not isinstance(tasks_input, list):
        raise ValueError("tasks must be a list")
    return compute_scores(tasks_input, strategy=strategy)
