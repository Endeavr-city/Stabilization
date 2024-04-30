import cv2
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator, colors

model = YOLO("bestv2_1_coco.pt")  # segmentation model
cap = cv2.VideoCapture("./4_21_2024/bothStable_roughest.avi")
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

out = cv2.VideoWriter('./masks/bothStable_roughest_maskv2.avi', cv2.VideoWriter_fourcc(*'XVID'), fps, (w, h))

while True:
    ret, im0 = cap.read()
    if not ret:
        print("Video frame is empty or video processing has been successfully completed.")
        break
        
    results = model.predict(im0, conf=0.6)
    annotated_frame = results[0].plot(boxes=True)

    out.write(annotated_frame)
    cv2.imshow("instance-segmentation", annotated_frame)

    cv2.waitKey(1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

out.release()
cap.release()
cv2.destroyAllWindows()