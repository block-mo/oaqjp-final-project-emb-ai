import requests
import json

def emotion_detector(text_to_analyse):
    # Api url and header
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    header = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}

    # Payload for the api request
    payload = { "raw_document": { "text": text_to_analyse } }

    # Sending post request and parsing the response
    response = requests.post(url, json = payload, headers=header)
    formatted_response = json.loads(response.text)
    
    
    # Extracting emotions from the response
    emotions = formatted_response.get("emotionPredictions", [{}])[0].get("emotion", {})

    # Extract relevant emotions
    scores = {emotion: emotions.get(emotion, 0) for emotion in ["anger", "disgust", "fear", "joy", "sadness"]}

    # Find the dominant emotion
    scores["dominant_emotion"] = max(scores, key=scores.get)

    return scores