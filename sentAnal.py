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


#assume some variable called total score has already been created...
#below we will add or detuct points to total score based on whether the words are negative or positive
total_score = 0
sent_score = sentAnal("this taco is delicious")
if(sent_score[0]['score'] < sent_score[1]['score']):
  total_score += 2
elif(sent_score[0]['score'] > sent_score[1]['score']):
  total_score -= 2

print(total_score)
#sentAnal(text)
