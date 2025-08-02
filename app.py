from flask import Flask, render_template, request
from ml_recommender import get_top_recommendations

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        skills = request.form.get("skills")
        top_jobs = get_top_recommendations(skills)
        return render_template("results.html", skills=skills, top_jobs=top_jobs)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
