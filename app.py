from flask import Flask, request, render_template_string
import joblib
import os
import math

app = Flask(__name__)

# ============================================================
# LOAD PERCEPTRON MODEL
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
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>NeuroHire AI | Perceptron Predictor</title>

    <style>

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        html {
            scroll-behavior: smooth;
        }

        body {
            min-height: 100vh;
            font-family: Arial, Helvetica, sans-serif;
            color: white;
            overflow-x: hidden;

            background:
                radial-gradient(circle at 15% 20%, rgba(0, 255, 255, 0.16), transparent 28%),
                radial-gradient(circle at 85% 25%, rgba(168, 85, 247, 0.18), transparent 30%),
                radial-gradient(circle at 50% 90%, rgba(236, 72, 153, 0.14), transparent 28%),
                #050816;
        }

        /* ====================================================
           BACKGROUND GRID
        ==================================================== */

        body::before {
            content: "";
            position: fixed;
            inset: 0;

            background-image:
                linear-gradient(rgba(255,255,255,0.035) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255,255,255,0.035) 1px, transparent 1px);

            background-size: 50px 50px;

            mask-image: linear-gradient(
                to bottom,
                transparent,
                black 20%,
                black 80%,
                transparent
            );

            pointer-events: none;
            z-index: -3;
        }


        /* ====================================================
           GLOWING ORBS
        ==================================================== */

        .orb {
            position: fixed;
            border-radius: 50%;
            filter: blur(3px);
            pointer-events: none;
            z-index: -2;
        }

        .orb-one {
            width: 240px;
            height: 240px;

            background: rgba(0, 255, 255, 0.14);

            top: 8%;
            left: -70px;

            animation: floatOne 8s ease-in-out infinite;
        }

        .orb-two {
            width: 280px;
            height: 280px;

            background: rgba(168, 85, 247, 0.14);

            right: -90px;
            top: 35%;

            animation: floatTwo 10s ease-in-out infinite;
        }

        .orb-three {
            width: 200px;
            height: 200px;

            background: rgba(236, 72, 153, 0.12);

            bottom: -50px;
            left: 35%;

            animation: floatThree 9s ease-in-out infinite;
        }

        @keyframes floatOne {
            0%, 100% {
                transform: translate(0, 0);
            }

            50% {
                transform: translate(70px, 100px);
            }
        }

        @keyframes floatTwo {
            0%, 100% {
                transform: translate(0, 0);
            }

            50% {
                transform: translate(-90px, -70px);
            }
        }

        @keyframes floatThree {
            0%, 100% {
                transform: translate(0, 0);
            }

            50% {
                transform: translate(80px, -80px);
            }
        }


        /* ====================================================
           PARTICLES
        ==================================================== */

        .particles {
            position: fixed;
            inset: 0;
            pointer-events: none;
            z-index: -1;
        }

        .particle {
            position: absolute;
            width: 3px;
            height: 3px;
            border-radius: 50%;
            background: rgba(255,255,255,0.55);
            box-shadow: 0 0 12px rgba(0,255,255,0.7);
            animation: particleFloat linear infinite;
        }

        .p1 { left: 10%; top: 30%; animation-duration: 9s; }
        .p2 { left: 22%; top: 70%; animation-duration: 12s; }
        .p3 { left: 38%; top: 18%; animation-duration: 10s; }
        .p4 { left: 55%; top: 80%; animation-duration: 14s; }
        .p5 { left: 70%; top: 22%; animation-duration: 11s; }
        .p6 { left: 84%; top: 65%; animation-duration: 8s; }
        .p7 { left: 92%; top: 15%; animation-duration: 13s; }
        .p8 { left: 47%; top: 45%; animation-duration: 10s; }

        @keyframes particleFloat {
            0% {
                transform: translateY(0) scale(1);
                opacity: 0.2;
            }

            50% {
                transform: translateY(-80px) scale(1.5);
                opacity: 1;
            }

            100% {
                transform: translateY(-160px) scale(0.5);
                opacity: 0;
            }
        }


        /* ====================================================
           MAIN CONTAINER
        ==================================================== */

        .page {
            width: 100%;
            min-height: 100vh;
            padding: 45px 20px 70px;
        }

        .container {
            max-width: 1100px;
            margin: auto;
        }


        /* ====================================================
           HEADER
        ==================================================== */

        .top-badge {
            width: fit-content;
            margin: 0 auto 18px;

            padding: 9px 18px;

            border: 1px solid rgba(0,255,255,0.3);
            border-radius: 999px;

            background: rgba(0,255,255,0.06);

            color: #7df9ff;

            font-size: 12px;
            font-weight: bold;
            letter-spacing: 2px;

            box-shadow:
                0 0 20px rgba(0,255,255,0.08);
        }

        .header {
            text-align: center;
            margin-bottom: 42px;
        }

        .header h1 {
            font-size: clamp(38px, 7vw, 76px);
            line-height: 0.95;
            font-weight: 900;
            letter-spacing: -3px;

            background: linear-gradient(
                90deg,
                #67e8f9,
                #a78bfa,
                #f472b6,
                #67e8f9
            );

            background-size: 300% auto;

            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;

            animation: gradientMove 5s linear infinite;
        }

        @keyframes gradientMove {
            0% {
                background-position: 0% center;
            }

            100% {
                background-position: 300% center;
            }
        }

        .header p {
            margin-top: 20px;
            color: #a7b0c8;
            font-size: 16px;
            line-height: 1.7;
        }


        /* ====================================================
           MAIN CARD
        ==================================================== */

        .main-card {
            position: relative;

            padding: 42px;

            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 30px;

            background:
                linear-gradient(
                    135deg,
                    rgba(255,255,255,0.09),
                    rgba(255,255,255,0.025)
                );

            backdrop-filter: blur(25px);
            -webkit-backdrop-filter: blur(25px);

            box-shadow:
                0 30px 100px rgba(0,0,0,0.45),
                inset 0 1px 0 rgba(255,255,255,0.08);

            overflow: hidden;

            transition: transform 0.15s ease;
        }

        .main-card::before {
            content: "";
            position: absolute;

            top: 0;
            left: 8%;

            width: 84%;
            height: 1px;

            background: linear-gradient(
                90deg,
                transparent,
                #67e8f9,
                #a78bfa,
                #f472b6,
                transparent
            );

            box-shadow: 0 0 25px #67e8f9;
        }


        /* ====================================================
           INPUT GRID
        ==================================================== */

        .input-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 25px;
        }

        .input-card {
            padding: 27px;

            border-radius: 22px;

            background: rgba(3, 7, 25, 0.55);

            border: 1px solid rgba(255,255,255,0.08);

            position: relative;

            overflow: hidden;

            transition:
                transform 0.3s ease,
                border-color 0.3s ease,
                box-shadow 0.3s ease;
        }

        .input-card:hover {
            transform: translateY(-5px);

            border-color: rgba(103,232,249,0.4);

            box-shadow:
                0 15px 45px rgba(0,0,0,0.25),
                0 0 30px rgba(103,232,249,0.06);
        }

        .input-number {
            width: 38px;
            height: 38px;

            display: flex;
            align-items: center;
            justify-content: center;

            border-radius: 12px;

            background: linear-gradient(
                135deg,
                #06b6d4,
                #6366f1
            );

            font-weight: 900;
            font-size: 14px;

            margin-bottom: 20px;

            box-shadow:
                0 8px 25px rgba(6,182,212,0.25);
        }

        .input-card:nth-child(2) .input-number {
            background: linear-gradient(
                135deg,
                #a855f7,
                #ec4899
            );

            box-shadow:
                0 8px 25px rgba(168,85,247,0.25);
        }

        .input-card h3 {
            font-size: 20px;
            margin-bottom: 7px;
        }

        .input-card p {
            color: #8791aa;
            font-size: 13px;
            margin-bottom: 22px;
        }


        /* ====================================================
           INPUT
        ==================================================== */

        .input-wrapper {
            position: relative;
        }

        .input-wrapper input {
            width: 100%;

            padding: 17px 18px;

            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 15px;

            background: rgba(255,255,255,0.045);

            color: white;

            outline: none;

            font-size: 18px;
            font-weight: bold;

            transition: 0.3s ease;
        }

        .input-wrapper input::placeholder {
            color: #5f6880;
        }

        .input-wrapper input:focus {
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


        /* ====================================================
           RANGE METER
        ==================================================== */

        .meter {
            margin-top: 18px;
        }

        .meter-top {
            display: flex;
            justify-content: space-between;

            color: #68738e;

            font-size: 11px;
            margin-bottom: 8px;
        }

        .meter-track {
            height: 6px;

            border-radius: 999px;

            background: rgba(255,255,255,0.06);

            overflow: hidden;
        }

        .meter-fill {
            width: 0%;
            height: 100%;

            border-radius: 999px;

            background: linear-gradient(
                90deg,
                #06b6d4,
                #22d3ee
            );

            box-shadow:
                0 0 15px rgba(34,211,238,0.7);

            transition: width 0.4s ease;
        }

        .input-card:nth-child(2) .meter-fill {
            background: linear-gradient(
                90deg,
                #a855f7,
                #ec4899
            );

            box-shadow:
                0 0 15px rgba(236,72,153,0.6);
        }


        /* ====================================================
           BUTTON
        ==================================================== */

        .predict-area {
            margin-top: 35px;
            text-align: center;
        }

        .predict-btn {
            position: relative;

            border: none;
            outline: none;

            padding: 18px 48px;

            border-radius: 999px;

            color: white;

            font-size: 15px;
            font-weight: 900;

            letter-spacing: 1px;

            cursor: pointer;

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

            box-shadow:
                0 12px 40px rgba(99,102,241,0.3),
                0 0 30px rgba(6,182,212,0.15);

            animation: buttonGradient 4s linear infinite;

            transition:
                transform 0.2s ease,
                box-shadow 0.2s ease;
        }

        @keyframes buttonGradient {
            0% {
                background-position: 0% center;
            }

            100% {
                background-position: 300% center;
            }
        }

        .predict-btn:hover {
            transform: translateY(-3px) scale(1.02);

            box-shadow:
                0 18px 55px rgba(99,102,241,0.45),
                0 0 45px rgba(6,182,212,0.2);
        }

        .predict-btn:active {
            transform: scale(0.97);
        }

        .predict-btn::after {
            content: "";

            position: absolute;

            top: -50%;
            left: -100%;

            width: 70%;
            height: 200%;

            transform: rotate(25deg);

            background: rgba(255,255,255,0.28);

            animation: shine 3s ease-in-out infinite;
        }

        @keyframes shine {
            0% {
                left: -100%;
            }

            35%, 100% {
                left: 150%;
            }
        }

        .small-note {
            margin-top: 15px;
            color: #606b84;
            font-size: 11px;
        }


        /* ====================================================
           ERROR
        ==================================================== */

        .error {
            margin-bottom: 25px;

            padding: 16px 20px;

            border-radius: 15px;

            background: rgba(239,68,68,0.1);

            border: 1px solid rgba(239,68,68,0.3);

            color: #fca5a5;

            text-align: center;

            font-size: 14px;
        }


        /* ====================================================
           RESULT
        ==================================================== */

        .result {
            margin-top: 35px;

            padding: 30px;

            border-radius: 25px;

            text-align: center;

            border: 1px solid rgba(255,255,255,0.1);

            background: rgba(255,255,255,0.035);

            animation: resultAppear 0.7s ease forwards;
        }

        @keyframes resultAppear {
            from {
                opacity: 0;
                transform: translateY(25px) scale(0.96);
            }

            to {
                opacity: 1;
                transform: translateY(0) scale(1);
            }
        }

        .result-icon {
            width: 78px;
            height: 78px;

            margin: 0 auto 18px;

            border-radius: 50%;

            display: flex;
            align-items: center;
            justify-content: center;

            font-size: 32px;

            animation: iconPulse 2s ease-in-out infinite;
        }

        @keyframes iconPulse {
            0%, 100% {
                transform: scale(1);
            }

            50% {
                transform: scale(1.08);
            }
        }

        .result.positive {
            border-color: rgba(52,211,153,0.35);

            box-shadow:
                0 0 50px rgba(52,211,153,0.08);
        }

        .result.positive .result-icon {
            background: rgba(16,185,129,0.13);
            color: #34d399;

            box-shadow:
                0 0 35px rgba(52,211,153,0.2);
        }

        .result.negative {
            border-color: rgba(248,113,113,0.35);

            box-shadow:
                0 0 50px rgba(248,113,113,0.07);
        }

        .result.negative .result-icon {
            background: rgba(239,68,68,0.13);
            color: #f87171;

            box-shadow:
                0 0 35px rgba(248,113,113,0.18);
        }

        .result h2 {
            font-size: 30px;
            margin-bottom: 10px;
        }

        .result p {
            color: #8d97ae;
            font-size: 14px;
        }

        .score-box {
            max-width: 520px;
            margin: 25px auto 0;
        }

        .score-header {
            display: flex;
            justify-content: space-between;

            margin-bottom: 9px;

            font-size: 12px;
            color: #8d97ae;
        }

        .score-header strong {
            color: white;
        }

        .score-track {
            height: 10px;

            border-radius: 999px;

            background: rgba(255,255,255,0.06);

            overflow: hidden;
        }

        .score-fill {
            height: 100%;

            width: {{ confidence }}%;

            border-radius: 999px;

            background:
                linear-gradient(
                    90deg,
                    #06b6d4,
                    #6366f1,
                    #a855f7,
                    #ec4899
                );

            box-shadow:
                0 0 20px rgba(168,85,247,0.45);

            animation: scoreLoad 1.2s ease;
        }

        @keyframes scoreLoad {
            from {
                width: 0%;
            }

            to {
                width: {{ confidence }}%;
            }
        }


        /* ====================================================
           INFO ROW
        ==================================================== */

        .info-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;

            max-width: 520px;

            margin: 22px auto 0;
        }

        .info-box {
            padding: 15px;

            border-radius: 15px;

            background: rgba(255,255,255,0.035);

            border: 1px solid rgba(255,255,255,0.06);
        }

        .info-box span {
            display: block;

            color: #69738b;

            font-size: 10px;

            text-transform: uppercase;

            letter-spacing: 1px;

            margin-bottom: 6px;
        }

        .info-box strong {
            font-size: 17px;
        }


        /* ====================================================
           SCANNING OVERLAY
        ==================================================== */

        .scan-overlay {
            position: fixed;
            inset: 0;

            display: none;
            align-items: center;
            justify-content: center;

            background:
                radial-gradient(
                    circle,
                    rgba(12,18,50,0.72),
                    rgba(2,4,15,0.97)
                );

            backdrop-filter: blur(10px);

            z-index: 9999;
        }

        .scan-overlay.active {
            display: flex;
        }

        .scanner {
            position: relative;

            width: 260px;
            height: 260px;

            display: flex;
            align-items: center;
            justify-content: center;
        }

        .ring {
            position: absolute;

            border-radius: 50%;

            border: 1px solid rgba(103,232,249,0.5);

            animation: ringRotate 3s linear infinite;
        }

        .ring-one {
            width: 250px;
            height: 250px;

            border-top-color: #67e8f9;
            border-bottom-color: #a78bfa;
        }

        .ring-two {
            width: 190px;
            height: 190px;

            border-left-color: #ec4899;
            border-right-color: #67e8f9;

            animation-direction: reverse;
            animation-duration: 2s;
        }

        .ring-three {
            width: 135px;
            height: 135px;

            border-top-color: #f472b6;
            border-right-color: #67e8f9;

            animation-duration: 1.5s;
        }

        @keyframes ringRotate {
            from {
                transform: rotate(0deg);
            }

            to {
                transform: rotate(360deg);
            }
        }

        .ai-core {
            width: 75px;
            height: 75px;

            border-radius: 50%;

            display: flex;
            align-items: center;
            justify-content: center;

            font-size: 28px;

            background:
                radial-gradient(
                    circle,
                    #ffffff,
                    #67e8f9 20%,
                    #6366f1 55%,
                    #a855f7 100%
                );

            color: #070a1c;

            box-shadow:
                0 0 25px #67e8f9,
                0 0 60px rgba(168,85,247,0.7);

            animation: corePulse 1s ease-in-out infinite;
        }

        @keyframes corePulse {
            0%, 100% {
                transform: scale(0.92);
                box-shadow:
                    0 0 20px #67e8f9,
                    0 0 40px rgba(168,85,247,0.5);
            }

            50% {
                transform: scale(1.08);
                box-shadow:
                    0 0 35px #67e8f9,
                    0 0 80px rgba(168,85,247,0.8);
            }
        }

        .scan-line {
            position: absolute;

            width: 280px;
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

            box-shadow:
                0 0 15px #67e8f9;

            animation: scanLine 1.5s ease-in-out infinite;
        }

        @keyframes scanLine {
            0%, 100% {
                transform: translateY(-105px);
                opacity: 0;
            }

            20% {
                opacity: 1;
            }

            50% {
                transform: translateY(105px);
                opacity: 1;
            }

            80% {
                opacity: 0;
            }
        }

        .scan-text {
            position: absolute;

            top: calc(50% + 155px);

            text-align: center;

            width: 100%;

            font-size: 14px;

            font-weight: bold;

            letter-spacing: 3px;

            color: #c4f7ff;

            animation: textBlink 0.8s infinite alternate;
        }

        @keyframes textBlink {
            from {
                opacity: 0.45;
            }

            to {
                opacity: 1;
            }
        }


        /* ====================================================
           FOOTER
        ==================================================== */

        footer {
            text-align: center;

            margin-top: 35px;

            color: #4e5870;

            font-size: 11px;

            letter-spacing: 1px;
        }


        /* ====================================================
           RESPONSIVE
        ==================================================== */

        @media (max-width: 750px) {

            .page {
                padding: 30px 15px 50px;
            }

            .main-card {
                padding: 22px;
                border-radius: 22px;
            }

            .input-grid {
                grid-template-columns: 1fr;
            }

            .header {
                margin-bottom: 28px;
            }

            .header h1 {
                letter-spacing: -2px;
            }

            .header p {
                font-size: 14px;
            }

            .predict-btn {
                width: 100%;
            }

            .info-row {
                grid-template-columns: 1fr;
            }
        }

    </style>
</head>


<body>

    <!-- BACKGROUND -->
    <div class="orb orb-one"></div>
    <div class="orb orb-two"></div>
    <div class="orb orb-three"></div>

    <div class="particles">
        <span class="particle p1"></span>
        <span class="particle p2"></span>
        <span class="particle p3"></span>
        <span class="particle p4"></span>
        <span class="particle p5"></span>
        <span class="particle p6"></span>
        <span class="particle p7"></span>
        <span class="particle p8"></span>
    </div>


    <!-- SCANNING OVERLAY -->

    <div class="scan-overlay" id="scanOverlay">

        <div class="scanner">

            <div class="ring ring-one"></div>
            <div class="ring ring-two"></div>
            <div class="ring ring-three"></div>

            <div class="scan-line"></div>

            <div class="ai-core">
                AI
            </div>

        </div>

        <div class="scan-text">
            ANALYZING CANDIDATE...
        </div>

    </div>


    <!-- MAIN PAGE -->

    <div class="page">

        <div class="container">

            <!-- HEADER -->

            <div class="header">

                <div class="top-badge">
                    ⚡ PERCEPTRON INTELLIGENCE SYSTEM
                </div>

                <h1>
                    NeuroHire AI
                </h1>

                <p>
                    Intelligent candidate prediction powered by
                    Machine Learning and Perceptron technology.
                </p>

            </div>


            <!-- MAIN CARD -->

            <div class="main-card" id="mainCard">

                {% if error %}

                    <div class="error">
                        ⚠ {{ error }}
                    </div>

                {% endif %}


                <!-- FORM -->

                <form
                    method="POST"
                    id="predictionForm"
                    onsubmit="startScanning()"
                >

                    <div class="input-grid">


                        <!-- CGPA -->

                        <div class="input-card">

                            <div class="input-number">
                                01
                            </div>

                            <h3>
                                Academic CGPA
                            </h3>

                            <p>
                                Enter the candidate's CGPA.
                            </p>

                            <div class="input-wrapper">

                                <input
                                    type="number"
                                    name="cgpa"
                                    id="cgpa"
                                    min="0"
                                    max="10"
                                    step="0.01"
                                    placeholder="e.g. 8.50"
                                    value="{{ cgpa }}"
                                    required
                                >

                            </div>

                            <div class="meter">

                                <div class="meter-top">
                                    <span>0</span>
                                    <span id="cgpaValue">0 / 10</span>
                                    <span>10</span>
                                </div>

                                <div class="meter-track">

                                    <div
                                        class="meter-fill"
                                        id="cgpaFill"
                                    ></div>

                                </div>

                            </div>

                        </div>


                        <!-- RESUME SCORE -->

                        <div class="input-card">

                            <div class="input-number">
                                02
                            </div>

                            <h3>
                                Resume Score
                            </h3>

                            <p>
                                Enter the candidate's resume score.
                            </p>

                            <div class="input-wrapper">

                                <input
                                    type="number"
                                    name="resume_score"
                                    id="resumeScore"
                                    min="0"
                                    max="100"
                                    step="0.01"
                                    placeholder="e.g. 82"
                                    value="{{ resume_score }}"
                                    required
                                >

                            </div>

                            <div class="meter">

                                <div class="meter-top">
                                    <span>0</span>
                                    <span id="resumeValue">0 / 100</span>
                                    <span>100</span>
                                </div>

                                <div class="meter-track">

                                    <div
                                        class="meter-fill"
                                        id="resumeFill"
                                    ></div>

                                </div>

                            </div>

                        </div>

                    </div>


                    <!-- BUTTON -->

                    <div class="predict-area">

                        <button
                            type="submit"
                            class="predict-btn"
                            id="predictButton"
                        >
                            ✦ ANALYZE CANDIDATE
                        </button>

                        <div class="small-note">
                            AI analysis usually completes in milliseconds
                        </div>

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
                            Perceptron model analysis completed successfully.
                        </p>


                        <div class="score-box">

                            <div class="score-header">

                                <span>
                                    Decision Strength
                                </span>

                                <strong>
                                    {{ confidence }}%
                                </strong>

                            </div>

                            <div class="score-track">

                                <div class="score-fill"></div>

                            </div>

                        </div>


                        <div class="info-row">

                            <div class="info-box">

                                <span>
                                    CGPA
                                </span>

                                <strong>
                                    {{ cgpa }}
                                </strong>

                            </div>

                            <div class="info-box">

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
                NEUROHIRE AI • PERCEPTRON MACHINE LEARNING SYSTEM
            </footer>

        </div>

    </div>


    <!-- ====================================================
         JAVASCRIPT
    ==================================================== -->

    <script>

        const cgpaInput = document.getElementById("cgpa");
        const resumeInput = document.getElementById("resumeScore");

        const cgpaFill = document.getElementById("cgpaFill");
        const resumeFill = document.getElementById("resumeFill");

        const cgpaValue = document.getElementById("cgpaValue");
        const resumeValue = document.getElementById("resumeValue");


        function updateCGPA() {

            if (!cgpaInput) {
                return;
            }

            let value = parseFloat(cgpaInput.value);

            if (isNaN(value)) {
                value = 0;
            }

            value = Math.max(0, Math.min(10, value));

            const percentage = (value / 10) * 100;

            if (cgpaFill) {
                cgpaFill.style.width = percentage + "%";
            }

            if (cgpaValue) {
                cgpaValue.textContent =
                    value.toFixed(2) + " / 10";
            }
        }


        function updateResume() {

            if (!resumeInput) {
                return;
            }

            let value = parseFloat(resumeInput.value);

            if (isNaN(value)) {
                value = 0;
            }

            value = Math.max(0, Math.min(100, value));

            if (resumeFill) {
                resumeFill.style.width = value + "%";
            }

            if (resumeValue) {
                resumeValue.textContent =
                    value.toFixed(0) + " / 100";
            }
        }


        if (cgpaInput) {
            cgpaInput.addEventListener(
                "input",
                updateCGPA
            );

            updateCGPA();
        }


        if (resumeInput) {
            resumeInput.addEventListener(
                "input",
                updateResume
            );

            updateResume();
        }


        function startScanning() {

            const cgpa = parseFloat(cgpaInput.value);
            const resume = parseFloat(resumeInput.value);

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
                document.getElementById("scanOverlay");

            const button =
                document.getElementById("predictButton");

            if (overlay) {
                overlay.classList.add("active");
            }

            if (button) {
                button.disabled = true;
                button.innerHTML =
                    "◉ ANALYZING CANDIDATE...";
            }
        }


        /* ====================================================
           MOUSE TILT EFFECT
        ==================================================== */

        const card =
            document.getElementById("mainCard");

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
                        ((y - centerY) / centerY) * -1.2;

                    const rotateY =
                        ((x - centerX) / centerX) * 1.2;

                    card.style.transform =
                        "perspective(1200px) " +
                        "rotateX(" + rotateX + "deg) " +
                        "rotateY(" + rotateY + "deg)";
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
# FLASK ROUTE
# ============================================================

@app.route("/", methods=["GET", "POST"])
def home():

    result = None
    result_class = ""
    result_icon = ""
    confidence = 50.0

    cgpa = ""
    resume_score = ""
    error = None

    if request.method == "POST":

        try:

            # ------------------------------------------------
            # GET INPUT VALUES
            # ------------------------------------------------

            cgpa = float(request.form.get("cgpa", 0))
            resume_score = float(
                request.form.get("resume_score", 0)
            )


            # ------------------------------------------------
            # VALIDATION
            # ------------------------------------------------

            if cgpa < 0 or cgpa > 10:

                raise ValueError(
                    "CGPA must be between 0 and 10."
                )

            if resume_score < 0 or resume_score > 100:

                raise ValueError(
                    "Resume Score must be between 0 and 100."
                )


            # ------------------------------------------------
            # MODEL INPUT
            #
            # Exact feature order of your Perceptron:
            #
            # 1. cgpa
            # 2. resume_score
            # ------------------------------------------------

            features = [
                [cgpa, resume_score]
            ]


            # ------------------------------------------------
            # PERCEPTRON PREDICTION
            # ------------------------------------------------

            prediction = model.predict(features)[0]


            # ------------------------------------------------
            # PERCEPTRON SCORE
            # ------------------------------------------------

            if hasattr(model, "decision_function"):

                decision = float(
                    model.decision_function(
                        features
                    )[0]
                )

                # Convert decision score into a
                # probability-like visual score.

                try:

                    visual_score = (
                        1.0 /
                        (
                            1.0 +
                            math.exp(-max(
                                -50,
                                min(50, decision)
                            ))
                        )
                    )

                    confidence = round(
                        visual_score * 100,
                        2
                    )

                except Exception:

                    confidence = 50.0

            else:

                decision = 0.0
                confidence = 50.0


            # ------------------------------------------------
            # RESULT
            #
            # Your model has classes [0, 1].
            # Here:
            # 1 = Positive / Selected
            # 0 = Negative / Not Selected
            # ------------------------------------------------

            if int(prediction) == 1:

                result = "Class 1 • Positive Prediction"

                result_class = "positive"

                result_icon = "✓"

            else:

                result = "Class 0 • Negative Prediction"

                result_class = "negative"

                result_icon = "×"


        except ValueError as e:

            error = str(e)

        except Exception as e:

            error = (
                "Prediction error: "
                + str(e)
            )


    # ========================================================
    # RENDER PAGE
    # ========================================================

    return render_template_string(
        HTML,
        result=result,
        result_class=result_class,
        result_icon=result_icon,
        confidence=confidence,
        cgpa=cgpa,
        resume_score=resume_score,
        error=error
    )


# ============================================================
# LOCAL RUN
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
