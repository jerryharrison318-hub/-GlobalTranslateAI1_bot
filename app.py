from flask import Flask, request, jsonify
import argostranslate.package
import argostranslate.translate

app = Flask(__name__)

installed = argostranslate.translate.get_installed_languages()

@app.route("/translate", methods=["POST"])
def translate():

    data = request.get_json()

    text = data["q"]

    source = data.get("source", "auto")

    target = data["target"]

    languages = argostranslate.translate.get_installed_languages()

    from_lang = None
    to_lang = None

    if source == "auto":
        from_lang = languages[0]
    else:
        from_lang = next(
            l for l in languages if l.code == source
        )

    to_lang = next(
        l for l in languages if l.code == target
    )

    translation = from_lang.get_translation(
        to_lang
    )

    translated = translation.translate(text)

    return jsonify({
        "translatedText": translated
    })


@app.route("/")
def home():
    return "LibreTranslate API Running"


if __name__ == "__main__":
    from waitress import serve

    serve(app, host="0.0.0.0", port=8080)
