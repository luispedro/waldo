import go.go
def test_is_cellular_component():
    assert go.go.is_cellular_component('GO:0000015')
    assert go.go.is_cellular_component('GO:0000108')
    assert not go.go.is_cellular_component('GO:0000107')

