#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.agent, .kiro, reports, AGENTS.md를 제외한 모든 파일과 폴더를 reports 아래로 이동
"""

import os
import shutil
from datetime import datetime
from pathlib import Path

def get_file_date_from_timestamp(filepath):
    """파일 타임스탬프에서 날짜 추출"""
    try:
        mtime = os.path.getmtime(filepath)
        dt = datetime.fromtimestamp(mtime)
        
        # 2026년 1월 범위만 처리
        if dt.year == 2026 and dt.month == 1:
            date_str = f"26{dt.month:02d}{dt.day:02d}"
            return date_str
    except:
        pass
    
    # 기본값으로 오늘 날짜 사용
    today = datetime.now()
    return f"26{today.month:02d}{today.day:02d}"

def should_exclude(item_name):
    """제외할 항목인지 확인"""
    exclude_items = {
        '.agent', '.kiro', 'reports', 'AGENTS.md',
        '.git', '.gitignore', '.vscode', 'node_modules',
        '__pycache__', '.DS_Store', 'Thumbs.db'
    }
    
    return (item_name in exclude_items or 
            item_name.startswith('.agent') or 
            item_name.startswith('.kiro') or
            item_name.endswith('.pyc'))

def main():
    """메인 함수"""
    current_dir = Path(".")
    reports_dir = Path("reports")
    
    # reports 폴더가 없으면 생성
    reports_dir.mkdir(exist_ok=True)
    
    moved_items = []
    skipped_items = []
    
    # 현재 디렉토리의 모든 항목 확인
    for item in current_dir.iterdir():
        item_name = item.name
        
        # 제외할 항목 건너뛰기
        if should_exclude(item_name):
            skipped_items.append(f"{item_name} (제외 대상)")
            continue
        
        try:
            if item.is_file():
                # 파일인 경우 - misc 폴더로 이동
                misc_dir = reports_dir / "misc"
                misc_dir.mkdir(exist_ok=True)
                
                target_path = misc_dir / item_name
                shutil.move(str(item), str(target_path))
                moved_items.append(f"파일: {item_name} -> reports/misc/")
                print(f"✓ 파일: {item_name} -> reports/misc/")
                
            elif item.is_dir():
                # 폴더인 경우 - reports 아래로 직접 이동
                target_path = reports_dir / item_name
                
                # 이미 존재하는 경우 백업 이름 생성
                if target_path.exists():
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    target_path = reports_dir / f"{item_name}_{timestamp}"
                
                shutil.move(str(item), str(target_path))
                moved_items.append(f"폴더: {item_name} -> reports/")
                print(f"✓ 폴더: {item_name} -> reports/")
                
        except Exception as e:
            skipped_items.append(f"{item_name} (이동 실패: {e})")
            print(f"✗ {item_name} 이동 실패: {e}")
    
    # 결과 출력
    print(f"\n=== 정리 완료 ===")
    print(f"이동된 항목: {len(moved_items)}개")
    print(f"건너뛴 항목: {len(skipped_items)}개")
    
    if moved_items:
        print(f"\n이동된 항목:")
        for item in moved_items:
            print(f"  - {item}")
    
    if skipped_items:
        print(f"\n건너뛴 항목:")
        for item in skipped_items:
            print(f"  - {item}")
    
    if not moved_items:
        print("\n모든 파일이 이미 정리되어 있습니다! ✨")

if __name__ == "__main__":
    main()