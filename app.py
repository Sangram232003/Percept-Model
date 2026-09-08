from flask import Flask, request, render_template_string
import joblib
import os

app = Flask(__name__)

# ---------------------------------------------------------
# LOAD MODEL
# ---------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "Perceptron.pkl")

model = joblib.load(MODEL_PATH)


# ---------------------------------------------------------
# HTML
# ---------------------------------------------------------
HTML = """
<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>AI Placement Predictor</title>

<style>

*{
    margin:0;
    padding:0;
    box-sizing:border-box;
}

body{
    min-height:100vh;
    font-family:Arial, Helvetica, sans-serif;
    background:#050816;
    color:white;
    overflow-x:hidden;
}

/* ================= BACKGROUND ================= */

.background{
    position:fixed;
    inset:0;
    overflow:hidden;
    z-index:-5;
}

.grid{
    position:absolute;
    inset:-50%;
    background-image:
        linear-gradient(rgba(0,255,255,0.06) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,255,255,0.06) 1px, transparent 1px);
    background-size:55px 55px;
    transform:rotate(10deg);
    animation:gridMove 18s linear infinite;
}

@keyframes gridMove{
    from{
        transform:translate(0,0) rotate(10deg);
    }
    to{
        transform:translate(55px,55px) rotate(10deg);
    }
}

.orb{
    position:absolute;
    border-radius:50%;
    filter:blur(2px);
    opacity:.35;
    animation:float 8s ease-in-out infinite;
}

.orb1{
    width:380px;
    height:380px;
    background:#00eaff;
    top:-140px;
    left:-100px;
}

.orb2{
    width:320px;
    height:320px;
    background:#8b5cf6;
    right:-80px;
    top:20%;
    animation-delay:2s;
}

.orb3{
    width:280px;
    height:280px;
    background:#ff00aa;
    left:30%;
    bottom:-130px;
    animation-delay:4s;
}

@keyframes float{

    0%,100%{
        transform:translate(0,0) scale(1);
    }

    50%{
        transform:translate(30px,-40px) scale(1.1);
    }
}


/* ================= PARTICLES ================= */

.particles{
    position:absolute;
    inset:0;
}

.particle{
    position:absolute;
    width:3px;
    height:3px;
    background:#fff;
    border-radius:50%;
    box-shadow:0 0 10px #00eaff;
    animation:particleMove linear infinite;
}

.particle:nth-child(1){left:8%;top:20%;animation-duration:7s}
.particle:nth-child(2){left:18%;top:70%;animation-duration:11s}
.particle:nth-child(3){left:30%;top:35%;animation-duration:8s}
.particle:nth-child(4){left:42%;top:80%;animation-duration:12s}
.particle:nth-child(5){left:55%;top:18%;animation-duration:9s}
.particle:nth-child(6){left:67%;top:65%;animation-duration:10s}
.particle:nth-child(7){left:78%;top:28%;animation-duration:8s}
.particle:nth-child(8){left:90%;top:75%;animation-duration:13s}
.particle:nth-child(9){left:48%;top:50%;animation-duration:6s}
.particle:nth-child(10){left:12%;top:48%;animation-duration:9s}

@keyframes particleMove{
    0%{
        transform:translateY(0);
        opacity:.2;
    }

    50%{
        opacity:1;
    }

    100%{
        transform:translateY(-120px);
        opacity:.1;
    }
}


/* ================= MAIN ================= */

.main{
    min-height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
    padding:40px 20px;
}

.card{
    width:100%;
    max-width:900px;
    padding:45px;
    border-radius:30px;

    background:rgba(10,15,35,.72);
    backdrop-filter:blur(25px);

    border:1px solid rgba(255,255,255,.12);

    box-shadow:
        0 30px 80px rgba(0,0,0,.6),
        inset 0 0 50px rgba(0,234,255,.03);

    position:relative;

    transition:transform .2s ease;
}


/* ================= TOP GLOW ================= */

.card::before{
    content:"";
    position:absolute;
    top:-1px;
    left:10%;
    width:80%;
    height:2px;

    background:linear-gradient(
        90deg,
        transparent,
        #00eaff,
        #a855f7,
        transparent
    );

    box-shadow:0 0 20px #00eaff;
}


/* ================= HEADER ================= */

.header{
    text-align:center;
    margin-bottom:40px;
}

.badge{
    display:inline-block;
    padding:8px 18px;
    border-radius:30px;

    font-size:12px;
    letter-spacing:2px;

    color:#00eaff;

    border:1px solid rgba(0,234,255,.35);

    background:rgba(0,234,255,.06);

    margin-bottom:18px;

    animation:pulse 2s infinite;
}

@keyframes pulse{
    0%,100%{
        box-shadow:0 0 5px rgba(0,234,255,.1);
    }

    50%{
        box-shadow:0 0 25px rgba(0,234,255,.35);
    }
}

h1{
    font-size:46px;
    line-height:1.1;

    background:linear-gradient(
        90deg,
        #ffffff,
        #00eaff,
        #a855f7,
        #ffffff
    );

    background-size:300%;

    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;

    animation:titleMove 5s linear infinite;
}

@keyframes titleMove{
    0%{background-position:0%}
    100%{background-position:300%}
}

.subtitle{
    color:#9ca3af;
    margin-top:12px;
    font-size:15px;
}


/* ================= INPUT GRID ================= */

.input-grid{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:25px;
}

.input-box{
    position:relative;
}

label{
    display:block;
    margin-bottom:10px;
    font-size:14px;
    color:#cbd5e1;
}

.input-wrapper{
    position:relative;
}

input{
    width:100%;
    padding:18px 20px;

    border-radius:15px;

    border:1px solid rgba(255,255,255,.12);

    background:rgba(255,255,255,.04);

    color:white;

    font-size:18px;
    outline:none;

    transition:.3s;
}

input:focus{
    border-color:#00eaff;

    box-shadow:
        0 0 20px rgba(0,234,255,.15),
        inset 0 0 15px rgba(0,234,255,.03);
}

input::placeholder{
    color:#64748b;
}


/* ================= METERS ================= */

.meter{
    margin-top:10px;
    height:4px;
    width:100%;

    border-radius:10px;

    background:#111827;

    overflow:hidden;
}

.meter-fill{
    height:100%;
    width:0%;

    border-radius:10px;

    background:linear-gradient(
        90deg,
        #00eaff,
        #a855f7
    );

    box-shadow:0 0 12px #00eaff;

    transition:width .4s ease;
}

.value{
    margin-top:7px;
    font-size:12px;
    color:#64748b;
}


/* ================= BUTTON ================= */

.predict-btn{
    width:100%;
    margin-top:35px;

    padding:19px;

    border:none;
    border-radius:16px;

    cursor:pointer;

    color:white;

    font-size:16px;
    font-weight:bold;

    letter-spacing:2px;

    background:
        linear-gradient(
            110deg,
            #00a6c7,
            #7c3aed,
            #ec4899,
            #00a6c7
        );

    background-size:300% 100%;

    animation:buttonMove 5s linear infinite;

    box-shadow:
        0 10px 30px rgba(124,58,237,.25);

    transition:.3s;
}

.predict-btn:hover{
    transform:translateY(-3px) scale(1.01);

    box-shadow:
        0 15px 40px rgba(0,234,255,.25);
}

@keyframes buttonMove{
    0%{background-position:0%}
    100%{background-position:300%}
}


/* ================= RESULT ================= */

.result{
    margin-top:35px;

    padding:30px;

    border-radius:22px;

    text-align:center;

    animation:resultAppear .7s ease;
}

@keyframes resultAppear{
    from{
        opacity:0;
        transform:scale(.85) translateY(20px);
    }

    to{
        opacity:1;
        transform:scale(1) translateY(0);
    }
}

.result.placed{
    border:1px solid rgba(34,197,94,.5);
    background:rgba(34,197,94,.07);
    box-shadow:0 0 40px rgba(34,197,94,.12);
}

.result.unplaced{
    border:1px solid rgba(239,68,68,.45);
    background:rgba(239,68,68,.06);
    box-shadow:0 0 40px rgba(239,68,68,.1);
}

.result-icon{
    width:65px;
    height:65px;

    margin:0 auto 15px;

    display:flex;
    justify-content:center;
    align-items:center;

    border-radius:50%;

    font-size:35px;
    font-weight:bold;

    animation:iconPop .6s ease;
}

.placed .result-icon{
    background:rgba(34,197,94,.15);
    border:1px solid #22c55e;
    color:#22c55e;
    box-shadow:0 0 25px rgba(34,197,94,.35);
}

.unplaced .result-icon{
    background:rgba(239,68,68,.12);
    border:1px solid #ef4444;
    color:#ef4444;
    box-shadow:0 0 25px rgba(239,68,68,.25);
}

@keyframes iconPop{
    0%{
        transform:scale(0) rotate(-90deg);
    }

    80%{
        transform:scale(1.15) rotate(5deg);
    }

    100%{
        transform:scale(1) rotate(0);
    }
}

.result h2{
    font-size:30px;
    letter-spacing:3px;
}

.result p{
    color:#94a3b8;
    margin-top:10px;
}

.stats{
    display:flex;
    justify-content:center;
    gap:20px;
    margin-top:25px;
}

.stat{
    min-width:180px;
    padding:15px;

    border-radius:14px;

    background:rgba(255,255,255,.04);

    border:1px solid rgba(255,255,255,.07);
}

.stat span{
    display:block;
    color:#64748b;
    font-size:11px;
    text-transform:uppercase;
    letter-spacing:1px;
    margin-bottom:6px;
}

.stat strong{
    font-size:20px;
}


/* ================= SCANNER ================= */

.scanner{
    display:none;

    position:fixed;
    inset:0;

    z-index:100;

    background:rgba(2,6,23,.94);

    backdrop-filter:blur(15px);

    justify-content:center;
    align-items:center;
    flex-direction:column;
}

.scanner.active{
    display:flex;
}

.scan-circle{
    width:150px;
    height:150px;

    border-radius:50%;

    border:2px solid rgba(0,234,255,.2);

    position:relative;

    display:flex;
    justify-content:center;
    align-items:center;

    box-shadow:
        0 0 30px rgba(0,234,255,.1),
        inset 0 0 30px rgba(0,234,255,.05);

    animation:circlePulse 1.5s infinite;
}

.scan-circle::before{
    content:"";

    position:absolute;

    width:100%;
    height:2px;

    background:#00eaff;

    box-shadow:0 0 20px #00eaff;

    animation:scanLine 1.2s linear infinite;
}

.scan-circle::after{
    content:"";

    position:absolute;

    inset:15px;

    border-radius:50%;

    border:1px dashed rgba(168,85,247,.6);

    animation:rotate 3s linear infinite;
}

.scan-symbol{
    font-size:45px;
    color:#00eaff;
    text-shadow:0 0 25px #00eaff;
}

@keyframes scanLine{
    0%{transform:translateY(-65px)}
    50%{transform:translateY(65px)}
    100%{transform:translateY(-65px)}
}

@keyframes rotate{
    from{transform:rotate(0)}
    to{transform:rotate(360deg)}
}

@keyframes circlePulse{
    0%,100%{
        transform:scale(1);
    }

    50%{
        transform:scale(1.08);
    }
}

.scanner-text{
    margin-top:30px;

    font-size:18px;

    letter-spacing:3px;

    color:#00eaff;

    animation:textBlink 1s infinite;
}

@keyframes textBlink{
    0%,100%{opacity:.4}
    50%{opacity:1}
}


/* ================= FOOTER ================= */

.footer{
    text-align:center;
    margin-top:25px;

    color:#475569;

    font-size:11px;
    letter-spacing:1px;
}


/* ================= RESPONSIVE ================= */

@media(max-width:700px){

    .card{
        padding:28px 20px;
    }

    h1{
        font-size:34px;
    }

    .input-grid{
        grid-template-columns:1fr;
    }

    .stats{
        flex-direction:column;
    }

    .stat{
        min-width:100%;
    }

}

</style>

</head>


<body>


<!-- BACKGROUND -->

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


<!-- SCANNER -->

<div class="scanner" id="scanner">

    <div class="scan-circle">

        <div class="scan-symbol">AI</div>

    </div>

    <div class="scanner-text">
        ANALYZING PLACEMENT DATA...
    </div>

</div>


<!-- MAIN -->

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
                Predict student placement using academic performance
                and resume strength.
            </p>

        </div>


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

                    <div class="input-wrapper">

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

                    </div>

                    <div class="meter">

                        <div
                            class="meter-fill"
                            id="cgpaMeter"
                        ></div>

                    </div>

                    <div class="value" id="cgpaValue">
                        0 / 10
                    </div>

                </div>


                <!-- RESUME SCORE -->

                <div class="input-box">

                    <label>
                        Resume Score
                    </label>

                    <div class="input-wrapper">

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

                    </div>

                    <div class="meter">

                        <div
                            class="meter-fill"
                            id="resumeMeter"
                        ></div>

                    </div>

                    <div class="value" id="resumeValue">
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

/* ================= INPUT METERS ================= */

function updateCgpa(){

    const input = document.getElementById("cgpa");
    const meter = document.getElementById("cgpaMeter");
    const value = document.getElementById("cgpaValue");

    let v = parseFloat(input.value) || 0;

    if(v < 0) v = 0;
    if(v > 10) v = 10;

    meter.style.width = (v / 10 * 100) + "%";

    value.innerText = v.toFixed(1) + " / 10";
}


function updateResume(){

    const input = document.getElementById("resume");
    const meter = document.getElementById("resumeMeter");
    const value = document.getElementById("resumeValue");

    let v = parseFloat(input.value) || 0;

    if(v < 0) v = 0;
    if(v > 100) v = 100;

    meter.style.width = v + "%";

    value.innerText = v.toFixed(1) + " / 100";
}


/* ================= SCANNING EFFECT ================= */

function startScanning(){

    const scanner = document.getElementById("scanner");

    scanner.classList.add("active");

}


/* ================= 3D CARD EFFECT ================= */

const card = document.getElementById("card");

document.addEventListener("mousemove", function(e){

    if(window.innerWidth <= 700){
        return;
    }

    const x = (window.innerWidth / 2 - e.clientX) / 60;
    const y = (window.innerHeight / 2 - e.clientY) / 60;

    card.style.transform =
        "perspective(1000px) rotateY(" +
        x +
        "deg) rotateX(" +
        y +
        "deg)";

});


document.addEventListener("mouseleave", function(){

    card.style.transform =
        "perspective(1000px) rotateY(0deg) rotateX(0deg)";

});


/* ================= INITIAL VALUES ================= */

updateCgpa();
updateResume();

</script>


</body>

</html>
"""


# ---------------------------------------------------------
# HOME
# ---------------------------------------------------------
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


# ---------------------------------------------------------
# PREDICTION
# ---------------------------------------------------------
@app.route("/predict", methods=["POST"])
def predict():

    try:

        cgpa = float(request.form.get("cgpa", ""))

        resume_score = float(
            request.form.get("resume_score", "")
        )


        # Validation

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
        # ONLY TWO FEATURES
        # -------------------------------------------------

        features = [[cgpa, resume_score]]


        # Model prediction

        prediction = model.predict(features)[0]


        # Placement result

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


# ---------------------------------------------------------
# RUN APP
# ---------------------------------------------------------
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
