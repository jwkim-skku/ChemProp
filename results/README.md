# Archived Results

이 디렉터리에는 원본 데이터나 checkpoint가 아니라, 사용자가 보존한 성공 실행 로그에서 확인한 요약 지표만 포함합니다.

## 5-fold test RMSE

| seed/fold | RMSE |
|---:|---:|
| 0 | 0.333313 |
| 1 | 0.371459 |
| 2 | 0.416622 |
| 3 | 0.353745 |
| 4 | 0.404121 |
| overall | **0.375852 ± 0.030916** |

ChemProp 로그의 RMSE는 S1, T1, ST Gap을 함께 학습한 3-target 회귀 실행 결과입니다.

별도 100개 테스트 표본의 ST Gap parity 후처리에서는 `MAE 0.23 eV`, `RMSE 0.28 eV`가 기록되었습니다. 평가 집계 범위가 다르므로 위 5-fold 값과 직접 비교하지 않습니다.
