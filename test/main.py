from uuid import uuid4

from jose import jwt
from starlette.testclient import TestClient
import importlib.util
import sys

MODULE, PATH = 'main.app', '../app/main.py'

spec = importlib.util.spec_from_file_location(MODULE, PATH)
main = importlib.util.module_from_spec(spec)
sys.modules[MODULE] = main
spec.loader.exec_module(main)

client = TestClient(main.app)

ORIGIN_REF = str(uuid4())


def test_index():
    response = client.get('/')
    assert response.status_code == 200


def test_status():
    response = client.get('/status')
    assert response.status_code == 200
    assert response.json()['status'] == 'up'


def test_client_token():
    response = client.get('/client-token')
    assert response.status_code == 200


def test_auth_v1_origin():
    payload = {
        "registration_pending": False,
        "environment": {
            "guest_driver_version": "guest_driver_version",
            "hostname": "myhost",
            "ip_address_list": ["192.168.1.123"],
            "os_version": "os_version",
            "os_platform": "os_platform",
            "fingerprint": {"mac_address_list": ["ff:ff:ff:ff:ff:ff"]},
            "host_driver_version": "host_driver_version"
        },
        "update_pending": False,
        "candidate_origin_ref": ORIGIN_REF,
    }

    response = client.post('/auth/v1/origin', json=payload)
    assert response.status_code == 200
    assert response.json()['origin_ref'] == ORIGIN_REF


def test_auth_v1_code():
    payload = {
        "code_challenge": "0wmaiAMAlTIDyz4Fgt2/j0tXnGv72TYbbLs4ISRCZlY",
        "origin_ref": ORIGIN_REF,
    }

    response = client.post('/auth/v1/code', json=payload)
    assert response.status_code == 200

    payload = jwt.get_unverified_claims(token=response.json()['auth_code'])
    assert payload['origin_ref'] == ORIGIN_REF


def test_auth_v1_token():
    pass


def test_leasing_v1_lessor():
    pass


def test_leasing_v1_lessor_lease():
    pass


def test_leasing_v1_lease_renew():
    pass


def test_leasing_v1_lessor_lease_remove():
    pass
