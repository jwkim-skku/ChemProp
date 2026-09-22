# Data Guide

원본 CSV와 SDF 파일은 수업 자료의 재배포 가능 여부가 확인되지 않아 이 저장소에 포함하지 않습니다.

## 입력 CSV 스키마

| column | type | description |
|---|---|---|
| `uid` | string | 분자 식별자 |
| `smiles` | string | 분자 구조의 SMILES 표현 |
| `S1_energy` | float | singlet excited-state energy (eV) |
| `T1_energy` | float | triplet excited-state energy (eV) |

`src/prepare_data.py`가 아래 파생변수를 생성합니다.

```text
ST_GAP(eV) = S1_energy - T1_energy
```

## 권장 디렉터리

```text
data/
├─ train.csv
├─ dev.csv
├─ invalid_uids.txt       # 선택 사항: 한 줄에 UID 하나
└─ processed/             # 스크립트가 생성하는 결과
```

`.gitignore`는 CSV·SDF와 학습 산출물을 기본적으로 제외합니다.
