# Job Estimate & Management API — 설계

1인 종합 건축사무소(시공·설계·배선·루핑·수리·인테리어·목공)를 위한 고객·작업·견적 관리 백엔드.

## 1. 데이터 구조

### customers (고객)
| 컬럼 | 타입 | 규칙 |
|---|---|---|
| id | INTEGER PK | 자동 증가 |
| name | TEXT | 필수, 1~50자 |
| phone | TEXT | 필수, 숫자와 `-`만, 숫자 9~15자리 |
| email | TEXT | 선택, 최대 254자 |
| address | TEXT | 선택, 최대 200자 |
| created_at | TEXT | ISO 8601, 서버가 생성 |

> email 최대 길이: 경계값을 표준에 맞춰서 정했다. 254자는 이메일 주소 길이의 표준 최대값(RFC 5321 기준)이다.

### jobs (작업)
| 컬럼 | 타입 | 규칙 |
|---|---|---|
| id | INTEGER PK | |
| customer_id | INTEGER FK | 존재하는 고객이어야 함 |
| title | TEXT | 필수, 1~100자 |
| job_type | TEXT | `construction` `design` `electrical` `roofing` `repair` `interior` `woodworking` 중 하나 |
| site_address | TEXT | 필수, 최대 200자 |
| description | TEXT | 선택, 최대 2000자 |
| status | TEXT | 생성 시 항상 `inquiry` |
| scheduled_start / scheduled_end | TEXT (YYYY-MM-DD) | 선택, end ≥ start |
| created_at / updated_at | TEXT | 서버가 관리 |

### estimates / estimate_items (견적) — 2주차
- estimate: job_id, discount_rate(0~30%), vat_rate(기본 10%), notes
- item: kind(`material` `labor` `travel`), description, quantity(>0), unit_price(≥0)
- 계산: 항목별 금액 = quantity × unit_price → 소계 → 할인 → 부가세 → 합계 (원 단위, 반올림 규칙은 2주차에 확정)

## 2. 상태 흐름 — 3주차

```
inquiry → estimating → contracted → in_progress → completed → settled
   └──────────┴────────────┴→ cancelled (완료 전까지만)
```
허용되지 않은 전환(예: inquiry → completed)은 `409 Conflict`.

## 3. 엔드포인트

| 주차 | Method | Path | 성공 | 주요 에러 |
|---|---|---|---|---|
| 1 | GET | /health | 200 | |
| 1 | POST | /customers | 201 | 422 입력 오류 |
| 1 | GET | /customers | 200 | |
| 1 | GET | /customers/{id} | 200 | 404 |
| 1 | PATCH | /customers/{id} | 200 | 404, 422 |
| 1 | DELETE | /customers/{id} | 204 | 404, 409 (작업이 있는 고객) |
| 1 | POST | /jobs | 201 | 404 고객 없음, 422 |
| 1 | GET | /jobs?status=&customer_id= | 200 | |
| 1 | GET | /jobs/{id} | 200 | 404 |
| 1 | PATCH | /jobs/{id} | 200 | 404, 422 (status는 여기서 못 바꿈) |
| 1 | DELETE | /jobs/{id} | 204 | 404 |
| 2 | POST | /jobs/{id}/estimates | 201 | |
| 2 | GET | /estimates/{id} | 200 | 계산된 합계 포함 |
| 3 | POST | /jobs/{id}/status | 200 | 409 잘못된 전환 |

## 4. 에러 응답 형식
FastAPI 기본 형식을 따름: `{"detail": "..."}` (422는 `detail`이 오류 목록).

## 5. 주차별 계획
1. 고객·작업 CRUD + Postman 컬렉션 + 고객 API 테스트
2. 견적 계산 로직 + 경계값 테스트
3. 상태 흐름 + JSON schema 검증 + SQL로 DB 값 검증
4. GitHub Actions + README (테스트 전략, 발견한 버그)
