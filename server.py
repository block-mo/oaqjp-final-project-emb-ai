''' Executing this function initiates the application of emotion 
    detection to be executed over the Flask channel and deployed on
    localhost:5000.
'''
# Import Flask, render_template, request from the flask framework package
# Import the emotion_detector function from the package created
from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

app = Flask("Emotion Detection")

@app.route("/emotionDetector")
def emotion_detector_route():
    '''
    Analyze the user-provided text for emotions and return the result.

    Returns:
        str: A formatted string containing the emotion scores and the dominant emotion.
    '''
    text_to_detect = request.args.get('textToAnalyze')
    response = emotion_detector(text_to_detect)
    if response['dominant_emotion'] is None:
        return "Invalid text! Please try again!"

    formated_response = response

    return (
        f"For the given statement, the system response is 'anger': {formated_response['anger']} "
        f"'disgust': {formated_response['disgust']}, 'fear': {formated_response['fear']}, "
        f"'joy': {formated_response['joy']} and 'sadness': {formated_response['sadness']}. "
        f"The dominant emotion is {formated_response['dominant_emotion']}."
    )

# Home route to render the HTML page
@app.route("/")
def index():
    '''
    Render the home page.

    Returns:
        str: The rendered HTML page.
    '''
    return render_template('index.html')

# Run the Flask app
if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
