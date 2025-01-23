from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  # Dossier pour stocker les fichiers PDF

# Créer le dossier 'uploads' s'il n'existe pas
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Données de test (à remplacer plus tard par des données réelles)
tasks = [
    {"sujet": "Révision du plan QMS", "expediteur": "Jean Dupont", "date": "2023-10-01", "deadline": "2023-10-15", "pdf_filename": None},
    {"sujet": "Audit interne", "expediteur": "Marie Curie", "date": "2023-10-05", "deadline": "2023-10-20", "pdf_filename": None},
    {"sujet": "Mise à jour des procédures", "expediteur": "Paul Martin", "date": "2023-10-10", "deadline": "2023-10-25", "pdf_filename": None}
]

# Route pour la page d'accueil
@app.route("/")
def index():
    return render_template("index.html", tasks=tasks)

# Route pour la recherche
@app.route("/search", methods=["GET"])
def search():
    search_text = request.args.get("query", "").lower()
    filtered_tasks = [task for task in tasks if
                      search_text in task["sujet"].lower() or
                      search_text in task["expediteur"].lower() or
                      search_text in task["date"] or
                      search_text in task["deadline"]]
    return jsonify(filtered_tasks)

# Route pour afficher la page d'ajout de tâche
@app.route("/add-task", methods=["GET"])
def add_task_page():
    return render_template("add_task.html")

# Route pour traiter l'ajout de tâche
@app.route("/add-task", methods=["POST"])
def add_task():
    sujet = request.form.get("sujet")
    expediteur = request.form.get("expediteur")
    date = request.form.get("date")
    deadline = request.form.get("deadline")
    pdf_file = request.files.get("pdf_file")

    # Gérer le fichier PDF
    pdf_filename = None
    if pdf_file and pdf_file.filename.endswith('.pdf'):
        pdf_filename = pdf_file.filename
        pdf_file.save(os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename))

    # Ajouter la nouvelle tâche à la liste
    tasks.append({
        "sujet": sujet,
        "expediteur": expediteur,
        "date": date,
        "deadline": deadline,
        "pdf_filename": pdf_filename
    })

    # Rediriger vers la page d'accueil
    return redirect(url_for("index"))

# Route pour télécharger un fichier PDF
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run(debug=True)