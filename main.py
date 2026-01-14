
# Ollama allows us to run models on our own computer using our own hardware like an openapi key
# cant run a 200gb model if you dont have a graphics card on your computer
# Langchain is a framework that allows us to work with LLMs
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

model=OllamaLLM(model="llama3.2")
template="""
You are an expert in answering questions about a pizza restaurant
Here are some relevant reviews: {reviews}
here is the question to answer:{question}
"""


prompt=ChatPromptTemplate.from_template(template) # prompt is equal to chat prompt template and we can pass both review and question
chain=prompt|model # create a chain , invokes chain that combines multiples things together to run our loop, prompt pipe model
while True:
    print("\n\n------------")
    question=input("Ask your question (q to quit): ")
    print("\n\n")
    if question == "q":
        break

    result=chain.invoke({"reviews":[],"question": "What is the best pizza in town"})
    print(result)




