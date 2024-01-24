from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap  # Importa Flask-Bootstra
import os
from werkzeug.utils import secure_filename
from docx import Document
from services.retriever_service import RetrieverService

app = Flask(__name__, template_folder='../app_templates', static_folder='../app_static', upload_folder='../uploads')

Bootstrap(app)  # Inizializza Flask-Bootstra

# Aggiorna il percorso della cartella dei template
app.template_folder = 'templates'

# Configura la cartella di upload
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'doc', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Assicurati che la cartella UPLOAD_FOLDER esista
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Esempio di elaborazione del documento .docx
        doc = Document(filepath)
        for paragraph in doc.paragraphs:
            print(paragraph.text)

        return 'Caricamento completato!'

    return 'Estensione del file non consentita!'

@app.route('/view_files')
def view_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('view_files.html', files=files)

@app.route('/delete_file/<filename>')
def delete_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    os.remove(file_path)
    return redirect(url_for('view_files'))
    
@app.route('/query_retriever', methods=['GET', 'POST'])
def query_retriever():
    if request.method == 'POST':
        user_query = request.form['user_query']

        # Esegui il retriever sulla query
        retriever = pipeline("question-answering", model=model_name, tokenizer=model_name)
        result = retriever({
            "question": user_query,
            "context": concatenated_text
        })

        # Mostra la risposta nella console del server
        print("Risposta alla query:", result["answer"])

        # Passa la risposta alla pagina
        return render_template('query_result.html', answer=result["answer"], user_query=user_query)

    return render_template('query_retriever.html')

if __name__ == '__main__':
    app.run(debug=True)
