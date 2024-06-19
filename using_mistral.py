
# import requests
# import torch
# from transformers import AutoModelForCausalLM, AutoTokenizer

# API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
# API_TOKEN = "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"

# headers = {"Authorization": f"Bearer {API_TOKEN}"}

# def query(payload):
#     response = requests.post(API_URL, headers=headers, json=payload)
#     return response.json()

# # Instantiate the model and tokenizer
# model_id = "mistralai/Mistral-7B-Instruct-v0.2"
# tokenizer = AutoTokenizer.from_pretrained(model_id)
# model = AutoModelForCausalLM.from_pretrained(model_id, device_map="auto")

# # Define your conversation messages
# messages = [
#     {"role": "user", "content": "What is your favourite condiment?"},
#     {"role": "assistant", "content": "Well, I'm quite partial to a good squeeze of fresh lemon juice. It adds just the right amount of zesty flavour to whatever I'm cooking up in the kitchen!"},
#     {"role": "user", "content": "Do you have mayonnaise recipes?"}
# ]

# # Tokenize the messages and prepare inputs
# inputs = tokenizer.apply_chat_template(messages, return_tensors="pt")
# inputs = {key: value.tolist() if isinstance(value, torch.Tensor) else value for key, value in inputs.items()}

# # Make a query to the Hugging Face API
# data = query(inputs)


# # Print the generated response
# print(data)


# import requests

# API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
# API_TOKEN = "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"

# headers = {"Authorization": f"Bearer {API_TOKEN}"}

# def query(payload):
#     response = requests.post(API_URL, headers=headers, json=payload)
#     try:
#         return response.json()
#     except Exception as e:
#         print("Error decoding response:", e)
#         print("Response content:", response.content)
#         return None

# # Define your conversation messages
# messages = [
#     {"role": "user", "content": "What is your favourite condiment?"},
#     {"role": "assistant", "content": "Well, I'm quite partial to a good squeeze of fresh lemon juice. It adds just the right amount of zesty flavour to whatever I'm cooking up in the kitchen!"},
#     {"role": "user", "content": "Do you have mayonnaise recipes?"}
# ]

# # Concatenate messages into a single string
# inputs = " ".join([message["content"] for message in messages])

# # Make a query to the Hugging Face API
# data = query({"inputs": inputs})

# # Print the generated response
# print(data)















import requests

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
API_TOKEN = "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"

headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    try:
        data = response.json()
        generated_text = data[0]['generated_text']
        print(generated_text)
        # Find the index of the first occurrence of '[/INST]'
        prompt_index = generated_text.find('[/INST]')
        # Extract the text after the prompt
        if prompt_index != -1:
            generated_text = generated_text[prompt_index + len('[/INST]'):]
            print(generated_text)
        return generated_text
    except Exception as e:
        print("Error decoding response:", e)
        print("Response content:", response.content)
        return None


text="""
02-02-2024 
OS-INT Investigation Report 
Event :- Regarding call for protest in Delhi on 13-02-2024 by Farm 
unions and other groups. 
Brief of Event :- During routine social media monitoring some twitter 
handles were observed posting extreme and radical contents, seemingly inciting 
violence in the planned protests. 
Analysis 
The study of various 
social media posts widely being disseminated regarding 
planned protest by farmer associations reveals the following major points:- 
1. Sentiments of people associated with faming and related activities is being 
tried to be exploited to create large gatherings inside Delhi and cause 
a 
blockade like situation seen in the farmers’ protest o£2020-21. Various media 
influencer profiles like @ramanmann1974, @Iam_MKharaud, @bkuSbs 
among various others are sharing radical posts to incite the sentiments of 
people. 
2. Twitter hashtags like #Iw_ﬁﬁ_amﬁf, #Battle4MSP, #FarmersProtest2 
are being shared with images reflecting violent nature like burning effigies, 
blocking 
of 
important 
roads, 
digging 
of highways, 
causing 
fires 
in 
government building and public places. 
3. Use of large convoy of tractors for symbolizing the cause of farmers and also 
as a potent means to cause law enforcement problems like traffic disruptions 
and damage to public property 1s highly anticipated. Possibility of a long-haul 
protest 1s also assumable as multiple videos of people arranging firewood and 
other camping material in tractor trolleys have been seen. 
4. Going through social media posts widely glorifying the unrest caused by 
farmers in various European countries, it’s evident that a synonymy is trying 
to be established to elevate the cause of farmers as 
a global fight between 
farmers and related local governments. Multiple posts 
are being shared 
glorifying the damages caused to public property in such nations and sighting 
them as examples to promote violent protests 
in the same manner in the 
country. 
5. Prominent organizations being talked about — Progressive Farmers Front, 
BKU (Shaheed Bhagat Singh). 
02-02-2024 
Hashtags Used :- 
#FarmersProtest 
#FarmersProtest2 
#FarmersProtest 2 
#Justice4LakhimpurFarmers 
#13wadt_fewedt 
g 
#Battle4MSP 
#NoFarmersNoFood 
Details of Twitter (X) Profiles :- 
SL. 
| Profile Name 
Profile ID 
URL 
No. 
01. 
| Ramandeep Singh 
(@ramanmannl974 | https:/twitter.com/ramanmann1974 
Mann 
02. 
| Manakdeep Singh 
@Iam_MKharaud | https:/twitter.com/Iam MEKharaud 
Kharaud 
03. | Bhartiya Kisan Union 
| @bkuSbs 
https://twitter.com/bkuSbs 
(Shaheed Bhagat 
Singh) 
04. | aviator hardeep 
@Aviator_hardeep | https:/twitter.com/Aviator_hardeep 
05. | Surjeet Singh Phul 
@phool_surjeet 
https:/twitter.com/phool_surjeet 
06. | Inderjeet Barak 
@inderjeetbarak 
https://twitter.com/inderjeetbarak 
07. 
E?rufrg Deep Sandhu 
| @_Deep_KSandhu | https:/twitter.com/_Deep_KSandhu 
08. 
| Murti Nain 
@Murti_Nain 
https://twitter.com/Murti_Nain 
Online Pamphlets circulated :- 
161 3ricieror 2 
@ 
13 wradl Rechl goar SRR 
sk 
https://twitter.com/ 
Deep KSandhu/status/1752172015749140965/photo/1 | https://twitter.com/ 
Deep KSandhu/status/1752172015749140965/photo/2 
02-02-2024 
Posts on Twitter (X) :- 
e 
B St 
e £ 
2 
s 
Y 
@ ah e 
‘twitter.com/bkuSbs/status/1752222694165393794 
hitps://twitter.com/kavitadahiyad9/status/1751950911990296827 
~ T @ 
assf 
mTeET 
TegAY TSy 
fasar=iY 
¥ 
arer, wrorar 
3 
fasar fararaare 
https: 
//twitter.com/Murti_Nain/status/1751781460162531336 
« 
 Post 
#rarmerserotest In Indla bes 
march towards Delhi o 
again on 13th of February 2024 with 
hitps://twitter.com/Aviator_hardeep/status/1751533018827915713 
https://twitter.com/phool surjeet/status/1751952465736724612 
https://twitter.com/inderjeetbarak/status/1752149606815936854 
02-02-2024 
« 
 Post 
T 
— 
Ramandecp Singh Mann 
13 T 
B MR TR 
T 1 e R 1 R 
e 
< Bt 
T 
A SR 
G TAENE  #FarmersProtest2 
1234PM - Jan 
2! 
https: 
//twitter.com/ramanmann1974/status/1751863967797133772 
2024 
3,300 
« 
 Post 
Ramandeep Singh Mann 
@ramanmanmgra 
13 B3a{l Rl 29 91 30l 
5 
e fsurl ar 
3 
S 0= A4 
e 
a 
et ot S <R £, FRell g 
o8t e 
3 
o1 
3 et o s 
S ARt 
e faaTT e o 
A R 
o 
T T 
MSP TRE 
T o, i T o MSP TR TR BT S 
1122 AM - Jan 
20, 2024 - 5,008 
Views 
hitps://twitter.com/ramanmann1974/status/1748584361698476324 
« 
 Post 
11 Ramandess Singh Mann reposted 
Ramandesp 
Singh Mann 
@ramanmanntaza 
Farmers are marching to Delhi 
on 13 February, for MSP Guarantee Law, 
‘which was promised by the Govt, at the end of #FarmersProtest; 
preparations are on In every village, farmers are coming for a long haul. 
Here, firewood is being collected in Mann Village for #FarmersProtest2 
| 
49 AM - Jan 28, 
4. 26.8K 
< 
Pose 
Farmer 
agitation is going on continuously 
In European countries. 
Even in 
The Aslan Country INGIA. farmers are ContinUGUALY 
TAKING 10 the streats 
andt 
2 biE call has baen given for the capital Delhi on 
13t February. But 
hitps://twitter.com/lam_MKharaud/status/1751789210414264811 
https://twitter.com/ramanmann1974/status/1751429713510445166 
< 
 Post 
Belglum Farmers come herel 
Solidarity Is now spreading across Europe as farmers 
Join protests In 
Belgium 
Germany 
Romania 
Belgium 
italy 
Potand 
Spain 
Netherlands 
Lathenia 
After 
2 years of Delhi #FarmersProtest, on 13th February. Indian farmers. 
are also marching towards Delhi demanding "MSP Guarantee 
Act'll 
@NoFarmsNoFoods @Randatiabib 
#FarmersProtest 2 #ImREE favet T 
https://twitter.com/lam MKharaud/status/1751825100067000523 
< 
Post 
avintor hordecp @ 
The unsung hero of India's #FarmersProtest of 2020 and 3 Pivot behind 
the unity of Farm unions then and now - 
S. @ramanmanms7a 1 
No amount of words can express his hard work, His untiring efforts to 
pull the Farming world out of distress. 
Farmers across the country see in him- a promising figure who would 
continue to express their hardships to the Political class in a forceful yet 
humble manner 
Fortunately the latter recognize 
his huge importance, his presence 
in this 
most Important sector for Country's economy. 
Mobilizing and bringing everyone on board for upcoming February 13 
March towards Delhi wouldn't have been possible without his efforts. 
& tva Viaaraingerbroak ana 
7 otnars 
1245 PM - Jan 28,2024 - 9,440 Views 
hitps://twitter.com/ramanmann1974/status/1751651949240615072 
02-02-2024 
« 
 Post 
@ 
momnases 
s ann 
e e 
a1 40 
e 
<« 
 Post 
@ oo S en 
Fires outside French Governmen Buildings. 
armers take to disging 
up 
Highways that 
Update on farmers’ Agitation (21/02/24)
Shambhu Border (Ambala-Patiala):
1. Approx. 14000 farmers are present at the Sambhu border.
2. Approx. 1500 tractors and 300 cars are present at the Shambhu border.
3. Haryana Police urged their Punjab counterparts to seize bulldozers and other
 earthmoving equipment from the interstate border which they say protesters will use to
 break barricades.
4. Haryana Police ASI Kaushal Kumar, posted at Shambhu border, died due to
 deteriorating health.
Dattasingh Border/Khanauri (Jind-Sangroor):
1. Approx. 8000 farmers are present at the Dattasingh border.
2. Approx. 1200 tractors are present at Dattasingh border.
Situation in Singhu border/ Rest of India:
1. The Delhi Police directed security personnel deployed at Tikri, Singhu and Ghazipur
border points to stay alert and conducted mock drills to counter protesting farmer's
proposed march towards the national capital.
2. Delhi Police has said that two lanes of the Ghazipur border have been closed. The
border can also be shut down if needed.
3. 50 farmers marching to Delhi have been detained by Gurugram police and brought to
Manesar.Update on farmers’ Agitation (16/02/24 till 1700 Hrs) 
  

Shambhu Border (Ambala-Patiala)

From amputations and fractures to corneal and head injuries, nearly 100 protesting farmers have been hospitalized with serious injuries after clashing with the Haryana Police on the Shambhu and Khanauri borders over the last 2 days.
Vehicles Stuck In Jam From Singhu To Auchandi Border Due To Farmers Protest. Commuters facing high inconvenience as border remains closed.
Police fired tear gas to disperse the protesting farmers at Shambhu border today. Video visuals showed farmers running away to escape the tear gas shells being fired at them. 
Limited impact of Bharat Bandh has been seen in some areas of Punjab and Haryana. Shops remained closed in many markets, while commercial and government institutions also remained closed in these areas.
Lawyers in Fatehgarh Sahib supported Bharat Bandh.
If the government does not accept the demands of the farmers, the momentum of movement will intensified  further." Statement of farmer leader Rakesh Tikait

Dattasingh Border/Khanauri (Jind-Sangroor)

The BKU (Ekta-Ugrahan), which has a significant farmer base in Punjab, today decided join the ongoing protest being spearheaded by the Samyukta Kisan Morcha and Kisan Mazdoor Sangharsh Committee (KMSC) at Shambhu and Khanauri borders besides holding sit-ins in front of the houses of state BJP president Sunil Jakhar, former CM Capt Amarinder Singh and ex-MLA Kewal Singh Dhillon on February 17 and 18.

Rajasthan
              
In Hanumangarh, Rajasthan  the farmers were protesting at a programme where Prime Minister Narendra Modi was speaking virtually. As the protesting farmers broke barricades, the police swung into action, lathi charging the crowd to stop them from disrupting the function.


"""
prompt = """
[INST]Please analyze the provided {text} data and identify all instances of security-related incidents, including encounters, apprehensions, deaths, detentions, closures, directives, or any other significant events involving law enforcement or militant activities. Consider activities like protests, clashes, arrests, drug trafficking, arms and ammunition, terrorist-related activities, killing, or any other disturbances related to public safety.Summarize the total number of distinct incidents recorded in the provided data in a table format with the following columns: 'Incidents Type', 'Location', 'Incident Details', and 'Total Incidents'. Ensure each incident is appropriately categorized, and provide additional context or insights wherever possible. For example, include details about the parties involved, the response from law enforcement agencies, or the impact on local communities. Your analysis should aim to capture all relevant security-related events comprehensively. Additionally, please include a row at the end of the table showing the total count of incidents across all categories.Please dont append prompts in the response.[/INST]
"""
data = query({"inputs": prompt})

print(data)




