#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
테마별 폴더의 파일들을 날짜별 폴더로 이동
"""

import re
import shutil
from pathlib import Path

def extract_date_from_filename(filename):
    """파일명에서 날짜 추출 (YYMMDD 형식)"""
    # 260119, 260120, 260121 형태 찾기
    pattern = r'^(26\d{4})_'
    match = re.match(pattern, filename)
    if match:
        return match.group(1)
    return None

def main():
    """메인 함수"""
    reports_dir = Path("reports")
    
    if not reports_dir.exists():
        print("reports 폴더가 존재하지 않습니다.")
        return
    
    # 이동할 폴더들
    folders_to_process = [
        'final_decision',
        'fundamental', 
        'investor_flow',
        'macro-event',
        'macro_event',
        'market_scan',
        'risk_strategy',
        'sessions'
    ]
    
    # 날짜별 폴더 생성 (필요시)
    date_folders = ['260119', '260120', '260121']
    for date_folder in date_folders:
        (reports_dir / date_folder).mkdir(exist_ok=True)
    
    total_moved = 0
    total_skipped = 0
    
    # 각 테마 폴더 처리
    for folder_name in folders_to_process:
        folder_path = reports_dir / folder_name
        
        if not folder_path.exists() or not folder_path.is_dir():
            print(f"⚠️ {folder_name} 폴더가 존재하지 않습니다.")
            continue
        
        print(f"\n📁 {folder_name} 폴더 처리 중...")
        moved_count = 0
        skipped_count = 0
        
        # 폴더 내 모든 파일 처리
        for file_path in folder_path.iterdir():
            if not file_path.is_file():
                continue
            
            filename = file_path.name
            
            # 파일명에서 날짜 추출
            date_str = extract_date_from_filename(filename)
            
            if not date_str:
                print(f"  ⚠️ {filename} - 날짜 추출 실패")
                skipped_count += 1
                continue
            
            # 대상 폴더 확인
            target_dir = reports_dir / date_str
            if not target_dir.exists():
                print(f"  ⚠️ {filename} - {date_str} 폴더가 존재하지 않음")
                skipped_count += 1
                continue
            
            # 파일 이동
            target_path = target_dir / filename
            
            # 동일한 파일명이 이미 존재하는 경우 처리
            if target_path.exists():
                # 원본 폴더명을 접미사로 추가
                name_parts = filename.rsplit('.', 1)
                if len(name_parts) == 2:
                    new_filename = f"{name_parts[0]}_{folder_name}.{name_parts[1]}"
                else:
                    new_filename = f"{filename}_{folder_name}"
                target_path = target_dir / new_filename
            
            try:
                shutil.move(str(file_path), str(target_path))
                print(f"  ✓ {filename} -> {date_str}/")
                moved_count += 1
            except Exception as e:
                print(f"  ✗ {filename} 이동 실패: {e}")
                skipped_count += 1
        
        total_moved += moved_count
        total_skipped += skipped_count
        
        # 빈 폴더인지 확인하고 삭제
        try:
            if not any(folder_path.iterdir()):
                folder_path.rmdir()
                print(f"  🗑️ 빈 폴더 {folder_name} 삭제됨")
            else:
                print(f"  📁 {folder_name} 폴더에 남은 파일이 있습니다.")
        except Exception as e:
            print(f"  ⚠️ {folder_name} 폴더 삭제 실패: {e}")
    
    # 결과 출력
    print(f"\n=== 파일 이동 완료 ===")
    print(f"이동된 파일: {total_moved}개")
    print(f"건너뛴 파일: {total_skipped}개")
    
    # 최종 날짜별 폴더 파일 수 확인
    print(f"\n📊 날짜별 폴더 현황:")
    for date_folder in date_folders:
        date_path = reports_dir / date_folder
        if date_path.exists():
            file_count = len([f for f in date_path.iterdir() if f.is_file()])
            print(f"  📂 {date_folder}: {file_count}개 파일")

if __name__ == "__main__":
    main()