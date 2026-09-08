from flask import Flask, request, render_template_string
import joblib
import os

app = Flask(__name__)

# ============================================================
# LOAD MODEL
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "Perceptron.pkl")

model = joblib.load(MODEL_PATH)


# ============================================================
# HTML
# ============================================================

HTML = r"""
<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>NeuroHire AI | Placement Prediction</title>

    <style>

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            min-height: 100vh;
            font-family: Arial, Helvetica, sans-serif;
            color: white;
            overflow-x: hidden;

            background:
                radial-gradient(
                    circle at 15% 20%,
                    rgba(0, 255, 255, 0.16),
                    transparent 30%
                ),
                radial-gradient(
                    circle at 85% 20%,
                    rgba(168, 85, 247, 0.18),
                    transparent 30%
                ),
                radial-gradient(
                    circle at 50% 100%,
                    rgba(236, 72, 153, 0.14),
                    transparent 30%
                ),
                #050816;
        }


        /* =========================
           BACKGROUND GRID
        ========================= */

        body::before {
            content: "";
            position: fixed;
            inset: 0;

            background-image:
                linear-gradient(
                    rgba(255,255,255,0.035) 1px,
                    transparent 1px
                ),
                linear-gradient(
                    90deg,
                    rgba(255,255,255,0.035) 1px,
                    transparent 1px
                );

            background-size: 50px 50px;

            pointer-events: none;
            z-index: -5;
        }


        /* =========================
           GLOW ORBS
        ========================= */

        .orb {
            position: fixed;
            border-radius: 50%;
            filter: blur(5px);
            pointer-events: none;
            z-index: -4;
        }

        .orb1 {
            width: 230px;
            height: 230px;

            left: -70px;
            top: 12%;

            background: rgba(0, 255, 255, 0.13);

            animation: float1 8s ease-in-out infinite;
        }

        .orb2 {
            width: 280px;
            height: 280px;

            right: -100px;
            top: 35%;

            background: rgba(168, 85, 247, 0.14);

            animation: float2 10s ease-in-out infinite;
        }

        .orb3 {
            width: 190px;
            height: 190px;

            bottom: -60px;
            left: 40%;

            background: rgba(236, 72, 153, 0.12);

            animation: float3 9s ease-in-out infinite;
        }

        @keyframes float1 {

            0%, 100% {
                transform: translate(0, 0);
            }

            50% {
                transform: translate(80px, 90px);
            }
        }

        @keyframes float2 {

            0%, 100% {
                transform: translate(0, 0);
            }

            50% {
                transform: translate(-80px, -70px);
            }
        }

        @keyframes float3 {

            0%, 100% {
                transform: translate(0, 0);
            }

            50% {
                transform: translate(70px, -80px);
            }
        }


        /* =========================
           PAGE
        ========================= */

        .page {
            min-height: 100vh;
            padding: 45px 20px 60px;
        }

        .container {
            max-width: 1050px;
            margin: auto;
        }


        /* =========================
           HEADER
        ========================= */

        .badge {
            width: fit-content;
            margin: 0 auto 20px;

            padding: 9px 18px;

            border-radius: 50px;

            border: 1px solid rgba(103,232,249,0.3);

            background: rgba(103,232,249,0.06);

            color: #67e8f9;

            font-size: 11px;
            font-weight: bold;

            letter-spacing: 2px;
        }

        header {
            text-align: center;
            margin-bottom: 42px;
        }

        header h1 {
            font-size: clamp(42px, 7vw, 76px);

            font-weight: 900;

            letter-spacing: -4px;

            background:
                linear-gradient(
                    90deg,
                    #67e8f9,
                    #818cf8,
                    #c084fc,
                    #f472b6,
                    #67e8f9
                );

            background-size: 300% auto;

            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;

            animation: gradient 5s linear infinite;
        }

        @keyframes gradient {

            0% {
                background-position: 0%;
            }

            100% {
                background-position: 300%;
            }
        }

        header p {
            margin-top: 18px;

            color: #8d97ae;

            font-size: 15px;

            line-height: 1.7;
        }


        /* =========================
           MAIN CARD
        ========================= */

        .card {
            position: relative;

            padding: 40px;

            border-radius: 30px;

            border: 1px solid rgba(255,255,255,0.1);

            background:
                linear-gradient(
                    135deg,
                    rgba(255,255,255,0.09),
                    rgba(255,255,255,0.025)
                );

            backdrop-filter: blur(25px);
            -webkit-backdrop-filter: blur(25px);

            box-shadow:
                0 35px 100px rgba(0,0,0,0.45),
                inset 0 1px 0 rgba(255,255,255,0.08);

            overflow: hidden;

            transition: transform 0.15s ease;
        }

        .card::before {
            content: "";

            position: absolute;

            top: 0;
            left: 8%;

            width: 84%;
            height: 1px;

            background:
                linear-gradient(
                    90deg,
                    transparent,
                    #67e8f9,
                    #a78bfa,
                    #f472b6,
                    transparent
                );

            box-shadow: 0 0 25px #67e8f9;
        }


        /* =========================
           INPUT GRID
        ========================= */

        .input-grid {
            display: grid;

            grid-template-columns: 1fr 1fr;

            gap: 24px;
        }

        .input-card {
            padding: 28px;

            border-radius: 22px;

            background: rgba(2,6,23,0.55);

            border: 1px solid rgba(255,255,255,0.08);

            transition: 0.3s ease;
        }

        .input-card:hover {
            transform: translateY(-5px);

            border-color: rgba(103,232,249,0.35);

            box-shadow:
                0 15px 40px rgba(0,0,0,0.25);
        }

        .number {
            width: 40px;
            height: 40px;

            display: flex;

            align-items: center;
            justify-content: center;

            border-radius: 12px;

            background:
                linear-gradient(
                    135deg,
                    #06b6d4,
                    #6366f1
                );

            font-weight: bold;

            margin-bottom: 20px;
        }

        .input-card:nth-child(2) .number {
            background:
                linear-gradient(
                    135deg,
                    #a855f7,
                    #ec4899
                );
        }

        .input-card h2 {
            font-size: 21px;
            margin-bottom: 7px;
        }

        .input-card p {
            color: #7d879f;
            font-size: 13px;
            margin-bottom: 20px;
        }


        /* =========================
           INPUT
        ========================= */

        input {
            width: 100%;

            padding: 17px;

            border-radius: 14px;

            border: 1px solid rgba(255,255,255,0.1);

            background: rgba(255,255,255,0.04);

            color: white;

            outline: none;

            font-size: 18px;
            font-weight: bold;

            transition: 0.3s ease;
        }

        input:focus {
            border-color: #67e8f9;

            box-shadow:
                0 0 0 3px rgba(103,232,249,0.08),
                0 0 30px rgba(103,232,249,0.1);
        }

        .input-card:nth-child(2) input:focus {
            border-color: #c084fc;

            box-shadow:
                0 0 0 3px rgba(192,132,252,0.08),
                0 0 30px rgba(192,132,252,0.1);
        }

        input::placeholder {
            color: #5d667b;
        }


        /* =========================
           METERS
        ========================= */

        .meter {
            margin-top: 18px;
        }

        .meter-label {
            display: flex;
            justify-content: space-between;

            color: #68738c;

            font-size: 11px;

            margin-bottom: 8px;
        }

        .track {
            height: 6px;

            border-radius: 50px;

            background: rgba(255,255,255,0.06);

            overflow: hidden;
        }

        .fill {
            width: 0%;

            height: 100%;

            border-radius: 50px;

            background:
                linear-gradient(
                    90deg,
                    #06b6d4,
                    #22d3ee
                );

            box-shadow:
                0 0 15px rgba(34,211,238,0.7);

            transition: width 0.4s ease;
        }

        .input-card:nth-child(2) .fill {
            background:
                linear-gradient(
                    90deg,
                    #a855f7,
                    #ec4899
                );
        }


        /* =========================
           BUTTON
        ========================= */

        .button-area {
            text-align: center;

            margin-top: 35px;
        }

        .predict-button {
            position: relative;

            padding: 18px 48px;

            border: none;

            border-radius: 999px;

            cursor: pointer;

            color: white;

            font-size: 14px;

            font-weight: 900;

            letter-spacing: 1px;

            overflow: hidden;

            background:
                linear-gradient(
                    90deg,
                    #06b6d4,
                    #6366f1,
                    #a855f7,
                    #ec4899,
                    #06b6d4
                );

            background-size: 300% auto;

            animation:
                buttonGradient 4s linear infinite;

            box-shadow:
                0 12px 40px rgba(99,102,241,0.3);

            transition: 0.2s ease;
        }

        @keyframes buttonGradient {

            0% {
                background-position: 0%;
            }

            100% {
                background-position: 300%;
            }
        }

        .predict-button:hover {
            transform: translateY(-3px) scale(1.02);

            box-shadow:
                0 18px 55px rgba(99,102,241,0.45);
        }

        .predict-button:active {
            transform: scale(0.97);
        }

        .shine {
            position: absolute;

            top: -60%;

            left: -100%;

            width: 60%;

            height: 220%;

            background: rgba(255,255,255,0.25);

            transform: rotate(25deg);

            animation: shine 3s infinite;
        }

        @keyframes shine {

            0% {
                left: -100%;
            }

            35%, 100% {
                left: 150%;
            }
        }


        /* =========================
           ERROR
        ========================= */

        .error {
            padding: 15px 20px;

            margin-bottom: 25px;

            border-radius: 15px;

            border: 1px solid rgba(239,68,68,0.3);

            background: rgba(239,68,68,0.1);

            color: #fca5a5;

            text-align: center;
        }


        /* =========================
           RESULT
        ========================= */

        .result {
            margin-top: 35px;

            padding: 32px;

            border-radius: 25px;

            text-align: center;

            animation: resultIn 0.7s ease;
        }

        @keyframes resultIn {

            from {
                opacity: 0;
                transform: translateY(25px) scale(0.96);
            }

            to {
                opacity: 1;
                transform: translateY(0) scale(1);
            }
        }

        .result.placed {
            background: rgba(16,185,129,0.07);

            border: 1px solid rgba(52,211,153,0.35);

            box-shadow:
                0 0 60px rgba(52,211,153,0.08);
        }

        .result.unplaced {
            background: rgba(239,68,68,0.07);

            border: 1px solid rgba(248,113,113,0.35);

            box-shadow:
                0 0 60px rgba(248,113,113,0.08);
        }

        .result-icon {
            width: 80px;
            height: 80px;

            margin: 0 auto 18px;

            border-radius: 50%;

            display: flex;

            align-items: center;
            justify-content: center;

            font-size: 34px;

            font-weight: bold;
        }

        .placed .result-icon {
            color: #34d399;

            background: rgba(52,211,153,0.12);

            box-shadow:
                0 0 35px rgba(52,211,153,0.2);
        }

        .unplaced .result-icon {
            color: #f87171;

            background: rgba(248,113,113,0.12);

            box-shadow:
                0 0 35px rgba(248,113,113,0.2);
        }

        .result h2 {
            font-size: 34px;

            letter-spacing: 2px;

            margin-bottom: 10px;
        }

        .result p {
            color: #8993aa;

            font-size: 14px;
        }


        /* =========================
           DETAILS
        ========================= */

        .details {
            display: grid;

            grid-template-columns: 1fr 1fr;

            gap: 15px;

            max-width: 550px;

            margin: 25px auto 0;
        }

        .detail {
            padding: 17px;

            border-radius: 15px;

            background: rgba(255,255,255,0.035);

            border: 1px solid rgba(255,255,255,0.06);
        }

        .detail span {
            display: block;

            color: #68738c;

            font-size: 10px;

            text-transform: uppercase;

            letter-spacing: 1px;

            margin-bottom: 7px;
        }

        .detail strong {
            font-size: 19px;
        }


        /* =========================
           SCAN OVERLAY
        ========================= */

        .scan-overlay {
            position: fixed;

            inset: 0;

            display: none;

            align-items: center;
            justify-content: center;

            background:
                radial-gradient(
                    circle,
                    rgba(20,25,65,0.7),
                    rgba(2,4,15,0.97)
                );

            backdrop-filter: blur(12px);

            z-index: 9999;
        }

        .scan-overlay.active {
            display: flex;
        }

        .scanner {
            position: relative;

            width: 270px;
            height: 270px;

            display: flex;

            align-items: center;
            justify-content: center;
        }

        .ring {
            position: absolute;

            border-radius: 50%;

            border: 1px solid rgba(103,232,249,0.5);

            animation: rotate 3s linear infinite;
        }

        .ring1 {
            width: 260px;
            height: 260px;

            border-top-color: #67e8f9;
            border-bottom-color: #a78bfa;
        }

        .ring2 {
            width: 200px;
            height: 200px;

            border-left-color: #ec4899;
            border-right-color: #67e8f9;

            animation-direction: reverse;

            animation-duration: 2s;
        }

        .ring3 {
            width: 140px;
            height: 140px;

            border-top-color: #f472b6;

            animation-duration: 1.5s;
        }

        @keyframes rotate {

            from {
                transform: rotate(0deg);
            }

            to {
                transform: rotate(360deg);
            }
        }

        .core {
            width: 75px;
            height: 75px;

            border-radius: 50%;

            display: flex;

            align-items: center;
            justify-content: center;

            font-weight: 900;

            background:
                radial-gradient(
                    circle,
                    white,
                    #67e8f9 25%,
                    #6366f1 60%,
                    #a855f7
                );

            color: #050816;

            box-shadow:
                0 0 30px #67e8f9,
                0 0 70px rgba(168,85,247,0.7);

            animation: pulse 1s infinite;
        }

        @keyframes pulse {

            0%, 100% {
                transform: scale(0.92);
            }

            50% {
                transform: scale(1.08);
            }
        }

        .scan-line {
            position: absolute;

            width: 290px;
            height: 2px;

            background:
                linear-gradient(
                    90deg,
                    transparent,
                    #67e8f9,
                    white,
                    #a855f7,
                    transparent
                );

            box-shadow: 0 0 15px #67e8f9;

            animation: scan 1.5s infinite;
        }

        @keyframes scan {

            0%, 100% {
                transform: translateY(-110px);

                opacity: 0;
            }

            25% {
                opacity: 1;
            }

            50% {
                transform: translateY(110px);

                opacity: 1;
            }

            80% {
                opacity: 0;
            }
        }

        .scan-text {
            position: absolute;

            top: calc(50% + 160px);

            width: 100%;

            text-align: center;

            color: #c4f7ff;

            font-size: 13px;

            font-weight: bold;

            letter-spacing: 3px;

            animation: blink 0.8s infinite alternate;
        }

        @keyframes blink {

            from {
                opacity: 0.4;
            }

            to {
                opacity: 1;
            }
        }


        /* =========================
           FOOTER
        ========================= */

        footer {
            text-align: center;

            margin-top: 30px;

            color: #4f5970;

            font-size: 10px;

            letter-spacing: 1.5px;
        }


        /* =========================
           MOBILE
        ========================= */

        @media (max-width: 750px) {

            .page {
                padding: 30px 15px 50px;
            }

            .card {
                padding: 22px;

                border-radius: 22px;
            }

            .input-grid {
                grid-template-columns: 1fr;
            }

            .details {
                grid-template-columns: 1fr;
            }

            .predict-button {
                width: 100%;
            }

            header h1 {
                letter-spacing: -2px;
            }
        }

    </style>

</head>


<body>

    <!-- BACKGROUND -->

    <div class="orb orb1"></div>
    <div class="orb orb2"></div>
    <div class="orb orb3"></div>


    <!-- SCANNING SCREEN -->

    <div
        class="scan-overlay"
        id="scanOverlay"
    >

        <div class="scanner">

            <div class="ring ring1"></div>

            <div class="ring ring2"></div>

            <div class="ring ring3"></div>

            <div class="scan-line"></div>

            <div class="core">
                AI
            </div>

        </div>

        <div class="scan-text">
            ANALYZING PLACEMENT...
        </div>

    </div>


    <!-- PAGE -->

    <div class="page">

        <div class="container">


            <!-- HEADER -->

            <header>

                <div class="badge">
                    ⚡ PERCEPTRON PLACEMENT INTELLIGENCE
                </div>

                <h1>
                    NeuroHire AI
                </h1>

                <p>
                    Predict candidate placement using
                    CGPA and Resume Score.
                </p>

            </header>


            <!-- CARD -->

            <div
                class="card"
                id="mainCard"
            >

                {% if error %}

                    <div class="error">
                        ⚠ {{ error }}
                    </div>

                {% endif %}


                <!-- FORM -->

                <form
                    action="/predict"
                    method="POST"
                    id="predictionForm"
                    onsubmit="startScanning()"
                >

                    <div class="input-grid">


                        <!-- CGPA -->

                        <div class="input-card">

                            <div class="number">
                                01
                            </div>

                            <h2>
                                Academic CGPA
                            </h2>

                            <p>
                                Enter CGPA between 0 and 10.
                            </p>

                            <input
                                type="number"
                                name="cgpa"
                                id="cgpa"
                                min="0"
                                max="10"
                                step="0.01"
                                placeholder="Example: 8.00"
                                value="{{ cgpa }}"
                                required
                            >

                            <div class="meter">

                                <div class="meter-label">

                                    <span>0</span>

                                    <span id="cgpaText">
                                        0 / 10
                                    </span>

                                    <span>10</span>

                                </div>

                                <div class="track">

                                    <div
                                        class="fill"
                                        id="cgpaFill"
                                    ></div>

                                </div>

                            </div>

                        </div>


                        <!-- RESUME SCORE -->

                        <div class="input-card">

                            <div class="number">
                                02
                            </div>

                            <h2>
                                Resume Score
                            </h2>

                            <p>
                                Enter Resume Score between 0 and 100.
                            </p>

                            <input
                                type="number"
                                name="resume_score"
                                id="resumeScore"
                                min="0"
                                max="100"
                                step="0.01"
                                placeholder="Example: 79.88"
                                value="{{ resume_score }}"
                                required
                            >

                            <div class="meter">

                                <div class="meter-label">

                                    <span>0</span>

                                    <span id="resumeText">
                                        0 / 100
                                    </span>

                                    <span>100</span>

                                </div>

                                <div class="track">

                                    <div
                                        class="fill"
                                        id="resumeFill"
                                    ></div>

                                </div>

                            </div>

                        </div>

                    </div>


                    <!-- BUTTON -->

                    <div class="button-area">

                        <button
                            class="predict-button"
                            id="predictButton"
                            type="submit"
                        >

                            <span class="shine"></span>

                            ✦ PREDICT PLACEMENT

                        </button>

                    </div>

                </form>


                <!-- RESULT -->

                {% if result %}

                    <div class="result {{ result_class }}">

                        <div class="result-icon">
                            {{ result_icon }}
                        </div>

                        <h2>
                            {{ result }}
                        </h2>

                        <p>
                            Placement prediction generated
                            successfully using the Perceptron model.
                        </p>


                        <div class="details">

                            <div class="detail">

                                <span>
                                    Academic CGPA
                                </span>

                                <strong>
                                    {{ cgpa }}
                                </strong>

                            </div>


                            <div class="detail">

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

            </div>


            <footer>
                NEUROHIRE AI • MACHINE LEARNING PLACEMENT PREDICTION
            </footer>

        </div>

    </div>


    <!-- =====================================================
         JAVASCRIPT
    ====================================================== -->

    <script>

        const cgpaInput =
            document.getElementById("cgpa");

        const resumeInput =
            document.getElementById("resumeScore");

        const cgpaFill =
            document.getElementById("cgpaFill");

        const resumeFill =
            document.getElementById("resumeFill");

        const cgpaText =
            document.getElementById("cgpaText");

        const resumeText =
            document.getElementById("resumeText");


        function updateCGPA() {

            let value =
                parseFloat(cgpaInput.value);

            if (isNaN(value)) {
                value = 0;
            }

            value =
                Math.max(
                    0,
                    Math.min(10, value)
                );

            let percentage =
                (value / 10) * 100;

            cgpaFill.style.width =
                percentage + "%";

            cgpaText.textContent =
                value.toFixed(2) + " / 10";
        }


        function updateResume() {

            let value =
                parseFloat(resumeInput.value);

            if (isNaN(value)) {
                value = 0;
            }

            value =
                Math.max(
                    0,
                    Math.min(100, value)
                );

            resumeFill.style.width =
                value + "%";

            resumeText.textContent =
                value.toFixed(2) + " / 100";
        }


        cgpaInput.addEventListener(
            "input",
            updateCGPA
        );

        resumeInput.addEventListener(
            "input",
            updateResume
        );


        updateCGPA();
        updateResume();


        /* =================================================
           SCANNING ANIMATION
        ================================================= */

        function startScanning() {

            const cgpa =
                parseFloat(cgpaInput.value);

            const resume =
                parseFloat(resumeInput.value);

            if (
                isNaN(cgpa) ||
                isNaN(resume) ||
                cgpa < 0 ||
                cgpa > 10 ||
                resume < 0 ||
                resume > 100
            ) {
                return;
            }

            const overlay =
                document.getElementById(
                    "scanOverlay"
                );

            const button =
                document.getElementById(
                    "predictButton"
                );

            overlay.classList.add("active");

            button.disabled = true;

            button.innerHTML =
                "◉ ANALYZING PLACEMENT...";
        }


        /* =================================================
           3D CARD EFFECT
        ================================================= */

        const card =
            document.getElementById(
                "mainCard"
            );

        if (card) {

            card.addEventListener(
                "mousemove",
                function(event) {

                    if (window.innerWidth < 750) {
                        return;
                    }

                    const rect =
                        card.getBoundingClientRect();

                    const x =
                        event.clientX - rect.left;

                    const y =
                        event.clientY - rect.top;

                    const centerX =
                        rect.width / 2;

                    const centerY =
                        rect.height / 2;

                    const rotateX =
                        ((y - centerY) /
                        centerY) * -1.2;

                    const rotateY =
                        ((x - centerX) /
                        centerX) * 1.2;

                    card.style.transform =
                        "perspective(1200px) " +
                        "rotateX(" +
                        rotateX +
                        "deg) " +
                        "rotateY(" +
                        rotateY +
                        "deg)";
                }
            );


            card.addEventListener(
                "mouseleave",
                function() {

                    card.style.transform =
                        "perspective(1200px) " +
                        "rotateX(0deg) " +
                        "rotateY(0deg)";
                }
            );

        }

    </script>

</body>

</html>
"""


# ============================================================
# HOME PAGE
# ============================================================

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


# ============================================================
# PREDICTION ROUTE
# ============================================================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        # ----------------------------------------------------
        # GET USER INPUT
        # ----------------------------------------------------

        cgpa = float(
            request.form.get("cgpa", "")
        )

        resume_score = float(
            request.form.get("resume_score", "")
        )


        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

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


        # ----------------------------------------------------
        # MODEL FEATURES
        #
        # Your Perceptron expects:
        #
        # 1. cgpa
        # 2. resume_score
        # ----------------------------------------------------

        features = [
            [cgpa, resume_score]
        ]


        # ----------------------------------------------------
        # PREDICTION
        # ----------------------------------------------------

        prediction = model.predict(features)[0]


        # ----------------------------------------------------
        # PLACEMENT RESULT
        #
        # Assumption:
        #
        # 1 = Placed
        # 0 = Unplaced
        # ----------------------------------------------------

        if int(prediction) == 1:

            result = "PLACED"

            result_class = "placed"

            result_icon = "✓"

        else:

            result = "UNPLACED"

            result_class = "unplaced"

            result_icon = "×"


        # ----------------------------------------------------
        # SHOW RESULT
        # ----------------------------------------------------

        return render_template_string(
            HTML,
            result=result,
            result_class=result_class,
            result_icon=result_icon,
            cgpa=cgpa,
            resume_score=resume_score,
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


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
