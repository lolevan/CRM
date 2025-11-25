import pytest

@pytest.mark.asyncio
async def test_weighted_distribution_basic(client):
    # create operators
    op1 = (await client.post("/api/v1/operators", json={"name": "op1", "max_active_contacts": 100})).json()
    op2 = (await client.post("/api/v1/operators", json={"name": "op2", "max_active_contacts": 100})).json()

    # create source
    s = (await client.post("/api/v1/sources", json={"code": "A", "name": "Bot A"})).json()

    # set weights 10 vs 30 (25% / 75%)
    await client.put(f"/api/v1/sources/{s['id']}/operators", json={
        "operators": [
            {"operator_id": op1["id"], "weight": 10},
            {"operator_id": op2["id"], "weight": 30},
        ]
    })

    # simulate 200 contacts
    counts = {op1["id"]: 0, op2["id"]: 0, None: 0}
    for i in range(200):
        c = (await client.post("/api/v1/contacts", json={
            "lead": {"external_id": f"L{i}"},
            "source_code": "A",
            "payload": "hi"
        })).json()
        counts[c["operator_id"]] += 1

    # expect roughly 1:3 ratio
    ratio = counts[op2["id"]] / max(counts[op1["id"]], 1)
    assert 2.0 < ratio < 4.5
