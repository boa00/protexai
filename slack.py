import requests
import os

def post_message_to_slack(URI: str, timestamp: str, rule_name: str, camera_name: str) -> requests.Response:
    text = f"""
    The rule has been violated \n
    *Timestamp*: {timestamp} \n
    *Rule name*: {rule_name} \n
    *Camera name*: {camera_name}
    """
    response = requests.post(URI, {
        'token': os.environ["slack_token"],
        'channel': os.environ["slack_channel_id"],
        'username': os.environ["slack_user_name"],
        'text': text,
    })
    return response
