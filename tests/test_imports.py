"""Import smoke tests for the PlanningHub skeleton."""


def test_imports():
    import planninghub
    from planninghub import infrastructure, ports, services
    from planninghub.domain import entities, value_objects

    assert planninghub
    assert entities
    assert value_objects
    assert infrastructure
    assert ports
    assert services
    assert True
