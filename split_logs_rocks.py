import re
import os

INPUT_LOG = "rocks_mapping.log" 

def split_log_file():
    current_trace = None
    f_out = None
    
    if not os.path.exists(INPUT_LOG):
        print(f"Error: {INPUT_LOG} not found.")
        return

    print(f"Reading {INPUT_LOG} and splitting RocksDB traces...")
    
    with open(INPUT_LOG, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            
            # 1. 시작 마커 감지 (MARKER_START_TRACE_rocks_ssdtrace-00)
            if "MARKER_START_TRACE_" in line:
                match = re.search(r"MARKER_START_TRACE_(rocks_[\w-]+)", line)
                if match:
                    if f_out: f_out.close()
                    
                    trace_name = match.group(1)
                    current_trace = trace_name
                    # 파일명: ftl_log_rocks_ssdtrace-00.txt
                    filename = f"ftl_log_{trace_name}.txt"
                    
                    f_out = open(filename, 'w')
                    print(f"  -> Generating: {filename}")
                    continue

            # 2. 종료 마커 감지
            if "MARKER_END_TRACE_" in line:
                if f_out:
                    f_out.close()
                    f_out = None
                    current_trace = None
                continue

            # 3. 내용 저장
            if f_out and current_trace:
                if "[TRACE]" in line:  # 혹은 필요한 필터링 조건
                    f_out.write(line + "\n")

    if f_out: f_out.close()
    print("Done splitting.")

if __name__ == "__main__":
    split_log_file()
