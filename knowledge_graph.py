import networkx as nx


def build_graph() -> nx.MultiDiGraph:
    G = nx.MultiDiGraph()

    G.add_node("cpu_overheat",  type="Fault", name="Перегрев_CPU")
    G.add_node("disk_failure",  type="Fault", name="Отказ_диска")
    G.add_node("clean_cooling", type="Action", name="Очистка_системы_охлаждения")
    G.add_node("replace_disk",  type="Action", name="Замена_диска")
    G.add_node("sysadmin",      type="Specialist", name="Сисадмин")
    G.add_node("hdd_tech",      type="Specialist", name="Техник_по_дискам")

    G.add_node("srv1", type="Server", name="srv-app-01")
    G.add_node("srv1_temp", type="Symptom", metric="cpu_temp", value=95)
    G.add_node("srv1_fan",  type="Symptom", metric="fan_rpm",  value=800)
    G.add_edge("srv1", "srv1_temp", rel="hasSymptom")
    G.add_edge("srv1", "srv1_fan",  rel="hasSymptom")

    G.add_node("srv2", type="Server", name="srv-db-01")
    G.add_node("srv2_temp", type="Symptom", metric="cpu_temp", value=60)
    G.add_node("srv2_fan",  type="Symptom", metric="fan_rpm",  value=2200)
    G.add_edge("srv2", "srv2_temp", rel="hasSymptom")
    G.add_edge("srv2", "srv2_fan",  rel="hasSymptom")

    G.add_node("srv3", type="Server", name="srv-storage-01")
    G.add_node("srv3_smart", type="Symptom", metric="smart_errors", value=3)
    G.add_edge("srv3", "srv3_smart", rel="hasSymptom")

    return G