import cv2 as cv

# 1. 카메라 설정
video = cv.VideoCapture(0)
target_format = 'avi'
target_fourcc = 'XVID'
is_recording = False

# 2. 초기 데이터 추출
fps = video.get(cv.CAP_PROP_FPS)
if fps <= 0: fps = 20.0

valid, img = video.read()
if not valid:
    print("프레임을 읽을 수 없습니다.")
    exit()

h, w, *_ = img.shape
is_color = (img.ndim > 2) and (img.shape[2] > 1)

# 3. VideoWriter 설정 (파일을 미리 열어둠)
target_file = 'webcam.' + target_format
target = cv.VideoWriter()
target.open(target_file, cv.VideoWriter_fourcc(*target_fourcc), fps, (w, h), is_color)

if video.isOpened():    
    wait_msec = int(1 / fps * 1000)
    
    while True:
        valid, img = video.read()
        if not valid:
            break
        
        # --- 상태별 처리 ---
        if is_recording:
            # 녹화 중일 때만 파일에 저장
            if target is not None:
                target.write(img)
            
            # 녹화 중 표시 (빨간색)
            cv.circle(img, (30, 30), 10, (0, 0, 255), -1)
            cv.putText(img, "REC", (50, 40), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        else:
            # 대기 중 표시 (연두색)
            cv.circle(img, (30, 30), 10, (0, 255, 0), -1)
            cv.putText(img, "PREVIEW", (50, 40), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv.imshow('Video Player', img)
        
        key = cv.waitKey(wait_msec) & 0xFF
        
        if key == 32:  # Spacebar 누름
            is_recording = not is_recording  # 상태 반전
            state_msg = "녹화 시작" if is_recording else "녹화 일시중지"
            print(state_msg)
            
        elif key == 27:  # ESC 누르면 종료
            break

    # 4. 자원 해제 (루프가 끝나면 한 번만 닫음)
    video.release()
    if target is not None:
        target.release()
    cv.destroyAllWindows()