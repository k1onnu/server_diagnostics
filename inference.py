def _symptoms(G, srv):
    return {G.nodes[n]["metric"]: G.nodes[n]
            for _, n, d in G.out_edges(srv, data=True)
            if d.get("rel") == "hasSymptom"}

def _servers(G):
    return [n for n, d in G.nodes(data=True) if d.get("type") == "Server"]

def _add(G, s, t, rel):
    if not G.has_edge(s, t):
        G.add_edge(s, t, rel=rel)
        return True
    return False

def _has_fault(G, fault):
    return any(d.get("rel") == "hasFault" and t == fault
               for _, t, d in G.edges(data=True))


def rule_overheat(G):
    ch = False
    for srv in _servers(G):
        s = _symptoms(G, srv)
        t, f = s.get("cpu_temp"), s.get("fan_rpm")
        if t and f and t["value"] > 85 and f["value"] < 1500:
            ch |= _add(G, srv, "cpu_overheat", "hasFault")
    return ch

def rule_disk(G):
    ch = False
    for srv in _servers(G):
        if _symptoms(G, srv).get("smart_errors", {}).get("value", 0) > 0:
            ch |= _add(G, srv, "disk_failure", "hasFault")
    return ch

def rule_overheat_actions(G):
    if not _has_fault(G, "cpu_overheat"):
        return False
    ch  = _add(G, "cpu_overheat", "clean_cooling", "requiresAction")
    ch |= _add(G, "cpu_overheat", "sysadmin",      "requiresSpecialist")
    return ch

def rule_disk_actions(G):
    if not _has_fault(G, "disk_failure"):
        return False
    ch  = _add(G, "disk_failure", "replace_disk", "requiresAction")
    ch |= _add(G, "disk_failure", "hdd_tech",     "requiresSpecialist")
    return ch


RULES = [rule_overheat, rule_disk, rule_overheat_actions, rule_disk_actions]

def forward_chain(G, rules=RULES, max_iter=10):
    it = 0
    while it < max_iter:
        changed = any(r(G) for r in rules)
        it += 1
        if not changed:
            break
    return it