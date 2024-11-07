import cohere
import random
import json
import os

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.Client(api_key = COHERE_API_KEY)

### Configuration ###
DISEASE_CONTEXTS = [
    {
        "disease": "Migraine",
        "symptoms": ["headache", "nausea", "sensitivity to light"],
        "background_info": "Patient has a history of migraines occurring at least once a month.",
    },
    {
        "disease": "Type 2 Diabetes",
        "symptoms": ["frequent urination", "increased thirst", "fatigue"],
        "background_info": "Patient was diagnosed with diabetes 3 years ago and is on medication.",
    },
    
]

### Functions for Core System Modules ###

def initialize_patient_profile():
    """Randomly selects a disease context to simulate a patient's condition."""
    profile = random.choice(DISEASE_CONTEXTS)
    print(f"[DEBUG] Patient Profile Initialized: {profile['disease']}")
    return profile

def generate_patient_response(disease_context, doctor_question, instructions=""):
    """
    Generates a patient response based on the disease context and doctor's question.
    """
    prompt = f"Patient has been diagnosed with {disease_context['disease']}. "
    prompt += f"Symptoms include {', '.join(disease_context['symptoms'])}. "
    prompt += f"{disease_context['background_info']}\n"
    prompt += f"Doctor's Question: {doctor_question}\n"
    prompt += f"{instructions}\n"
    prompt += "Patient's Response: "

    response = co.generate(prompt = prompt)
        
    return response.generations[0].text.strip()

def evaluate_question_tone(doctor_question):
    """
    Evaluates the tone of the doctor's question.
    """
    prompt = f"Rate the tone of this question on empathy and professionalism, classify as acceptable, ok, or not acceptable: {doctor_question}"
    response = co.generate(prompt = prompt)
    return response.generations[0].text.strip()

def log_conversation(turn_data, log_file="conversation_log.json"):
    """
    Logs each conversation turn to a JSON file.
    """
    with open(log_file, 'a') as f:
        json.dump(turn_data, f)
        f.write("\n")


def start_conversation():
    """
    Initializes a patient profile and starts the doctor-patient conversation loop.
    """
    patient_profile = initialize_patient_profile()
    print("Patient initialized with disease context:", patient_profile['disease'])
    
    conversation_active = True

    while conversation_active:
        # Step 1: Doctor asks a question
        doctor_question = input("Doctor's question to patient: ")

        if doctor_question.lower() in ["exit", "quit"]:
            print("Ending conversation.")
            break


        # Step 2: Evaluate the question's tone
        tone_evaluation = evaluate_question_tone(doctor_question)
        print(f"[Tone Evaluation] {tone_evaluation}")


        # Step 3: Generate patient's response based on disease context and doctor question
        patient_response = generate_patient_response(patient_profile, doctor_question)
        print("Patient:", patient_response)


        # Step 4: Log the conversation turn
        turn_data = {
            "doctor_question": doctor_question,
            "tone_evaluation": tone_evaluation,
            "patient_response": patient_response,
            "disease_context": patient_profile["disease"]
        }
        log_conversation(turn_data)

        if tone_evaluation in ["ok", "not acceptable"]:
            print("[Feedback] Consider rephrasing for better empathy and professionalism.")
    
    print("Conversation ended.")

start_conversation()