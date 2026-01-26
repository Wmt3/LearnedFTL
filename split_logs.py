import re
import os

# 호스트에서 tee 명령어로 저장했던 로그 파일명
INPUT_LOG = "mapping.log" 

def split_log_file():
    current_trace = None
    f_out = None
    
    if not os.path.exists(INPUT_LOG):
        print(f"Error: {INPUT_LOG} 파일을 찾을 수 없습니다.")
        return

    print(f"Reading {INPUT_LOG} and splitting...")
    
    with open(INPUT_LOG, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            
            # 1. 시작 마커 감지 (MARKER_START_TRACE_hm_0 등)
            if "MARKER_START_TRACE_" in line:
                match = re.search(r"MARKER_START_TRACE_(\w+)", line)
                if match:
                    if f_out: f_out.close()
                    
                    trace_name = match.group(1)
                    current_trace = trace_name
                    filename = f"ftl_log_{trace_name}.txt"
                    
                    f_out = open(filename, 'w')
                    print(f"  -> Found Marker: Generating {filename}")
                    continue

            # 2. 종료 마커 감지
            if "MARKER_END_TRACE_" in line:
                if f_out:
                    f_out.close()
                    f_out = None
                    current_trace = None
                continue

            # 3. 내용 저장 (수정된 부분!)
            if f_out and current_trace:
                # 사용자 로그 포맷: [TRACE] WRITE, 2210941, ...
                # "[TRACE]"가 포함된 줄만 골라서 저장합니다.
                if "[TRACE]" in line:
                    f_out.write(line + "\n")

    if f_out: f_out.close()
    print("Done splitting.")

if __name__ == "__main__":
    split_log_file()
