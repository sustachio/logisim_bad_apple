import cv2

path = "./badapple.mp4"

sample_fps = 2

def downscale_to_array():
    vid = cv2.VideoCapture(path)
    if not vid.isOpened():
        print("cant open ):")
        return []

    fps = vid.get(cv2.CAP_PROP_FPS)
    interval = int(fps / sample_fps)

    frames = []
    i = 0

    while True:
        ret, frame = vid.read()
        if not ret:
            break

        if i % interval == 0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            small = cv2.resize(gray, (12, 9), interpolation=cv2.INTER_AREA)
            _, thresh = cv2.threshold(small, 128, 1, cv2.THRESH_BINARY)

            frames.append(thresh.tolist())

        i += 1

    vid.release()
    return frames

print(len(downscale_to_array()))
