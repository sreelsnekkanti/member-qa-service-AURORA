This project provides a simple question-answering system that can answer natural-language questions about member data provided.

Examples questions:

“When is Layla planning her trip to London?”

“How many cars does Vikram Desai have?”

“What are Amira’s favorite restaurants?”

“What’s Sree’s favorite place to go on vacation?” (example added for testing)

The API service must accept a natural-language question and respond with an answer from the member messages.

The Output format must be:

{ "answer": "..." }

How the System Works

1. Loading the Messages

* All member messages are loaded once from the local file sample_messages.json.

2. Identifying the Relevant Message and retrieve it

* The system converts both the question and each message into lowercase tokens.

* Each message gets a relevance score based on word overlap with the question.

* The message with the highest overlap is selected as the best match.

* If there is no overlap then it returns the most relevant text message directly.

3. Extracting the Answer

* Once the most relevant message is found, the system extracts the answer based on the question.

* If the question includes “how many”, the system returns the first number in the message.

* For other questions, it returns the text message directly as the answer.

To run the project

1. Create and activate a virtual environment

Windows (PowerShell):

python -m venv venv

venv\Scripts\activate.ps1

2. Install dependencies

pip install -r requirements.txt

3. Start the API server
   
uvicorn app:app --reload --host 0.0.0.0 --port 8000

5. Access the API documentation

Once the server is running, you can visit:

Public API Base URL: https://member-qa-service-aurora.onrender.com

Swagger UI: https://member-qa-service-aurora.onrender.com/docs

Example Query: How many cars does Vikram Desai have?

Request URL: https://member-qa-service-aurora.onrender.com/ask?q=How%20many%20cars%20does%20Vikram%20Desai%20have%3F

Output:

{
  "answer": "2"
}


Alternative approaches:
* Alternative approaches that can be considered are TF-IDF similarity, full semantic search and a miniature RAG pipeline.
* These would improve accuracy, but for a small dataset they add unnecessary complexity.


Data Insights

* Some messages might contain vague timelines (“next Friday”)
* Favorites sometimes appear multiple times
* Some messages lack dates, numbers, or specific entities
* There may be repeating similar information or latest-message prioritization

Future Improvements

Implementing TF-IDF or embedding-based retrieval for better accuracy for a large data set.

Adding extraction logic for dates, entities, and specific attributes.

Replacing the local JSON file with the live /messages API.

Improving error handling and validation.

Introducing logging and monitoring for production use.

Adding caching or database storage for larger datasets.

Author

Sree Lakshmi Sowmya Nekkanti for AURORA

GitHub: https://github.com/sreelsnekkanti
