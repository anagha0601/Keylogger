# Keylogger with ML-based Anomaly Detection

## 📌 Overview

This project involves the **design and development of a custom keylogger system from scratch**, combined with **machine learning-based anomaly detection** to monitor user behavior and identify potential cyber threats.

Unlike projects that only apply ML on existing datasets, this system includes **end-to-end implementation**—from data collection (keystrokes, screenshots, IP, audio) to intelligent threat detection.

The system captures real-time user activity and analyzes behavioral patterns to detect deviations that may indicate malicious or unauthorized access.

> ⚠️ Note: This project is developed strictly for **educational, research, and cybersecurity awareness purposes**. It must be used ethically and in compliance with privacy laws.

---

## 🚀 Features

* Real-time keystroke logging
* User activity monitoring
* Screenshot capture at defined intervals
* IP address tracking for session monitoring
* Audio capture for activity context (where permitted)
* Secure data handling and storage
* ML-based anomaly detection
* Detection of unusual typing patterns and behaviors
* Scalable and modular design

---

## 🧠 Problem Statement

Cyber threats often involve unauthorized access or abnormal user behavior that is difficult to detect using traditional rule-based systems. This project aims to:

* Monitor user interactions
* Learn normal behavioral patterns
* Detect anomalies that may indicate potential security risks

---

## 🏗️ System Architecture

1. **Data Collection**

   * Keystroke logging
   * User activity tracking
   * Screenshot capture
   * IP address logging
   * Audio data capture (where permitted)

2. **Data Preprocessing**

   * Cleaning and structuring logs
   * Feature extraction (typing speed, frequency, patterns)

3. **Feature Engineering**

   * Time intervals between keystrokes
   * Session-based activity features

4. **Model Training**

   * Machine learning models for anomaly detection (e.g., Isolation Forest, One-Class SVM)

5. **Anomaly Detection**

   * Identify deviations from normal behavior

6. **Alert System**

   * Flag suspicious activities

---

## 🛠️ Tech Stack

* Python
* Scikit-learn
* Pandas, NumPy
* Logging libraries
* Matplotlib / Seaborn (for visualization)

---

## 📊 Key Concepts

* Behavioral biometrics
* Anomaly detection
* Cybersecurity analytics
* User activity monitoring

---


---

## 📈 Evaluation Metrics

* Precision & Recall for anomaly detection
* False positive rate
* Detection accuracy

---

## 👥 Team

Developed as part of a **team of 4**, with contributions including:

* Building the keylogger system from scratch
* Designing the data collection pipeline (keystrokes, screenshots, IP, audio)
* Developing ML-based anomaly detection models
* Integrating system components for end-to-end functionality

---

## 🔐 Ethical Considerations

* Ensure informed consent before monitoring any user activity
* Follow data privacy regulations (e.g., GDPR)
* Use strictly for security research and defensive purposes

---

## 🔮 Future Improvements

* Integrate deep learning models for behavioral analysis
* Real-time dashboard for monitoring
* Deployment as a security tool or API



## ⭐ Acknowledgements
* Grant Collins
* Open-source cybersecurity community
* Research papers on anomaly detection and behavioral analytics
