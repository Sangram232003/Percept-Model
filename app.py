from flask import Flask, request, render_template_string
import joblib
import os

app = Flask(__name__)

# =========================================================
# LOAD ONLY THE SAVED PERCEPTRON MODEL
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "Perceptron.pkl")

model = joblib.load(MODEL_PATH)


# =========================================================
# HTML + CSS + JAVASCRIPT
# =========================================================

HTML = """
<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>AI Placement Predictor</title>

<style>

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    min-height: 100vh;
    font-family: Arial, Helvetica, sans-serif;
    background: #050816;
    color: white;
    overflow-x: hidden;
}


/* =====================================================
   ANIMATED BACKGROUND
   ===================================================== */

.background {
    position: fixed;
    inset: 0;
    overflow: hidden;
    z-index: -10;
}

.grid {
    position: absolute;
    inset: -50%;

    background-image:
        linear-gradient(rgba(0, 234, 255, 0.06) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 234, 255, 0.06) 1px, transparent 1px);

    background-size: 55px 55px;

    transform: rotate(10deg);

    animation: gridMove 18s linear infinite;
}

@keyframes gridMove {

    0% {
        transform: translate(0, 0) rotate(10deg);
    }

    100% {
        transform: translate(55px, 55px) rotate(10deg);
    }
}


/* =====================================================
   GLOWING ORBS
   ===================================================== */

.orb {
    position: absolute;
    border-radius: 50%;
    filter: blur(5px);
    opacity: 0.35;
    animation: floatOrb 8s ease-in-out infinite;
}

.orb1 {
    width: 380px;
    height: 380px;
    background: #00eaff;
    top: -150px;
    left: -100px;
}

.orb2 {
    width: 330px;
    height: 330px;
    background: #8b5cf6;
    right: -100px;
    top: 20%;
    animation-delay: 2s;
}

.orb3 {
    width: 300px;
    height: 300px;
    background: #ff00aa;
    left: 30%;
    bottom: -150px;
    animation-delay: 4s;
}

@keyframes floatOrb {

    0%, 100% {
        transform: translate(0, 0) scale(1);
    }

    50% {
        transform: translate(30px, -40px) scale(1.1);
    }
}


/* =====================================================
   PARTICLES
   ===================================================== */

.particles {
    position: absolute;
    inset: 0;
}

.particle {
    position: absolute;

    width: 3px;
    height: 3px;

    background: white;
    border-radius: 50%;

    box-shadow: 0 0 12px #00eaff;

    animation: particleMove linear infinite;
}

.particle:nth-child(1) {
    left: 8%;
    top: 20%;
    animation-duration: 7s;
}

.particle:nth-child(2) {
    left: 18%;
    top: 70%;
    animation-duration: 11s;
}

.particle:nth-child(3) {
    left: 30%;
    top: 35%;
    animation-duration: 8s;
}

.particle:nth-child(4) {
    left: 42%;
    top: 80%;
    animation-duration: 12s;
}

.particle:nth-child(5) {
    left: 55%;
    top: 18%;
    animation-duration: 9s;
}

.particle:nth-child(6) {
    left: 67%;
    top: 65%;
    animation-duration: 10s;
}

.particle:nth-child(7) {
    left: 78%;
    top: 28%;
    animation-duration: 8s;
}

.particle:nth-child(8) {
    left: 90%;
    top: 75%;
    animation-duration: 13s;
}

.particle:nth-child(9) {
    left: 48%;
    top: 50%;
    animation-duration: 6s;
}

.particle:nth-child(10) {
    left: 12%;
    top: 48%;
    animation-duration: 9s;
}

@keyframes particleMove {

    0% {
        transform: translateY(0);
        opacity: 0.2;
    }

    50% {
        opacity: 1;
    }

    100% {
        transform: translateY(-120px);
        opacity: 0.1;
    }
}


/* =====================================================
   MAIN CARD
   ===================================================== */

.main {
    min-height: 100vh;

    display: flex;
    justify-content: center;
    align-items: center;

    padding: 40px 20px;
}

.card {

    width: 100%;
    max-width: 900px;

    padding: 45px;

    border-radius: 30px;

    background: rgba(10, 15, 35, 0.75);

    backdrop-filter: blur(25px);

    border: 1px solid rgba(255, 255, 255, 0.12);

    box-shadow:
        0 30px 80px rgba(0, 0, 0, 0.6),
        inset 0 0 50px rgba(0, 234, 255, 0.03);

    position: relative;

    transition: transform 0.2s ease;
}


/* TOP GLOW LINE */

.card::before {

    content: "";

    position: absolute;

    top: -1px;
    left: 10%;

    width: 80%;
    height: 2px;

    background:
        linear-gradient(
            90deg,
            transparent,
            #00eaff,
            #a855f7,
            transparent
        );

    box-shadow: 0 0 20px #00eaff;
}


/* =====================================================
   HEADER
   ===================================================== */

.header {
    text-align: center;
    margin-bottom: 40px;
}

.badge {

    display: inline-block;

    padding: 8px 18px;

    border-radius: 30px;

    font-size: 12px;

    letter-spacing: 2px;

    color: #00eaff;

    border: 1px solid rgba(0, 234, 255, 0.35);

    background: rgba(0, 234, 255, 0.06);

    margin-bottom: 18px;

    animation: badgePulse 2s infinite;
}

@keyframes badgePulse {

    0%, 100% {
        box-shadow: 0 0 5px rgba(0, 234, 255, 0.1);
    }

    50% {
        box-shadow: 0 0 25px rgba(0, 234, 255, 0.35);
    }
}

h1 {

    font-size: 46px;
    line-height: 1.1;

    background:
        linear-gradient(
            90deg,
            #ffffff,
            #00eaff,
            #a855f7,
            #ffffff
        );

    background-size: 300%;

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    animation: titleMove 5s linear infinite;
}

@keyframes titleMove {

    0% {
        background-position: 0%;
    }

    100% {
        background-position: 300%;
    }
}

.subtitle {

    color: #9ca3af;

    margin-top: 12px;

    font-size: 15px;
}


/* =====================================================
   INPUTS
   ===================================================== */

.input-grid {

    display: grid;

    grid-template-columns: 1fr 1fr;

    gap: 25px;
}

.input-box {
    position: relative;
}

label {

    display: block;

    margin-bottom: 10px;

    font-size: 14px;

    color: #cbd5e1;
}

input {

    width: 100%;

    padding: 18px 20px;

    border-radius: 15px;

    border: 1px solid rgba(255, 255, 255, 0.12);

    background: rgba(255, 255, 255, 0.04);

    color: white;

    font-size: 18px;

    outline: none;

    transition: 0.3s;
}

input:focus {

    border-color: #00eaff;

    box-shadow:
        0 0 20px rgba(0, 234, 255, 0.15),
        inset 0 0 15px rgba(0, 234, 255, 0.03);
}

input::placeholder {
    color: #64748b;
}


/* =====================================================
   METERS
   ===================================================== */

.meter {

    margin-top: 10px;

    height: 4px;

    width: 100%;

    border-radius: 10px;

    background: #111827;

    overflow: hidden;
}

.meter-fill {

    height: 100%;

    width: 0%;

    border-radius: 10px;

    background:
        linear-gradient(
            90deg,
            #00eaff,
            #a855f7
        );

    box-shadow: 0 0 12px #00eaff;

    transition: width 0.4s ease;
}

.value {

    margin-top: 7px;

    font-size: 12px;

    color: #64748b;
}


/* =====================================================
   BUTTON
   ===================================================== */

.predict-btn {

    width: 100%;

    margin-top: 35px;

    padding: 19px;

    border: none;

    border-radius: 16px;

    cursor: pointer;

    color: white;

    font-size: 16px;

    font-weight: bold;

    letter-spacing: 2px;

    background:
        linear-gradient(
            110deg,
            #00a6c7,
            #7c3aed,
            #ec4899,
            #00a6c7
        );

    background-size: 300% 100%;

    animation: buttonMove 5s linear infinite;

    box-shadow:
        0 10px 30px rgba(124, 58, 237, 0.25);

    transition: 0.3s;
}

.predict-btn:hover {

    transform: translateY(-3px) scale(1.01);

    box-shadow:
        0 15px 40px rgba(0, 234, 255, 0.25);
}

.predict-btn:active {

    transform: scale(0.97);
}

@keyframes buttonMove {

    0% {
        background-position: 0%;
    }

    100% {
        background-position: 300%;
    }
}


/* =====================================================
   RESULT
   ===================================================== */

.result {

    margin-top: 35px;

    padding: 30px;

    border-radius: 22px;

    text-align: center;

    animation: resultAppear 0.7s ease;
}

@keyframes resultAppear {

    from {
        opacity: 0;
        transform: scale(0.85) translateY(20px);
    }

    to {
        opacity: 1;
        transform: scale(1) translateY(0);
    }
}

.result.placed {

    border: 1px solid rgba(34, 197, 94, 0.5);

    background: rgba(34, 197, 94, 0.07);

    box-shadow:
        0 0 40px rgba(34, 197, 94, 0.12);
}

.result.unplaced {

    border: 1px solid rgba(239, 68, 68, 0.45);

    background: rgba(239, 68, 68, 0.06);

    box-shadow:
        0 0 40px rgba(239, 68, 68, 0.10);
}

.result-icon {

    width: 65px;
    height: 65px;

    margin: 0 auto 15px;

    display: flex;

    justify-content: center;
    align-items: center;

    border-radius: 50%;

    font-size: 35px;

    font-weight: bold;

    animation: iconPop 0.6s ease;
}

.placed .result-icon {

    background: rgba(34, 197, 94, 0.15);

    border: 1px solid #22c55e;

    color: #22c55e;

    box-shadow:
        0 0 25px rgba(34, 197, 94, 0.35);
}

.unplaced .result-icon {

    background: rgba(239, 68, 68, 0.12);

    border: 1px solid #ef4444;

    color: #ef4444;

    box-shadow:
        0 0 25px rgba(239, 68, 68, 0.25);
}

@keyframes iconPop {

    0% {
        transform: scale(0) rotate(-90deg);
    }

    80% {
        transform: scale(1.15) rotate(5deg);
    }

    100% {
        transform: scale(1) rotate(0);
    }
}

.result h2 {

    font-size: 30px;

    letter-spacing: 3px;
}

.result p {

    color: #94a3b8;

    margin-top: 10px;
}


/* =====================================================
   RESULT STATS
   ===================================================== */

.stats {

    display: flex;

    justify-content: center;

    gap: 20px;

    margin-top: 25px;
}

.stat {

    min-width: 180px;

    padding: 15px;

    border-radius: 14px;

    background: rgba(255, 255, 255, 0.04);

    border: 1px solid rgba(255, 255, 255, 0.07);
}

.stat span {

    display: block;

    color: #64748b;

    font-size: 11px;

    text-transform: uppercase;

    letter-spacing: 1px;

    margin-bottom: 6px;
}

.stat strong {

    font-size: 20px;
}


/* =====================================================
   SCANNING SCREEN
   ===================================================== */

.scanner {

    display: none;

    position: fixed;

    inset: 0;

    z-index: 100;

    background: rgba(2, 6, 23, 0.94);

    backdrop-filter: blur(15px);

    justify-content: center;

    align-items: center;

    flex-direction: column;
}

.scanner.active {
    display: flex;
}

.scan-circle {

    width: 150px;
    height: 150px;

    border-radius: 50%;

    border: 2px solid rgba(0, 234, 255, 0.2);

    position: relative;

    display: flex;

    justify-content: center;

    align-items: center;

    box-shadow:
        0 0 30px rgba(0, 234, 255, 0.1),
        inset 0 0 30px rgba(0, 234, 255, 0.05);

    animation: circlePulse 1.5s infinite;
}

.scan-circle::before {

    content: "";

    position: absolute;

    width: 100%;
    height: 2px;

    background: #00eaff;

    box-shadow: 0 0 20px #00eaff;

    animation: scanLine 1.2s linear infinite;
}

.scan-circle::after {

    content: "";

    position: absolute;

    inset: 15px;

    border-radius: 50%;

    border: 1px dashed rgba(168, 85, 247, 0.6);

    animation: rotateCircle 3s linear infinite;
}

.scan-symbol {

    font-size: 45px;

    color: #00eaff;

    text-shadow: 0 0 25px #00eaff;
}

@keyframes scanLine {

    0% {
        transform: translateY(-65px);
    }

    50% {
        transform: translateY(65px);
    }

    100% {
        transform: translateY(-65px);
    }
}

@keyframes rotateCircle {

    from {
        transform: rotate(0);
    }

    to {
        transform: rotate(360deg);
    }
}

@keyframes circlePulse {

    0%, 100% {
        transform: scale(1);
    }

    50% {
        transform: scale(1.08);
    }
}

.scanner-text {

    margin-top: 30px;

    font-size: 18px;

    letter-spacing: 3px;

    color: #00eaff;

    animation: textBlink 1s infinite;
}

@keyframes textBlink {

    0%, 100% {
        opacity: 0.4;
    }

    50% {
        opacity: 1;
    }
}


/* =====================================================
   FOOTER
   ===================================================== */

.footer {

    text-align: center;

    margin-top: 25px;

    color: #475569;

    font-size: 11px;

    letter-spacing: 1px;
}


/* =====================================================
   MOBILE
   ===================================================== */

@media (max-width: 700px) {

    .card {
        padding: 28px 20px;
    }

    h1 {
        font-size: 34px;
    }

    .input-grid {
        grid-template-columns: 1fr;
    }

    .stats {
        flex-direction: column;
    }

    .stat {
        min-width: 100%;
    }
}

</style>

</head>


<body>


<!-- =====================================================
     ANIMATED BACKGROUND
     ===================================================== -->

<div class="background">

    <div class="grid"></div>

    <div class="orb orb1"></div>
    <div class="orb orb2"></div>
    <div class="orb orb3"></div>

    <div class="particles">

        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>

    </div>

</div>


<!-- =====================================================
     AI SCANNER
     ===================================================== -->

<div class="scanner" id="scanner">

    <div class="scan-circle">

        <div class="scan-symbol">
            AI
        </div>

    </div>

    <div class="scanner-text">
        ANALYZING PLACEMENT DATA...
    </div>

</div>


<!-- =====================================================
     MAIN APPLICATION
     ===================================================== -->

<div class="main">

    <div class="card" id="card">


        <div class="header">

            <div class="badge">
                PERCEPTRON • AI MODEL
            </div>

            <h1>
                Placement Predictor
            </h1>

            <p class="subtitle">
                Predict student placement using CGPA
                and resume score.
            </p>

        </div>


        <!-- =================================================
             PREDICTION FORM
             ================================================= -->

        <form
            action="/predict"
            method="POST"
            id="predictionForm"
            onsubmit="startScanning()"
        >


            <div class="input-grid">


                <!-- CGPA -->

                <div class="input-box">

                    <label>
                        Academic CGPA
                    </label>

                    <input
                        type="number"
                        name="cgpa"
                        id="cgpa"
                        min="0"
                        max="10"
                        step="0.1"
                        placeholder="Enter CGPA"
                        value="{{ cgpa }}"
                        required
                        oninput="updateCgpa()"
                    >

                    <div class="meter">

                        <div
                            class="meter-fill"
                            id="cgpaMeter"
                        ></div>

                    </div>

                    <div
                        class="value"
                        id="cgpaValue"
                    >
                        0 / 10
                    </div>

                </div>


                <!-- RESUME SCORE -->

                <div class="input-box">

                    <label>
                        Resume Score
                    </label>

                    <input
                        type="number"
                        name="resume_score"
                        id="resume"
                        min="0"
                        max="100"
                        step="0.1"
                        placeholder="Enter Resume Score"
                        value="{{ resume_score }}"
                        required
                        oninput="updateResume()"
                    >

                    <div class="meter">

                        <div
                            class="meter-fill"
                            id="resumeMeter"
                        ></div>

                    </div>

                    <div
                        class="value"
                        id="resumeValue"
                    >
                        0 / 100
                    </div>

                </div>

            </div>


            <button
                type="submit"
                class="predict-btn"
            >
                ⚡ PREDICT PLACEMENT
            </button>

        </form>


        <!-- =================================================
             RESULT
             ================================================= -->

        {% if result %}

        <div class="result {{ result_class }}">

            <div class="result-icon">
                {{ result_icon }}
            </div>

            <h2>
                {{ result }}
            </h2>

            <p>
                Perceptron model prediction
            </p>


            <div class="stats">

                <div class="stat">

                    <span>
                        Academic CGPA
                    </span>

                    <strong>
                        {{ cgpa }}
                    </strong>

                </div>


                <div class="stat">

                    <span>
                        Resume Score
                    </span>

                    <strong>
                        {{ resume_score }}
                    </strong>

                </div>

            </div>

        </div>

        {% endif %}


        <!-- =================================================
             ERROR
             ================================================= -->

        {% if error %}

        <div class="result unplaced">

            <div class="result-icon">
                !
            </div>

            <h2>
                INVALID INPUT
            </h2>

            <p>
                {{ error }}
            </p>

        </div>

        {% endif %}


        <div class="footer">

            Powered by Scikit-Learn Perceptron • 2 Features

        </div>


    </div>

</div>


<script>


// =========================================================
// CGPA METER
// =========================================================

function updateCgpa() {

    const input = document.getElementById("cgpa");

    const meter = document.getElementById("cgpaMeter");

    const value = document.getElementById("cgpaValue");

    let v = parseFloat(input.value) || 0;

    if (v < 0) {
        v = 0;
    }

    if (v > 10) {
        v = 10;
    }

    meter.style.width =
        (v / 10 * 100) + "%";

    value.innerText =
        v.toFixed(1) + " / 10";
}


// =========================================================
// RESUME SCORE METER
// =========================================================

function updateResume() {

    const input = document.getElementById("resume");

    const meter = document.getElementById("resumeMeter");

    const value = document.getElementById("resumeValue");

    let v = parseFloat(input.value) || 0;

    if (v < 0) {
        v = 0;
    }

    if (v > 100) {
        v = 100;
    }

    meter.style.width =
        v + "%";

    value.innerText =
        v.toFixed(1) + " / 100";
}


// =========================================================
// SCANNING EFFECT
// =========================================================

function startScanning() {

    const scanner =
        document.getElementById("scanner");

    scanner.classList.add("active");

}


// =========================================================
// 3D MOUSE MOVEMENT
// =========================================================

const card =
    document.getElementById("card");

document.addEventListener(
    "mousemove",
    function(event) {

        if (window.innerWidth <= 700) {
            return;
        }

        const x =
            (window.innerWidth / 2 - event.clientX) / 60;

        const y =
            (window.innerHeight / 2 - event.clientY) / 60;

        card.style.transform =
            "perspective(1000px) " +
            "rotateY(" + x + "deg) " +
            "rotateX(" + y + "deg)";
    }
);


document.addEventListener(
    "mouseleave",
    function() {

        card.style.transform =
            "perspective(1000px) " +
            "rotateY(0deg) " +
            "rotateX(0deg)";
    }
);


// =========================================================
// INITIALIZE METERS
// =========================================================

updateCgpa();

updateResume();

</script>


</body>

</html>
"""


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/", methods=["GET"])
def home():

    return render_template_string(
        HTML,
        result=None,
        result_class="",
        result_icon="",
        cgpa="",
        resume_score="",
        error=None
    )


# =========================================================
# PREDICTION
# =========================================================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        cgpa = float(
            request.form.get("cgpa", "")
        )

        resume_score = float(
            request.form.get("resume_score", "")
        )


        # -------------------------------------------------
        # VALIDATION
        # -------------------------------------------------

        if cgpa < 0 or cgpa > 10:

            return render_template_string(
                HTML,

                result=None,
                result_class="",
                result_icon="",

                cgpa=cgpa,
                resume_score=resume_score,

                error="CGPA must be between 0 and 10."
            )


        if resume_score < 0 or resume_score > 100:

            return render_template_string(
                HTML,

                result=None,
                result_class="",
                result_icon="",

                cgpa=cgpa,
                resume_score=resume_score,

                error="Resume Score must be between 0 and 100."
            )


        # -------------------------------------------------
        # ONLY THE TWO MODEL FEATURES
        # -------------------------------------------------

        features = [
            [cgpa, resume_score]
        ]


        # -------------------------------------------------
        # PREDICT USING Perceptron.pkl
        # -------------------------------------------------

        prediction = model.predict(features)[0]


        # -------------------------------------------------
        # DISPLAY RESULT
        # -------------------------------------------------

        if int(prediction) == 1:

            result = "PLACED"

            result_class = "placed"

            result_icon = "✓"

        else:

            result = "UNPLACED"

            result_class = "unplaced"

            result_icon = "×"


        return render_template_string(

            HTML,

            result=result,

            result_class=result_class,

            result_icon=result_icon,

            cgpa=f"{cgpa:.1f}",

            resume_score=f"{resume_score:.1f}",

            error=None

        )


    except ValueError:

        return render_template_string(

            HTML,

            result=None,

            result_class="",

            result_icon="",

            cgpa="",

            resume_score="",

            error="Please enter valid numeric values."

        )


    except Exception as e:

        return render_template_string(

            HTML,

            result=None,

            result_class="",

            result_icon="",

            cgpa="",

            resume_score="",

            error="Prediction error: " + str(e)

        )


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    port = int(
        os.environ.get("PORT", 5000)
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
