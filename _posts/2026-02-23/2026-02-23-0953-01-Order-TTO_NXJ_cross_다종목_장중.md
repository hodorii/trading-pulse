---
layout: post
date: 2026-02-23 09:53:00 +0900
session_id: "2026-02-23-0953"
session_order: "01"
title: "Order-TTO_NXJ_cross_다종목_장중"
---
# 🌐 TTO NXJ 교차 분석 장중 보고서 (한국어 우선) - 다종목
세션 시간: 2026-02-23 09:53:00 (KST)
태그: NXJ_cross, 다종목, 장중

목표
- Regular(J) 시장 vs Nextrade(NX) 교차 가격 차이 및 시사점 도출
- IDR 결과와의 교차 참조 포함

데이터 및 가정
- J: 정규시장 가격 데이터, NX: Nextrade 가격 데이터. 레이턴시 및 지연 가능성 반영
- 본 문서는 샘플 데이터 기반 초안이며, 실제 데이터로 재계산 필요

주요 분석 내용 (샘플 데이터 기반)
- 09:55: J 1,000.00 vs NX 1,005.00 → price_diff +5.00, gap_ratio 0.50%
- 09:56: J 1,002.00 vs NX 1,006.00 → price_diff +4.00, gap_ratio ~0.40%
- 09:57: J 1,001.00 vs NX 1,004.00 → price_diff +3.00, gap_ratio ~0.30%

해석 포인트
- NX 프리미엄 형성 신호 지속 여부 확인 필요
- 유동성 변동과 체결 강도 차이가 가격 차이에 미치는 영향 평가 필요

IDR 참조
- IDR Phase 1/2 결과와의 교차 포인트를 아래 파일에서 확인 가능: reports/2026-02-23/2026-02-23-0953-TTO_IDR_KOR.md

저장 위치: /home/hodorii/dev/trading/reports/2026-02-23/
