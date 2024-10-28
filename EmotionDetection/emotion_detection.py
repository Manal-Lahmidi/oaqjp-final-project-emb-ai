import requests

def emotion_detector(text_to_analyse):
    
    if not text.strip():  # Check for blank entries
        return {
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None
        }, 400  # Set status code to 400 for blank entries

    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
    }
    data = {
        "raw_document": {"text": text_to_analyse}
    }
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        # Access the first emotion prediction
        emotion_predictions = response.json()['emotionPredictions']
        if emotion_predictions:
            emotions = emotion_predictions[0]['emotion']
            # Extract individual emotions
            scores = {
                'anger': emotions['anger'],
                'disgust': emotions['disgust'],
                'fear': emotions['fear'],
                'joy': emotions['joy'],
                'sadness': emotions['sadness'],
            }
            # Find the dominant emotion
            dominant_emotion = max(scores, key=scores.get)
            scores['dominant_emotion'] = dominant_emotion
            return scores
        else:
            return {"error": "No emotion predictions found"}
    else:
        return {"error": "API request failed with status code " + str(response.status_code)}
