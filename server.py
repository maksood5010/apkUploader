from flask import Flask, request, send_from_directory, render_template_string
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

HTML = """
<!DOCTYPE html>
<html>
<head><title>APK Uploader</title></head>
<body style="font-family:sans-serif; text-align:center; padding:40px;">
  <h2>Upload APK</h2>
  <form method="post" enctype="multipart/form-data">
    <input type="file" name="file" accept=".apk" required><br><br>
    <button type="submit">Upload</button>
  </form>
  {% if link %}
  <p>✅ Uploaded! Download link:</p>
  <a href="{{ link }}">{{ link }}</a>
  {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    link = None
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            link = f"http://{request.host}/download/{filename}"
    return render_template_string(HTML, link=link)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
