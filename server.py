"""Server module for deploying the emotion detection web application."""

from flask import Flask, request, jsonify, render_template
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)

@app.route('/')
def index():
    """Render the homepage."""
    return render_template('index.html')

@app.route('/emotionDetector', methods=['POST'])
def detect_emotion():
    """
    Endpoint to detect emotion in the provided text.

    Receives JSON input with a "text" field, processes it with the emotion_detector, 
    and returns the detected emotions or an error message if input is blank.
    """
    text = request.json.get("text", "")
    result, status_code = emotion_detector(text)

    if status_code == 400:
        return jsonify(message="Invalid text! Please try again!", data=result), 400
    return jsonify(data=result), 200

def emotion_detector_endpoint():
    """
    Alternative endpoint function to detect emotions in the text provided in the request.

    Returns a formatted msg with emotions if successful, or  error if no text.
    """
    text_to_analyse = request.json.get('text')

    if text_to_analyse:
        result = emotion_detector(text_to_analyse)
        if 'error' not in result:
            response_message = (
                f"For the given statement, the system response is "
                f"'anger': {result['anger']}, 'disgust': {result['disgust']}, "
                f"'fear': {result['fear']}, 'joy': {result['joy']} and "
                f"'sadness': {result['sadness']}. The dominant is {result['dominant_emotion']}."
            )
            return jsonify({'response': response_message}), 200
        return jsonify({'error': result['error']}), 400

    return jsonify({'error': 'No text provided'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
