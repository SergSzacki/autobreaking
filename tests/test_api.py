CAR = {"make": "Toyota", "model": "Corolla", "year": 2019, "vin": "JTDBU4EE9B9123456", "mileage": 45000}


def create_car(client, **overrides):
    response = client.post("/api/cars", json={**CAR, **overrides})
    assert response.status_code == 201, response.text
    return response.json()


def test_car_crud_and_pagination(client):
    car = create_car(client)
    create_car(client, make="BMW", model="X5", vin=None)
    create_car(client, make="Audi", model="A4", vin="")

    page = client.get("/api/cars", params={"page": 2, "per_page": 2}).json()
    assert page["meta"] == {"page": 2, "per_page": 2, "total": 3}
    assert len(page["cars"]) == 1

    assert client.get("/api/cars", params={"q": "bmw"}).json()["meta"]["total"] == 1

    patched = client.patch(f"/api/cars/{car['id']}", json={"color": "white"}).json()
    assert patched["color"] == "white" and patched["make"] == "Toyota"

    assert client.delete(f"/api/cars/{car['id']}").status_code == 204
    assert client.get(f"/api/cars/{car['id']}").status_code == 404


def test_validation_and_duplicates(client):
    assert client.post("/api/cars", json={**CAR, "year": 1500}).status_code == 422
    assert client.post("/api/cars", json={**CAR, "mileage": -1}).status_code == 422
    create_car(client)
    assert client.post("/api/cars", json=CAR).status_code == 409


def test_part_keeps_all_fields_and_photos(client):
    car = create_car(client)
    payload = {
        "name": "Oil filter",
        "sku": "OF-1",
        "quantity": 2,
        "min_quantity": 5,
        "price": 12.5,
        "supplier": "OEM",
        "location": "A1",
        "notes": "new",
        "photos": ["https://example.com/a.jpg"],
        "make": "ignored",
    }
    part = client.post(f"/api/cars/{car['id']}/parts", json=payload)
    assert part.status_code == 201, part.text
    data = part.json()
    for key in ("min_quantity", "supplier", "location", "notes", "photos", "price"):
        assert data[key] == payload[key]
    assert data["car_id"] == car["id"]


def test_inventory_search_and_car_info(client):
    car = create_car(client)
    client.post(f"/api/cars/{car['id']}/parts", json={"name": "Brake pad", "sku": ""})
    client.post("/api/parts", json={"name": "Wiper", "sku": ""})

    items = client.get("/api/inventory").json()
    assert {item["name"] for item in items} == {"Brake pad", "Wiper"}
    brake = next(item for item in items if item["name"] == "Brake pad")
    assert (brake["make"], brake["model"]) == ("Toyota", "Corolla")

    assert [i["name"] for i in client.get("/api/inventory", params={"q": "corolla"}).json()] == ["Brake pad"]
    assert [i["name"] for i in client.get("/api/inventory", params={"q": "wip"}).json()] == ["Wiper"]


def test_standalone_part_endpoints(client):
    car_a = create_car(client)
    car_b = create_car(client, vin="WBA00000000000001")
    part = client.post("/api/parts", json={"name": "Mirror"}).json()
    assert part["car_id"] is None

    moved = client.patch(f"/api/parts/{part['id']}", json={"car_id": car_b["id"], "quantity": 3}).json()
    assert moved["car_id"] == car_b["id"] and moved["quantity"] == 3
    assert client.patch(f"/api/parts/{part['id']}", json={"car_id": 999}).status_code == 404

    assert client.patch(f"/api/cars/{car_a['id']}/parts/{part['id']}", json={"quantity": 1}).status_code == 404

    assert client.delete(f"/api/cars/{car_b['id']}").status_code == 204
    assert client.get(f"/api/parts/{part['id']}").json()["car_id"] is None
    assert client.delete(f"/api/parts/{part['id']}").status_code == 204
    assert client.get(f"/api/parts/{part['id']}").status_code == 404
