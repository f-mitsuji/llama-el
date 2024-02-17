from dotenv import load_dotenv
import replicate

load_dotenv()

llama2_70b = "meta/llama-2-70b"

prompt = '''
INPUT: what does the letters eu stand for?
OUTPUT: \"entities_text\": [], \"wikipedia_urls\": []
INPUT: what country is the grand bahama island in?
OUTPUT: \"entities_text\": [\"grand bahama\"], \"wikipedia_urls\": [\"https://en.wikipedia.org/wiki/Grand_Bahama\"]
INPUT: what character did john noble play in lord of the rings?
OUTPUT: \"entities_text\": [\"john noble\", \"lord of the rings\"], \"wikipedia_urls\": [\"https://en.wikipedia.org/wiki/John_Noble\", \"https://en.wikipedia.org/wiki/The_Lord_of_the_Rings:_The_Two_Towers\"]
INPUT: what city is the state capital of washington?
OUTPUT: \"entities_text\": [\"washington\"], \"wikipedia_urls\": [\"https://en.wikipedia.org/wiki/Washington_(state)\"]
INPUT: how old is sacha baron cohen?
OUTPUT:'''


def ChatCompletion(prompt, system_prompt):
    output = replicate.run(
        llama2_70b,
        input={
            "system_prompt": system_prompt,
            "prompt": prompt,
            "temperature": 0.01}
    )
    return "".join(output)


output = ChatCompletion(
    prompt,
    system_prompt="Extract named entities from the following text and provide their Wikipedia URLs\nOutput is always one line"
)

print(output)
