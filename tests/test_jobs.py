"""Job API tests — 1주차 후반에 직접 작성.

TODO:
# [ ] job fixture를 conftest.py에 추가 (customer fixture 재사용)
# [ ] POST /jobs → 201, status는 항상 "inquiry"
# [ ] POST /jobs에 status를 넣으면 → 422 (extra field)
# [ ] 존재하지 않는 customer_id → 404
# [ ] job_type 7종 모두 → 201 (parametrize), 정의되지 않은 값 → 422
# [ ] scheduled_end < scheduled_start → 422 / 같은 날 → 201 (경계값)
# [ ] PATCH로 scheduled_end만 바꿔서 기존 start보다 앞서게 → 422
# [ ] PATCH 후 updated_at이 바뀌는지
# [ ] GET /jobs?status=inquiry&customer_id=... 필터 결과 확인
# [ ] GET /jobs?status=unknown → 422
"""
