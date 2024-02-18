import os
import together
import json
import openai
from pydantic import BaseModel, Field

together_api_key = "8edaf787e9be1c89244aae8f7d903c46beb182215bf2e98d3d822a19850496ca"
together.api_key = together_api_key 
wandb_api_key = "8b87053f36270a3afddd98e782ced32670927d85"
# define model
m = "togethercomputer/Llama-2-7B-32K-Instruct"

# Create client
client = openai.OpenAI(
    base_url = "https://api.together.xyz/v1",
    api_key = together_api_key,
)

# Define the schema for the output.
class Eligibility(BaseModel):
    exclusion_criteria: str = Field(description="exclusion")
    inclusion_criteria: str = Field(description="inclusion")
    
# Generate
chat_completion = client.chat.completions.create(
    model="mistralai/Mixtral-8x7B-Instruct-v0.1",
    response_format={
        "type": "json_object", 
        "schema": Eligibility.model_json_schema()
    },
    messages=[
        {"role": "system", "content": "You are a helpful assistant that answers in JSON."},
        {"role": "user", "content": "Create an exclusion and inclusion criteria "}
    ],
)

created_user = json.loads(chat_completion.choices[0].message.content)
print(json.dumps(created_user, indent=2))



def load_data():
# Upload file
    data_path = "clinicaldata.jsonl" 
    resp1 = together.Files.check(file=data_path)
    file_resp = together.Files.upload(file=data_path)
    #print(file_resp) 
    file_id = file_resp["id"]
    return file_id
def start_finetune(file_id):
    resp = together.Finetune.create(
        training_file = file_id,
        model = m,
            n_epochs = 3,
            n_checkpoints = 1,
            batch_size = 4,
            learning_rate = 1e-5,
            suffix = 'test_510k_2',
            wandb_api_key = wandb_api_key
    )

    fine_tune_id = resp['id']
    id = "ft-143dbbbb-6380-415f-b033-156cbd0a349f" 
def deploy():
    name = "natashamaniar3@gmail.com/Llama-2-7B-32K-Instruct-test_510k-2024-02-17-20-30-12"
    together.Models.start(name)
    print(together.Models.ready(name))

def inference():
    output = together.Complete.create(
    prompt = "Write a clinical trial summary given this device description: a wrist watch ecg study",
    model = "natashamaniar3@gmail.com/Llama-2-7B-32K-Instruct-test_510k-2024-02-17-20-30-12",  
    )
    print(output['output']['choices'][0]['text'])


if __name__ == "__main__":
    file_id = load_data()
    # see if you want to finetune
    start_finetune(file_id)
    deploy()


