
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse
import json

# EDUSUTRA - Chapter-wise Short Questions and Answers
# Starter question bank: verify chapter names with your prescribed JAC books.

DATA = {
    "गणित": [
        ("वास्तविक संख्याएँ", [
            ("यूक्लिड विभाजन प्रमेय लिखिए।", "यदि a और b धनात्मक पूर्णांक हैं, तो a = bq + r, जहाँ 0 ≤ r < b होता है।"),
            ("अपरिमेय संख्या किसे कहते हैं?", "जिस संख्या को p/q के रूप में नहीं लिखा जा सकता, जहाँ q शून्य नहीं है, वह अपरिमेय संख्या है।")
        ]),
        ("बहुपद", [
            ("बहुपद के शून्यक किसे कहते हैं?", "बहुपद p(x) का वह मान α शून्यक कहलाता है जिसके लिए p(α) = 0 हो।"),
            ("द्विघात बहुपद के शून्यकों का योग और गुणनफल लिखिए।", "ax² + bx + c के शून्यकों का योग −b/a और गुणनफल c/a होता है।")
        ]),
        ("दो चर वाले रैखिक समीकरणों का युग्म", [
            ("दो चर वाले रैखिक समीकरण का सामान्य रूप लिखिए।", "a₁x + b₁y + c₁ = 0 इसका सामान्य रूप है।"),
            ("संगत समीकरण युग्म किसे कहते हैं?", "जिस समीकरण युग्म का कम-से-कम एक हल हो, वह संगत कहलाता है।")
        ]),
        ("द्विघात समीकरण", [
            ("द्विघात समीकरण का सामान्य रूप लिखिए।", "ax² + bx + c = 0, जहाँ a ≠ 0, इसका सामान्य रूप है।"),
            ("विविक्तकर का सूत्र लिखिए।", "विविक्तकर D = b² − 4ac होता है।")
        ]),
        ("अंकगणितीय प्रगति", [
            ("अंकगणितीय प्रगति किसे कहते हैं?", "ऐसी संख्या श्रेणी जिसमें क्रमागत पदों का अंतर समान हो, अंकगणितीय प्रगति कहलाती है।"),
            ("AP के nवें पद का सूत्र लिखिए।", "aₙ = a + (n−1)d, जहाँ a प्रथम पद और d सार्व अंतर है।")
        ]),
        ("त्रिभुज", [
            ("समरूप त्रिभुज किसे कहते हैं?", "जिन त्रिभुजों के संगत कोण बराबर और संगत भुजाएँ समान अनुपात में हों, वे समरूप कहलाते हैं।"),
            ("पाइथागोरस प्रमेय लिखिए।", "समकोण त्रिभुज में कर्ण का वर्ग, अन्य दो भुजाओं के वर्गों के योग के बराबर होता है।")
        ]),
        ("निर्देशांक ज्यामिति", [
            ("दो बिंदुओं के बीच दूरी का सूत्र लिखिए।", "दूरी = √[(x₂−x₁)² + (y₂−y₁)²]।"),
            ("मध्य-बिंदु का सूत्र लिखिए।", "मध्य-बिंदु ((x₁+x₂)/2, (y₁+y₂)/2) होता है।")
        ]),
        ("त्रिकोणमिति का परिचय", [
            ("sin θ और cos θ की परिभाषा लिखिए।", "sin θ = लंब/कर्ण तथा cos θ = आधार/कर्ण होता है।"),
            ("tan θ किसके बराबर है?", "tan θ = लंब/आधार = sin θ/cos θ होता है।")
        ]),
        ("त्रिकोणमिति के कुछ अनुप्रयोग", [
            ("उन्नयन कोण किसे कहते हैं?", "क्षैतिज रेखा से ऊपर की ओर बनी दृष्टि-रेखा का कोण उन्नयन कोण कहलाता है।"),
            ("ऊँचाई ज्ञात करने में tan θ का उपयोग कैसे होता है?", "tan θ = ऊँचाई/क्षैतिज दूरी से ऊँचाई ज्ञात की जाती है।")
        ]),
        ("वृत्त", [
            ("स्पर्श रेखा किसे कहते हैं?", "जो रेखा वृत्त को केवल एक बिंदु पर छूती है, वह स्पर्श रेखा कहलाती है।"),
            ("स्पर्श बिंदु पर त्रिज्या और स्पर्श रेखा में क्या संबंध है?", "स्पर्श बिंदु पर त्रिज्या, स्पर्श रेखा पर लंब होती है।")
        ]),
        ("वृत्त से संबंधित क्षेत्र", [
            ("वृत्त की परिधि का सूत्र लिखिए।", "वृत्त की परिधि 2πr होती है।"),
            ("वृत्त के क्षेत्रफल का सूत्र लिखिए।", "वृत्त का क्षेत्रफल πr² होता है।")
        ]),
        ("पृष्ठीय क्षेत्रफल और आयतन", [
            ("बेलन के आयतन का सूत्र लिखिए।", "बेलन का आयतन πr²h होता है।"),
            ("गोले के आयतन का सूत्र लिखिए।", "गोले का आयतन (4/3)πr³ होता है।")
        ]),
        ("सांख्यिकी", [
            ("माध्य किसे कहते हैं?", "सभी प्रेक्षणों के योग को प्रेक्षणों की कुल संख्या से भाग देने पर माध्य मिलता है।"),
            ("बहुलक किसे कहते हैं?", "जो मान आँकड़ों में सबसे अधिक बार आता है, वह बहुलक कहलाता है।")
        ]),
        ("प्रायिकता", [
            ("प्रायिकता का मान किस सीमा में होता है?", "किसी घटना की प्रायिकता 0 से 1 के बीच होती है।"),
            ("निश्चित घटना की प्रायिकता कितनी होती है?", "निश्चित घटना की प्रायिकता 1 होती है।")
        ])
    ],

    "विज्ञान": [
        ("रासायनिक अभिक्रियाएँ एवं समीकरण", [
            ("रासायनिक अभिक्रिया किसे कहते हैं?", "वह प्रक्रिया जिसमें पदार्थ बदलकर नए पदार्थ बनाते हैं, रासायनिक अभिक्रिया कहलाती है।"),
            ("संतुलित रासायनिक समीकरण क्यों आवश्यक है?", "द्रव्यमान संरक्षण के नियम के अनुसार दोनों ओर प्रत्येक तत्व के परमाणुओं की संख्या बराबर रखने के लिए।")
        ]),
        ("अम्ल, क्षारक एवं लवण", [
            ("अम्ल किसे कहते हैं?", "वे पदार्थ जो जलीय विलयन में H⁺ आयन देते हैं, अम्ल कहलाते हैं।"),
            ("pH का मान 7 से कम होने पर विलयन कैसा होता है?", "विलयन अम्लीय होता है।")
        ]),
        ("धातु एवं अधातु", [
            ("धातुओं के दो गुण लिखिए।", "धातुएँ सामान्यतः चमकीली होती हैं और ऊष्मा तथा विद्युत की सुचालक होती हैं।"),
            ("आघातवर्धनीयता क्या है?", "धातुओं को पीटकर पतली चादरों में बदलने का गुण आघातवर्धनीयता कहलाता है।")
        ]),
        ("कार्बन एवं उसके यौगिक", [
            ("कार्बन की चतुःसंयोजकता क्या है?", "कार्बन की संयोजकता चार होती है, इसलिए यह चार सहसंयोजक बंध बना सकता है।"),
            ("समजातीय श्रेणी किसे कहते हैं?", "ऐसी कार्बनिक यौगिक श्रेणी जिसके क्रमागत सदस्यों में −CH₂− का अंतर हो, समजातीय श्रेणी कहलाती है।")
        ]),
        ("जैव प्रक्रम", [
            ("जीवन की चार प्रमुख अनुरक्षण प्रक्रियाएँ कौन-सी हैं?", "पोषण, श्वसन, परिवहन और उत्सर्जन प्रमुख अनुरक्षण प्रक्रियाएँ हैं।"),
            ("प्रकाश संश्लेषण क्या है?", "हरे पौधे सूर्य के प्रकाश में CO₂ और जल से भोजन बनाते हैं। इसे प्रकाश संश्लेषण कहते हैं।")
        ]),
        ("नियंत्रण एवं समन्वय", [
            ("न्यूरॉन क्या है?", "न्यूरॉन तंत्रिका तंत्र की संरचनात्मक और क्रियात्मक इकाई है।"),
            ("एक पादप हार्मोन का नाम लिखिए।", "ऑक्सिन एक पादप हार्मोन है जो पौधों की वृद्धि में सहायता करता है।")
        ]),
        ("जीव जनन कैसे करते हैं?", [
            ("अलैंगिक जनन किसे कहते हैं?", "जिस जनन में एक जनक भाग लेता है और युग्मकों का संलयन नहीं होता, वह अलैंगिक जनन है।"),
            ("परागण किसे कहते हैं?", "परागकणों का परागकोश से वर्तिकाग्र तक पहुँचना परागण कहलाता है।")
        ]),
        ("आनुवंशिकता", [
            ("आनुवंशिकता किसे कहते हैं?", "माता-पिता से संतानों में लक्षणों का स्थानांतरण आनुवंशिकता कहलाता है।"),
            ("जीन क्या है?", "जीन DNA का वह खंड है जो किसी विशेष लक्षण की सूचना रखता है।")
        ]),
        ("प्रकाश: परावर्तन तथा अपवर्तन", [
            ("परावर्तन का नियम लिखिए।", "आपतन कोण परावर्तन कोण के बराबर होता है।"),
            ("अपवर्तन किसे कहते हैं?", "प्रकाश का एक पारदर्शी माध्यम से दूसरे में जाने पर दिशा बदलना अपवर्तन कहलाता है।")
        ]),
        ("मानव नेत्र तथा रंगबिरंगा संसार", [
            ("रेटिना का क्या कार्य है?", "रेटिना पर वस्तु का प्रतिबिंब बनता है और यह प्रकाश संकेतों को तंत्रिका संकेतों में बदलती है।"),
            ("निकट-दृष्टि दोष किस लेंस से ठीक होता है?", "निकट-दृष्टि दोष अवतल लेंस से ठीक किया जाता है।")
        ]),
        ("विद्युत", [
            ("ओम का नियम लिखिए।", "स्थिर ताप पर V = IR होता है।"),
            ("विद्युत शक्ति का सूत्र लिखिए।", "विद्युत शक्ति P = VI होती है।")
        ]),
        ("विद्युत धारा के चुंबकीय प्रभाव", [
            ("चुंबकीय क्षेत्र रेखाएँ क्या दर्शाती हैं?", "वे चुंबकीय क्षेत्र की दिशा और सापेक्ष तीव्रता दर्शाती हैं।"),
            ("विद्युत मोटर किस ऊर्जा को किसमें बदलती है?", "विद्युत मोटर विद्युत ऊर्जा को यांत्रिक ऊर्जा में बदलती है।")
        ]),
        ("हमारा पर्यावरण", [
            ("जैव निम्नीकरणीय पदार्थ किसे कहते हैं?", "जिन पदार्थों को सूक्ष्मजीव सरल पदार्थों में तोड़ सकते हैं, वे जैव निम्नीकरणीय हैं।"),
            ("खाद्य श्रृंखला क्या है?", "जीवों के बीच भोजन और ऊर्जा के स्थानांतरण का क्रम खाद्य श्रृंखला कहलाता है।")
        ])
    ],

    "सामाजिक विज्ञान": [
        ("यूरोप में राष्ट्रवाद का उदय", [("राष्ट्रवाद से क्या तात्पर्य है?", "साझा इतिहास, संस्कृति या पहचान के आधार पर एक राष्ट्र से जुड़ाव की भावना राष्ट्रवाद कहलाती है।")]),
        ("भारत में राष्ट्रवाद", [("असहयोग आंदोलन क्यों शुरू किया गया?", "रॉलेट एक्ट, जलियाँवाला बाग हत्याकांड और खिलाफत मुद्दे के विरोध में असहयोग आंदोलन शुरू किया गया।")]),
        ("भूमंडलीकृत विश्व का बनना", [("रेशम मार्ग का क्या महत्व था?", "रेशम मार्ग एशिया और यूरोप के बीच व्यापार तथा सांस्कृतिक आदान-प्रदान का माध्यम था।")]),
        ("औद्योगीकरण का युग", [("प्रोटो-औद्योगीकरण क्या था?", "कारखानों के व्यापक विकास से पहले घरों और गाँवों में व्यापारियों के लिए उत्पादन की व्यवस्था प्रोटो-औद्योगीकरण कहलाती थी।")]),
        ("मुद्रण संस्कृति और आधुनिक दुनिया", [("मुद्रण क्रांति का एक प्रभाव लिखिए।", "मुद्रण से पुस्तकों और विचारों का प्रसार तेज हुआ।")]),
        ("संसाधन एवं विकास", [("संसाधन किसे कहते हैं?", "पर्यावरण में उपलब्ध उपयोगी वस्तु जो मानवीय आवश्यकताओं को पूरा करे, संसाधन कहलाती है।")]),
        ("वन एवं वन्यजीव संसाधन", [("जैव विविधता क्या है?", "किसी क्षेत्र में पाए जाने वाले पौधों, जीवों और सूक्ष्मजीवों की विविधता जैव विविधता कहलाती है।")]),
        ("जल संसाधन", [("वर्षा जल संचयन क्या है?", "वर्षा के पानी को एकत्र करके भविष्य में उपयोग के लिए सुरक्षित रखना वर्षा जल संचयन कहलाता है।")]),
        ("कृषि", [("रबी फसलें कब बोई जाती हैं?", "रबी फसलें सामान्यतः सर्दियों में बोई जाती हैं और वसंत ऋतु में काटी जाती हैं।")]),
        ("खनिज तथा ऊर्जा संसाधन", [("खनिज क्या हैं?", "प्राकृतिक रूप से पाए जाने वाले निश्चित गुणों वाले पदार्थ खनिज कहलाते हैं।")]),
        ("विनिर्माण उद्योग", [("विनिर्माण का अर्थ क्या है?", "कच्चे माल को प्रसंस्करण द्वारा तैयार वस्तुओं में बदलना विनिर्माण कहलाता है।")]),
        ("राष्ट्रीय अर्थव्यवस्था की जीवन रेखाएँ", [("परिवहन का महत्व लिखिए।", "परिवहन लोगों और वस्तुओं को एक स्थान से दूसरे स्थान तक पहुँचाकर व्यापार में मदद करता है।")]),
        ("सत्ता की साझेदारी", [("सत्ता की साझेदारी क्यों आवश्यक है?", "यह सामाजिक समूहों के बीच संघर्ष कम करती है और लोकतंत्र को स्थिर बनाती है।")]),
        ("संघवाद", [("संघीय शासन व्यवस्था क्या है?", "जिस शासन व्यवस्था में सत्ता केंद्र और राज्य सरकारों के बीच बाँटी जाती है, उसे संघवाद कहते हैं।")]),
        ("लोकतंत्र और विविधता", [("सामाजिक विभाजन के आधार क्या हो सकते हैं?", "भाषा, धर्म, जाति, क्षेत्र और सांस्कृतिक पहचान सामाजिक विभाजन के आधार हो सकते हैं।")]),
        ("जाति, धर्म और लैंगिक मसले", [("लैंगिक असमानता क्या है?", "लिंग के आधार पर अवसरों या अधिकारों में भेदभाव लैंगिक असमानता कहलाता है।")]),
        ("जन-संघर्ष और आंदोलन", [("लोकतंत्र में जन आंदोलन की भूमिका क्या है?", "जन आंदोलन लोगों की माँगें सामने लाते हैं और सरकार को जवाबदेह बनाते हैं।")]),
        ("राजनीतिक दल", [("राजनीतिक दल किसे कहते हैं?", "लोगों का संगठित समूह जो चुनाव लड़कर सत्ता प्राप्त करने और नीतियाँ लागू करने का प्रयास करता है।")]),
        ("लोकतंत्र के परिणाम", [("लोकतंत्र का एक प्रमुख परिणाम लिखिए।", "लोकतंत्र नागरिकों को सरकार चुनने और उससे जवाब माँगने का अवसर देता है।")]),
        ("लोकतंत्र की चुनौतियाँ", [("लोकतंत्र की एक चुनौती बताइए।", "सामाजिक और आर्थिक असमानता लोकतंत्र की एक प्रमुख चुनौती है।")]),
        ("विकास", [("प्रति व्यक्ति आय कैसे निकाली जाती है?", "कुल आय को कुल जनसंख्या से भाग देने पर प्रति व्यक्ति आय मिलती है।")]),
        ("भारतीय अर्थव्यवस्था के क्षेत्रक", [("प्राथमिक क्षेत्रक क्या है?", "जिस क्षेत्रक में प्राकृतिक संसाधनों से सीधे उत्पादन होता है, वह प्राथमिक क्षेत्रक है।")]),
        ("मुद्रा और साख", [("मुद्रा का एक प्रमुख कार्य लिखिए।", "मुद्रा विनिमय के माध्यम के रूप में कार्य करती है।")]),
        ("वैश्वीकरण और भारतीय अर्थव्यवस्था", [("वैश्वीकरण क्या है?", "विभिन्न देशों की अर्थव्यवस्थाओं का व्यापार, निवेश और तकनीक के माध्यम से जुड़ना वैश्वीकरण है।")]),
        ("उपभोक्ता अधिकार", [("उपभोक्ता का एक अधिकार लिखिए।", "उपभोक्ता को सुरक्षित वस्तुएँ और सेवाएँ पाने का अधिकार है।")])
    ],

    "अंग्रेज़ी": [
        ("A Letter to God", [("Why did Lencho write a letter to God?", "Lencho asked God for money after his crop was destroyed by hail.")]),
        ("Nelson Mandela: Long Walk to Freedom", [("What does courage mean to Mandela?", "For Mandela, courage is not the absence of fear but the triumph over it.")]),
        ("Two Stories about Flying", [("Why was the young seagull afraid to fly?", "He feared that his wings would not support him.")]),
        ("From the Diary of Anne Frank", [("Why did Anne decide to write a diary?", "She felt she had no true friend with whom she could share her thoughts.")]),
        ("The Hundred Dresses - I", [("Who was Wanda Petronski?", "Wanda was a quiet Polish girl who studied with Peggy and Maddie.")]),
        ("The Hundred Dresses - II", [("Why did Wanda's classmates feel sorry?", "They realised that their teasing had hurt Wanda.")]),
        ("A Triumph of Surgery", [("Why was Tricki taken to the hospital?", "Tricki became ill because he was overfed and did not get enough exercise.")]),
        ("The Thief's Story", [("Why did Hari Singh return to Anil?", "He returned because Anil's trust and kindness made him want to change.")]),
        ("The Midnight Visitor", [("How did Ausable fool Max?", "Ausable invented a story about a balcony and a police arrival, making Max panic.")]),
        ("A Question of Trust", [("Why did Horace Danby rob houses?", "He robbed houses once a year to buy rare books.")]),
        ("Footprints Without Feet", [("How did Griffin become invisible?", "Griffin discovered a scientific way to make his body transparent.")]),
        ("The Making of a Scientist", [("What qualities helped Richard Ebright succeed?", "Curiosity, hard work, patience and willingness to learn helped him succeed.")]),
        ("The Necklace", [("Why was Matilda unhappy?", "Matilda desired a life of luxury and believed she deserved wealth.")]),
        ("Bholi", [("How did education change Bholi?", "Education gave Bholi confidence, self-respect and courage.")]),
        ("The Proposal", [("Why do Lomov and Natalya argue?", "They argue over Oxen Meadows and later over their dogs.")])
    ],

    "हिंदी A": [
        ("गद्य खंड - पाठ अध्ययन", [
            ("गद्य पाठ का केंद्रीय विचार कैसे लिखें?", "पाठ की मुख्य घटना, लेखक का उद्देश्य और उससे मिलने वाली सीख को अपने शब्दों में संक्षेप में लिखें।")
        ]),
        ("पद्य खंड - कविता अध्ययन", [
            ("कविता का केंद्रीय भाव क्या होता है?", "कविता में व्यक्त मुख्य विचार, भावना या संदेश को केंद्रीय भाव कहते हैं।")
        ]),
        ("व्याकरण", [
            ("समास किसे कहते हैं?", "दो या दो से अधिक शब्दों के मेल से बने संक्षिप्त शब्द को समास कहते हैं।")
        ]),
        ("लेखन कौशल", [
            ("औपचारिक पत्र में किन बातों का ध्यान रखना चाहिए?", "पत्र में पता, दिनांक, संबोधन, विषय, मुख्य भाग और समापन सही क्रम में लिखना चाहिए।")
        ])
    ]
}

HTML = r"""
<!DOCTYPE html>
<html lang="hi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>EDUSUTRA</title>
<style>
*{box-sizing:border-box}
body{margin:0;background:#f2f5fb;color:#17233c;font-family:Arial,sans-serif;line-height:1.6}
header{background:linear-gradient(120deg,#101d42,#28558e);color:white;padding:25px 6%}
.brand{font-size:30px;font-weight:bold}
.tag{margin-top:6px;color:#dce8ff}
nav{display:flex;gap:8px;flex-wrap:wrap;margin-top:18px}
button,select,input{border:0;border-radius:9px;padding:12px;font-size:15px}
button{cursor:pointer}
nav button{background:#ffffff25;color:white}
main{max-width:1000px;margin:25px auto;padding:0 15px}
.panel{background:white;border-radius:15px;padding:22px;margin-bottom:18px;box-shadow:0 4px 18px #17233c10}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px}
.subject{background:#eaf1ff;color:#18345e;font-weight:bold;min-height:65px}
.note{background:#f5f7fc;border-left:4px solid #315f9f;padding:14px;margin:12px 0;border-radius:8px}
select,input{background:#edf2fc;margin:8px 5px 8px 0;max-width:100%}
.hidden{display:none}
.qa{border:1px solid #e0e6f0;border-radius:10px;margin:12px 0;padding:14px}
.qa h3{margin:0 0 8px;font-size:17px}
.answer{background:#f5f8ff;padding:10px;border-radius:8px}
.count{font-weight:bold;color:#244f89}
footer{text-align:center;padding:22px;color:#7b8495}
@media(max-width:600px){header{padding:20px 4%}.brand{font-size:25px}.panel{padding:16px}}
</style>
</head>
<body>
<header>
<div class="brand">EDUSUTRA</div>
<div class="tag">ज्ञान से सफलता की ओर। · Learn • Practice • Achieve</div>
<nav>
<button onclick="page('home')">Home</button>
<button onclick="page('questions')">Short Questions</button>
<button onclick="page('about')">About</button>
</nav>
</header>
<main>
<section id="home" class="panel" style="text-align:center">
<img src="/founder.jpg" alt="Founder photo" onerror="this.style.display='none'"
style="width:130px;height:130px;border-radius:50%;object-fit:cover;border:4px solid #28558e;">
<h1 style="color:#244f89;font-size:32px">EDUSUTRA</h1>
<h3>ज्ञान से सफलता की ओर।</h3>
<p>Learn • Practice • Achieve</p>
<h2>Class 10 Learning Hub</h2>
<p>अपना विषय चुनें और chapter-wise short questions पढ़ें।</p>
<div class="grid" id="subjects"></div>
</section>

<section id="questions" class="panel hidden">
<h1>📚 Chapter-wise Short Questions</h1>
<p>विषय और अध्याय चुनें। हर प्रश्न के नीचे उसका उत्तर दिया गया है।</p>
<label for="subjectSelect">विषय चुनें:</label>
<select id="subjectSelect" onchange="fillChapters()"></select>
<label for="chapterSelect">अध्याय चुनें:</label>
<select id="chapterSelect" onchange="showQuestions()"></select>
<br>
<input id="searchBox" type="search" placeholder="प्रश्न खोजें..." oninput="showQuestions()">
<p id="chapterInfo" class="count"></p>
<div id="questionArea"></div>
</section>

<section id="about" class="panel hidden">
<h1>About EDUSUTRA</h1>
<p>विद्यार्थियों के लिए chapter-wise अभ्यास सामग्री।</p>
<h3>Founder: Suraj Yadav</h3>
</section>
</main>
<footer>EDUSUTRA · Learn • Practice • Achieve</footer>

<script>
const DATA = __DATA__;
const subjects = Object.keys(DATA);

function page(id){
    document.querySelectorAll("main section").forEach(s=>s.classList.add("hidden"));
    document.getElementById(id).classList.remove("hidden");
}

function init(){
    document.getElementById("subjects").innerHTML = subjects.map(s =>
        `<button class="subject" onclick="openSubject('${s}')">${s}</button>`
    ).join("");

    document.getElementById("subjectSelect").innerHTML = subjects.map(s =>
        `<option value="${s}">${s}</option>`
    ).join("");

    fillChapters();
}

function openSubject(s){
    document.getElementById("subjectSelect").value = s;
    fillChapters();
    page("questions");
}

function fillChapters(){
    const s = document.getElementById("subjectSelect").value;
    const chapters = DATA[s] || [];

    document.getElementById("chapterSelect").innerHTML = chapters.map((c,i) =>
        `<option value="${i}">${i+1}. ${c[0]}</option>`
    ).join("");

    showQuestions();
}

function showQuestions(){
    const s = document.getElementById("subjectSelect").value;
    const i = Number(document.getElementById("chapterSelect").value || 0);
    const chapter = (DATA[s] || [])[i];
    const area = document.getElementById("questionArea");

    if(!chapter){
        area.innerHTML = "<p>इस विषय के लिए सामग्री उपलब्ध नहीं है।</p>";
        return;
    }

    const term = (document.getElementById("searchBox").value || "").toLowerCase();
    const items = chapter[1].filter(q =>
        (q[0] + " " + q[1]).toLowerCase().includes(term)
    );

    document.getElementById("chapterInfo").textContent =
        chapter[0] + " · " + items.length + " प्रश्न";

    area.innerHTML = items.length ? items.map((q,j) =>
        `<article class="qa">
            <h3>प्रश्न ${j+1}. ${q[0]}</h3>
            <div class="answer"><b>उत्तर:</b> ${q[1]}</div>
        </article>`
    ).join("") : "<p>इस खोज से संबंधित प्रश्न नहीं मिला।</p>";
}

init();
</script>
</body>
</html>
"""

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path

        if path in ("/", "/index.html"):
            page = HTML.replace("__DATA__", json.dumps(DATA, ensure_ascii=False))
            body = page.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        elif path == "/founder.jpg":
            image_path = Path(__file__).with_name("founder.jpg")

            if not image_path.exists():
                self.send_error(404, "Founder photo not found")
                return

            body = image_path.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "image/jpeg")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        else:
            self.send_error(404)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    print("EDUSUTRA chal raha hai: http://localhost:8000")
    print("Band karne ke liye Ctrl + C dabayein.")
   import os

HTTPServer(("0.0.0.0", int(os.environ.get("PORT", 10000))), Handler).serve_forever()
