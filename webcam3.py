import cv2 as cv

# 1. 카메라 설정
video = cv.VideoCapture(0)
target_format = 'avi'
target_fourcc = 'XVID'
is_recording = False

# 2. 초기 데이터 및 FPS 설정
fps = 20.0 
wait_msec = int(1 / fps * 1000)

valid, img = video.read()
if not valid: exit()

h, w, *_ = img.shape
is_color = (img.ndim > 2) and (img.shape[2] > 1)

# 크롭 좌표 미리 계산 (중앙 1/3 지점)
one_third_w = w // 3
start_x = (w // 2) - (one_third_w // 2)
end_x = start_x + one_third_w

# VideoWriter 설정
target_file = 'webcam_split.' + target_format
target = cv.VideoWriter()
target.open(target_file, cv.VideoWriter_fourcc(*target_fourcc), fps, (w, h), is_color)

while True:
    valid, img = video.read()
    if not valid: break
    
    if is_recording:
        # --- [녹화 중: 3분할 모드] ---
        cropped = img[0:h, start_x:end_x]
        mirror = cv.flip(cropped, 1) # 양옆은 반전해서 방송 느낌 극대화
        
        # 3분할 합치기 (좌반전 | 본래 | 우반전)
        display_img = cv.hconcat([mirror, cropped, mirror])
        display_img = cv.resize(display_img, (w, h)) 
        
        # 파일 저장
        if target is not None:
            target.write(display_img)
            
        # UI 표시 (빨간색)
        cv.circle(display_img, (30, 30), 10, (0, 0, 255), -1)
        cv.putText(display_img, "REC (3-SPLIT)", (50, 40), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    else:
        # --- [대기 중: 일반 화면 모드] ---
        display_img = img # 원본 그대로 사용
        
        # UI 표시 (연두색)
        cv.circle(display_img, (30, 30), 10, (0, 255, 0), -1)
        cv.putText(display_img, "PREVIEW (NORMAL)", (50, 40), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv.imshow('Dynamic Recording Mode', display_img)
    
    key = cv.waitKey(wait_msec) & 0xFF
    if key == 32: # Spacebar
        is_recording = not is_recording
        print(f"모드 전환: {'녹화 중(3분할)' if is_recording else '대기 중(일반)'}")
    elif key == 27: # ESC
        break

video.release()
if target is not None: target.release()
cv.destroyAllWindows()