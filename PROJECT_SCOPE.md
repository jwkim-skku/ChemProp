# Project Scope and Disclosure

## 프로젝트 성격

이 저장소는 2025년 2학기 성균관대학교 화학공학과 화공전자재료 교과에서 수행한 ChemProp 기반 ST Gap 예측 실습을 채용 검토용으로 재구성한 아카이브입니다.

## 개인 수행 범위

- CSV 로드와 `ST_GAP(eV)` 파생변수 생성
- SDF 비정상 종료 및 알려진 구조 오류 후보 필터링
- 학습·테스트 표본 구성과 고정 시드 적용
- ChemProp D-MPNN 학습·예측 실행
- fold별 RMSE, parity plot, 큰 오차 사례 분석
- 실행 조건과 결과의 문서화

## 외부 제공 요소

- ChemProp 라이브러리와 기본 실습 흐름
- 수업에서 제공된 원본 CSV·SDF 및 강의 자료

ChemProp 자체나 원본 데이터셋을 제작했다는 의미가 아닙니다.

## 공개하지 않은 자료

- 강의 PDF·영상·자막
- 원본 `train.csv`, `dev.csv`, SDF 묶음
- 학습 checkpoint
- 로컬 경로와 장시간 터미널 원문 로그

원본 자료의 권리와 개인정보를 보호하고 저장소를 검토 가능한 크기로 유지하기 위한 조치입니다.

## 지표 범위

- `0.375852 ± 0.030916`: 3개 목표값(S1, T1, ST Gap)을 대상으로 한 보존 ChemProp 5-fold 실행 로그의 overall test RMSE
- `MAE 0.23 eV / RMSE 0.28 eV`: 별도 100개 테스트 표본의 ST Gap parity 후처리 분석 요약

평가 대상과 집계 방식이 다르므로 두 값을 직접 비교하지 않습니다.
