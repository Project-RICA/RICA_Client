[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
> __MIT 라이센스는 _이 레포지토리에 있는 코드_에만 적용됩니다..__ 이 프로젝트의 다른 파일들은 배포되지 않습니다.\
> 전체 파일에 대한 배포는 'Abstract' 및 'Open Source Policy' 부분을 참고해주세요.

> README_KR은 README에서 번역하는 방식으로 업데이트 됩니다.\
> 가장 최신 버전의 README를 보시려면 원본 또는 ReadMe-Modifying브랜치의 ReadMe를 참고해주시기 바랍니다.\
> README_KR Updated Date : 2021/12/08 v.beta1

# 🌊 RICA 🐳


<img src="/Document/RICA%20Logo.png" width="100" height="100" align="left">

```
Realtime Improving Comment Analyzer


Made by ForestHouse
```

---
## 🧾 Abstract
요즘에는, 매우 많은 형태의 댓글들이 콘텐츠 시청자 상호간의 소통을 위해 사용되고 있습니다.\
그리고 댓글의 질 또한 큰 문제로써 대두되고 있습니다. 그것들은 다른 시청자들을 불쾌하게 만듭니다.\
이것을 방지하고자, Google사는 그들의 AI를 이용하여 어떤 게 악성 댓글인지 찾아내고자 하지만, 한국어에서는 그것의 결과가 그리 좋지 않아보입니다.\
한국어의 복잡성 때문에, 그 AI가 한국어를 분석할 때는 영어를 분석할 때 보다 낮은 성능을 보여줍니다.\
많은 콘텐츠 창작자들이 댓글에 포함된 수많은 욕설들에 의해 고통받고 있습니다.\
해결책은 더 강력하고, 자동화된 댓글 관리 시스템을 만드는 것입니다.\
하지만 시간이 흐름에 따라, 유저들이 분석 시스템을 회피하려 들 것이고 실시간으로 생겨나는 신조어 때문에 이 시스템의 정확도는 낮아질 것입니다.\
그래서 RICA는 스스로 학습을 계속할 것이고 주기적으로 개발자들로부터 피드백을 받을 것입니다.\

### About open source policy
RICA의 메인 소스코드를 공개하는 것은 힘들 것 같습니다. 완벽한 AI가 아니기 때문이죠.\
만일 댓글을 작성하는 사람들 중 이 코드를 이해할 수 있는 사람이 작동 원리를 퍼뜨려 버린다면, 몇몇 댓글 작성자는 RICA가 감지할 수 없는 방식으로 댓글을 작성하려 들 것입니다.\
즉 누군가가 RICA의 취약점을 악의적으로 이용할 수 있다는 것이죠.\
그러므로 Contributors와 Providers를 제외하고, 메인 코드는 대중에게 공개되지 않으며 이곳에 업로드되지 않습니다.\
만약 코드를 교육적/공적 목적으로 이용하고 싶으시거나 Contributor로서 프로젝트에 참여하고자 한다면 이 [설문지](https://docs.google.com/forms/d/e/1FAIpQLScpYl2XCLTufoG6TLIWVuHwA3G7Wn_CtMxDw9WqPMusE3Fx7w/viewform?usp=sf_link)를 작성해주세요.\
응답까지 약 1~3일 걸립니다. 늦어도 1주 이내에는 답장을 드리도록 하겠습니다.

---
## 🧱 Structure
RICA는 두 엔진을 가지고 있습니다.

- ### ⚙ RICA Engine
  - #### Feature Class
    RICA는 각 특성들의 강도를 측정하여 댓글 작성자의 의도를 파악합니다.
    ```
    - Positive <-> Negative : words(± type, x(weight) type), conjunctions, flow of context
    - Happiness <-> Anger : words(± type, x(weight) type)
    - Criticism : words
    - Blame : words
    - Advertisement : words, flow of context, [Obfuscation]
    - Obfuscation : words construction and organization, complexity of consonant and vowel compound
    - Formalness : words, end of sentence
    ```
    높은 수치는 댓글이 해당 특성을 더 많이 포함하고 있다는 것을 의미합니다.\
    RICA는 이 특성 수치들을 통해 학습합니다. 각각의 수치는 0부터 100까지의 범위를 가집니다.\
    만일 부정적인 특성들의 수치가 임계값보다 높을 경우 RICA는 해당 댓글에 대해 조치를 취할 것입니다. (임계값은 지속적으로 바뀔 수 있습니다.)

  - #### Operation Sequence
    RICA는 아래 처리순서에 따라 각 특성들의 수치를 뽑아냅니다.
    ```
    Obfuscation -> [Trick Engine] Converting -> Positive -> Happiness -> Formalness -> Criticism & Blame -> Advertisement
    ```
    (* [Trick Engine] 은 *난독성 수치 > 임계값* 일 때에만 동작합니다.)\
    만약 난독성 수치가 임계값보다 크다면, 부정적인 수치들 처럼, 문장(댓글)은 Trick Engine으로 보내지고 RICA가 해석할 수 있는 형태로 변환됩니다.\
    그리고 만약 난독성 수치가 임계값보다 지나치게 높다면, [추론 기반 사전 차단 시스템]이 즉시 해당 댓글을 불필요한 댓글로 간주할 것입니다.

  - #### Learning
    이 엔진은 LSTM 모델을 사용합니다. (또한 실시간 학습 역시 가능합니다. 'RICA Engine RLS'를 확인하세요.)\
    모든 초기 데이터는 개발자들에 의해 전처리 과정을 거쳐야만 합니다.\
    그리고 후에, RLS에 의해 대부분의 학습은 자동적으로 시행될 것이며 개발자는 종종 이것을 검토할 것입니다.\
    \
    학습 방식은 스팸메일 분류기와 비슷합니다. 문장을 모으고 각 특성 수치를 할당하고 집어넣죠.
    각 특성은 각각의 신경망을 가집니다. 그리고 몇몇 특성들은 선행하는 특성으로부터 영향을 받습니다.
    (e.g. 비판 특성의 수치는 단어와 격식 특성의 수치를 통해 결정됩니다.)
    그래서 다음 작업 순서에 따라 신경망을 학습해야만 합니다.
    각 특성들의 학습 방법 :
    ```
    Obfuscation : Normal(0) <-> Weird Sentence(100)
    
    Positive : Negative Sentence(0) <-> Positive(Declarative) Sentence(100)
    
    Happiness : Angry(0) <-> Normal(50) <-> Happy(100)
    
    Formalness : Informal(0) <-> Formal(100)
    
    Criticism : Blame(0) <-> Normal(50) <-> Criticism(100)
    
    Sexuality : Normal(0) <-> Sexual Sentence(100)
    
    Advertisement : Normal(0) <-> Advertisement(100)
    ```
    예를 들어, 개발자가 난독 모델을 학습시킬 때, 모델의 유연성을 위해 난독 특성을 제외한 학습 문장들의 특성들은 같지 않아야만 합니다.
    만약 개발자가 난독 모델에게 격식적이고, 광고가 아닌 평서문만을 준다면, 난독 모델은 비격식체와 부정문, 그리고 광고성 문장들에 취약해집니다.
    그리고 모델을 유연하게(융통성있게) 하기 위해서는 다양한 데이터가 필요합니다. 그렇지 않으면 이 난독 모델의 판단 기준은 난독성 척도가 아니라 다른 특성이 될 겁니다.


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
    - Keyboard Language Converter (Google Translation, Googling) (e.g. '안녕'->'dkssud' , 'Hello'->'ㅗ디ㅣㅐ')
    ``` 
    
- ### ✂ Preprocessor
  Because we need flow of context and positive level, we cannot consider interjection, mimetic words, and onomatopoeia as 'Stopword'.\
  Just copying stopwords from web pages and pasting them isn't a good solution.\
  So, RICA needs a unique preprocessing mechanism for itself.

  - #### Kind of Processing
    ```
    - Split & Replace (Some part of common stopwords)
    - ===============================================================================================================Delete this.
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
## 💬 Usage
This part shows you where RICA can exert its power, and contains the guide of the initial setting per each place.

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
    
  - ### 🎮 Discord
    _RICA bot will start to be developed after the first YouTube version of RICA successfully works there._\
    _And also RICA need DB before analyzing the various chat in Discord channel. Normal talks are much complex to do it._
    _Comming Soon!_
    
  - ### (Will be added)

---
## 🔌 Third-Party Lib & Data Source
- __Some data is generated by Team RICA.__

- [KoNLPy](https://github.com/konlpy/konlpy)\
  Notice : KoNLPy adopted GPL3.0 license, but because this program's main module is not for distribution, RICA doesn't have to adopt this license.

- [AI Hub](https://aihub.or.kr/)\
  Sentence Data

- ~~[Everyone's Corpus](https://corpus.korean.go.kr/main.do)~~\
  ~~Corpus Data~~
