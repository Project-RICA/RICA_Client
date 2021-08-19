[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
> __This license applies only to _code files_ on this repository.__ Other files of this project aren't distributed.\
> Check the 'Abstract' and 'Open Source Policy' part.

# RICA
  

<img src="/Document/RICA%20Logo.png" width="100" height="100" align="left">

```
Realtime Improving Comment Analyzer


Made by ForestHouse
```

---
## Abstract
Nowadays, various type of comment is being used to help content viewers communicate with each other.\
And also the quality of comment is a big problem. It makes other viewers feel unpleasantness.\
To prohibit this, google is using their AI to figure out what is the bad comment, but in Korean, its results look not good.\
Because of Korean Language's complexity, of course it shows lower performance than that in English analyzing.\
Many content uploaders suffering by many insults.\
The solution is make more powerful, automated comment manager.\
But over time, it's accuracy would be decreased.\
To prvent this, RICA will keep learning itself, and get some feedbacks from developers regularly.

### About open source policy
It could be hard to open main source code to the public, because this is not completly perfect AI.\
If comment writers who can understand this code spread the principle of operation, some of writers would write comment that RICA cannot catch.\
It means someone can use vulnerable part viciously.\
So except contributors, the main source code will not upload to here.\
If you want source code for education, public usage, or wnat to join as a contributor, please submit this [Google Form](https://docs.google.com/forms/d/e/1FAIpQLSf6HtJSLUeD-HPErs-TCQXS96EDYWow1qciISIiXQIloPRrww/viewform?usp=sf_link)\
It takes about 1~3 days. We will try to reply to you within a week at the latest.

---
## Structure
RICA operates with two engine.

- ### RICA Engine
  - #### Feature Class
    RICA check the intensity of each feature to apprehend comment writer's intention.
    ```
    - Positive ( <-> Negative ) : words, conjunctions, flow of context
    - Criticism : words
    - Blame : words
    - Obfuscation : words construction and organization, complexity of consonant and vowel compound
    - Formalness : words, end of sentence
    ```
    Higher value means the comment contains that feature.\
    RICA learn with this feature values.\

  - #### Learning
    This engine use []

  - #### Operation Sequence
    RICA extracts the value of each features in this sequence :
    ```
    Obfuscation -> [Trick Engine] Converting -> Positive -> Formalness -> Criticism & Blame
    ```
    If Obfuscation level is not 0, it will be sent to Trick Engine and converted to normal sentence RICA can understand.


- ### Trick Engine
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
    
    - 안?녕?하?세?요? (The comment mosaiced by using special ascii code)
    ```
    Trick engine, as its name implies, finds tricks so that prevent vicious users' bad comment.
    That is, it's a kind of preprocessing engine using AI. This engine returns value to RICA Engine
    RICA will save some comment that it cannot interpret to request analyze about new type of comment.
    So other tricks not written in here will be updated later when RICA found it.
    
  - #### Functions
    GoogleTranslation seems that they also using the pronunciation when they translate sentences.\
    So they could answer correctly in some words.\
    Also they have databases about newly coined words and slangs. (e.g. '멋졍' translated to 'cool', 'ㅇㅇ' to 'Yep')\
    But it is the part of word too, it should handle by RICA engine.\
    Now we can know what we need.
    ```
    - Pronunciation Converter
    - Shape Converter (Pattern / AI Analyzation)
    - Keyboard language Converter (e.g. '안녕'->'dkssud' , 'Hello'->'ㅗ디ㅣㅐ')
    ``` 
    
- ### Preprocessor
  Because we need flow of context and positive level, we cannot consider interjection, mimetic words, and onomatopoeia as 'Stopword'.\
  Just copying stopwords and pasting them isn't a good solution.\
  So, RICA needs a unique preprocessing mechanism for itself.

  - #### Kind of Processing
    ```
    - Replace (Some part of common stopwords)
    - 
    ```

- ### Realtime Learning System
  Realtime learning is the most important part of RICA becuase of continuously changing comment types.


---
## 

---
## Open Source
- [KoNLPy](https://github.com/konlpy/konlpy)\
  Notice : KoNLPy adopted GPL3.0 license, but because this program's main module is not for distribution, RICA doesn't have to adopt this license.
