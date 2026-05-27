# Project Report

## Abstract
This project is an AI-enhanced smart tour management platform that combines traditional booking workflows with machine learning and generative AI.

## Problem Statement
Tour planning often involves scattered information, manual decision-making, and limited personalization. This project solves that by offering an easy booking workflow along with AI-based support.

## Objectives
- Build a full-stack web application
- Implement user and admin modules
- Add ML-based booking prediction
- Add GenAI itinerary generation
- Create a simple analytics dashboard

## Existing System
Earlier systems focused mostly on booking and package display. They did not include AI-powered suggestions or personalized planning.

## Proposed System
The new system adds prediction, itinerary generation, a chatbot, and dashboard analytics while keeping the code simple for students.

## System Architecture
- Flask backend
- HTML/CSS/JS frontend
- SQLite for local demo and MySQL schema file
- Random Forest model for prediction
- OpenAI-compatible API for GenAI

## Modules Description
- Authentication
- Tour packages
- Booking workflow
- AI prediction
- AI itinerary generation
- Chatbot
- Analytics

## ML Workflow
1. Create tourism dataset
2. Preprocess features
3. Train Random Forest
4. Evaluate accuracy
5. Save model using joblib

## GenAI Workflow
1. Collect destination, days, budget, interests, and travel type
2. Build prompt
3. Call OpenAI-compatible API
4. Return itinerary in sections

## Technologies Used
- Flask
- Bootstrap
- scikit-learn
- pandas
- joblib
- OpenAI
- Chart.js

## Advantages
- Easy for viva explanation
- Realistic workflow
- Low complexity
- Good demo potential

## Future Enhancements
- Real payment gateway integration
- SMS/email notifications
- Better AI prompts
- Mobile app version

## Conclusion
The final platform provides a complete student-level tour management solution enhanced with AI and ML.
