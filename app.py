from flask import Flask, request, render_template_string
import joblib
import os
import math

app = Flask(__name__)

# ============================================================
# LOAD MODEL
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "Perceptron.pkl")

model = joblib.load(MODEL_PATH)


# ============================================================
# HTML + CSS + JAVASCRIPT
# ============================================================

HTML = r"""
<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>NeuroHire AI</title>


<style>

/* =========================================================
   RESET
========================================================= */

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}


/* =========================================================
   BODY
========================================================= */

body {

    min-height: 100vh;

    font-family:
        Inter,
        "Segoe UI",
        Arial,
        sans-serif;

    color: #ffffff;

    overflow-x: hidden;

    background:
        radial-gradient(
            circle at 10% 15%,
            rgba(0, 255, 220, 0.18),
            transparent 27%
        ),

        radial-gradient(
            circle at 90% 15%,
            rgba(150, 80, 255, 0.22),
            transparent 30%
        ),

        radial-gradient(
            circle at 50% 100%,
            rgba(255, 45, 145, 0.15),
            transparent 32%
        ),

        #070711;

}


/* =========================================================
   GRID BACKGROUND
========================================================= */

body::before {

    content: "";

    position: fixed;

    inset: 0;

    z-index: -20;

    pointer-events: none;

    background-image:

        linear-gradient(
            rgba(255,255,255,0.025) 1px,
            transparent 1px
        ),

        linear-gradient(
            90deg,
            rgba(255,255,255,0.025) 1px,
            transparent 1px
        );

    background-size: 48px 48px;

    mask-image:
        linear-gradient(
            to bottom,
            black 0%,
            transparent 90%
        );

}


/* =========================================================
   MOVING LIGHT ORBS
========================================================= */

.light-orb {

    position: fixed;

    border-radius: 50%;

    pointer-events: none;

    filter: blur(90px);

    z-index: -10;

}


.orb-1 {

    width: 320px;
    height: 320px;

    left: -120px;
    top: -80px;

    background: #00ffe0;

    opacity: 0.11;

    animation:
        orbMove1 12s
        ease-in-out
        infinite alternate;

}


.orb-2 {

    width: 360px;
    height: 360px;

    right: -130px;
    top: 20%;

    background: #8957ff;

    opacity: 0.13;

    animation:
        orbMove2 15s
        ease-in-out
        infinite alternate;

}


.orb-3 {

    width: 300px;
    height: 300px;

    left: 30%;
    bottom: -150px;

    background: #ff268d;

    opacity: 0.10;

    animation:
        orbMove3 11s
        ease-in-out
        infinite alternate;

}


@keyframes orbMove1 {

    from {
        transform:
            translate(0,0)
            scale(1);
    }

    to {
        transform:
            translate(260px,190px)
            scale(1.35);
    }

}


@keyframes orbMove2 {

    from {
        transform:
            translate(0,0);
    }

    to {
        transform:
            translate(-220px,120px)
            scale(1.2);
    }

}


@keyframes orbMove3 {

    from {
        transform:
            translate(0,0);
    }

    to {
        transform:
            translate(170px,-130px)
            scale(1.3);
    }

}


/* =========================================================
   PARTICLES
========================================================= */

.particles {

    position: fixed;

    inset: 0;

    pointer-events: none;

    z-index: -5;

}


.particle {

    position: absolute;

    width: 4px;
    height: 4px;

    border-radius: 50%;

    background: #00ffe0;

    box-shadow:
        0 0 8px #00ffe0,
        0 0 18px #00ffe0;

    animation:
        particleRise
        linear
        infinite;

}


@keyframes particleRise {

    0% {

        transform:
            translateY(110vh)
            scale(0.4);

        opacity: 0;

    }

    15% {
        opacity: 1;
    }

    85% {
        opacity: 1;
    }

    100% {

        transform:
            translateY(-10vh)
            scale(1.3);

        opacity: 0;

    }

}


/* =========================================================
   PAGE
========================================================= */

.page {

    width: 94%;

    max-width: 1050px;

    margin: auto;

    padding:
        48px 0 40px;

}


/* =========================================================
   HEADER
========================================================= */

.header {

    text-align: center;

    margin-bottom: 35px;

}


.online {

    display: inline-flex;

    align-items: center;

    gap: 9px;

    padding:
        8px 17px;

    border-radius: 50px;

    border:
        1px solid
        rgba(0,255,220,0.30);

    background:
        rgba(0,255,220,0.055);

    color: #61ffe8;

    font-size: 10px;

    font-weight: 900;

    letter-spacing: 2px;

    box-shadow:
        0 0 25px
        rgba(0,255,220,0.08);

}


.online-dot {

    width: 8px;
    height: 8px;

    border-radius: 50%;

    background: #00ffd5;

    box-shadow:
        0 0 14px #00ffd5;

    animation:
        onlinePulse 1.1s infinite;

}


@keyframes onlinePulse {

    50% {

        transform:
            scale(1.6);

        opacity:
            0.4;

    }

}


.header h1 {

    margin-top: 20px;

    font-size:
        clamp(48px, 8vw, 84px);

    line-height:
        0.92;

    font-weight: 950;

    letter-spacing:
        -5px;

    background:

        linear-gradient(
            90deg,
            #00ffe0,
            #665cff,
            #ff3e9e,
            #ffb347,
            #00ffe0
        );

    background-size:
        400%;

    -webkit-background-clip:
        text;

    -webkit-text-fill-color:
        transparent;

    animation:
        headingFlow
        7s
        linear
        infinite;

}


@keyframes headingFlow {

    to {
        background-position:
            400%;
    }

}


.header p {

    margin-top:
        18px;

    color:
        #9292a8;

    font-size:
        15px;

}


/* =========================================================
   MAIN CARD
========================================================= */

.card {

    position: relative;

    padding:
        34px;

    border-radius:
        30px;

    background:

        linear-gradient(
            145deg,
            rgba(255,255,255,0.085),
            rgba(255,255,255,0.025)
        );

    border:
        1px solid
        rgba(255,255,255,0.11);

    backdrop-filter:
        blur(28px);

    -webkit-backdrop-filter:
        blur(28px);

    box-shadow:

        0 40px 120px
        rgba(0,0,0,0.55),

        inset
        0 1px 0
        rgba(255,255,255,0.08);

    transition:
        transform 0.2s ease;

}


/* =========================================================
   TOP LASER
========================================================= */

.card::before {

    content: "";

    position: absolute;

    top: 0;
    left: 8%;

    width: 84%;
    height: 2px;

    background:

        linear-gradient(
            90deg,
            transparent,
            #00ffe0,
            #6d5cff,
            #ff3e9e,
            #ffb347,
            transparent
        );

    box-shadow:
        0 0 25px #6d5cff;

}


/* =========================================================
   CARD HEADER
========================================================= */

.card-header {

    display: flex;

    align-items:
        center;

    justify-content:
        space-between;

    margin-bottom:
        28px;

}


.card-title {

    display: flex;

    align-items:
        center;

    gap:
        13px;

}


.ai-symbol {

    width: 46px;
    height: 46px;

    display: flex;

    align-items:
        center;

    justify-content:
        center;

    border-radius:
        14px;

    font-size:
        22px;

    background:

        linear-gradient(
            135deg,
            #00d9bb,
            #7655ff
        );

    box-shadow:

        0 0 28px
        rgba(0,255,220,0.20);

    animation:
        aiFloat 3s
        ease-in-out
        infinite;

}


@keyframes aiFloat {

    50% {

        transform:
            translateY(-5px)
            rotate(4deg);

    }

}


.title-main {

    font-size:
        17px;

    font-weight:
        850;

}


.title-sub {

    margin-top:
        4px;

    color:
        #6d6d83;

    font-size:
        11px;

}


.model-chip {

    padding:
        8px 12px;

    border-radius:
        9px;

    background:
        rgba(255,255,255,0.045);

    border:
        1px solid
        rgba(255,255,255,0.08);

    color:
        #77778d;

    font-size:
        10px;

    letter-spacing:
        1px;

}


/* =========================================================
   INPUT GRID
========================================================= */

.input-grid {

    display: grid;

    grid-template-columns:
        repeat(2, 1fr);

    gap:
        20px;

}


/* =========================================================
   INPUT CARD
========================================================= */

.input-card {

    position:
        relative;

    padding:
        23px;

    border-radius:
        20px;

    background:
        rgba(5,5,18,0.62);

    border:
        1px solid
        rgba(255,255,255,0.08);

    overflow:
        hidden;

    transition:
        0.35s;

}


.input-card:hover {

    transform:
        translateY(-6px);

    border-color:
        rgba(0,255,220,0.34);

    box-shadow:
        0 18px 40px
        rgba(0,0,0,0.25);

}


.input-card::before {

    content: "";

    position: absolute;

    width: 100px;
    height: 100px;

    right:
        -60px;

    top:
        -60px;

    border-radius:
        50%;

    background:
        #00ffe0;

    filter:
        blur(45px);

    opacity:
        0;

    transition:
        0.4s;

}


.input-card:hover::before {

    opacity:
        0.13;

}


/* =========================================================
   LABEL
========================================================= */

.label {

    display:
        flex;

    align-items:
        center;

    gap:
        11px;

    margin-bottom:
        14px;

}


.icon {

    width:
        38px;

    height:
        38px;

    display:
        flex;

    align-items:
        center;

    justify-content:
        center;

    border-radius:
        11px;

    font-size:
        18px;

}


.cgpa-icon {

    color:
        #00ffe0;

    background:
        rgba(0,255,220,0.08);

}


.resume-icon {

    color:
        #ff4ba5;

    background:
        rgba(255,60,150,0.09);

}


.label-name {

    font-size:
        13px;

    font-weight:
        850;

}


.label-help {

    color:
        #64647b;

    font-size:
        10px;

    margin-top:
        3px;

}


/* =========================================================
   INPUT
========================================================= */

input {

    width:
        100%;

    padding:
        15px 16px;

    border-radius:
        13px;

    outline:
        none;

    border:
        1px solid
        rgba(255,255,255,0.10);

    background:
        rgba(255,255,255,0.045);

    color:
        #ffffff;

    font-size:
        16px;

    font-weight:
        700;

    transition:
        0.3s;

}


input::placeholder {

    color:
        #525267;

}


input:focus {

    border-color:
        #00ffe0;

    box-shadow:

        0 0 0 3px
        rgba(0,255,220,0.06),

        0 0 30px
        rgba(0,255,220,0.10);

}


/* =========================================================
   SCORE BAR
========================================================= */

.score-bar {

    height:
        6px;

    margin-top:
        14px;

    border-radius:
        30px;

    overflow:
        hidden;

    background:
        rgba(255,255,255,0.06);

}


.score-fill {

    height:
        100%;

    width:
        0%;

    border-radius:
        30px;

    transition:
        width 0.45s ease;

}


.cgpa-fill {

    background:
        linear-gradient(
            90deg,
            #00ffe0,
            #00a8ff
        );

    box-shadow:
        0 0 15px
        rgba(0,255,220,0.5);

}


.resume-fill {

    background:
        linear-gradient(
            90deg,
            #ff3c9a,
            #815cff
        );

    box-shadow:
        0 0 15px
        rgba(255,60,150,0.45);

}


/* =========================================================
   BUTTON
========================================================= */

.action {

    text-align:
        center;

    margin-top:
        30px;

}


.predict-btn {

    position:
        relative;

    width:
        370px;

    max-width:
        100%;

    padding:
        19px 28px;

    border:
        none;

    border-radius:
        17px;

    cursor:
        pointer;

    overflow:
        hidden;

    color:
        white;

    font-size:
        14px;

    font-weight:
        950;

    letter-spacing:
        2px;

    background:

        linear-gradient(
            100deg,
            #00cdb3,
            #6658ff,
            #ff328e,
            #ff9f43,
            #00cdb3
        );

    background-size:
        400%;

    animation:
        buttonFlow
        6s linear infinite;

    box-shadow:

        0 15px 45px
        rgba(0,0,0,0.35),

        0 0 30px
        rgba(0,220,190,0.16);

    transition:
        0.3s;

}


@keyframes buttonFlow {

    to {
        background-position:
            400%;
    }

}


.predict-btn:hover {

    transform:
        translateY(-5px)
        scale(1.025);

    box-shadow:

        0 20px 60px
        rgba(0,0,0,0.45),

        0 0 55px
        rgba(115,80,255,0.35);

}


.predict-btn:active {

    transform:
        scale(0.94);

}


.predict-btn::before {

    content: "";

    position:
        absolute;

    top:
        0;

    left:
        -100%;

    width:
        55%;

    height:
        100%;

    transform:
        skewX(-20deg);

    background:

        linear-gradient(
            100deg,
            transparent,
            rgba(255,255,255,0.55),
            transparent
        );

}


.predict-btn:hover::before {

    animation:
        buttonShine
        0.8s;

}


@keyframes buttonShine {

    to {
        left:
            150%;
    }

}


/* =========================================================
   RESULT
========================================================= */

.result {

    margin-top:
        30px;

    padding:
        32px;

    text-align:
        center;

    border-radius:
        25px;

    animation:
        resultReveal
        0.9s
        cubic-bezier(.16,1,.3,1);

}


.result.pass {

    border:
        1px solid
        rgba(0,255,160,0.38);

    background:

        radial-gradient(
            circle at 50% 0%,
            rgba(0,255,160,0.13),
            transparent 65%
        ),

        rgba(0,255,160,0.025);

}


.result.fail {

    border:
        1px solid
        rgba(255,60,100,0.38);

    background:

        radial-gradient(
            circle at 50% 0%,
            rgba(255,60,100,0.13),
            transparent 65%
        ),

        rgba(255,60,100,0.025);

}


@keyframes resultReveal {

    0% {

        opacity:
            0;

        transform:
            translateY(50px)
            scale(0.78)
            rotateX(18deg);

    }

    70% {

        transform:
            translateY(-6px)
            scale(1.03);

    }

    100% {

        opacity:
            1;

        transform:
            translateY(0)
            scale(1)
            rotateX(0);

    }

}


.result-orb {

    width:
        105px;

    height:
        105px;

    margin:
        0 auto 20px;

    display:
        flex;

    align-items:
        center;

    justify-content:
        center;

    border-radius:
        50%;

    font-size:
        45px;

    animation:
        resultPulse
        1.4s
        ease-in-out
        infinite alternate;

}


.pass .result-orb {

    border:
        2px solid
        #00ff9d;

    background:
        rgba(0,255,150,0.07);

    box-shadow:

        0 0 35px
        rgba(0,255,150,0.28),

        inset
        0 0 30px
        rgba(0,255,150,0.08);

}


.fail .result-orb {

    border:
        2px solid
        #ff416c;

    background:
        rgba(255,50,90,0.07);

    box-shadow:

        0 0 35px
        rgba(255,50,90,0.28),

        inset
        0 0 30px
        rgba(255,50,90,0.08);

}


@keyframes resultPulse {

    from {
        transform:
            scale(1);
    }

    to {
        transform:
            scale(1.09);
    }

}


.result h2 {

    font-size:
        30px;

    margin-bottom:
        9px;

}


.result p {

    color:
        #9292a8;

}


/* =========================================================
   CONFIDENCE
========================================================= */

.confidence {

    max-width:
        500px;

    margin:
        26px auto 0;

    text-align:
        left;

}


.confidence-head {

    display:
        flex;

    justify-content:
        space-between;

    margin-bottom:
        9px;

    color:
        #77778e;

    font-size:
        11px;

    letter-spacing:
        1px;

}


.confidence-track {

    height:
        9px;

    border-radius:
        20px;

    overflow:
        hidden;

    background:
        rgba(255,255,255,0.07);

}


.confidence-fill {

    width:
        {{ confidence }}%;

    height:
        100%;

    border-radius:
        20px;

    background:

        linear-gradient(
            90deg,
            #00ffe0,
            #725cff,
            #ff3d9a
        );

    box-shadow:
        0 0 18px
        rgba(120,80,255,0.55);

    animation:
        confidenceGrow
        1.4s ease-out;

}


@keyframes confidenceGrow {

    from {
        width:
            0%;
    }

}


/* =========================================================
   AI SCANNING SCREEN
========================================================= */

.scan-screen {

    position:
        fixed;

    inset:
        0;

    z-index:
        99999;

    display:
        none;

    align-items:
        center;

    justify-content:
        center;

    flex-direction:
        column;

    background:
        rgba(3,3,14,0.95);

    backdrop-filter:
        blur(18px);

}


.scan-screen.active {

    display:
        flex;

}


/* =========================================================
   NEURAL AI CORE
========================================================= */

.ai-core {

    position:
        relative;

    width:
        190px;

    height:
        190px;

    display:
        flex;

    align-items:
        center;

    justify-content:
        center;

}


.core {

    width:
        68px;

    height:
        68px;

    display:
        flex;

    align-items:
        center;

    justify-content:
        center;

    border-radius:
        50%;

    font-size:
        25px;

    background:

        radial-gradient(
            circle,
            #ffffff 0%,
            #00ffe0 20%,
            #715cff 55%,
            transparent 72%
        );

    box-shadow:

        0 0 30px
        #00ffe0,

        0 0 70px
        rgba(110,90,255,0.65);

    animation:
        corePulse
        0.9s
        infinite alternate;

}


@keyframes corePulse {

    from {
        transform:
            scale(0.78);
    }

    to {
        transform:
            scale(1.12);
    }

}


.ring {

    position:
        absolute;

    border-radius:
        50%;

    border:
        2px solid
        transparent;

}


.ring-a {

    width:
        105px;

    height:
        105px;

    border-top-color:
        #00ffe0;

    border-right-color:
        #00ffe0;

    animation:
        spin
        0.9s linear infinite;

}


.ring-b {

    width:
        140px;

    height:
        140px;

    border-left-color:
        #ff3c9a;

    border-bottom-color:
        #715cff;

    animation:
        spinReverse
        1.5s linear infinite;

}


.ring-c {

    width:
        178px;

    height:
        178px;

    border-top-color:
        #ffb347;

    border-bottom-color:
        #00ffe0;

    opacity:
        0.6;

    animation:
        spin
        2.3s linear infinite;

}


@keyframes spin {

    to {
        transform:
            rotate(360deg);
    }

}


@keyframes spinReverse {

    to {
        transform:
            rotate(-360deg);
    }

}


/* =========================================================
   SCANNING LINE
========================================================= */

.scan-line {

    position:
        absolute;

    width:
        220px;

    height:
        2px;

    background:

        linear-gradient(
            90deg,
            transparent,
            #00ffe0,
            #ffffff,
            #00ffe0,
            transparent
        );

    box-shadow:
        0 0 20px
        #00ffe0;

    animation:
        scanLine
        1.2s
        ease-in-out
        infinite;

}


@keyframes scanLine {

    0% {

        transform:
            translateY(-95px);

        opacity:
            0;

    }

    20% {
        opacity:
            1;
    }

    80% {
        opacity:
            1;
    }

    100% {

        transform:
            translateY(95px);

        opacity:
            0;

    }

}


/* =========================================================
   SCAN TEXT
========================================================= */

.scan-title {

    margin-top:
        42px;

    color:
        #00ffe0;

    font-size:
        16px;

    font-weight:
        950;

    letter-spacing:
        4px;

    animation:
        scanBlink
        0.8s
        infinite alternate;

}


.scan-subtitle {

    margin-top:
        10px;

    color:
        #696981;

    font-size:
        12px;

}


.scan-dots {

    margin-top:
        16px;

    color:
        #755cff;

    letter-spacing:
        6px;

}


@keyframes scanBlink {

    from {
        opacity:
            0.3;
    }

    to {
        opacity:
            1;
    }

}


/* =========================================================
   FOOTER
========================================================= */

.footer {

    text-align:
        center;

    margin-top:
        25px;

    color:
        #505065;

    font-size:
        10px;

    letter-spacing:
        1.5px;

}


/* =========================================================
   MOBILE
========================================================= */

@media(max-width: 720px) {

    .page {

        padding-top:
            25px;

    }


    .card {

        padding:
            20px;

        border-radius:
            23px;

    }


    .input-grid {

        grid-template-columns:
            1fr;

    }


    .model-chip {

        display:
            none;

    }


    .header h1 {

        letter-spacing:
            -3px;

    }


    .predict-btn {

        width:
            100%;

    }


    .card-header {

        margin-bottom:
            22px;

    }


    .result h2 {

        font-size:
            24px;

    }

}

</style>

</head>


<body>


<!-- =======================================================
     BACKGROUND
======================================================= -->

<div class="light-orb orb-1"></div>
<div class="light-orb orb-2"></div>
<div class="light-orb orb-3"></div>


<div class="particles">

    <div class="particle"
         style="left:4%; animation-duration:11s;"></div>

    <div class="particle"
         style="left:12%; animation-duration:8s;"></div>

    <div class="particle"
         style="left:22%; animation-duration:13s;"></div>

    <div class="particle"
         style="left:34%; animation-duration:10s;"></div>

    <div class="particle"
         style="left:47%; animation-duration:15s;"></div>

    <div class="particle"
         style="left:60%; animation-duration:9s;"></div>

    <div class="particle"
         style="left:73%; animation-duration:12s;"></div>

    <div class="particle"
         style="left:86%; animation-duration:8s;"></div>

    <div class="particle"
         style="left:95%; animation-duration:14s;"></div>

</div>


<!-- =======================================================
     AI SCANNING SCREEN
======================================================= -->

<div
    class="scan-screen"
    id="scanScreen"
>


    <div class="ai-core">

        <div class="ring ring-a"></div>

        <div class="ring ring-b"></div>

        <div class="ring ring-c"></div>

        <div class="scan-line"></div>

        <div class="core">

            ✦

        </div>

    </div>


    <div class="scan-title">

        AI ANALYZING CANDIDATE

    </div>


    <div class="scan-subtitle">

        Perceptron decision engine is processing your profile...

    </div>


    <div class="scan-dots">

        ● ● ●

    </div>


</div>


<!-- =======================================================
     MAIN PAGE
======================================================= -->

<div class="page">


    <!-- HEADER -->

    <div class="header">


        <div class="online">

            <span class="online-dot"></span>

            NEUROHIRE AI • SYSTEM ONLINE

        </div>


        <h1>

            NeuroHire<br>AI

        </h1>


        <p>

            Intelligent candidate prediction powered by machine learning.

        </p>


    </div>


    <!-- ===================================================
         MAIN CARD
    =================================================== -->

    <div
        class="card"
        id="mainCard"
    >


        <div class="card-header">


            <div class="card-title">


                <div class="ai-symbol">

                    ✦

                </div>


                <div>

                    <div class="title-main">

                        Candidate Intelligence

                    </div>


                    <div class="title-sub">

                        Enter performance metrics to generate a prediction

                    </div>

                </div>


            </div>


            <div class="model-chip">

                PERCEPTRON MODEL

            </div>


        </div>


        <!-- =================================================
             FORM
        ================================================= -->

        <form
            method="POST"
            id="predictionForm"
        >


            <div class="input-grid">


                <!-- CGPA -->

                <div class="input-card">


                    <div class="label">


                        <div class="icon cgpa-icon">

                            🎓

                        </div>


                        <div>

                            <div class="label-name">

                                CGPA

                            </div>


                            <div class="label-help">

                                Academic performance • 0 to 10

                            </div>

                        </div>


                    </div>


                    <input
                        type="number"
                        name="cgpa"
                        id="cgpa"
                        min="0"
                        max="10"
                        step="0.01"
                        placeholder="e.g. 8.50"
                        required
                    >


                    <div class="score-bar">

                        <div
                            class="score-fill cgpa-fill"
                            id="cgpaFill"
                        ></div>

                    </div>


                </div>


                <!-- RESUME SCORE -->

                <div class="input-card">


                    <div class="label">


                        <div class="icon resume-icon">

                            📄

                        </div>


                        <div>

                            <div class="label-name">

                                Resume Score

                            </div>


                            <div class="label-help">

                                Resume evaluation • 0 to 100

                            </div>

                        </div>


                    </div>


                    <input
                        type="number"
                        name="resume_score"
                        id="resumeScore"
                        min="0"
                        max="100"
                        step="0.01"
                        placeholder="e.g. 82"
                        required
                    >


                    <div class="score-bar">

                        <div
                            class="score-fill resume-fill"
                            id="resumeFill"
                        ></div>

                    </div>


                </div>


            </div>


            <!-- =================================================
                 PREDICT BUTTON
            ================================================= -->

            <div class="action">


                <button
                    type="submit"
                    class="predict-btn"
                    id="predictBtn"
                >

                    <span id="buttonText">

                        ✦ RUN AI PREDICTION

                    </span>

                </button>


            </div>


        </form>


        <!-- =================================================
             RESULT
        ================================================= -->

        {% if prediction is not none %}


        <div
            class="result
            {% if prediction == 1 %}
                pass
            {% else %}
                fail
            {% endif %}"
        >


            <div class="result-orb">


                {% if prediction == 1 %}

                    🚀

                {% else %}

                    ⚠️

                {% endif %}


            </div>


            {% if prediction == 1 %}


                <h2>

                    Positive Prediction

                </h2>


                <p>

                    The Perceptron model classified this candidate as Class 1.

                </p>


            {% else %}


                <h2>

                    Negative Prediction

                </h2>


                <p>

                    The Perceptron model classified this candidate as Class 0.

                </p>


            {% endif %}


            {% if confidence is not none %}


            <div class="confidence">


                <div class="confidence-head">

                    <span>

                        MODEL SCORE

                    </span>


                    <span>

                        {{ confidence }}%

                    </span>

                </div>


                <div class="confidence-track">

                    <div
                        class="confidence-fill"
                    ></div>

                </div>


            </div>


            {% endif %}


        </div>


        {% endif %}


    </div>


    <div class="footer">

        POWERED BY SCIKIT-LEARN • PERCEPTRON • NEUROHIRE AI

    </div>


</div>


<script>

/* =========================================================
   CGPA METER
========================================================= */

const cgpa =
    document.getElementById("cgpa");

const cgpaFill =
    document.getElementById("cgpaFill");


cgpa.addEventListener(
    "input",
    function() {

        let value =
            parseFloat(cgpa.value) || 0;

        let percentage =
            Math.min(
                Math.max(
                    (value / 10) * 100,
                    0
                ),
                100
            );

        cgpaFill.style.width =
            percentage + "%";

    }
);


/* =========================================================
   RESUME SCORE METER
========================================================= */

const resumeScore =
    document.getElementById("resumeScore");

const resumeFill =
    document.getElementById("resumeFill");


resumeScore.addEventListener(
    "input",
    function() {

        let value =
            parseFloat(resumeScore.value) || 0;

        let percentage =
            Math.min(
                Math.max(
                    value,
                    0
                ),
                100
            );

        resumeFill.style.width =
            percentage + "%";

    }
);


/* =========================================================
   PREDICT BUTTON EFFECT
========================================================= */

const form =
    document.getElementById(
        "predictionForm"
    );


const button =
    document.getElementById(
        "predictBtn"
    );


const buttonText =
    document.getElementById(
        "buttonText"
    );


const scanScreen =
    document.getElementById(
        "scanScreen"
    );


form.addEventListener(
    "submit",
    function() {


        /*
         * Show full-screen
         * AI scanning animation.
         */

        scanScreen.classList.add(
            "active"
        );


        /*
         * Prevent double click.
         */

        button.disabled =
            true;


        /*
         * Change button text.
         */

        buttonText.innerHTML =
            "◉  ANALYZING PROFILE...";


    }
);


/* =========================================================
   3D CARD MOUSE EFFECT
========================================================= */

const mainCard =
    document.getElementById(
        "mainCard"
    );


document.addEventListener(
    "mousemove",
    function(event) {


        if (
            window.innerWidth < 850
        ) {

            return;

        }


        const x =
            (
                window.innerWidth / 2 -
                event.clientX
            ) / 150;


        const y =
            (
                window.innerHeight / 2 -
                event.clientY
            ) / 150;


        mainCard.style.transform =
            `perspective(1400px)
             rotateY(${x}deg)
             rotateX(${-y}deg)`;


    }
);


document.addEventListener(
    "mouseleave",
    function() {

        mainCard.style.transform =
            "perspective(1400px) rotateY(0deg) rotateX(0deg)";

    }
);


/* =========================================================
   INPUT FOCUS EFFECT
========================================================= */

document.querySelectorAll(
    "input"
).forEach(
    function(input) {

        input.addEventListener(
            "focus",
            function() {

                this.closest(
                    ".input-card"
                ).style.transform =
                    "translateY(-6px)";

            }
        );


        input.addEventListener(
            "blur",
            function() {

                this.closest(
                    ".input-card"
                ).style.transform =
                    "translateY(0)";

            }
        );

    }
);

</script>


</body>

</html>
"""


# ============================================================
# FLASK ROUTE
# ============================================================

@app.route("/", methods=["GET", "POST"])
def home():

    prediction = None
    confidence = None

    if request.method == "POST":

        try:

            # ------------------------------------------------
            # GET USER INPUT
            # ------------------------------------------------

            cgpa = float(
                request.form["cgpa"]
            )

            resume_score = float(
                request.form["resume_score"]
            )


            # ------------------------------------------------
            # MODEL INPUT
            #
            # EXACT ORDER EXPECTED BY MODEL:
            #
            # cgpa
            # resume_score
            # ------------------------------------------------

            features = [[
                cgpa,
                resume_score
            ]]


            # ------------------------------------------------
            # PREDICTION
            # ------------------------------------------------

            prediction = model.predict(
                features
            )[0]


            # ------------------------------------------------
            # PERCEPTRON SCORE
            # ------------------------------------------------

            if hasattr(
                model,
                "decision_function"
            ):

                # ------------------------------------------------
            # PERCEPTRON SCORE
            # ------------------------------------------------

            if hasattr(
                model,
                "decision_function"
            ):

                decision = float(model.decision_function(features)[0])

                # Convert decision score into a
                # probability-like visual score.
                #

                # Convert decision score into a
                # probability-like visual score.
                #
                # This is NOT a true probability because
                # Perceptron does not provide predict_proba().

                probability_like = (
                    1 /
                    (
                        1 +
                        math.exp(
                            -max(
                                min(
                                    decision,
                                    20
                                ),
                                -20
                            )
                        )
                    )
                )


                if int(prediction) == 1:

                    confidence = round(
                        probability_like * 100,
                        2
                    )

                else:

                    confidence = round(
                        (1 - probability_like) * 100,
                        2
                    )


        except Exception as e:

            print(
                "Prediction Error:",
                e
            )

            prediction = None


    return render_template_string(
        HTML,
        prediction=prediction,
        confidence=confidence
    )


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(
            os.environ.get(
                "PORT",
                5000
            )
        ),
        debug=False
    )
