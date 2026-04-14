import requests
import json

METABASE_URL = "http://localhost:3000"
USERNAME = "YOUR_METABASE_EMAIL"
PASSWORD = "YOUR_METABASE_PASSWORD"
DB_NAME = "DuckDB"


def main():
    # 1. Authenticate
    session = requests.post(
        f"{METABASE_URL}/api/session", json={"username": USERNAME, "password": PASSWORD}
    )
    assert session.ok, session.text
    TOKEN = session.json()["id"]
    HEADERS = {"X-Metabase-Session": TOKEN}

    # 2. Get database ID
    dbs = requests.get(f"{METABASE_URL}/api/database", headers=HEADERS).json()["data"]
    db_id = next(db["id"] for db in dbs if db["name"] == DB_NAME)

    # 3. Create OEE Question
    q_payload = {
        "name": "OEE by Asset",
        "dataset_query": {
            "type": "native",
            "native": {
                "query": "SELECT unit_number, oee, availability, performance, quality FROM oee_final ORDER BY unit_number"
            },
            "database": db_id,
        },
        "display": "line",
        "visualization_settings": {
            "graph.dimensions": ["unit_number"],
            "graph.metrics": ["oee"],
        },
    }
    q_resp = requests.post(f"{METABASE_URL}/api/card", headers=HEADERS, json=q_payload)
    assert q_resp.ok, q_resp.text
    q_id = q_resp.json()["id"]

    # 4. Create Dashboard
    board_payload = {"name": "Factory OEE & Health"}
    b_resp = requests.post(
        f"{METABASE_URL}/api/dashboard", headers=HEADERS, json=board_payload
    )
    assert b_resp.ok, b_resp.text
    board_id = b_resp.json()["id"]

    # 5. Add Question to Dashboard
    add_payload = {
        "cardId": q_id,
        "dashboardId": board_id,
        "sizeX": 4,
        "sizeY": 4,
        "col": 0,
        "row": 0,
    }
    add_resp = requests.post(
        f"{METABASE_URL}/api/dashboard/{board_id}/cards",
        headers=HEADERS,
        json=add_payload,
    )
    assert add_resp.ok, add_resp.text

    print(f"Dashboard created: {METABASE_URL}/dashboard/{board_id}")


if __name__ == "__main__":
    main()
