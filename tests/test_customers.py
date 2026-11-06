"""Customer API tests.

예시 2개는 패턴을 보여주기 위한 것. 아래 TODO는 직접 작성해 보세요.
"""
import pytest


# ---------- 예시 1: happy path ----------

def test_create_customer_returns_201_and_echoes_fields(api, base_url, customer_payload):
    r = api.post(f"{base_url}/customers", json=customer_payload)

    assert r.status_code == 201
    body = r.json()
    assert body["name"] == customer_payload["name"]
    assert body["phone"] == customer_payload["phone"]
    assert isinstance(body["id"], int)
    assert "created_at" in body

    api.delete(f"{base_url}/customers/{body['id']}")  # cleanup


# ---------- 예시 2: negative cases with parametrize ----------

@pytest.mark.parametrize(
    "phone",
    [
        "abc-defg-hijk",  # letters
        "12345",          # too few digits
        "",               # empty
    ],
)
def test_create_customer_rejects_invalid_phone(api, base_url, customer_payload, phone):
    customer_payload["phone"] = phone
    r = api.post(f"{base_url}/customers", json=customer_payload)
    assert r.status_code == 422


# ---------- TODO: 직접 작성 ----------
# [ ] GET /customers/{id} → 200, 생성한 값과 일치 (customer fixture 사용)
# [ ] GET /customers/999999 → 404, detail == "Customer not found"
# [ ] name 누락 / 빈 문자열 / 51자 → 422 (parametrize)
# [ ] name 정확히 50자 → 201 (경계값)
# [ ] 전화번호 숫자 9자리, 15자리 → 201 / 16자리 → 422 (경계값)
# [ ] 정의되지 않은 필드(예: "vip": true) → 422
# [ ] PATCH로 address만 변경 → 다른 필드는 그대로
# [ ] PATCH로 phone을 null로 → 422
# [ ] DELETE → 204, 이후 GET → 404
# [ ] 작업(job)이 있는 고객 DELETE → 409
# [ ] 앞뒤 공백 있는 name → 저장 시 공백 제거되는지
