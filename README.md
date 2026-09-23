🗑️ Garbage Bin Fill Level Detection using Fuzzy Logic and LangChain AI

📌 Description

Garbage Bin Fill Level Detection is an intelligent waste-management mini project that combines Fuzzy Logic and Artificial Intelligence (AI) using LangChain to determine the urgency of garbage-bin collection.

The system takes three main parameters:

- Garbage bin fill level (%)
- Smell intensity (0–10)
- Number of days since the last collection

The Fuzzy Logic system processes these inputs using membership functions and fuzzy IF-THEN rules to calculate a Collection Urgency Score (0–100).

The LangChain-based AI component understands the user's natural-language question and provides a conversational explanation of the fuzzy-logic result.

The project is implemented using Streamlit, providing a simple and interactive web interface.

---

✨ Features

- 🗑️ Garbage bin fill-level input
- 👃 Smell-intensity input
- 📅 Days since last collection input
- 🧠 Genuine Fuzzy Logic inference system
- 📊 Fuzzification using membership functions
- 🔀 Multiple fuzzy IF-THEN rules
- 🎯 Defuzzification to obtain urgency score
- 🤖 LangChain-based AI explanation
- 💬 Natural-language user queries
- 📈 Visual urgency indicator
- 🟢 Low urgency detection
- 🟡 Medium urgency detection
- 🔴 High urgency detection
- 🌐 Interactive Streamlit web application
- ☁️ Can be deployed online using Streamlit Community Cloud

---

🛠️ Technologies Used

Technology| Purpose
Python| Main programming language
Streamlit| Web-based user interface
Scikit-Fuzzy| Fuzzy inference system
LangChain| AI/LLM application framework
OpenAI API| Natural-language understanding and explanation
NumPy| Numerical calculations
Git| Version control
GitHub| Source-code repository
Streamlit Community Cloud| Application deployment

---

🔄 System Workflow

The system follows the workflow below:

                ┌───────────────────────┐
                │      User Input       │
                │                       │
                │ Fill Level            │
                │ Smell Intensity       │
                │ Days Since Collection │
                └───────────┬───────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │     Fuzzification   │
                 │                     │
                 │ Low / Medium / High │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │    Fuzzy Rules      │
                 │                     │
                 │ IF-THEN Rules       │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │    Defuzzification  │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Collection Urgency  │
                 │      0 - 100        │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │     LangChain       │
                 │       + LLM         │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ AI Explanation and  │
                 │ Recommendation      │
                 └─────────────────────┘

Workflow Steps

1. Input

The user provides:

- Fill level of the bin
- Smell intensity
- Days since the previous collection

2. Fuzzification

The numerical values are converted into fuzzy linguistic categories.

For example:

Fill Level:
Low → Medium → High

Smell:
Low → Medium → High

Days:
Recent → Moderate → Long

3. Fuzzy Rule Evaluation

The fuzzy system evaluates predefined rules.

Example:

IF fill level is HIGH
THEN collection urgency is HIGH

Another example:

IF fill level is MEDIUM
AND smell is HIGH
THEN collection urgency is HIGH

4. Defuzzification

The fuzzy output is converted into a numerical urgency value between:

0 – 100

5. AI Explanation

The urgency score and user question are passed through a LangChain-based LLM chain.

The AI generates a human-readable explanation of the result.

---

📁 Project Structure

garbage-bin-fuzzy-ai/
│
├── app.py
│
├── fuzzy_logic.py
│
├── llm_chain.py
│
├── requirements.txt
│
├── README.md
│
└── .gitignore

---

📄 File Description

"app.py"

The main Streamlit application.

It:

- Creates the web interface
- Takes user inputs
- Calls the fuzzy-logic system
- Displays the urgency score
- Displays the collection status
- Sends the result to the AI component
- Displays the AI-generated explanation

---

"fuzzy_logic.py"

Contains the complete fuzzy inference system.

It includes:

- Input variables
- Output variable
- Membership functions
- Fuzzy rules
- Fuzzy control system
- Fuzzification
- Rule evaluation
- Defuzzification

Input Variables

Fill Level
Smell Intensity
Days Since Collection

Output Variable

Collection Urgency

---

"llm_chain.py"

Contains the LangChain AI component.

It:

1. Creates the LLM.
2. Creates the prompt.
3. Receives the user's natural-language question.
4. Receives the fuzzy urgency result.
5. Sends the information through the LangChain chain.
6. Generates a natural-language explanation.

---

"requirements.txt"

Contains the Python libraries required to run the project.

Example:

streamlit
scikit-fuzzy
langchain
langchain-openai
python-dotenv
numpy

---

".gitignore"

Prevents sensitive and unnecessary files from being uploaded to GitHub.

Example:

venv/
.env
__pycache__/
*.pyc

The ".env" file should never be uploaded to GitHub because it can contain an API key.

---

⚙️ Installation and Setup

Step 1: Clone the Repository

git clone https://github.com/YOUR-USERNAME/garbage-bin-fuzzy-ai.git

Move into the project directory:

cd garbage-bin-fuzzy-ai

---

Step 2: Create a Virtual Environment

python -m venv venv

Windows

venv\Scripts\activate

Linux/macOS

source venv/bin/activate

---

Step 3: Install Dependencies

pip install -r requirements.txt

---

Step 4: Configure OpenAI API Key

Create a ".env" file:

OPENAI_API_KEY=your_api_key_here

Replace "your_api_key_here" with your API key.

Important: Do not upload the ".env" file to GitHub.

---

▶️ Running the Application

After installing the dependencies, run:

streamlit run app.py

The application will open in your browser.

Usually, Streamlit provides a local address similar to:

http://localhost:8501

Open the displayed address in your browser.

---

🧪 Example Input

Example input values:

Parameter| Example Value
Fill Level| 90%
Smell Intensity| 8/10
Days Since Collection| 7
User Question| Should this garbage bin be collected soon?

Expected Result

The fuzzy system should produce a relatively high collection urgency because:

- The bin has a high fill level.
- The smell intensity is high.
- Several days have passed since collection.

The system then provides an AI-generated explanation.

---

💬 Example Extracted Preferences

The AI component can understand natural-language requests related to the garbage-bin situation.

Example User Query

The bin is almost full, smells bad, and hasn't been collected
for a week. Should it be collected soon?

The system identifies the relevant information:

Fill Level       → Almost full / High
Smell Intensity  → High
Collection Time  → About one week

The fuzzy system then uses the numerical input values to calculate the collection urgency.

The LangChain component uses the user's question and fuzzy result to generate a conversational explanation.

Another Example

The bin is only slightly filled and was emptied yesterday.
Do I need to request collection?

Relevant information:

Fill Level       → Low
Collection Time  → Recent
Urgency          → Low

The AI can explain why immediate collection may not be necessary according to the fuzzy result.

---

🧠 Fuzzy Logic Component

The project uses a genuine fuzzy inference system rather than simple "if-else" conditions.

Membership Functions

Fill Level

Low
Medium
High

Smell Intensity

Low
Medium
High

Days Since Collection

Recent
Moderate
Long

Collection Urgency

Low
Medium
High

Triangular membership functions are used to represent these linguistic categories.

---

📋 Fuzzy Rules

Some of the rules used by the system are:

Rule 1

IF fill level is LOW
AND smell is LOW
AND collection is RECENT
THEN urgency is LOW

Rule 2

IF fill level is MEDIUM
AND smell is MEDIUM
THEN urgency is MEDIUM

Rule 3

IF fill level is HIGH
THEN urgency is HIGH

Rule 4

IF fill level is HIGH
AND smell is HIGH
THEN urgency is HIGH

Rule 5

IF days since collection is LONG
AND smell is HIGH
THEN urgency is HIGH

Rule 6

IF fill level is MEDIUM
AND days since collection is LONG
THEN urgency is HIGH

These rules allow several factors to contribute to the final urgency score.

---

🤖 AI / LangChain Component

The project uses LangChain to connect the user's natural-language question with the LLM.

The flow is:

User Question
      ↓
LangChain Prompt
      ↓
Fuzzy Logic Result
      ↓
LLM
      ↓
Natural Language Explanation

For example:

User:
"The bin is almost full and smells bad.
Should it be collected?"

Fuzzy Result:
Urgency = 85/100

AI:
"The bin has a high collection urgency because the
fill level and smell intensity indicate that collection
should be scheduled soon."

This makes the LLM an actual language-processing component rather than simply displaying a fixed response.

---

🇮🇳 IKS Connection

Indian Knowledge Systems Connection

The project can be connected to Indian Knowledge Systems (IKS) through the traditional Indian emphasis on cleanliness, environmental responsibility, and community well-being.

Indian traditions have historically emphasized the importance of maintaining clean surroundings and responsible use of natural resources. The concept of cleanliness can be connected with modern smart-waste-management practices.

This project applies modern technologies such as:

- Artificial Intelligence
- Fuzzy Logic
- Automation
- Smart monitoring

to support responsible waste management.

IKS Perspective

Traditional Value
      ↓
Clean surroundings
      ↓
Responsible resource use
      ↓
Community well-being
      ↓
Modern Smart Waste Management
      ↓
AI + Fuzzy Logic

The project therefore demonstrates how modern computational techniques can be used in an area that aligns with the broader traditional value of maintaining clean and sustainable surroundings.

---

🌐 Deployment

The application can be deployed using Streamlit Community Cloud.

Step 1

Push the project to GitHub.

Your repository should contain:

app.py
fuzzy_logic.py
llm_chain.py
requirements.txt
README.md
.gitignore

Do not upload:

.env
venv/

---

Step 2

Open Streamlit Community Cloud and sign in using your GitHub account.

Create a new application and select your repository.

Set:

Branch:
main

Main file:
app.py

Then deploy the application.

---

Step 3: Add API Secret

For the deployed application, configure the OpenAI API key using the platform's Secrets settings instead of putting the key in the source code.

Example:

OPENAI_API_KEY = "your_api_key_here"

After deployment, Streamlit provides a public application URL.

Example:

https://your-project-name.streamlit.app

---

🚀 Future Scope

The current project uses user-provided values for demonstration. It can be extended into a complete smart-waste-management system.

1. IoT Sensor Integration

Ultrasonic sensors can be connected to a microcontroller such as ESP32 to automatically measure the distance between the sensor and garbage level.

Ultrasonic Sensor
       ↓
ESP32
       ↓
Fill Level
       ↓
Fuzzy Logic

---

2. Real-Time Monitoring

The system can continuously monitor garbage bins and update their status in real time.

---

3. Automatic Notifications

The system could send notifications when a bin reaches a high collection urgency.

Possible notifications include:

- Email
- SMS
- Mobile notification

---

4. Multiple Garbage Bins

The system can be extended to monitor multiple bins:

Bin 1 → 35%
Bin 2 → 82%
Bin 3 → 67%
Bin 4 → 94%

A dashboard could display the status of all bins.

---

5. GPS-Based Collection

Each bin could be associated with GPS coordinates so that collection teams can identify the locations requiring service.

---

6. Route Optimization

A future version could use route-optimization algorithms to determine efficient collection routes for garbage trucks.

---

7. Image-Based Fill Detection

A camera could be used to capture an image of the garbage bin.

A computer-vision model could estimate the fill level automatically:

Camera
  ↓
Image
  ↓
Computer Vision Model
  ↓
Fill Percentage
  ↓
Fuzzy Logic
  ↓
Collection Urgency

---

8. Predictive Waste Management

Historical data could be used to predict when a particular bin is likely to become full.

This could help schedule collection before overflow occurs.

---

🎯 Project Objectives

The major objectives of the project are:

1. To develop an intelligent garbage-bin monitoring system.
2. To use fuzzy logic for handling uncertain garbage-bin conditions.
3. To calculate a collection urgency score.
4. To integrate LangChain for natural-language interaction.
5. To provide an easy-to-use Streamlit interface.
6. To demonstrate the practical application of AI and fuzzy reasoning.
7. To support smarter and more efficient waste-management practices.

---

📊 Sample Output

For example:

-----------------------------------------
       SMART GARBAGE BIN
-----------------------------------------

Fill Level              : 90%
Smell Intensity         : 8/10
Days Since Collection   : 7

-----------------------------------------
FUZZY LOGIC RESULT
-----------------------------------------

Collection Urgency      : 85/100
Status                  : HIGH URGENCY

-----------------------------------------
AI EXPLANATION
-----------------------------------------

The garbage bin has a high collection urgency.
The high fill level and smell intensity contribute
to the elevated urgency score. Collection should
therefore be scheduled soon.
-----------------------------------------

---

👩‍💻 Project Type

Logic Mini Project

Components

AI / LLM Component
        +
Fuzzy Logic Component
        +
Streamlit UI
        +
GitHub
        +
Cloud Deployment

---

📌 Conclusion

The Garbage Bin Fill Level Detection project demonstrates how Fuzzy Logic and Artificial Intelligence can work together to solve a practical waste-management problem.

Fuzzy Logic handles uncertain and gradual conditions such as fill level, smell intensity, and collection time, while LangChain and an LLM provide natural-language understanding and explanations.

The project provides a foundation for developing a larger IoT-based smart waste-management system with sensors, real-time monitoring, notifications, image processing, and route optimization.

---

👤 Author

Name: Your Name

Project: Garbage Bin Fill Level Detection

Technology: Python, Streamlit, Fuzzy Logic, LangChain

Academic Project: Logic Mini Project
