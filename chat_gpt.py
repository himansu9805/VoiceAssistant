import openai

openai.api_key = "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"


def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=2000,
        n=1,
        stop=None,
        temperature=0.75,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].text  # type: ignore
