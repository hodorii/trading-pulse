#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
날짜 형식이 아닌 폴더들의 파일명을 YYMMDD_HHmm 형식으로 표준화
"""

import os
import re
from datetime import datetime
from pathlib import Path

def extract_date_time_from_filename(filename):
    """파일명에서 날짜와 시간 추출"""
    # 202601DDHHNN 형태 찾기
    pattern1 = r'202601(\d{2})(\d{2})(\d{2})'
    match1 = re.search(pattern1, filename)
    if match1:
        day, hour, minute = match1.groups()
        return f"2601{day}", f"{hour}{minute}"
    
    # 20260121 형태 찾기 (시간 없음)
    pattern2 = r'20260(\d{2})(\d{2})'
    match2 = re.search(pattern2, filename)
    if match2:
        month, day = match2.groups()
        return f"26{month}{day}", "0000"
    
    return None, None

def get_file_timestamp(filepath):
    """파일 타임스탬프에서 날짜/시간 추출"""
    try:
        mtime = os.path.getmtime(filepath)
        dt = datetime.fromtimestamp(mtime)
        
        # 2026년 1월 19-21일 범위만 처리
        if dt.year == 2026 and dt.month == 1 and dt.day in [19, 20, 21]:
            date_str = f"26{dt.month:02d}{dt.day:02d}"
            time_str = f"{dt.hour:02d}{dt.minute:02d}"
            return date_str, time_str
    except:
        pass
    
    return None, None

def extract_tag_from_filename(filename):
    """파일명에서 태그 추출"""
    # 기존 태그가 있는 경우
    tag_match = re.search(r'\[([^\]]+)\]', filename)
    if tag_match:
        return tag_match.group(1)
    
    # 파일명 패턴으로 태그 추정
    if '최종의사결정' in filename or '최종결정' in filename:
        return '결정'
    elif '펀더멘털분석' in filename or '펀더멘털' in filename:
        return '가치'
    elif '세력분석' in filename or '투자자' in filename:
        return '수급'
    elif '리스크전략' in filename or '리스크분석' in filename:
        return '리스크'
    elif '이벤트드리븐' in filename or '이벤트분석' in filename:
        return '이벤트'
    elif '마켓' in filename or '시장' in filename:
        return '시장'
    elif '매매복기' in filename or '복기' in filename:
        return '복기'
    elif '시뮬레이션' in filename:
        return '시뮬'
    elif '워크플로' in filename:
        return '워크플로'
    else:
        return '분석'

def extract_stock_name(filename):
    """파일명에서 종목명 추출"""
    # 종목명 패턴들
    stocks = [
        '삼성전자', '삼성바이오로직스', '현대자동차', '현대차', '현대위아', '현대로템',
        '한화', '한화시스템', '포스코홀딩스', '포스코인터내셔널', 
        '삼천당제약', '삼현', '우진', '우리기술', '에스피지', '에스오에스랩',
        '두산에너빌리티', '두산밥캣', '한라캐스트', '레인보우로보틱스', '이랜시스'
    ]
    
    for stock in stocks:
        if stock in filename:
            return stock
    
    # 전체 관련 키워드
    if '전체' in filename or 'global' in filename.lower():
        return '전체'
    
    return '기타'

def create_new_filename(date_str, time_str, tag, stock_name, original_name):
    """새로운 파일명 생성"""
    # 기존 확장자 유지
    if original_name.endswith('.md'):
        ext = '.md'
        base_name = original_name[:-3]
    else:
        ext = ''
        base_name = original_name
    
    # 설명 추출
    if '최종의사결정' in base_name:
        description = '최종의사결정'
    elif '펀더멘털분석' in base_name:
        description = '펀더멘털분석'
    elif '세력분석' in base_name:
        description = '세력분석'
    elif '리스크전략' in base_name:
        description = '리스크전략'
    elif '이벤트드리븐' in base_name:
        description = '이벤트드리븐'
    elif '매매복기' in base_name:
        description = '매매복기'
    elif '시뮬레이션' in base_name:
        description = '시뮬레이션'
    elif '워크플로' in base_name:
        description = '워크플로분석'
    elif 'report' in base_name.lower():
        description = '보고서'
    else:
        description = '분석보고서'
    
    return f"{date_str}_{time_str}_[{tag}]_{stock_name}_{description}{ext}"

def process_folder(folder_path):
    """폴더 내 파일들 처리"""
    processed_files = []
    skipped_files = []
    
    print(f"\n📁 {folder_path.name} 폴더 처리 중...")
    
    for file_path in folder_path.iterdir():
        if not file_path.is_file():
            continue
            
        filename = file_path.name
        
        # 이미 표준화된 파일명인지 확인
        if re.match(r'26\d{4}_\d{4}_\[.+\]_.+', filename):
            skipped_files.append(f"{filename} (이미 표준화됨)")
            continue
        
        # 날짜/시간 추출 (파일명 우선, 없으면 타임스탬프)
        date_str, time_str = extract_date_time_from_filename(filename)
        if not date_str:
            date_str, time_str = get_file_timestamp(file_path)
        
        if not date_str:
            skipped_files.append(f"{filename} (날짜 추출 실패)")
            continue
        
        # 태그와 종목명 추출
        tag = extract_tag_from_filename(filename)
        stock_name = extract_stock_name(filename)
        
        # 새 파일명 생성
        new_filename = create_new_filename(date_str, time_str, tag, stock_name, filename)
        new_path = file_path.parent / new_filename
        
        # 파일명 변경
        try:
            file_path.rename(new_path)
            processed_files.append(f"{filename} -> {new_filename}")
            print(f"  ✓ {filename} -> {new_filename}")
        except Exception as e:
            skipped_files.append(f"{filename} (변경 실패: {e})")
            print(f"  ✗ {filename} 변경 실패: {e}")
    
    return processed_files, skipped_files

def main():
    """메인 함수"""
    reports_dir = Path("reports")
    
    if not reports_dir.exists():
        print("reports 폴더가 존재하지 않습니다.")
        return
    
    # 처리할 폴더들 (날짜 형식과 misc 제외)
    folders_to_process = []
    date_pattern = re.compile(r'^26\d{4}$')  # 260119, 260120, 260121 등
    
    for item in reports_dir.iterdir():
        if (item.is_dir() and 
            not date_pattern.match(item.name) and 
            item.name != 'misc'):
            folders_to_process.append(item)
    
    if not folders_to_process:
        print("처리할 폴더가 없습니다.")
        return
    
    total_processed = 0
    total_skipped = 0
    
    # 각 폴더 처리
    for folder in folders_to_process:
        processed, skipped = process_folder(folder)
        total_processed += len(processed)
        total_skipped += len(skipped)
    
    # 결과 출력
    print(f"\n=== 파일명 표준화 완료 ===")
    print(f"처리된 파일: {total_processed}개")
    print(f"건너뛴 파일: {total_skipped}개")
    print(f"처리된 폴더: {len(folders_to_process)}개")

if __name__ == "__main__":
    main()