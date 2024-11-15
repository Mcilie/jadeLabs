import os 
key = os.getenv("OPENPERPLEX_KEY")

from openperplex import OpenperplexSync

client_sync = OpenperplexSync(key)
name = input("Enter the name of the person you want to write to: ")
extra_info = input("Enter any extra information about the person you want to write to: ")
result = client_sync.search(
    query=f"Who is {name} {extra_info}? What are their research interests? What has they accomplished?",
    date_context="2024-08-25",
    location="us",
    pro_mode=False,
    response_language="en",
    answer_type="text",
    verbose_mode=False,
    search_type="general",
    return_citations=False,
    return_sources=False,
    return_images=False
    )

try:
    result = result['llm_response']
except:
    result = "No information found"

filePath = input("Enter the path to the information file you have about this person: ")
contents = open(filePath, "r").read().strip()

togetherKey = os.getenv("TOGETHER_KEY")


# Mixture-of-Agents in 50 lines of code
import asyncio
import os
from together import AsyncTogether, Together

client = Together(api_key=togetherKey)
async_client = AsyncTogether(api_key=togetherKey)
#You are reaching out because you are interested in their research and accomplishments, and want to invite them to a meet and greet at the Hamilton in DC. Your job is to write the most persuasive email you can to get them to A) accept the invite B) if they cannot attend, have them schedule up a meeting with you and C) at the very least, get them to respond. The link to the meet and greet/invite only lunch is the following: https://partiful.com/e/nkcPEQzTvAX72BlZepkT  and your calendar link is the following: https://calendar.app.google/ZDVLfxHeRSyE975M8 .
details = input("Enter any extra details about the email you want to send: ")
user_prompt = f"""
Your name is James Chen, an aspiring builder/hacker, student, and founder of Jade Labs. Jade labs is an up and coming applied AI research lab. It's new and currently in stealth so there aren't many details about it. You are writing an email to {name}. Here are the details of what you need to write: {details}. Please format your email well, do not have arbitrary "fill in" brackets and such. Use a youthful tone. You really want to make sure that you come across as this young new researcher trying to make this big thing work and meet great people. Make it personalised. Here is some information about {name} to make the email more personal and persuasive: Heres some information: {str(result)} and here is more in depth information: {str(contents)}.
"""
reference_models = [
    "Qwen/Qwen2-72B-Instruct",
    "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
    "mistralai/Mixtral-8x22B-Instruct-v0.1",
    "databricks/dbrx-instruct",
]
aggregator_model = "Qwen/Qwen2.5-72B-Instruct-Turbo"
aggreagator_system_prompt = """You have been provided with a set of responses from various open-source models to the latest user query. Your task is to synthesize these responses into a single, high-quality response. It is crucial to critically evaluate the information provided in these responses, recognizing that some of it may be biased or incorrect. Your response should not simply replicate the given answers but should offer a refined, accurate, and comprehensive reply to the instruction. Ensure your response is well-structured, coherent, and adheres to the highest standards of accuracy and reliability.

Responses from models:"""


async def run_llm(model):
    """Run a single LLM call with a reference model."""
    response = await async_client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": user_prompt}],
        temperature=0.7,
        max_tokens=512,
    )
    print(model)
    return response.choices[0].message.content


async def main():
    results = await asyncio.gather(*[run_llm(model) for model in reference_models])

    finalStream = client.chat.completions.create(
        model=aggregator_model,
        messages=[
            {"role": "system", "content": aggreagator_system_prompt},
            {"role": "user", "content": ",".join(str(element) for element in results)},
        ],
        stream=True,
    )

    for chunk in finalStream:
        print(chunk.choices[0].delta.content or "", end="", flush=True)


asyncio.run(main())
