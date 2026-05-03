"""
Example: Parallel Execution with MaticGraph
===========================================
This example shows how to run multiple nodes in parallel using parallel_group
and join the results back into a single state.
"""

import time
from maticlib.graph import MaticGraph


def init_node(state):
    print("[Node] Starting complex analysis...")
    return {"status": "started"}


def task_a(state):
    """Wait and compute A"""
    print("  [Task A] Computing part 1...")
    time.sleep(1)
    return {"part_a": 10}


def task_b(state):
    """Wait and compute B"""
    print("  [Task B] Computing part 2...")
    time.sleep(1)
    return {"part_b": 20}


def task_c(state):
    """Wait and compute C"""
    print("  [Task C] Computing part 3...")
    time.sleep(1)
    return {"part_c": 30}


def combine(state):
    total = state.get("part_a", 0) + state.get("part_b", 0) + state.get("part_c", 0)
    print(f"\n[Combine] Grand total: {total}")
    return {"total": total}


def run_parallel_graph():
    graph = MaticGraph(max_workers=3)

    # 1. Add nodes
    graph.add_node("start", init_node)
    graph.add_node("a", task_a)
    graph.add_node("b", task_b)
    graph.add_node("c", task_c)
    graph.add_node("merge", combine)

    # 2. Define parallel group
    # After 'start' completes, run 'a', 'b', and 'c' in parallel.
    # When all three are done, proceed to 'merge'.
    graph.parallel_group(
        from_node="start", parallel_nodes=["a", "b", "c"], join_node="merge"
    )

    # 3. Finalize exit
    graph.add_edge("merge", "END")
    graph.set_entry("start")

    print("Executing graph with parallel nodes...")
    print("(This should take ~1 second total despite 3 seconds of sleep time)\n")

    start_time = time.time()
    final_state = graph.run(verbose=True)
    end_time = time.time()

    print(f"\nCompleted in: {end_time - start_time:.2f} seconds")
    print(f"Resulting state keys: {list(final_state.keys())}")


if __name__ == "__main__":
    run_parallel_graph()
