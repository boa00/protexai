from pydantic import BaseModel

class SharedConfig(BaseModel):
    raw_data_path: str = "annotations.json"
    ragions_of_interest_data_path: str = "rois.json"
    figsize_widht: float = 19.2
    figsize_height: float = 10.8
    dpi: int = 100
    color_schema: dict[str, str] = {
        "car": "red",
        "truck": "blue",
        "person": "green",
        "roi": "purple"
    }
    frame_path: str = "./frames"
    video_codec: str = "mp4v"
    video_path: str = "./videos/video_recording.mp4"
    fps: int = 5
    not_allowed_together: set[str] = {"car", "person"}
    slack_post_uri: str = "https://slack.com/api/chat.postMessage"
    rule_name: str = "a Person and a Car cannot be together in the given area"