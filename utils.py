import json

def read_json_data(file_path: str):
    f = open(file_path)
    data = json.load(f)
    f.close()
    return data

def get_object_coordinates(bbox: dict[str, float], W: int, H: int) -> list[tuple[float, float]]:
    x, y = bbox["left"]*W, bbox["top"]*H
    width, height = bbox["width"]*W, bbox["height"]*H
    top_left = (x, y)
    bottom_left = (x, y-height)
    top_right = (x+width, y)
    bottom_right = (x+width, y-height)
    return [bottom_left, top_left, bottom_right, top_right]