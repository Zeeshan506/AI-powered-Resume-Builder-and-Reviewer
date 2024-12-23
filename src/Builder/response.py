import os
import google.generativeai as genai

api_key = "AIzaSyDHcWLsDv5REcL54DBAcdSiiQKqtgWeTIU"
genai.configure(api_key=api_key)

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash-exp",
  generation_config=generation_config,
)

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "I want to create a tone analyzer which returns a score out of 15. you will analyze the text i provide you and return the score. how does it sound? can u do that.\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Okay, I understand! You want me to act as a tone analyzer, taking text as input and returning a score out of 15, representing the overall emotional tone of the text. \n\n**Yes, I can definitely do that!** \n\nHere's how I envision it working:\n\n*   **You provide the text:** You'll paste or type the text you want me to analyze.\n*   **I'll analyze the text:** I will look for clues within the text to determine the overall tone. This will include things like:\n    *   **Sentiment:** Positive, negative, or neutral language.\n    *   **Emotion:** Words expressing joy, sadness, anger, fear, etc.\n    *   **Intensity:** The strength of the emotions expressed.\n    *   **Subjectivity:** How much of the text is based on personal opinion or experience.\n    *   **Clues from punctuation, formatting, and structure**\n\n*   **I'll provide a score:** I will assign a score from 0 to 15, where:\n    *   **Lower scores (0-5):** Generally indicate a very negative, sad, or critical tone.\n    *   **Mid-range scores (6-10):** Typically suggest a neutral, factual, or slightly positive/negative tone.\n    *   **Higher scores (11-15):** Generally represent a very positive, happy, or enthusiastic tone.\n\n**Important Notes:**\n\n*   **This is an approximation:** Tone analysis is complex and can sometimes be subjective. My analysis will be based on the patterns I've learned.\n*   **I'm not a human:** I don't \"feel\" emotions. I analyze text patterns and assign a score based on them.\n*   **I can't explain *why* I give each score** I will return just the score.\n*   **Please be clear about your expectations:** If you're looking for something more specific, let me know (e.g., if you want to focus on a particular emotion or type of language).\n\n**Ready to Try It?**\n\nPlease provide me with the text you'd like me to analyze, and I'll give you a score out of 15!\n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "j  n n  g  r  n e r 4567 main street chic ago illinois 98052 • 716 555 0100 • jannaexamplecom human resources generalist  6 years  experience assisting   fulfilling organization staffing needs  requirements  proven track record  using  excellent personal communication  organization skills  lead  improve hr departments recruit excellent personnel  improve department efficiencies team player  excellent communication skills high quality  work driven  highly self motivated strong negotiating skills  business acumen  able  work independently e x p e r  e n c e 20xx – present human resources generalist lamna healthcare company chicago illinois review update  revise company hiring practices vacation   human resources policies  ensure compliance  osha   local state  federal labor regulations  creating  maintaining  positive  responsive work envi ronment  raised employee retention rates   10  achieve  greater  90 employee retention   2 year period developed recruitment programs  successfully increase minority recruitment  meet affirmative action requirements led develo pment team  build  deploy  dedicated recruitment website  reduced year  year recruitment costs  14 june 20xx – august 2 0xx human resources intern wholeness healthcare boomtown ohio assisted  recruitment outreach  prospective emp loyees organized  conducted several seminars  hospital employees  educate  update  regarding available employment benefit options arranged hospital wide guest speakers symposia  educate management  new employment laws  workplace confidence  morale building techniques administrative tasks  k  l l  type 96 words per minute • proficient  project management software • team player • excellent time management skills • conflict management • public speaking • data analytics e  u c     n may 20xx bachelor  arts human resources management jasper university ft lauderdale fl 38 gpa • member  university’s honor societ   c   v    e  literature • environmental conservation • art • yoga • skiing • travel",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Okay, I've analyzed the text you provided. Based on the content, which is a resume/CV, I'm assigning it a score of **10 out of 15.**\n\n**Reasoning:**\n\n*   **Neutral and Professional Tone:** Resumes and CVs are generally written in a neutral and professional tone. The focus is on factual information, skills, and accomplishments rather than strong emotions or opinions.\n*   **Positive but Objective Language:** Words like \"excellent,\" \"high-quality,\" \"proven track record,\" \"successfully,\" and \"positive\" indicate positive qualities. However, they are presented as objective claims about skills and results, not as expressions of intense feelings.\n*   **Absence of Negative Language:** There is no significantly negative language present.\n*   **Focus on Achievements:** The text highlights accomplishments and skills, which is a good thing in a resume. These achievements are presented as neutral factual claims rather than emotionally charged pronouncements.\n\nLet me know if you have any other text you'd like me to analyze!\n",
      ],
    },
  ]
)

response = chat_session.send_message("may riley 4567 main street buffalo new york 98052 716 555 0100 mrileylivecom wwwlinkedincominmriley profile friendly  engaging team player  leader able  inspire staff  perform  best detail oriented  experienced restaurant manager passionate  food  beverages  multi tasker  excels  staff training  recruiting   track record  inspiring great customer service  customer satisfaction regularly exceed sales goals  master   art  upselling experience restaurant manager contoso bar  grill september 20xx – present · recruit hire train  coach  30 staff members  customer service skills food beverage knowledge sales  health safety standards · reduced costs  7  controls  overtime operational efficiencies  reduced waste · consistently exceed monthly sales goals   minimum  10  training foh staff  upselling techniques   creating  featured food  beverage program restaurant manager fourth coffee bistro june 20xx – august 20xx · created  cross training program ensuring foh staff members  able  perform confidently  effectively   positions · grew customer based  increased restaurant social media accounts  19  interactive promotions engaging postings  contests · created  implemented staff health  safety standards compliance training program achieving  score  99   board  health · successfully redesigned existing inventory system ordering  food storage practices resulting   6 decrease  food waste  higher net profits education bs  business administrat ion june 20xx bigtown college chicago illinois aa  hospitality manageme nt june 20xx bigtown college chicago illinois skills abilities · accounting budgeting · proficient  pos systems · excellent interpersonal  communication skills · poised  pressure · experienced   res taurant positions · fun  energetic activities  interests theater environmental conservation art hiking skiing travel")

print(response.text)