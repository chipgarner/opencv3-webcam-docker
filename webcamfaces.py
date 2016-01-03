import cv2

video_capture = cv2.VideoCapture(0)
if not video_capture.isOpened():
    print('No video camera found')
    exit()

# Uncomment the "..FULLSCREEN" calls and comment out "..AUTOSIZE" to display full screen
# Mouse click on the screen and hit q to exit
# cv2.namedWindow("Video", cv2.WND_PROP_FULLSCREEN)
# cv2.setWindowProperty("Video", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.namedWindow("Video", cv2.WND_PROP_AUTOSIZE)
cv2.setWindowProperty("Video", cv2.WND_PROP_AUTOSIZE, cv2.WINDOW_AUTOSIZE)

print("OpenCV version :  {0}".format(cv2.__version__))

t = cv2.getTickCount()
t_count = 0.0
t_sum = 0.0


faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


def get_faces(frm):
    # Gray scale image for the face detector, shrink it to make it faster
    gray = cv2.cvtColor(frm, cv2.COLOR_BGR2GRAY)
    image_scale = 3
    scl = 1.0 / image_scale
    smallgray = cv2.resize(gray, (0, 0), fx=scl, fy=scl)
    faces = faceCascade.detectMultiScale(
        smallgray,
        scaleFactor=1.1,
        minNeighbors=3,
        minSize=(10, 10),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    # Draw andy face rectangles on the full size image
    for (x, y, w, h) in faces:
        x1 = int(x * image_scale)
        x2 = int((x + w) * image_scale)
        y1 = int(y * image_scale)
        y2 = int((y + h) * image_scale)
        cv2.rectangle(frm, (x1, y1), (x2, y2), (0, 0, 255), 2)

    return frm

while True:

    t = cv2.getTickCount()
    t_count += 1.0

    # Capture frame-by-frame
    ret, frame = video_capture.read()

    cv2.imshow('Video', get_faces(frame))

    # Calculate and print the frame rate every 10 frames.
    t_sum += cv2.getTickFrequency() / (cv2.getTickCount() - t)
    if t_count > 9:
        print(t_sum / t_count)
        t_count = 0.0
        t_sum = 0.0

    # OpenCV won't display anything until it hits the waitkey() function.
    # Press q to exit the program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When finished release the capture and window
video_capture.release()
cv2.destroyAllWindows()
