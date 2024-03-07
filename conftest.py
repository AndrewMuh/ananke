import copy

import numpy as np
import pytest
import sympy as sp

from ananke.graphs import DAG
from ananke.models import (
    BayesianNetwork,
    bayesian_network,
    create_symbolic_cpds,
)


@pytest.fixture
def conditional_ignorability_graph():
    graph = DAG(
        di_edges=[("A", "Y"), ("C", "A"), ("C", "Y")],
        vertices={"A": 2, "C": 2, "Y": 2},
    )
    cpds = bayesian_network.generate_random_cpds(graph, dir_conc=1)

    net = bayesian_network.BayesianNetwork(graph, cpds)

    return graph, net


@pytest.fixture
def simple_graph():
    graph = DAG(
        di_edges=[
            ("A", "Y"),
            ("U", "A"),
            ("U", "Y"),
            ("S", "A"),
            ("S", "Y"),
        ],
        vertices={"A": 2, "Y": 3, "U": 2, "S": 4},
    )
    contexts = [set(), {"A"}, {"Y"}, {"A", "Y"}]
    cards = {"A": 2, "Y": 3, "S": len(contexts), "U": 2}
    return graph, contexts, cards


@pytest.fixture
def bow_arc_bayesian_network_models():
    dag = DAG(
        vertices={"Y": 2, "A": 2, "U_A_Y": 3},
        di_edges=[("A", "Y"), ("U_A_Y", "A"), ("U_A_Y", "Y")],
    )
    cpds, params = create_symbolic_cpds(dag)
    params_1 = [
        (sp.Symbol("q_Y_0_00"), sp.Rational(7, 10)),
        (sp.Symbol("q_Y_0_01"), sp.Rational(5, 8)),
        (sp.Symbol("q_Y_0_02"), sp.Rational(1, 4)),
        (sp.Symbol("q_Y_0_10"), sp.Rational(7, 8)),
        (sp.Symbol("q_Y_0_11"), sp.Rational(1, 4)),
        (sp.Symbol("q_Y_0_12"), sp.Rational(5, 8)),
        (sp.Symbol("q_A_0_0"), sp.Rational(5, 8)),
        (sp.Symbol("q_A_0_1"), sp.Rational(1, 4)),
        (sp.Symbol("q_A_0_2"), sp.Rational(5, 8)),
    ]
    params_2 = [
        (sp.Symbol("q_Y_0_00"), sp.Rational(21, 40)),
        (sp.Symbol("q_Y_0_01"), sp.Rational(1, 8)),
        (sp.Symbol("q_Y_0_02"), sp.Rational(3, 4)),
        (sp.Symbol("q_Y_0_10"), sp.Rational(7, 8)),
        (sp.Symbol("q_Y_0_11"), sp.Rational(3, 8)),
        (sp.Symbol("q_Y_0_12"), sp.Rational(3, 8)),
        (sp.Symbol("q_A_0_0"), sp.Rational(5, 8)),
        (sp.Symbol("q_A_0_1"), sp.Rational(3, 8)),
        (sp.Symbol("q_A_0_2"), sp.Rational(1, 2)),
    ]
    cpds_1 = dict()
    for variable, cpd in cpds.items():
        new_cpd = copy.deepcopy(cpd)
        new_cpd.values = new_cpd.values.subs(params_1)
        cpds_1[variable] = new_cpd

    cpds_2 = dict()
    for variable, cpd in cpds.items():
        new_cpd = copy.deepcopy(cpd)
        new_cpd.values = new_cpd.values.subs(params_2)
        cpds_2[variable] = new_cpd

    net_1 = BayesianNetwork(dag, cpds_1)
    net_2 = BayesianNetwork(dag, cpds_2)
    return net_1, net_2
