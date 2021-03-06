[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
> __This license applies only to _code files_ on this repository.__ Other files of this project aren't distributed.\
> Check the 'Abstract' and 'Open Source Policy' part.

> Updated Date : 2021/12/20 v.fix
# ๐ RICA ๐ณ
  

<img src="/Document/RICA%20Logo.png" width="100" height="100" align="left">

```
Realtime Improving Comment Analyzer


Made by ForestHouse
```

---
## ๐งพ Abstract
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
So except contributors and providers, the main source code will not be gone public and uploaded to here.\
If you want source code for education, public usage, or want to join as a contributor, please submit this [Google Form](https://docs.google.com/forms/d/e/1FAIpQLSf6HtJSLUeD-HPErs-TCQXS96EDYWow1qciISIiXQIloPRrww/viewform?usp=sf_link)\
It takes about 1~3 days. We will try to reply to you within a week at the latest.

---
## ๐งฑ Structure
RICA operates with two engine.

- ### โ RICA Engine
  - #### Feature Class
    RICA check the intensity of each feature to apprehend comment writer's intention.
    ```
    - Obfuscation : words construction and organization, complexity of consonant and vowel compound
    - Positive <-> Negative : words(ยฑ type, x(weight) type), conjunctions, flow of context
    - Happiness <-> Anger : words(ยฑ type, x(weight) type)
    - Formalness : words, end of sentence
    - Criticism <-> Blame : words, [Formalness]
    - Sexuality : words
    - Advertisement : words, flow of context, [Obfuscation]
    ```
    Higher value means the comment contains that feature more.\
    RICA learn with this feature values. Each values range 0 to 100.\
    (In the Positive and Happiness features, the neutral value is 50.)\
    If negative features' value is bigger than the critical point(Might be change continuously), RICA will take an action.

  - #### Operation Sequence
    RICA extracts the value of each features in this sequence :
    ```
    Obfuscation -> [Trick Engine] -> Positive -> Happiness -> Formalness -> Criticism -> Sexuality -> Advertisement
    ```
    (* *[Trick Engine] activates when Obfuscation > Crit.Point*)\
    If Obfuscation level is bigger than critical point, like negative features' value, sentences will be sent to Trick Engine and converted to normal sentence RICA can understand.\
    And if that level is much bigger than critical point, [Inference based Pre-Block System] will immediately concider the comment as a kind of garbage.

  - #### Learning
    This engine use LSTM. (And also it can learn data in __realtime__. Check the 'RICA Engine RLS')\
    All initial data should be preprocessed via devs.\
    And later, most learning will be automatically executed by RLS, devs often checking it.\
    \
    The learning method is similar to spam mail one. Collect sentences and assign each feature value, and put it.\
    Each features have each neural networks. And some features affected by preceding feature.\
    (e.g. Criticism value is decided with words and [Formalness] value.)\
    So we should train networks following the Operation Sequence.\
    The method of each features' train :
    ```
    Obfuscation : Normal(0) <-> Weird Sentence(100)
    
    Positive : Negative Sentence(0) <-> Positive(Declarative) Sentence(100)
    
    Happiness : Angry(0) <-> Normal(50) <-> Happy(100)
    
    Formalness : Informal(0) <-> Formal(100)
    
    Criticism : Blame(0) <-> Normal(50) <-> Criticism(100)
    
    Sexuality : Normal(0) <-> Sexual Sentence(100)
    
    Advertisement : Normal(0) <-> Advertisement(100)
    ```
    For example, when dev train Obfuscation model, the train sentences' features except Obfuscation must not be same to be flexible.\
    If dev gives only formal, positive, non-AD sentences to that model, it could be vulnerable to informal, negative, AD sentences.\
    And to achieve this goal(flexibility), we need various data, or this Obfuscation model's criteria will not be Obfuscation but another thing.


- ### โ Trick Engine
  - #### Applicable Comment Type
    Some examples will let you know what type of comment is appropriate to be handled in this.
    ```
    * The => sign means translated sentence.

    - 28 ์ํ์ผ
    => 28 Sheep

    - ์ด๋?ฟ๊ณ ํ๋ฉด ๋ณ์ญํด๋ ์ก๋ ๋ฌซ ์์๋ฃ๊ณ์ฃ?? ์ฌ๊ธฐ ๊ฒ๋ ๋จ๋ค์์ ๊ฐ์ฆค ๋ง์ฐ์.
    => If you talk about this, did you understand the translation quill? It's scary, it's hot here, it's Mache.

    - ์คใใ ๋ใใใใ ์ฐ๋ฉด ๋ชป ์ใใ ๋ฃ๋ ใฑใ์?
    => I can't understand it if I write it, but I hear it?
    
    - ใฑ ใ ใท ใ ใ ใ  ๋ฌด ใ ใ
                   ใด   ใด
    => a ใ ใ ha ha ha ha
                no
    
    - ^^|๋ฐ
    => ^^|
    
    - hํฐํฐps://h0st.address.์ปด

    - ใใ ใ ใใด ํ? ์ผ = yousu์ฐ๋ฆฌ8์ผ
    
    - ์?๋?ํ?์ธ?์? (The comment mosaiced by using special ascii code)

    -๋ณ์ง์, ๋ ๋ญํ๋?
     ์?๋๊ฒ ๋๊ณ? ์๋๋ฐ?
     ์จ์์ ๋ค ๋ชจ์ผ๊ณ? ๋๊ณ? ์๋๊ฑฐ์ง?
     ๋ฐ์?๊ธฐ ์ ์์์ ๋๋์ด. ๋ง์ด ๋ชจ์๋จ์ผ๋๊น ๊ฑฑ์?๋ง๋ผ๊ณ?.
     ๊ณ?๋ง๋ค. ๋ถ๋ฐฐ๋ 1/3 ์ฝ?
     ๋ก๋ผ๋งํธ์ ํ์์ ๊ฐ์?ธ๊ฐ๋ ์์๋ฃ๋ณด๋ค ๋ ํฌ๋ค
     ์ธ์ ๋ฌผ์? ๋ชจ๋ฅด๋ ๋์ผ์ธ, ์จ์๋ง ๋ชจ์๋๊ณ? ๋ญ ๋ ๋ฐ๋ผ๋๊ฒจ
     ๋ผ๋ ์ฑ๊ธธ ์?๋๋ ์ค์ผํ๋๊ฑฐ ์๋? ๋ผ๋ 3๋ฒ์ ๊ตญ๋ฃฐ์ด์ง
     ์๋ง ๊ทธ๋ผ ๋๊ฐ ๋ค ํค์์ ๋งํธ ๊ฐ์ ์ง์? ํ์๋ผ.
     ในใ?
     ใใ
    ```
    Trick engine, as its name implies, finds tricks so that prevent vicious users' bad comment.\
    That is, it's a kind of preprocessing engine using AI. This engine returns value to RICA Engine.
    
  - #### Functions
    Trick engine can be composed various neural networks to enhance the accuracy of each type of tricks.\
    For example, handle ^^|๋ฐ with CNN, handle 28 ์ํ์ผ with sound RNN, etc.\
    In this occasion, GoogleTranslation's system may help us to analyze the tricks..\
    It seems that they also using the pronunciation when they translate sentences.\
    So they could answer correctly in some words.\
    Also they have databases about newly coined words and slangs. (e.g. '๋ฉ์ก' translated to 'cool', 'ใใ' to 'Yep')\
    But it is the part of word too, it should handle by RICA engine.\
    Now we can know what we need.
    ```
    - Pronunciation Converter (Matching with dict values -> RNN, Google Translation)
    - Shape Converter (CNN)
    - Keyboard Language Converter (Google Translation, Googling) (e.g. '์๋'->'dkssud' , 'Hello'->'ใ๋ใฃใ')
    ``` 
    
- ### โ Preprocessor
  Because we need flow of context and positive level, we cannot consider interjection, mimetic words, and onomatopoeia as 'Stopword'.\
  Just copying stopwords from web pages and pasting them isn't a good solution.\
  So, RICA needs a unique preprocessing mechanism for itself.

  - #### Kind of Processing
    ```
    - Split & Replace (Some part of common stopwords)
    - ===============================================================================================================Delete this.
    ```

- ### ๐ Realtime Learning System (RLS)
  Realtime learning is the most important part of RICA becuase of continuously changing comment types\
  RLS will be triggered by some type of comments.\
  For the accuracy of RLS and to prevent mishandling, they'll will be sent to devs.
  
  - #### RICA Engine RLS
    If the obfuscation level is 0 and there is a newly coined word, RICA will find it on the internet.\
    And if level is not 0, RICA won't find the mean of the word processed by Trick Engine, just send it, because of risk of mishandling.
    
  - #### Trick Engine RLS
    RICA will save some comments that it cannot interpret to request analysis about a new type of comments.\
    So other tricks not written in here will be updated later when RICA found them.


---
## ๐ฌ Usage
This part shows you where RICA can exert its power, and contains the guide of the initial setting per each place.

  - ### โถ YouTube
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
    
  - ### ๐ฎ Discord
    _RICA bot will start to be developed after the first YouTube version of RICA successfully works there._\
    _And also RICA need DB before analyzing the various chat in Discord channel. Normal talks are much complex to do it._\
    _Comming Soon!_
    
  - ### (Will be added)

---
## ๐ Third-Party Lib & Data Source
- __Some data is generated by Team RICA.__

- [KoNLPy](https://github.com/konlpy/konlpy)\
  Notice : KoNLPy adopted GPL3.0 license, but because this program's main module is not for distribution, RICA doesn't have to adopt this license.

- [AI Hub](https://aihub.or.kr/)\
  Sentence Data

- ~~[Everyone's Corpus](https://corpus.korean.go.kr/main.do)~~\
  ~~Corpus Data~~
