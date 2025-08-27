#!/bin/bash
# 중간에 오류가 발생하면 즉시 중단
set -e

echo "---- 프로젝트 최상위 폴더로 이동 ----"
# 스크립트가 있는 위치를 기준으로, 한 단계 위(LearnedFTL)로 이동
cd "$(dirname "$0")/.."

echo "---- 빌드 전용 폴더(build-femu) 생성 ----"
# 컴파일 결과물만 담을 별도의 깨끗한 폴더를 생성
BUILD_DIR="build-femu"
mkdir -p ${BUILD_DIR}

echo "---- 빌드 폴더 안에서 configure 실행 ----"
# 빌드 폴더 안으로 들어간 뒤, 상위 폴더에 있는 configure 스크립트를 실행
# 이렇게 하면 모든 빌드 관련 파일이 build-femu 폴더 안에만 생성됨
cd ${BUILD_DIR}
../configure --enable-kvm --target-list=x86_64-softmmu
# 참고: 만약 컴파일 시 warning 때문에 오류가 나면 아래 줄의 주석을 해제하고 사용
# ../configure --enable-kvm --target-list=x86_64-softmmu --disable-werror

echo "---- 사용 가능한 모든 CPU 코어를 사용하여 FEMU 컴파일 ----"
# make를 실행하여 실제 컴파일 진행. 다음부터는 변경된 부분만 빠르게 컴파일됨
make -j$(nproc)

echo ""
echo "======================================================="
echo "      FEMU 컴파일이 성공적으로 완료되었습니다!"
echo " 실행 파일 위치: $(pwd)/qemu-system-x86_64"
echo "======================================================="
