# aino
Speak Pal

# Installation Instructions
## 1. Follow this guide 
From OpenAI to set up your account, finish **Step 1: Setting up Python** and **Step 2: Set up your API key**
https://platform.openai.com/docs/quickstart

## 2. Install these packages with pip: 
```
pip install -r requirements.txt
```

## 3. Configure the Assistant

By default, the Assistant will be created with the first prompt in the `ASSISTANT_INSTRUCTIONS` variable in `configs.py`. You can place the desired prompt in the first position of the list when running the program.

Voice can be configured with `VOICE` variable in `configs.py`. For the full list of voices from OpenAI: https://platform.openai.com/docs/guides/text-to-speech/voice-options

The first sentence `Hi, I'm Aino/Ismo. How may I help you?` is hardcoded from line 23,24 of `main.py`. You can tweak this as you like.

## 4. Run the program
The program can be run with either

Create a new assistant
```
python main.py -c
```

Or use the old assistant
```
python main.py <ASSISTANT_ID>
```
where `ASSISTANT_ID` is retreived from OpenAI assistants page: https://platform.openai.com/assistants (You need to login)


# More Infomartion about OpenAI API:
https://platform.openai.com/docs/introduction
