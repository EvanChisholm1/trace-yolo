from inference import get_model
import supervision as sv
from inference.core.utils.image_utils import load_image_bgr
import cv2
import os
import json

images = os.listdir('./imgs')

i = 0

most_recent_p = None

posns = []

model = get_model(model_id="yolov8n-640")
for img in images:
    i += 1
    print(i)
    image = f'./imgs/{img}'
    image = load_image_bgr(image)

    results = model.infer(image)[0]
    # print(results.predictions)
    results.predictions = [p for p in results.predictions if p.class_name == "person" ]
    if len(results.predictions) > 0 and results.predictions[0]:
        pred = results.predictions[0]
        most_recent_p = pred
        print(pred.x)
        posns.append({'x': pred.x, 'width': pred.width})
    results = sv.Detections.from_inference(results)
    # print(results[0])
    # results = results.filter(results.class_id == 0)
    annotator = sv.BoxAnnotator(thickness=4)
    annotated_image = annotator.annotate(image, results)
    annotator = sv.LabelAnnotator(text_scale=2, text_thickness=2)
    annotated_image = annotator.annotate(annotated_image, results)
    # sv.plot_image(annotated_image)
    cv2.imwrite(f"./out/{img}", annotated_image)


json.dump(posns, open('posns.json', 'w'))

# image = './test1.png'