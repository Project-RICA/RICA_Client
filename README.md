[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
> __This license applies only to _code files_ on this repository.__ Other files of this project aren't distributed.\
> Check the 'Abstract' and 'Open Source Policy' part.

# 🐋 RICA
  

<img src="/Document/RICA%20Logo.png" width="100" height="100" align="left">

```
Realtime Improving Comment Analyzer


Made by ForestHouse
```

---
## 🧾 Abstract
Nowadays, various type of comment is being used to help content viewers communicate with each other.\
And also the quality of comment is a big problem. It makes other viewers feel unpleasantness.\
To prohibit this, google is using their AI to figure out what is the bad comment, but in Korean, its results look not good.\
Because of Korean Language's complexity, it shows lower performance than that in English analyzing.\
Many content uploaders suffering by many insults included in the comments.\
The solution is make more powerful, automated comment manager.\
But over time, it's accuracy would be decreased because users try to bypass this system and many words are newly coined in realtime.\
To prvent this, RICA will keep learning itself, and get some feedbacks from developers regularly.

### About open source policy
It could be hard to open main source code to the public, because this is not a completly perfect AI.\
If comment writers who can understand this code spread the principle of operation, some of writers would write comment that RICA cannot catch.\
It means someone can viciously use vulnerable part of RICA.\
So except contributors, the main source code will not be uploaded to here.\
If you want source code for education, public usage, or wnat to join as a contributor, please submit this [Google Form](https://docs.google.com/forms/d/e/1FAIpQLSf6HtJSLUeD-HPErs-TCQXS96EDYWow1qciISIiXQIloPRrww/viewform?usp=sf_link)\
It takes about 1~3 days. We will try to reply to you within a week at the latest.

---
## 🧱 Structure
RICA operates with two engine.

- ### ⚙ RICA Engine
  - #### Feature Class
    RICA check the intensity of each feature to apprehend comment writer's intention.
    ```
    - Positive <-> Negative : words(± type, x(weight) type), conjunctions, flow of context
    - Happiness <-> Anger : words(± type, x(weight) type)
    - Criticism : words
    - Blame : words
    - Advertisement : words, flow of context, [Obfuscation]
    - Obfuscation : words construction and organization, complexity of consonant and vowel compound
    - Formalness : words, end of sentence
    ```
    Higher value means the comment contains that feature.\
    RICA learn with this feature values. Each values range 0 to 100.\
    (In the Positive and Happiness features, the neutral value is 50.)\
    If negative features' value is bigger than the critical point(Might be change continuously), RICA will be take an action.

  - #### Operation Sequence
    RICA extracts the value of each features in this sequence :
    ```
    Obfuscation -> [Trick Engine] Converting -> Positive -> Happiness -> Formalness -> Criticism & Blame -> Advertisement
    ```
    If Obfuscation level is not 0, it will be sent to Trick Engine and converted to normal sentence RICA can understand.

  - #### Learning
    This engine use RNN. (And also it can learn data in __realtime__. Check the 'RICA Engine RLS')\
    All initial data should be preprocessed via devs.\
    The learning method is similar to spam mail one. Collect sentences and assign each feature value, and put it.\
    And later, most learning will be automatically executed by RLS, devs often checking it.


- ### ⚙ Trick Engine
  - #### Applicable Comment Type
    Some examples will let you know what type of comment is appropriate to be handled in this.
    ```
    * The => sign means translated sentence.

    - 28 섀킈야
    => 28 Sheep

    - 이렿계 하면 변역퀴도 졀떄 묫 알아듣곘죠? 여기 겁놔 뜨뤄워요 가즤 마셰요.
    => If you talk about this, did you understand the translation quill? It's scary, it's hot here, it's Mache.

    - 설ㅁㅏ 띄ㅇㅓㅅㅓ 쓰면 못 알ㅇㅏ 듣는 ㄱㅓ임?
    => I can't understand it if I write it, but I hear it?
    
    - ㄱ ㅓ ㄷ ㅐ ㅎ ㅏ  무 ㅈ ㅏ
                   ㄴ   ㄴ
    => a ㅓ ㅐ ha ha ha ha
                no
    
    - ^^|발
    => ^^|
    
    - h티티ps://h0st.address.컴

    - ㅋㅋ ㅏ ㅋㄴ 토 옼 = yousu쓰리8삼
    
    - 안?녕?하?세?요? (The comment mosaiced by using special ascii code)

    -병진아, 너 뭐하니?
     신나게 놀고 있는데?
     씨앗은 다 모으고 놀고 있는거지?
     발전기 옆 상자에 놔뒀어. 많이 모아놨으니까 걱정말라고.
     고맙다. 분배는 1/3 콜?
     로떼마트에 팔아서 가져가는 수수료보다 더 크네
     세상 물정 모르는 놈일세, 씨앗만 모아놓고 뭘 더 바라는겨
     끼니 챙길 정도는 줘야하는거 아님? 끼니 3번은 국룰이지
     임마 그럼 니가 다 키워서 마트 가서 직접 팔아라.
     ㄹㅇ?
     ㅇㅇ
     
    ```
    Trick engine, as its name implies, finds tricks so that prevent vicious users' bad comment.\
    That is, it's a kind of preprocessing engine using AI. This engine returns value to RICA Engine.
    
  - #### Functions
    Trick engine can be composed various neural networks to enhance the accuracy of each type of tricks.\
    For example, handle ^^|발 with CNN, handle 28 섀킈야 with sound RNN, etc.\
    In this occasion, GoogleTranslation's system may help us to analyze the tricks..
    It seems that they also using the pronunciation when they translate sentences.\
    So they could answer correctly in some words.\
    Also they have databases about newly coined words and slangs. (e.g. '멋졍' translated to 'cool', 'ㅇㅇ' to 'Yep')\
    But it is the part of word too, it should handle by RICA engine.\
    Now we can know what we need.
    ```
    - Pronunciation Converter (Matching with dict values -> RNN, Google Translation)
    - Shape Converter (CNN)
    - Keyboard language Converter (Google Translation, Googling) (e.g. '안녕'->'dkssud' , 'Hello'->'ㅗ디ㅣㅐ')
    ``` 
    
- ### ✂ Preprocessor
  Because we need flow of context and positive level, we cannot consider interjection, mimetic words, and onomatopoeia as 'Stopword'.\
  Just copying stopwords and pasting them isn't a good solution.\
  So, RICA needs a unique preprocessing mechanism for itself.

  - #### Kind of Processing
    ```
    - Replace (Some part of common stopwords)
    - 
    ```

- ### 📝 Realtime Learning System (RLS)
  Realtime learning is the most important part of RICA becuase of continuously changing comment types\
  RLS will be triggered by some type of comments.
  For the accuracy of RLS and to prevent mishandling, they'll will be sent to devs.
  
  - #### RICA Engine RLS
    If the obfuscation level is 0 and there is a newly coined word, RICA will find it on the internet.\
    And if level is not 0, RICA won't find the mean of the word processed by Trick Engine, just send it, because of risk of mishandling.
    
  - #### Trick Engine RLS
    RICA will save some comments that it cannot interpret to request analysis about a new type of comments.\
    So other tricks not written in here will be updated later when RICA found them.


---
## 💬 Comments
  - ### ▶ YouTube
    There is two options to make a queue of new comments.\
    \
    In the comment tab of YouTube creator studio, there is a filter owner can check the unreplied comment.\
    'Unreplied' means the owner of channel hasn't responsed, and the response contains not only owner's comment, also sending a 'heart'.\
    So grant the authority of comment manager to RICA in YouTube channel, and check the comments by press 'heart'.\
    \
    Or we can check the option 'block all comment temporarily to check it' and wait to RICA analyze it.\
    \
    The latter will be better than the former, but it can look like a censorship.\
    So we recommend you to select the former one.
    
  - ### (Will be added)

---
## 🔌 Source
- [KoNLPy](https://github.com/konlpy/konlpy)\
  Notice : KoNLPy adopted GPL3.0 license, but because this program's main module is not for distribution, RICA doesn't have to adopt this license.

- [AI Hub](https://aihub.or.kr/)\
  Sentence Data

- ~~[Everyone's Corpus](https://corpus.korean.go.kr/main.do)~~\
  ~~Corpus Data~~
