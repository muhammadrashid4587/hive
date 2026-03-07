"""
Tests for sub_agents reference validation.

Validates that all node IDs listed in a node's sub_agents field
are actually registered in the graph's nodes list.
"""

from framework.graph.edge import GraphSpec
from framework.graph.node import NodeSpec


class TestSubAgentRegistrationValidation:
    """sub_agents references to unregistered nodes must be rejected."""

    def test_sub_agent_not_registered_fails(self):
        """A node referencing a sub_agent that isn't in the nodes list -> error."""
        graph = GraphSpec(
            id="g1",
            goal_id="goal1",
            entry_node="main",
            terminal_nodes=["main"],
            nodes=[
                NodeSpec(
                    id="main",
                    name="Main",
                    description="Main node",
                    sub_agents=["missing_gcu"],
                ),
            ],
            edges=[],
        )

        errors = graph.validate()["errors"]
        sa_errors = [e for e in errors if "not registered" in e]
        assert len(sa_errors) == 1
        assert "'missing_gcu'" in sa_errors[0]
        assert "'main'" in sa_errors[0]

    def test_sub_agent_registered_passes(self):
        """A node referencing a sub_agent that exists in nodes -> no error."""
        graph = GraphSpec(
            id="g1",
            goal_id="goal1",
            entry_node="main",
            terminal_nodes=["main"],
            nodes=[
                NodeSpec(
                    id="main",
                    name="Main",
                    description="Main node",
                    sub_agents=["helper"],
                ),
                NodeSpec(
                    id="helper",
                    name="Helper",
                    description="Helper GCU node",
                    node_type="gcu",
                ),
            ],
            edges=[],
        )

        errors = graph.validate()["errors"]
        sa_errors = [e for e in errors if "not registered" in e]
        assert len(sa_errors) == 0

    def test_multiple_unregistered_sub_agents(self):
        """Multiple missing sub_agents -> one error per missing reference."""
        graph = GraphSpec(
            id="g1",
            goal_id="goal1",
            entry_node="main",
            terminal_nodes=["main"],
            nodes=[
                NodeSpec(
                    id="main",
                    name="Main",
                    description="Main node",
                    sub_agents=["missing_a", "missing_b"],
                ),
            ],
            edges=[],
        )

        errors = graph.validate()["errors"]
        sa_errors = [e for e in errors if "not registered" in e]
        assert len(sa_errors) == 2

    def test_no_sub_agents_passes(self):
        """A node with no sub_agents -> no error from this rule."""
        graph = GraphSpec(
            id="g1",
            goal_id="goal1",
            entry_node="main",
            terminal_nodes=["main"],
            nodes=[
                NodeSpec(id="main", name="Main", description="Main node"),
            ],
            edges=[],
        )

        errors = graph.validate()["errors"]
        sa_errors = [e for e in errors if "not registered" in e]
        assert len(sa_errors) == 0
