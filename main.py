from config import SharedConfig
from utils import read_json_data
from graphics import create_frame, record_video


def main() -> None:
    conf = SharedConfig()
    rois = read_json_data(file_path=conf.ragions_of_interest_data_path)
    data = read_json_data(file_path=conf.raw_data_path)
    cam_name, frames = data["cam_name"], data["frames"]
    for frame in frames:
        create_frame(
            frame=frame,
            rois=rois,
            cam_name=cam_name,
            conf=conf
        )

    record_video(
        frame_path=conf.frame_path,
        video_path=conf.video_path,
        video_codec=conf.video_codec,
        fps=conf.fps
    )

if __name__ == "__main__":
    main()

