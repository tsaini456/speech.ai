# whisper imports
from IPython.display import display, Image, Markdown, Audio
import requests
import string
!pip install sapling-py
# sapling - grammar checker
from sapling import SaplingClient
# google drive access
import os
from google.colab import drive
drive.mount('/content/drive')
def whisper(url):
  account_id = "c392da31dbfc326137e5f0b47ae2e330"
  model = "@cf/openai/whisper"
  api_token = "AcNWFFv4Ui5vxCcpBx4sl9LvvYYOtY8lTLmfIcdc"

  display(Audio(url))
  with open(url, 'rb') as f:
    contents = f.read()

  response = requests.post(
      f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/{model}",
      headers={"Authorization": f"Bearer {api_token}"},
      data=contents
  )

  inference = response.json()
  return inference['result']
  text = frame['text']
word_count = frame['word_count']
words = frame['words']
duration = frame['words'][-1]['end']
print(duration)
feedback = {}
# filler count
fillers = ["um", "uh", "like", "you know", "actually", "basically", "sort of", "kind of", "I mean", "you see", "well", "so", "right", "okay", "anyways", "look", "listen", "believe me", "you see", "frankly", "literally", "just", "pretty much", "perhaps", "I guess", "I think", "you know what", "at the end of the day", "to be honest", "to tell you the truth", "in a sense", "if you will", "you know what I mean", "at all", "whatsoever", "thing", "stuff", "let’s say", "in other words", "I suppose", "definitely", "certainly", "surely", "absolutely", "totally", "completely", "utterly", "basically", "essentially", "fundamentally", "practically", "virtually", "nearly", "almost", "about", "around", "approximately", "roughly", "someway", "somehow", "sometime", "sometimes", "occasionally", "often", "frequently", "regularly", "usually", "typically", "generally", "mainly", "mostly", "largely", "particularly", "especially", "specifically", "expressly", "explicitly", "precisely", "exactly", "just", "merely", "simply", "only", "solely", "perhaps", "probably", "maybe", "possibly", "seemingly", "apparently", "ostensibly", "evidently", "presumably", "assumably", "likely", "probably", "almost", "nearly", "quite", "rather", "somewhat", "more or less", "to some extent", "in some way", "in many ways", "to a degree", "to an extent", "up to a point", "in part", "partly", "partially", "not entirely", "not totally", "not wholly", "not fully", "by and large", "on the whole", "all in all", "for the most part", "in general", "as a rule", "generally speaking", "usually", "typically"]

def lower_iter(s):
  return s.lower()
fillers = map(lower_iter, fillers)

clean_text = text.translate(str.maketrans('', '', string.punctuation)).lower().split()
found_fillers = []

for i in range(len(clean_text)):
  word = clean_text[i]

  sequence = word
  for pad in range(1, 5):

    if sequence in fillers:
      # find sequences of fillers
      found_fillers.append(sequence)
    else:
      break

    sequence += (" " + clean_text[i + pad])
    print(pad)


print(text)
print(found_fillers)
# filler time
word_lengths = []

for word in words:
  # presenter wpm
  wpm = word_count / (duration / 60)
  feedback['wpm'] = wpm
  print(wpm)

# grammar checker - sapling
api_key = '6ZVPCQ56U63PX3QP9XNATELQ3FOHWEIH'
client = SaplingClient(api_key=api_key)
edits = client.edits(text, session_id='test_session')
feedback['grammar'] = edits
print(edits)

# SENTIMENT ANALYSIS PORTION
# TAKES WORDS FROM AUTOMATIC SPEECH RECOGNITION AND THEN DETERMINES SENTIMENT
def sentAnal(text):
  model = "@cf/huggingface/distilbert-sst-2-int8"
  account_id = "c392da31dbfc326137e5f0b47ae2e330"
  api_token = "AcNWFFv4Ui5vxCcpBx4sl9LvvYYOtY8lTLmfIcdc"

  response = requests.post(
    f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/{model}",
    headers={"Authorization": f"Bearer {api_token}"},
    json={"text": text}
  )

  inference = response.json()
  return inference["result"]

sentAnal("this taco is delicious")
sentAnal(text)
