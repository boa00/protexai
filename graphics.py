import os

import cv2
from shapely.geometry import Polygon
import matplotlib.pyplot as plt

from utils import get_object_coordinates
from slack import post_message_to_slack


def create_frame(frame, rois: dict[str, list[list[int]]], cam_name: str, conf) -> None:
    objects = frame["detections"]
    W, H = frame["frame_width"], frame["frame_height"]

    plt.figure(figsize=(conf.figsize_widht, conf.figsize_height), dpi=conf.dpi, facecolor="black")
    plt.xlim(0, W)
    plt.ylim(0, H)
    plt.axis('off')

    roi_polygons = dict()
    for roi, coordinates in rois.items():
        roi_polygon = Polygon(coordinates)
        roi_polygons[roi] = {
            "polygon": roi_polygon, "objects_inside": set()
        }
        plt.plot(*roi_polygon.exterior.xy, color=conf.color_schema["roi"])
    

    for object in objects:
        bbox = object["bbox"]
        object_class = object["class"]
        object_coordinates = get_object_coordinates(bbox, W, H)
        polygon = Polygon(object_coordinates)
        plt.plot(*polygon.exterior.xy, color=conf.color_schema[object_class])

        for roi, roi_info in roi_polygons.items():
            roi_polygon = roi_info["polygon"]
            if polygon.intersects(roi_polygon): 
                roi_info["objects_inside"].add(object_class)
            
    for roi, roi_info in roi_polygons.items():
        if conf.not_allowed_together.issubset(roi_info["objects_inside"]):
            plt.plot(*roi_info["polygon"].exterior.xy, color="white")
            post_message_to_slack(
                URI=conf.slack_post_uri,
                timestamp=frame["timestamp"],
                rule_name=conf.rule_name,
                camera_name=cam_name,
            )

    plt.savefig(f'{conf.frame_path}/frame_{frame["timestamp"]}.png', bbox_inches='tight')

def record_video(frame_path: str, video_path: str, video_codec: str, fps: int) -> None:
    fourcc = cv2.VideoWriter_fourcc(*video_codec)
    images = [img for img in os.listdir(frame_path)]
    image_example = cv2.imread(os.path.join(frame_path, images[0]))
    h, w, _ = image_example.shape
    video = cv2.VideoWriter(video_path, fourcc, fps, (w, h))
    for image in images:
        image_path = os.path.join(frame_path, image)
        video.write(cv2.imread(image_path))
        os.remove(image_path)
    cv2.destroyAllWindows()
    video.release()