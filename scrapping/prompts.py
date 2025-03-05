GENERATE_QUESTIONS = """
    Generate 10 questions related with the following query 
    ##QUERY
    {query}
    And return the answer in a text format
"""

GENERATE_SUMMARIZE = """
    Generate a summary of the following text
    ##TEXT
    {query}
    And return the answer in a text format
"""

GENERATE_IDEAS = """
    Generate 5 principal ideas from the following text
    ##TEXT
    {query}
    And return the answer in a text format
"""

IMAGES_CAPTION = """
    The following text may contains images and captions for images

    ##TEXT
    {query}

    Your task is, given the previous text, extract the caption related to the following image text. 
    
    ## IMAGE TEXT
    {image_text}

    like the following example:

    ##EXAMPLE
    Figure 1. A schematic of A Basic Refrigeration System. _Source:_ _http://en.wikipedia.org/wiki/Vapor-__compression_refrigeration_

    where in the previous example the caption of the image would be "A schematic of A Basic Refrigeration System.
    Keep in mind that the text could contains more than one image, always the caption of a image will be the most closed caption to her down vertical. Here is an example

    ##EXAMPLE
    ![-9-0.png](-9-0.png)

    ![-9-1.png](-9-1.png)                                                                                                                                                                               

    ![-9-2.png](-9-2.png)                                                                                                                                                                               

    Figure 3. Comparison of electric energy use between simulation models and actual usage 

    In the previous example the caption of the image -9-0 would be "Comparison of electric energy use between simulation models and actual usage", and the caption of
    the image -9-1 would be "Comparison of electric energy use between simulation models and actual usage", and the caption of the image -9-2 would be "Comparison of 
    electric energy use between simulation models and actual usage"

    But if you have 2 images in this format:

    ##EXAMPLE
    ![-9-0.png](-9-0.png)
    Figure 1. Explanation lalala

    ![-9-1.png](-9-1.png)
    Figure 2. Explanation more lala

    The caption of the image -9-0 would be "Explanation lalala" and the caption of the image -9-1 would be "Explanation more lala".

    Provide your answer in a JSON object as follows:

    {{
        "explanation": "...",
        "caption": "...",
    }}


"""

IMAGE_TEMPLATE = """
    The following context is a series of extract that will be usefull information to answer to a user query
    
    ## EXTRACT 0
    {context0}

    ## EXTRACT 1
    {context1}

    ## EXTRACT 2
    {context2}

    Given the previous information, you are assigned to do the following actions:
    ## ACTION 1: Answer the following user query based on the information provided in the previous extracts 

    ## QUERY
    {query}

    ## ACTION 2: If you use information from a specific EXTRACT of the 3 given and the text information has the word "Figure" with a number, add in your response a #Figure Number with the caption like this

    #Figure NUMBER
    ## EXAMPLE
    #Figure 1. A schematic of A Basic Refrigeration System

    where NUMBER represent the number of the EXTRACT of what you take the information from for answering the user query.

    ## ACTION 3: If you used a information from a specific EXTRACT of the 3 given that contains a table, include in your response the table in a new line.
    Also add in a new line a description of the table and remove from your text headers like #Table 1, use it only for references and captions.
    
    ## ACTION 4: Modify your answer and keep it in a format where you are an assistant to return only the answers for the question, avoid frases like:
    "In the provided extract"
    "Based on the user query"
    "In the previous context"
    """

CLASSIFICATION_PROMPT = """
You will be given a question. Your task is to provide a 'total score' that represents how context-independent this question is.
Give your answer on a scale from general to specific, where general means that the question is very general like a greeting or questions without technical content from any branch of knowledge.
The questions may contain obscure technical nouns or acronyms such as SORBA, AutoML, automation or content considered technical in the field of Artificial Intelligence, IoT or automation, in this case the value is considered to be specific. Also be aware of some context related words that will be considered to be specific to.

Answer only with a JSON object with the following schema:

{{
    "explanation": "..." # your explanation for the classification
    "classification": "..." # the classification of the question, either general or specific
}}

Question: {query}
"""

SIMILITUDE_PROMPT = """
"You will be given 2 information texts. Give your answer on Yes or No where Yes means that the texts are in the same context and are talking about the same theme and No means that the text are different
 and are no talking about the same theme. The following texts are the information that you will be given: \n\n"

Answer only with a JSON object with the following schema:

{{
    "explanation": "..." # your explanation for the classification
    "classification": "..." # the classification of the question, either general or specific
}}

Text 1: {context}
Text 2: {transcription}

"""

GENERAL_TEMPLATE = """
The user made this query: {query}

Reply to the user, politely, that you are not designed to answer general-purpose questions,
such as topics related with the query. Inform the user that your purpose is to
answer general questions in the domain of automation and industrial applications
as well as questions regarding SORBA, its services and products,
and how to use the SORBA platform.
"""

RAG_TEMPLATE = """
The following is an extract of information that may be relevant for the user query
##EXTRACT
{context}

Given the previous context, you will answer the following query. Reply concisely in a formal and technical language.
##QUERY
{query}
"""

CHATBOT_TEMPLATE = """
You are a customer service bot implemented by the company SORBA-AI. Your purpose is to answer general questions in the domain of automation and industrial applications 
as well as questions regarding SORBA, its services and products, and how to use the SORBA platform.
"""

RAG_WITH_FEEDBACK_TEMPLATE = """
The following text is a response for a query made by the user
##TEXT
{text}

##QUERY
{query}

You task is, given the response and the query, fix the response to be more accurate with the query.
You also have to improve the answer keeping in mind that the response need to be in a technical language and
Modify your answer and keep it in a format where you are an assistant to return only the answers for the question, avoid frases like:
"In the provided extract"
"Based on the user query"
"In the previous context"
"""

GUIDED_SEARCH_TEMPLATE = """
The following text contains information related with the query introduced by the user

##TEXT
{context}



"""
