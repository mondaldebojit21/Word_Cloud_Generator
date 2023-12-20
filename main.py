from flask import Flask, request, render_template, jsonify
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

# Function to generate word cloud
def generate_wordcloud(text, stopwords=None, max_font_size=120, max_words=100,stopwords_option='exclude'):

    stopwords=stopwords.lower().split(',')

    if stopwords_option=='include':
        eng_stopwords = set(STOPWORDS)
        stopwords.extend(eng_stopwords)   
    
    wordcloud = WordCloud(stopwords=stopwords, max_font_size=max_font_size, max_words=max_words).generate(text.lower())

    # wordcloud = WordCloud(stopwords=stopwords, max_font_size=max_font_size, max_words=max_words, background_color="rgba(255, 255, 255, 0)", mode="RGBA").generate(text.lower())



    # plt.figure(figsize=(6, 20))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')

    # Save the word cloud image to a BytesIO object
    img = BytesIO()
    plt.savefig(img, format='png',bbox_inches='tight', facecolor='k')

    img.seek(0)
    plt.close()

    # Encode the image to base64 for HTML display
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    return img_base64

# Route to render the HTML form
@app.route('/')
def index():
    return render_template('index.html')

# Route to generate word cloud
@app.route('/generate_wordcloud', methods=['POST'])
def generate_wordcloud_route():
    text = request.form['text']
    stopwords = request.form.get('stopwords')

    stopwords_option = request.form.get('stopwords_option')

    if request.form.get('max_font_size').strip()=='':
        max_font_size = 80
    else:
        max_font_size = int(request.form.get('max_font_size'))

    if request.form.get('max_font_size').strip()=='':
        max_font_size = 80
    else:
        max_font_size = int(request.form.get('max_font_size'))
    
    if request.form.get('max_words').strip()=='':
        max_words = 80
    else:
        max_words = int(request.form.get('max_words'))


    if not text:
        return jsonify({'message': 'No text input provided'})

    wordcloud_image = generate_wordcloud(text, stopwords, max_font_size, max_words,stopwords_option)

    return jsonify({'image': wordcloud_image})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int('3000'))
