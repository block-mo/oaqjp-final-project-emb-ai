''' Defining emotion detector function for finding
    emotions based on user text inputs.
'''
import json
import re       # Import re i.e. regular expression module
import requests

def emotion_detector(text_to_analyse):
    '''
    Detect the emotions present in the given text.

    Args:
        text_to_analyse (str): The text to analyze for emotions.
    '''
    # Api url and header
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    header = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}

    # Handling blank input and invalid characters (numbers and symbols)
    if not text_to_analyse.strip() or not re.match("^[a-zA-Z\s]+$", text_to_analyse):
        return {"anger": None, "disgust": None, "fear": None, "joy": None, "sadness": None, "dominant_emotion": None}

    # Payload for the api request
    payload = {"raw_document": {"text": text_to_analyse}}

    try:
        # Sending post request and parsing the response
        response = requests.post(url, json=payload, headers=header, timeout=5)
        # Check if the response status code is 400
        if response.status_code == 400:
            return {"anger": None, "disgust": None, "fear": None, "joy": None, "sadness": None, "dominant_emotion": None}
        formatted_response = json.loads(response.text)
        # Extracting emotions from the response
        emotions = formatted_response.get("emotionPredictions", [{}])[0].get("emotion", {})
        # Extract relevant emotions
        scores = {emotion: emotions.get(emotion, 0) for emotion in ["anger", "disgust", "fear", "joy", "sadness"]}
        # Find the dominant emotion
        scores["dominant_emotion"] = max(scores, key=scores.get)
        return scores
    except Exception as e:
        # Return None for all emotions in case of any exception
        return {"anger": None, "disgust": None, "fear": None, "joy": None, "sadness": None, "dominant_emotion": None}
