from ultralytics import YOLO
import torch
torch.cuda.empty_cache()

if __name__ == '__main__':
    model = YOLO('yolov8n-seg.pt')
    model.to('cuda')
    model.train(data='data.yaml', epochs=15, imgsz=640, batch=32, workers=4)