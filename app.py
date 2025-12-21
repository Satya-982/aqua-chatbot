from flask import Flask, render_template, request
from data import qa_data

app = Flask(__name__)

def offline_ai_response(question, lang):
    q = question.lower()

    if any(word in q for word in ["disease", "spot", "white", "infection"]):
        return (
            "This looks like a disease-related issue. Observe shrimp behavior closely and consult an aqua expert."
            if lang == "en"
            else "ఇది వ్యాధికి సంబంధించిన సమస్యలా ఉంది. రొయ్యల ప్రవర్తనను గమనించి నిపుణులను సంప్రదించండి."
        )

    if any(word in q for word in ["water", "oxygen", "ph", "ammonia"]):
        return (
            "This seems related to water quality. Check pH, oxygen, and ammonia levels immediately."
            if lang == "en"
            else "ఇది నీటి నాణ్యతకు సంబంధించిన సమస్యగా కనిపిస్తోంది. వెంటనే pH, ఆక్సిజన్, అమోనియా స్థాయిలను పరీక్షించండి."
        )

    if any(word in q for word in ["feed", "food", "eating"]):
        return (
            "Feeding should be adjusted based on shrimp growth and water condition."
            if lang == "en"
            else "రొయ్యల పెరుగుదల మరియు నీటి పరిస్థితిని బట్టి ఆహారం ఇవ్వాలి."
        )

    if any(word in q for word in ["harvest", "catch", "market"]):
        return (
            "Harvest shrimp when they reach market size and growth rate slows."
            if lang == "en"
            else "రొయ్యలు మార్కెట్ పరిమాణానికి చేరుకున్నప్పుడు కోత చేయాలి."
        )

    return (
        "This is a general aquaculture query. Regular monitoring and expert advice are recommended."
        if lang == "en"
        else "ఇది సాధారణ ఆక్వా ప్రశ్న. క్రమం తప్పకుండా పరిశీలించి నిపుణుల సలహా తీసుకోవడం మంచిది."
    )

@app.route("/", methods=["GET", "POST"])
def home():
    reply = None   # IMPORTANT: None means “no reply yet”

    if request.method == "POST":
        user_msg = request.form["message"].lower()
        lang = request.form["lang"]

        # Rule-based answers
        for key in qa_data:
            if key in user_msg:
                reply = qa_data[key][lang]
                break

        # Offline AI fallback
        if reply is None:
            reply = offline_ai_response(user_msg, lang)

    return render_template("index.html", reply=reply)

if __name__ == "__main__":
    app.run(debug=True)
