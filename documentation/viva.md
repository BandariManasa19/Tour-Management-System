# Viva Questions and Answers

1. **What is the project about?**
   It is an AI-enhanced tour management system that helps users browse packages, book tours, and get AI-based recommendations.

2. **Which ML algorithm is used?**
   A Random Forest Classifier is used to predict whether a user is likely to book a tour and to suggest a suitable category.

3. **How is the GenAI used?**
   The platform uses an OpenAI-compatible API to generate personalized itineraries based on destination, budget, days, and interests.

4. **How is the database handled?**
   The app uses SQLite by default for local runs and includes a MySQL SQL file for deployment.

5. **How is security handled?**
   Passwords are hashed using Werkzeug, and sessions are used to manage login state.
