# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 20:42:23 2017
revised on Oct 15 2017
@author: Aipan1
"""

import networkx as nx
import random
import copy


__all__ = ['edge_in_community',
           'dict_degree_nodes',
           'inner_random_1k',
           'inner_random_2k',
           'inner_random_25k',
           'inner_random_3k',
           'inter_random_1k',
           'inter_random_2k',
           'inter_random_25k',
           'inter_random_3k',
           'inner_community_swap',
           'inter_community_swap',
           'Q_increase',
           'Q_decrease', ]


def edge_in_community(node_community_list, edge):
    """Returns True if the edge is in the community, false otherwise.

    Parameters
    ----------
    node_community_list : list
        nodes and the communities they belong to
    edge:
        an edge in the graph

    Notes
    -----

    Examples
    --------
    """
    return_value = 0
    for community_i in node_community_list:
        if edge[0] in community_i and edge[1] in community_i:
            return_value += 1
    if return_value == 0:
        return 0
    else:
        return 1


def dict_degree_nodes(degree_node_list):
    # 返回的字典为{度：[节点1，节点2，..]}，其中节点1和节点2有相同的度
    D = {}
    for degree_node_i in degree_node_list:
        if degree_node_i[0] not in D:
            D[degree_node_i[0]] = [degree_node_i[1]]
        else:
            D[degree_node_i[0]].append(degree_node_i[1])
    return D


def inner_random_1k(G0, node_community_list, nswap=1, max_tries=100, connected=1):
    # 保证度分布特性不变和网络联通的情况下，交换社团内部的连边
    # G0：待改变结构的网络
    # node_community_list：是网络中节点的社团归属信息
    # nswap：是改变成功的系数，默认值为1
    # max_tries：是尝试改变的次数，默认值为100
    # connected：是否需要保证网络的联通特性，参数为1需要保持，参数为0不需要保持

    if not nx.is_connected(G0):
        raise nx.NetworkXError("非连通图，必须为连通图")
    if G0.is_directed():
        raise nx.NetworkXError("仅适用于无向图")
    if nswap > max_tries:
        raise nx.NetworkXError("交换次数超过允许的最大次数")
    if len(G0) < 3:
        raise nx.NetworkXError("节点数太少，至少要含三个节点")

    tn = 0  # 尝试次数
    swapcount = 0  # 有效交换次数

    G = copy.deepcopy(G0)
    keys, degrees = zip(*G.degree().items())
    cdf = nx.utils.cumulative_distribution(degrees)

    while swapcount < nswap:  # 有效交换次数小于规定交换次数
        if tn >= max_tries:
            e = ('尝试次数 (%s) 已超过允许的最大次数' % tn + '有效交换次数（%s)' % swapcount)
            print(e)
            break
        tn += 1

        # 在保证度分布不变的情况下，随机选取两条连边u-v，x-y
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        if ui == xi:
            continue
        u = keys[ui]
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))

        if len(set([u, v, x, y])) == 4:  # 保证是四个独立节点
            if edge_in_community(node_community_list, (u, v)) == 1 and edge_in_community(node_community_list, (x, y)) == 1:  # 保证所取的连边为社团内部连边
                # 保证新生成的边还是社团内连边
                if edge_in_community(node_community_list, (u, y)) == 1 and edge_in_community(node_community_list, (v, x)) == 1:

                    if (y not in G[u]) and (v not in G[x]):  # 保证新生成的连边是原网络中不存在的边
                        G.add_edge(u, y)  # 增加两条新连边
                        G.add_edge(v, x)

                        G.remove_edge(u, v)  # 删除两条旧连边
                        G.remove_edge(x, y)

                    if connected == 1:  # 判断是否需要保持联通特性，为1的话则需要保持该特性
                        # 保证网络是全联通的:若网络不是全联通网络，则撤回交换边的操作
                        if not nx.is_connected(G):
                            G.add_edge(u, v)
                            G.add_edge(x, y)
                            G.remove_edge(u, y)
                            G.remove_edge(x, v)
                            continue
                    swapcount = swapcount + 1
    return G


def inner_random_2k(G0, node_community_list, nswap=1, max_tries=100, connected=1):
    # 保证2k特性不变和网络联通的情况下，交换社团内部的连边
    # G0：待改变结构的网络
    # node_community_list：是网络中节点的社团归属信息
    # nswap：是改变成功的系数，默认值为1
    # max_tries：是尝试改变的次数，默认值为100
    # connected：是否需要保证网络的联通特性，参数为1需要保持，参数为0不需要保持

    if not nx.is_connected(G0):
        raise nx.NetworkXError("非连通图，必须为连通图")
    if G0.is_directed():
        raise nx.NetworkXError("仅适用于无向图")
    if nswap > max_tries:
        raise nx.NetworkXError("交换次数超过允许的最大次数")
    if len(G0) < 3:
        raise nx.NetworkXError("节点数太少，至少要含三个节点")

    tn = 0  # 尝试次数
    swapcount = 0  # 有效交换次数

    G = copy.deepcopy(G0)
    keys, degrees = zip(*G.degree().items())
    cdf = nx.utils.cumulative_distribution(degrees)

    while swapcount < nswap:  # 有效交换次数小于规定交换次数
        if tn >= max_tries:
            e = ('尝试次数 (%s) 已超过允许的最大次数' % tn + '有效交换次数（%s)' % swapcount)
            print(e)
            break
        tn += 1

        # 在保证度分布不变的情况下，随机选取两条连边u-v，x-y
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        if ui == xi:
            continue
        u = keys[ui]
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))

        if len(set([u, v, x, y])) == 4:  # 保证是四个独立节点
            if edge_in_community(node_community_list, (u, v)) == 1 and edge_in_community(node_community_list, (x, y)) == 1:  # 保证所取的连边为社团内部连边
                # 保证新生成的边还是社团内连边
                if edge_in_community(node_community_list, (u, y)) == 1 and edge_in_community(node_community_list, (v, x)) == 1:

                    if G.degree(v) == G.degree(y):  # 保证节点的度匹配特性不变
                        if (y not in G[u]) and (v not in G[x]):  # 保证新生成的连边是原网络中不存在的边
                            G.add_edge(u, y)  # 增加两条新连边
                            G.add_edge(v, x)

                            G.remove_edge(u, v)  # 删除两条旧连边
                            G.remove_edge(x, y)

                            if connected == 1:  # 判断是否需要保持联通特性，为1的话则需要保持该特性
                                # 保证网络是全联通的:若网络不是全联通网络，则撤回交换边的操作
                                if not nx.is_connected(G):
                                    G.add_edge(u, v)
                                    G.add_edge(x, y)
                                    G.remove_edge(u, y)
                                    G.remove_edge(x, v)
                                    continue
                            swapcount = swapcount + 1
    return G


def inner_random_25k(G0, node_community_list, nswap=1, max_tries=100, connected=1):
    # 保证2.5k特性不变和网络联通的情况下，交换社团内部的连边
    # G0：待改变结构的网络
    # node_community_list：是网络中节点的社团归属信息
    # nswap：是改变成功的系数，默认值为1
    # max_tries：是尝试改变的次数，默认值为100
    # connected：是否需要保证网络的联通特性，参数为1需要保持，参数为0不需要保持

    if not nx.is_connected(G0):
        raise nx.NetworkXError("非连通图，必须为连通图")
    if G0.is_directed():
        raise nx.NetworkXError("仅适用于无向图")
    if nswap > max_tries:
        raise nx.NetworkXError("交换次数超过允许的最大次数")
    if len(G0) < 3:
        raise nx.NetworkXError("节点数太少，至少要含三个节点")

    tn = 0  # 尝试次数
    swapcount = 0  # 有效交换次数

    G = copy.deepcopy(G0)
    keys, degrees = zip(*G.degree().items())
    cdf = nx.utils.cumulative_distribution(degrees)

    while swapcount < nswap:  # 有效交换次数小于规定交换次数
        if tn >= max_tries:
            e = ('尝试次数 (%s) 已超过允许的最大次数' % tn + '有效交换次数（%s)' % swapcount)
            print(e)
            break
        tn += 1

        # 在保证度分布不变的情况下，随机选取两条连边u-v，x-y
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        if ui == xi:
            continue
        u = keys[ui]
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))

        if len(set([u, v, x, y])) == 4:  # 保证是四个独立节点
            if edge_in_community(node_community_list, (u, v)) == 1 and edge_in_community(node_community_list, (x, y)) == 1:  # 保证所取的连边为社团内部连边
                # 保证新生成的边还是社团内连边
                if edge_in_community(node_community_list, (u, y)) == 1 and edge_in_community(node_community_list, (v, x)) == 1:

                    if G.degree(v) == G.degree(y):  # 保证节点的度匹配特性不变
                        if (y not in G[u]) and (v not in G[x]):  # 保证新生成的连边是原网络中不存在的边
                            G.add_edge(u, y)  # 增加两条新连边
                            G.add_edge(v, x)

                            G.remove_edge(u, v)  # 删除两条旧连边
                            G.remove_edge(x, y)

                            degree_node_list = map(lambda t: (t[1], t[0]), G0.degree(
                                [u, v, x, y] + list(G[u]) + list(G[v]) + list(G[x]) + list(G[y])).items())
                            # 先找到四个节点以及他们邻居节点的集合，然后取出这些节点所有的度值对应的节点，格式为（度，节点）形式的列表

                            # 找到每个度对应的所有节点，具体形式为
                            D = dict_degree_nodes(degree_node_list)
                            for i in range(len(D)):
                                avcG0 = nx.average_clustering(
                                    G0, nodes=D.values()[i], weight=None, count_zeros=True)
                                avcG = nx.average_clustering(
                                    G, nodes=D.values()[i], weight=None, count_zeros=True)
                                i += 1
                                if avcG0 != avcG:  # 若置乱前后度相关的聚类系数不同，则撤销此次置乱操作
                                    G.add_edge(u, v)
                                    G.add_edge(x, y)
                                    G.remove_edge(u, y)
                                    G.remove_edge(x, v)
                                    break
                                if connected == 1:  # 判断是否需要保持联通特性，为1的话则需要保持该特性
                                    # 保证网络是全联通的:若网络不是全联通网络，则撤回交换边的操作
                                    if not nx.is_connected(G):
                                        G.add_edge(u, v)
                                        G.add_edge(x, y)
                                        G.remove_edge(u, y)
                                        G.remove_edge(x, v)
                                        continue
                                swapcount = swapcount + 1

    return G


def inner_random_3k(G0, node_community_list, nswap=1, max_tries=100, connected=1):
    # 保证3k特性不变和网络联通的情况下，交换社团内部的连边
    # G0：待改变结构的网络
    # node_community_list：是网络中节点的社团归属信息
    # nswap：是改变成功的系数，默认值为1
    # max_tries：是尝试改变的次数，默认值为100
    # connected：是否需要保证网络的联通特性，参数为1需要保持，参数为0不需要保持

    if not nx.is_connected(G0):
        raise nx.NetworkXError("非连通图，必须为连通图")
    if G0.is_directed():
        raise nx.NetworkXError("仅适用于无向图")
    if nswap > max_tries:
        raise nx.NetworkXError("交换次数超过允许的最大次数")
    if len(G0) < 3:
        raise nx.NetworkXError("节点数太少，至少要含三个节点")

    tn = 0  # 尝试次数
    swapcount = 0  # 有效交换次数

    G = copy.deepcopy(G0)
    keys, degrees = zip(*G.degree().items())
    cdf = nx.utils.cumulative_distribution(degrees)

    while swapcount < nswap:  # 有效交换次数小于规定交换次数
        if tn >= max_tries:
            e = ('尝试次数 (%s) 已超过允许的最大次数' % tn + '有效交换次数（%s)' % swapcount)
            print(e)
            break
        tn += 1

        # 在保证度分布不变的情况下，随机选取两条连边u-v，x-y
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        if ui == xi:
            continue
        u = keys[ui]
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))

        if len(set([u, v, x, y])) == 4:  # 保证是四个独立节点
            if edge_in_community(node_community_list, (u, v)) == 1 and edge_in_community(node_community_list, (x, y)) == 1:  # 保证所取的连边为社团间连边
                # 保证新生成的边还是社团内连边
                if edge_in_community(node_community_list, (u, y)) == 1 and edge_in_community(node_community_list, (v, x)) == 1:
                    if G.degree(v) == G.degree(y):  # 保证节点的度匹配特性不变

                        if (y not in G[u]) and (v not in G[x]):  # 保证新生成的连边是原网络中不存在的边
                            G.add_edge(u, y)  # 增加两条新连边
                            G.add_edge(v, x)

                            G.remove_edge(u, v)  # 删除两条旧连边
                            G.remove_edge(x, y)

                            # 找到四个节点以及他们邻居节点的集合
                            node_list = [
                                u, v, x, y] + list(G[u]) + list(G[v]) + list(G[x]) + list(G[y])
                            # 计算旧网络中4个节点以及他们邻居节点的聚类系数
                            avcG0 = nx.clustering(G0, nodes=node_list)
                            # 计算新网络中4个节点以及他们邻居节点的聚类系数
                            avcG = nx.clustering(G, nodes=node_list)

                            if avcG0 != avcG:  # 保证涉及到的四个节点聚类系数相同:若聚类系数不同，则撤回交换边的操作
                                G.add_edge(u, v)
                                G.add_edge(x, y)
                                G.remove_edge(u, y)
                                G.remove_edge(x, v)
                                continue
                            if connected == 1:  # 判断是否需要保持联通特性，为1的话则需要保持该特性
                                # 保证网络是全联通的:若网络不是全联通网络，则撤回交换边的操作
                                if not nx.is_connected(G):
                                    G.add_edge(u, v)
                                    G.add_edge(x, y)
                                    G.remove_edge(u, y)
                                    G.remove_edge(x, v)
                                    continue
                            swapcount = swapcount + 1
    return G


def inter_random_1k(G0, node_community_list, nswap=1, max_tries=100, connected=1):
    # 保证度分布特性不变和网络联通的情况下，交换社团外部的连边
    # G0：待改变结构的网络
    # node_community_list：是网络中节点的社团归属信息
    # nswap：是改变成功的系数，默认值为1
    # max_tries：是尝试改变的次数，默认值为100
    # connected：是否需要保证网络的联通特性，参数为1需要保持，参数为0不需要保持

    if not nx.is_connected(G0):
        raise nx.NetworkXError("非连通图，必须为连通图")
    if G0.is_directed():
        raise nx.NetworkXError("仅适用于无向图")
    if nswap > max_tries:
        raise nx.NetworkXError("交换次数超过允许的最大次数")
    if len(G0) < 3:
        raise nx.NetworkXError("节点数太少，至少要含三个节点")

    tn = 0  # 尝试次数
    swapcount = 0  # 有效交换次数

    G = copy.deepcopy(G0)
    keys, degrees = zip(*G.degree().items())
    cdf = nx.utils.cumulative_distribution(degrees)

    while swapcount < nswap:  # 有效交换次数小于规定交换次数
        if tn >= max_tries:
            e = ('尝试次数 (%s) 已超过允许的最大次数' % tn + '有效交换次数（%s)' % swapcount)
            print(e)
            break
        tn += 1

        # 在保证度分布不变的情况下，随机选取两条连边u-v，x-y
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        if ui == xi:
            continue
        u = keys[ui]
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))

        if len(set([u, v, x, y])) == 4:  # 保证是四个独立节点
            if edge_in_community(node_community_list, (u, v)) == 0 and edge_in_community(node_community_list, (x, y)) == 0:  # 保证所取的连边为社团内部连边
                # 保证新生成的边还是社团内连边
                if edge_in_community(node_community_list, (u, y)) == 0 and edge_in_community(node_community_list, (v, x)) == 0:

                    if (y not in G[u]) and (v not in G[x]):  # 保证新生成的连边是原网络中不存在的边
                        G.add_edge(u, y)  # 增加两条新连边
                        G.add_edge(v, x)

                        G.remove_edge(u, v)  # 删除两条旧连边
                        G.remove_edge(x, y)

                    if connected == 1:  # 判断是否需要保持联通特性，为1的话则需要保持该特性
                        # 保证网络是全联通的:若网络不是全联通网络，则撤回交换边的操作
                        if not nx.is_connected(G):
                            G.add_edge(u, v)
                            G.add_edge(x, y)
                            G.remove_edge(u, y)
                            G.remove_edge(x, v)
                            continue
                    swapcount = swapcount + 1
    return G


def inter_random_2k(G0, node_community_list, nswap=1, max_tries=100, connected=1):
    # 保证2k特性不变和网络联通的情况下，交换社团外部的连边
    # G0：待改变结构的网络
    # node_community_list：是网络中节点的社团归属信息
    # nswap：是改变成功的系数，默认值为1
    # max_tries：是尝试改变的次数，默认值为100
    # connected：是否需要保证网络的联通特性，参数为1需要保持，参数为0不需要保持

    if not nx.is_connected(G0):
        raise nx.NetworkXError("非连通图，必须为连通图")
    if G0.is_directed():
        raise nx.NetworkXError("仅适用于无向图")
    if nswap > max_tries:
        raise nx.NetworkXError("交换次数超过允许的最大次数")
    if len(G0) < 3:
        raise nx.NetworkXError("节点数太少，至少要含三个节点")

    tn = 0  # 尝试次数
    swapcount = 0  # 有效交换次数

    G = copy.deepcopy(G0)
    keys, degrees = zip(*G.degree().items())
    cdf = nx.utils.cumulative_distribution(degrees)

    while swapcount < nswap:  # 有效交换次数小于规定交换次数
        if tn >= max_tries:
            e = ('尝试次数 (%s) 已超过允许的最大次数' % tn + '有效交换次数（%s)' % swapcount)
            print(e)
            break
        tn += 1

        # 在保证度分布不变的情况下，随机选取两条连边u-v，x-y
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        if ui == xi:
            continue
        u = keys[ui]
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))

        if len(set([u, v, x, y])) == 4:  # 保证是四个独立节点
            if edge_in_community(node_community_list, (u, v)) == 0 and edge_in_community(node_community_list, (x, y)) == 0:  # 保证所取的连边为社团内部连边
                # 保证新生成的边还是社团内连边
                if edge_in_community(node_community_list, (u, y)) == 0 and edge_in_community(node_community_list, (v, x)) == 0:

                    if G.degree(v) == G.degree(y):  # 保证节点的度匹配特性不变
                        if (y not in G[u]) and (v not in G[x]):  # 保证新生成的连边是原网络中不存在的边
                            G.add_edge(u, y)  # 增加两条新连边
                            G.add_edge(v, x)

                            G.remove_edge(u, v)  # 删除两条旧连边
                            G.remove_edge(x, y)

                            if connected == 1:  # 判断是否需要保持联通特性，为1的话则需要保持该特性
                                # 保证网络是全联通的:若网络不是全联通网络，则撤回交换边的操作
                                if not nx.is_connected(G):
                                    G.add_edge(u, v)
                                    G.add_edge(x, y)
                                    G.remove_edge(u, y)
                                    G.remove_edge(x, v)
                                    continue
                            swapcount = swapcount + 1
    return G


def inter_random_25k(G0, node_community_list, nswap=1, max_tries=100, connected=1):
    # 保证2.5k特性不变和网络联通的情况下，交换社团外部的连边
    # G0：待改变结构的网络
    # node_community_list：是网络中节点的社团归属信息
    # nswap：是改变成功的系数，默认值为1
    # max_tries：是尝试改变的次数，默认值为100
    # connected：是否需要保证网络的联通特性，参数为1需要保持，参数为0不需要保持

    if not nx.is_connected(G0):
        raise nx.NetworkXError("非连通图，必须为连通图")
    if G0.is_directed():
        raise nx.NetworkXError("仅适用于无向图")
    if nswap > max_tries:
        raise nx.NetworkXError("交换次数超过允许的最大次数")
    if len(G0) < 3:
        raise nx.NetworkXError("节点数太少，至少要含三个节点")

    tn = 0  # 尝试次数
    swapcount = 0  # 有效交换次数

    G = copy.deepcopy(G0)
    keys, degrees = zip(*G.degree().items())
    cdf = nx.utils.cumulative_distribution(degrees)

    while swapcount < nswap:  # 有效交换次数小于规定交换次数
        if tn >= max_tries:
            e = ('尝试次数 (%s) 已超过允许的最大次数' % tn + '有效交换次数（%s)' % swapcount)
            print(e)
            break
        tn += 1

        # 在保证度分布不变的情况下，随机选取两条连边u-v，x-y
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        if ui == xi:
            continue
        u = keys[ui]
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))

        if len(set([u, v, x, y])) == 4:  # 保证是四个独立节点
            if edge_in_community(node_community_list, (u, v)) == 0 and edge_in_community(node_community_list, (x, y)) == 0:  # 保证所取的连边为社团内部连边
                # 保证新生成的边还是社团内连边
                if edge_in_community(node_community_list, (u, y)) == 0 and edge_in_community(node_community_list, (v, x)) == 0:

                    if G.degree(v) == G.degree(y):  # 保证节点的度匹配特性不变
                        if (y not in G[u]) and (v not in G[x]):  # 保证新生成的连边是原网络中不存在的边
                            G.add_edge(u, y)  # 增加两条新连边
                            G.add_edge(v, x)

                            G.remove_edge(u, v)  # 删除两条旧连边
                            G.remove_edge(x, y)

                            degree_node_list = map(lambda t: (t[1], t[0]), G0.degree(
                                [u, v, x, y] + list(G[u]) + list(G[v]) + list(G[x]) + list(G[y])).items())
                            # 先找到四个节点以及他们邻居节点的集合，然后取出这些节点所有的度值对应的节点，格式为（度，节点）形式的列表

                            # 找到每个度对应的所有节点，具体形式为
                            D = dict_degree_nodes(degree_node_list)
                            for i in range(len(D)):
                                avcG0 = nx.average_clustering(
                                    G0, nodes=D.values()[i], weight=None, count_zeros=True)
                                avcG = nx.average_clustering(
                                    G, nodes=D.values()[i], weight=None, count_zeros=True)
                                i += 1
                                if avcG0 != avcG:  # 若置乱前后度相关的聚类系数不同，则撤销此次置乱操作
                                    G.add_edge(u, v)
                                    G.add_edge(x, y)
                                    G.remove_edge(u, y)
                                    G.remove_edge(x, v)
                                    break
                                if connected == 1:  # 判断是否需要保持联通特性，为1的话则需要保持该特性
                                    # 保证网络是全联通的:若网络不是全联通网络，则撤回交换边的操作
                                    if not nx.is_connected(G):
                                        G.add_edge(u, v)
                                        G.add_edge(x, y)
                                        G.remove_edge(u, y)
                                        G.remove_edge(x, v)
                                        continue
                                swapcount = swapcount + 1

    return G


def inter_random_3k(G0, node_community_list, nswap=1, max_tries=100, connected=1):
    # 保证3k特性不变和网络联通的情况下，交换社团外部的连边
    # G0：待改变结构的网络
    # node_community_list：是网络中节点的社团归属信息
    # nswap：是改变成功的系数，默认值为1
    # max_tries：是尝试改变的次数，默认值为100
    # connected：是否需要保证网络的联通特性，参数为1需要保持，参数为0不需要保持

    if not nx.is_connected(G0):
        raise nx.NetworkXError("非连通图，必须为连通图")
    if G0.is_directed():
        raise nx.NetworkXError("仅适用于无向图")
    if nswap > max_tries:
        raise nx.NetworkXError("交换次数超过允许的最大次数")
    if len(G0) < 3:
        raise nx.NetworkXError("节点数太少，至少要含三个节点")

    tn = 0  # 尝试次数
    swapcount = 0  # 有效交换次数

    G = copy.deepcopy(G0)
    keys, degrees = zip(*G.degree().items())
    cdf = nx.utils.cumulative_distribution(degrees)

    while swapcount < nswap:  # 有效交换次数小于规定交换次数
        if tn >= max_tries:
            e = ('尝试次数 (%s) 已超过允许的最大次数' % tn + '有效交换次数（%s)' % swapcount)
            print(e)
            break
        tn += 1

        # 在保证度分布不变的情况下，随机选取两条连边u-v，x-y
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        if ui == xi:
            continue
        u = keys[ui]
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))

        if len(set([u, v, x, y])) == 4:  # 保证是四个独立节点
            if edge_in_community(node_community_list, (u, v)) == 0 and edge_in_community(node_community_list, (x, y)) == 0:  # 保证所取的连边为社团间连边
                # 保证新生成的边还是社团内连边
                if edge_in_community(node_community_list, (u, y)) == 0 and edge_in_community(node_community_list, (v, x)) == 0:
                    if G.degree(v) == G.degree(y):  # 保证节点的度匹配特性不变

                        if (y not in G[u]) and (v not in G[x]):  # 保证新生成的连边是原网络中不存在的边
                            G.add_edge(u, y)  # 增加两条新连边
                            G.add_edge(v, x)

                            G.remove_edge(u, v)  # 删除两条旧连边
                            G.remove_edge(x, y)

                            # 找到四个节点以及他们邻居节点的集合
                            node_list = [
                                u, v, x, y] + list(G[u]) + list(G[v]) + list(G[x]) + list(G[y])
                            # 计算旧网络中4个节点以及他们邻居节点的聚类系数
                            avcG0 = nx.clustering(G0, nodes=node_list)
                            # 计算新网络中4个节点以及他们邻居节点的聚类系数
                            avcG = nx.clustering(G, nodes=node_list)

                            if avcG0 != avcG:  # 保证涉及到的四个节点聚类系数相同:若聚类系数不同，则撤回交换边的操作
                                G.add_edge(u, v)
                                G.add_edge(x, y)
                                G.remove_edge(u, y)
                                G.remove_edge(x, v)
                                continue
                            if connected == 1:  # 判断是否需要保持联通特性，为1的话则需要保持该特性
                                # 保证网络是全联通的:若网络不是全联通网络，则撤回交换边的操作
                                if not nx.is_connected(G):
                                    G.add_edge(u, v)
                                    G.add_edge(x, y)
                                    G.remove_edge(u, y)
                                    G.remove_edge(x, v)
                                    continue
                            swapcount = swapcount + 1
    return G


def inner_community_swap(G0, node_community_list, nswap=1, max_tries=100):
    # 保证度分布不变的情况下，交换社团内的连边
    # G0：待改变结构的网络
    # node_community_list：是网络中节点的社团归属信息
    # nswap：是改变成功的系数，默认值为1
    # max_tries：是尝试改变的次数，默认值为100

    if not nx.is_connected(G0):
        raise nx.NetworkXError("非连通图，必须为连通图")
    if G0.is_directed():
        raise nx.NetworkXError("仅适用于无向图")
    if nswap > max_tries:
        raise nx.NetworkXError("交换次数超过允许的最大次数")
    if len(G0) < 3:
        raise nx.NetworkXError("节点数太少，至少要含三个节点")

    tn = 0  # 尝试次数
    swapcount = 0  # 有效交换次数

    G = copy.deepcopy(G0)
    keys, degrees = zip(*G.degree().items())
    cdf = nx.utils.cumulative_distribution(degrees)

    while swapcount < nswap:  # 有效交换次数小于规定交换次数
        if tn >= max_tries:
            e = ('尝试次数 (%s) 已超过允许的最大次数' % tn + '有效交换次数（%s)' % swapcount)
            print(e)
            break
        tn += 1

        # 在保证度分布不变的情况下，随机选取两条连边u-v，x-y
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        if ui == xi:
            continue
        u = keys[ui]
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))

        if len(set([u, v, x, y])) == 4:  # 保证是四个独立节点
            if edge_in_community(node_community_list, (u, v)) == 1 and edge_in_community(node_community_list, (x, y)) == 1:  # 保证所取的连边为社团内连边
                # 保证新生成的边还是社团内连边
                if edge_in_community(node_community_list, (u, y)) == 1 and edge_in_community(node_community_list, (v, x)) == 1:
                    if (y not in G[u]) and (v not in G[x]):  # 保证新生成的连边是原网络中不存在的边
                        G.add_edge(u, y)  # 增加两条新连边
                        G.add_edge(v, x)

                        G.remove_edge(u, v)  # 删除两条旧连边
                        G.remove_edge(x, y)

                        swapcount += 1  # 改变成功次数加1
    return G


def inter_community_swap(G0, node_community_list, nswap=1, max_tries=100):
    # 保证度分布不变的情况下，交换社团间的连边
    # G0：待改变结构的网络
    # node_community_list：是网络中节点的社团归属信息
    # nswap：是改变成功的系数，默认值为1
    # max_tries：是尝试改变的次数，默认值为100

    if not nx.is_connected(G0):
        raise nx.NetworkXError("非连通图，必须为连通图")
    if G0.is_directed():
        raise nx.NetworkXError("仅适用于无向图")
    if nswap > max_tries:
        raise nx.NetworkXError("交换次数超过允许的最大次数")
    if len(G0) < 3:
        raise nx.NetworkXError("节点数太少，至少要含三个节点")

    tn = 0  # 尝试次数
    swapcount = 0  # 有效交换次数

    G = copy.deepcopy(G0)
    keys, degrees = zip(*G.degree().items())
    cdf = nx.utils.cumulative_distribution(degrees)

    while swapcount < nswap:  # 有效交换次数小于规定交换次数
        if tn >= max_tries:
            e = ('尝试次数 (%s) 已超过允许的最大次数' % tn + '有效交换次数（%s)' % swapcount)
            print(e)
            break
        tn += 1

        # 在保证度分布不变的情况下，随机选取两条连边u-v，x-y
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        if ui == xi:
            continue
        u = keys[ui]
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))

        if len(set([u, v, x, y])) == 4:  # 保证为四个独立节点
            if edge_in_community(node_community_list, (u, v)) == 0 and edge_in_community(node_community_list, (x, y)) == 0:  # 保证所取的连边是社团间部连边
                # 保证新生成的边是社团间的连边
                if edge_in_community(node_community_list, (u, y)) == 0 and edge_in_community(node_community_list, (v, x)) == 0:
                    if (y not in G[u]) and (v not in G[x]):  # 保证新生成的连边是原网络中不存在的边
                        G.add_edge(u, y)  # 增加两条新连边
                        G.add_edge(v, x)

                        G.remove_edge(u, v)  # 删除两条旧连边
                        G.remove_edge(x, y)

                        swapcount = swapcount + 1  # 改变成功次数加1

    return G


def Q_increase(G0, node_community_list, nswap=1, max_tries=100):
    # 保证度分布不变的情况下，增强社团结构特性
    # G0：待改变结构的网络
    # node_community_list：是网络中节点的社团归属信息
    # nswap：是改变成功的系数，默认值为1
    # max_tries：是尝试改变的次数，默认值为100

    if not nx.is_connected(G0):
        raise nx.NetworkXError("非连通图，必须为连通图")
    if G0.is_directed():
        raise nx.NetworkXError("仅适用于无向图")
    if nswap > max_tries:
        raise nx.NetworkXError("交换次数超过允许的最大次数")
    if len(G0) < 3:
        raise nx.NetworkXError("节点数太少，至少要含三个节点")

    tn = 0  # 尝试次数
    swapcount = 0  # 有效交换次数

    G = copy.deepcopy(G0)
    keys, degrees = zip(*G.degree().items())
    cdf = nx.utils.cumulative_distribution(degrees)

    while swapcount < nswap:  # 有效交换次数小于规定交换次数
        if tn >= max_tries:
            e = ('尝试次数 (%s) 已超过允许的最大次数' % tn + '有效交换次数（%s)' % swapcount)
            print(e)
            break
        tn += 1

        # 在保证度分布不变的情况下，随机选取两条连边u-v，x-y
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        if ui == xi:
            continue
        u = keys[ui]
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))

        if len(set([u, v, x, y])) == 4:  # 保证是四个独立节点
            if edge_in_community(node_community_list, (u, v)) == 0 and edge_in_community(node_community_list, (x, y)) == 0:  # 保证所取的连边为社团间连边
                # 保证新生成的边是内部连边
                if edge_in_community(node_community_list, (u, y)) == 1 and edge_in_community(node_community_list, (v, x)) == 1:
                    if (y not in G[u]) and (v not in G[x]):  # 保证新生成的连边是原网络中不存在的边
                        G.add_edge(u, y)  # 增加两条新连边
                        G.add_edge(v, x)

                        G.remove_edge(u, v)  # 删除两条旧连边
                        G.remove_edge(x, y)

                        swapcount += 1  # 改变成功次数加1

    return G


def Q_decrease(G0, node_community_list, nswap=1, max_tries=100):
    # 保证度分布不变的情况下，减弱社团结构特性
    # G0：待改变结构的网络
    # node_community_list：是网络中节点的社团归属信息
    # nswap：是改变成功的系数，默认值为1
    # max_tries：是尝试改变的次数，默认值为100

    if not nx.is_connected(G0):
        raise nx.NetworkXError("非连通图，必须为连通图")
    if G0.is_directed():
        raise nx.NetworkXError("仅适用于无向图")
    if nswap > max_tries:
        raise nx.NetworkXError("交换次数超过允许的最大次数")
    if len(G0) < 3:
        raise nx.NetworkXError("节点数太少，至少要含三个节点")

    tn = 0  # 尝试次数
    swapcount = 0  # 有效交换次数

    G = copy.deepcopy(G0)
    keys, degrees = zip(*G.degree().items())
    cdf = nx.utils.cumulative_distribution(degrees)

    while swapcount < nswap:  # 有效交换次数小于规定交换次数
        if tn >= max_tries:
            e = ('尝试次数 (%s) 已超过允许的最大次数' % tn + '有效交换次数（%s)' % swapcount)
            print(e)
            break
        tn += 1

        # 在保证度分布不变的情况下，随机选取两条连边u-v，x-y
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
        if ui == xi:
            continue
        u = keys[ui]
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))

        if len(set([u, v, x, y])) == 4:  # 保证为四个独立节点
            if edge_in_community(node_community_list, (u, v)) == 1 and edge_in_community(node_community_list, (x, y)) == 1:  # 保证所取的连边是社团内部连边
                # 保证新生成的边是社团间的连边
                if edge_in_community(node_community_list, (u, y)) == 0 and edge_in_community(node_community_list, (v, x)) == 0:
                    if (y not in G[u]) and (v not in G[x]):  # 保证新生成的连边是原网络中不存在的边
                        G.add_edge(u, y)  # 增加两条新连边
                        G.add_edge(v, x)

                        G.remove_edge(u, v)  # 删除两条旧连边
                        G.remove_edge(x, y)

                        swapcount += 1  # 改变成功次数加1

    return G
