'''
    created on 01 February 2020
    
    @author: Gergely
'''

from tables.synced import SynchronizedTable
import random


def table_to_graph(wait_for_table: SynchronizedTable):
    elems = wait_for_table.get()
    nodes = {entry.trans_has_lock for entry in elems}.union({entry.trans_waits_lock for entry in elems})
    graph = {entry: [] for entry in nodes}
    for entry in elems:
        graph[entry.trans_has_lock].append(entry.trans_waits_lock)
    return graph


def detect_cycle(graph):
    '''
    topological sort to detect cycles
    :param graph
    :return:
    '''
    in_degree = {key: 0 for key in graph}
    for a in graph:
        for b in graph[a]:
            in_degree[b] += 1
    queue = [tr_id for tr_id in graph if in_degree[tr_id] == 0]
    visited = 0
    topological_order = []
    while queue:
        front = queue.pop(0)
        topological_order.append(front)
        for node in graph[front]:
            in_degree[node] -= 1
            if in_degree[node] == 0:
                queue.append(node)
        visited += 1
    if visited != len(graph):
        return list(set(graph.keys()).difference(set(topological_order)))
    return None


def without_cycles(graph):
    cycle_nodes = detect_cycle(graph)
    to_delete = []
    while cycle_nodes is not None:
        node_to_delete = random.choice(cycle_nodes)
        to_delete.append(node_to_delete)
        del graph[node_to_delete]
        graph = {key: [x for x in graph[key] if x != node_to_delete] for key in graph}
        cycle_nodes = detect_cycle(graph)
    return to_delete
