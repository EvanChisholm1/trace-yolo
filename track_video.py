from inference import get_model
import supervision as sv
from inference.core.utils.image_utils import load_image_bgr
import cv2
import os

images = os.listdir('./imgs')

i = 0

model = get_model(model_id="yolov8n-640")
for img in images:
    i += 1
    print(i)
    image = f'./imgs/{img}'
    image = load_image_bgr(image)

    results = model.infer(image)[0]
    results = sv.Detections.from_inference(results)
    print(results)
    annotator = sv.BoxAnnotator(thickness=4)
    annotated_image = annotator.annotate(image, results)
    annotator = sv.LabelAnnotator(text_scale=2, text_thickness=2)
    annotated_image = annotator.annotate(annotated_image, results)
    # sv.plot_image(annotated_image)
    cv2.imwrite(f"./out/{img}", annotated_image)


# image = './test1.png'