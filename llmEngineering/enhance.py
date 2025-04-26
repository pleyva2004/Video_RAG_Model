import json

def enhanceQuery(client, user_query, model="llama-3.3-70b-versatile"):

    SYSTEM_PROMPT = """
        You are an expert query rewriter specialized in optimizing user queries for embedding-based information retrieval systems.

        Your task is to transform the user's query into a clear, expanded statement by following these instructions carefully:

        - Remove any statements similar to "Using only the videos" from the initial query.
        - Rephrase the query as a complete, natural-sounding statement. Ensure the query no longer sounds like a question.
        - Remove all punctuation from the query.
        - Expand any abbreviations but also include the abbreviation in parentheses (e.g., "convolutional neural network (CNN)").
        - Disambiguate vague terms by adding clarifying context when appropriate (e.g., specify whether "Python" refers to the programming language).
        - Correct any spelling errors.
        - Enhance short or unclear queries by adding common implied context (such as "in machine learning," "definition of," "explanation of," or "use case for," if appropriate).
        - If the query is ambiguous, assume the most common intended meaning based on typical usage (e.g., assume "CNN" refers to "convolutional neural network" in the context of machine learning unless otherwise specified).

        After enhancing the original query, generate five new queries that explore different aspects of the same topic. These should cover a variety of angles such as:

        - Definition
        - Explanation
        - Use cases or applications
        - Comparison with related concepts
        - Advantages or limitations

        Respond with your output as a list of exactly five rephrased statements in valid JSON format. Return only the JSON list — no explanations, comments, or extra text.
        Ensure that all output statements are lowercased.
    """

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Query:\n{user_query}"}
            ],
            temperature=0  # Deterministic output for consistent results
        )
        content = response.choices[0].message.content

        try:
            return json.loads(content)
        except json.JSONDecodeError as decode_error:
            print("Failed to parse JSON. Here's the raw response:\n")
            print(content)  # Print the response
            print(f"\nJSON error: {decode_error}")
            return None

    except Exception as e:
        print(f"Error during Groq API call: {e}")
        return None


