from knowledge_graph import build_graph
from inference import forward_chain


def describe(G, srv):
    print(f"\nСервер {G.nodes[srv]['name']}:")
    faults = [(f, d) for _, f, d in G.out_edges(srv, data=True) if d.get("rel") == "hasFault"]
    if not faults:
        print("  неисправностей не выявлено")
        return
    for f, _ in faults:
        acts = [G.nodes[a]["name"] for _, a, d in G.out_edges(f, data=True)
                if d.get("rel") == "requiresAction"]
        specs = [G.nodes[s]["name"] for _, s, d in G.out_edges(f, data=True)
                 if d.get("rel") == "requiresSpecialist"]
        print(f"  диагноз: {G.nodes[f]['name']}")
        print(f"    действия: {acts}")
        print(f"    специалист: {specs}")


if __name__ == "__main__":
    G = build_graph()
    iters = forward_chain(G)
    print(f"Вывод за {iters} итераций.")
    for srv in [n for n, d in G.nodes(data=True) if d.get("type") == "Server"]:
        describe(G, srv)


# output
"""
Вывод за 5 итераций.

Сервер srv-app-01:
  диагноз: Перегрев_CPU
    действия: ['Очистка_системы_охлаждения']
    специалист: ['Сисадмин']

Сервер srv-db-01:
  неисправностей не выявлено

Сервер srv-storage-01:
  диагноз: Отказ_диска
    действия: ['Замена_диска']
    специалист: ['Техник_по_дискам']

"""