from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse
import json

DATA = {
    "गणित": [
        ("वास्तविक संख्याएँ", [
            ("यूक्लिड विभाजन प्रमेय लिखिए।", "a = bq + r, जहाँ 0 ≤ r < b होता है।"),
            ("अपरिमेय संख्या किसे कहते हैं?", "जिस संख्या को p/q के रूप में नहीं लिख सकते, वह अपरिमेय संख्या है।")
        ]),
        ("बहुपद", [
            ("बहुपद के शून्यक किसे कहते हैं?", "p(x) = 0 को संतुष्ट करने वाला x का मान शून्यक कहलाता है।"),
            ("द्विघात बहुपद के शून्यकों का योग लिखिए।", "ax² + bx + c के शून्यकों का योग −b/a होता है।")
        ]),
        ("दो चर वाले रैखिक समीकरण", [
            ("रैखिक समीकरण का सामान्य रूप लिखिए।", "ax + by + c = 0 इसका सामान्य रूप है।"),
            ("संगत समीकरण किसे कहते हैं?", "जिस समीकरण युग्म का कम-से-कम एक हल हो, वह संगत कहलाता है।")
        ]),
        ("द्विघात समीकरण", [
            ("द्विघात समीकरण का सामान्य रूप लिखिए।", "ax² + bx + c = 0, जहाँ a ≠ 0।"),
            ("विविक्तकर का सूत्र लिखिए।", "D = b² − 4ac होता है।")
        ]),
        ("अंकगणितीय प्रगति", [
            ("अंकगणितीय प्रगति किसे कहते हैं?", "जिस श्रेणी में क्रमागत पदों का अंतर समान हो, वह AP है।"),
            ("AP के nवें पद का सूत्र लिखिए।", "aₙ = a + (n−1)d")
        ]),
        ("त्रिभुज", [
            ("समरूप त्रिभुज किसे कहते हैं?", "जिनके संगत कोण बराबर और संगत भुजाएँ समान अनुपात में हों।"),
            ("पाइथागोरस प्रमेय लिखिए।", "कर्ण² = आधार² + लंब²")
        ]),
        ("निर्देशांक ज्यामिति", [
            ("दूरी का सूत्र लिखिए।", "√[(x₂−x₁)² + (y₂−y₁)²]"),
            ("मध्य-बिंदु का सूत्र लिखिए।", "((x₁+x₂)/2, (y₁+y₂)/2)")
        ]),
        ("त्रिकोणमिति", [
            ("sin θ का मान लिखिए।", "sin θ = लंब/कर्ण"),
            ("tan θ का मान लिखिए।", "tan θ = लंब/आधार")
        ]),
        ("वृत्त", [
            ("स्पर्श रेखा किसे कहते हैं?", "जो रेखा वृत्त को केवल एक बिंदु पर छूती है।"),
            ("त्रिज्या और स्पर्श रेखा में क्या संबंध है?", "स्पर्श बिंदु पर त्रिज्या स्पर्श रेखा पर लंब होती है।")
        ]),
        ("वृत्त से संबंधित क्षेत्र", [
            ("वृत्त की परिधि का सूत्र लिखिए।", "2πr"),
            ("वृत्त के क्षेत्रफल का सूत्र लिखिए।", "πr²")
        ]),
        ("पृष्ठीय क्षेत्रफल और आयतन", [
            ("बेलन के आयतन का सूत्र लिखिए।", "πr²h"),
            ("गोले के आयतन का सूत्र लिखिए।", "(4/3)πr³")
        ]),
        ("सांख्यिकी", [
            ("माध्य किसे कहते हैं?", "प्रेक्षणों के योग को कुल प्रेक्षणों की संख्या से भाग देने पर माध्य मिलता है।"),
            ("बहुलक किसे कहते हैं?", "सबसे अधिक बार आने वाला मान बहुलक कहलाता है।")
        ]),
        ("प्रायिकता", [
            ("प्रायिकता का मान किस सीमा में होता है?", "0 से 1 के बीच।"),
            ("निश्चित घटना की प्रायिकता कितनी होती है?", "1")
        ])
    ],

    "विज्ञान": [
        ("रासायनिक अभिक्रियाएँ एवं समीकरण", [
            ("रासायनिक अभिक्रिया किसे कहते हैं?", "जिस प्रक्रिया में नए पदार्थ बनते हैं, वह रासायनिक अभिक्रिया है।"),
            ("संतुलित समीकरण क्यों आवश्यक है?", "द्रव्यमान संरक्षण के नियम का पालन करने के लिए।")
        ]),
        ("अम्ल, क्षारक एवं लवण", [
            ("अम्ल किसे कहते हैं?", "वे पदार्थ जो जलीय विलयन में H⁺ आयन देते हैं।"),
            ("pH 7 से कम होने पर विलयन कैसा होता है?", "अम्लीय।")
        ]),
        ("धातु एवं अधातु", [
            ("धातुओं के दो गुण लिखिए।", "धातुएँ सामान्यतः चमकीली और ऊष्मा तथा विद्युत की सुचालक होती हैं।"),
            ("आघातवर्धनीयता क्या है?", "धातुओं को पीटकर पतली चादर बनाने का गुण।")
        ]),
        ("कार्बन एवं उसके यौगिक", [
            ("कार्बन की संयोजकता कितनी है?", "चार।"),
            ("समजातीय श्रेणी किसे कहते हैं?", "जिसके क्रमागत सदस्यों में −CH₂− का अंतर हो।")
        ]),
        ("जैव प्रक्रम", [
            ("चार प्रमुख जीवन प्रक्रियाएँ कौन-सी हैं?", "पोषण, श्वसन, परिवहन और उत्सर्जन।"),
            ("प्रकाश संश्लेषण क्या है?", "हरे पौधों द्वारा सूर्य के प्रकाश में भोजन बनाने की प्रक्रिया।")
        ]),
        ("नियंत्रण एवं समन्वय", [
            ("न्यूरॉन क्या है?", "तंत्रिका तंत्र की संरचनात्मक और क्रियात्मक इकाई।"),
            ("एक पादप हार्मोन का नाम लिखिए।", "ऑक्सिन।")
        ]),
        ("जीव जनन कैसे करते हैं?", [
            ("अलैंगिक जनन किसे कहते हैं?", "जिसमें एक जनक भाग लेता है और युग्मकों का संलयन नहीं होता।"),
            ("परागण किसे कहते हैं?", "परागकणों का परागकोश से वर्तिकाग्र तक पहुँचना।")
        ]),
        ("आनुवंशिकता", [
            ("आनुवंशिकता किसे कहते हैं?", "माता-पिता से संतानों में लक्षणों का स्थानांतरण।"),
            ("जीन क्या है?", "DNA का वह खंड जो किसी विशेष लक्षण की सूचना रखता है।")
        ]),
        ("प्रकाश: परावर्तन तथा अपवर्तन", [
            ("परावर्तन का नियम लिखिए।", "आपतन कोण परावर्तन कोण के बराबर होता है।"),
            ("अपवर्तन किसे कहते हैं?", "एक माध्यम से दूसरे माध्यम में जाने पर प्रकाश की दिशा बदलना।")
        ]),
        ("मानव नेत्र तथा रंगबिरंगा संसार", [
            ("रेटिना का क्या कार्य है?", "रेटिना पर वस्तु का प्रतिबिंब बनता है।"),
            ("निकट-दृष्टि दोष किस लेंस से ठीक होता है?", "अवतल लेंस से।")
        ]),
        ("विद्युत", [
            ("ओम का नियम लिखिए।", "V = IR"),
            ("विद्युत शक्ति का सूत्र लिखिए।", "P = VI")
        ]),
        ("विद्युत धारा के चुंबकीय प्रभाव", [
            ("चुंबकीय क्षेत्र रेखाएँ क्या दर्शाती हैं?", "चुंबकीय क्षेत्र की दिशा और सापेक्ष तीव्रता।"),
            ("विद्युत मोटर किस ऊर्जा को किसमें बदलती है?", "विद्युत ऊर्जा को यांत्रिक ऊर्जा में।")
        ]),
        ("हमारा पर्यावरण", [
            ("जैव निम्नीकरणीय पदार्थ किसे कहते हैं?", "जिन्हें सूक्ष्मजीव सरल पदार्थों में तोड़ सकते हैं।"),
            ("खाद्य श्रृंखला क्या है?", "जीवों के बीच भोजन और ऊर्जा के स्थानांतरण का क्रम।")
        ])
    ],

    "सामाजिक विज्ञान": [
        ("यूरोप में राष्ट्रवाद का उदय", [
            ("राष्ट्रवाद क्या है?", "एक राष्ट्र से जुड़ाव और साझा पहचान की भावना।"),
            ("फ्रांसीसी क्रांति का राष्ट्रवाद पर क्या प्रभाव पड़ा?", "इसने राष्ट्रीयता और नागरिकता के विचारों को बढ़ावा दिया।")
        ]),
        ("भारत में राष्ट्रवाद", [
            ("असहयोग आंदोलन क्यों शुरू हुआ?", "ब्रिटिश शासन की दमनकारी नीतियों के विरोध में।"),
            ("दांडी यात्रा किस आंदोलन से संबंधित थी?", "सविनय अवज्ञा आंदोलन से।")
        ]),
        ("भूमंडलीकृत विश्व का बनना", [
            ("रेशम मार्ग का क्या महत्व था?", "यह व्यापार और सांस्कृतिक आदान-प्रदान का माध्यम था।"),
            ("वैश्वीकरण का अर्थ क्या है?", "देशों की अर्थव्यवस्थाओं का आपस में जुड़ना।")
        ]),
        ("संसाधन एवं विकास", [
            ("संसाधन किसे कहते हैं?", "उपयोगी वस्तु जो मानवीय आवश्यकताओं को पूरा करे।"),
            ("संसाधन संरक्षण क्यों आवश्यक है?", "भविष्य की पीढ़ियों के लिए संसाधन बचाने हेतु।")
        ]),
        ("वन एवं वन्यजीव संसाधन", [
            ("जैव विविधता क्या है?", "पौधों और जीवों की विभिन्न प्रजातियों की विविधता।"),
            ("वन संरक्षण क्यों आवश्यक है?", "पर्यावरण संतुलन और जैव विविधता बनाए रखने के लिए।")
        ]),
        ("जल संसाधन", [
            ("वर्षा जल संचयन क्या है?", "वर्षा के पानी को एकत्र करके सुरक्षित रखना।"),
            ("बहुउद्देशीय नदी परियोजना का एक लाभ लिखिए।", "सिंचाई और बिजली उत्पादन।")
        ]),
        ("कृषि", [
            ("रबी फसलें कब बोई जाती हैं?", "सर्दियों में।"),
            ("खरीफ फसल का एक उदाहरण दीजिए।", "धान।")
        ]),
        ("सत्ता की साझेदारी", [
            ("सत्ता की साझेदारी क्यों आवश्यक है?", "संघर्ष कम करने और लोकतंत्र को मजबूत बनाने के लिए।"),
            ("सत्ता की साझेदारी का एक रूप लिखिए।", "सरकार के विभिन्न अंगों के बीच सत्ता का बँटवारा।")
        ]),
        ("संघवाद", [
            ("संघीय शासन व्यवस्था क्या है?", "जिसमें सत्ता केंद्र और राज्य सरकारों के बीच बाँटी जाती है।"),
            ("भारत में सरकार के कितने स्तर हैं?", "मुख्यतः केंद्र, राज्य और स्थानीय स्तर।")
        ]),
        ("लोकतंत्र और विविधता", [
            ("सामाजिक विभाजन के आधार क्या हैं?", "भाषा, धर्म, जाति और क्षेत्र।"),
            ("सामाजिक विविधता का अर्थ क्या है?", "समाज में अलग-अलग भाषा, संस्कृति और समुदायों का होना।")
        ]),
        ("लोकतंत्र के परिणाम", [
            ("लोकतंत्र का एक प्रमुख गुण लिखिए।", "यह नागरिकों को सरकार चुनने का अधिकार देता है।"),
            ("जवाबदेह सरकार का क्या अर्थ है?", "जो जनता के प्रति उत्तरदायी हो।")
        ]),
        ("अर्थव्यवस्था और आजीविका", [
            ("प्राथमिक क्षेत्र क्या है?", "जिसमें प्राकृतिक संसाधनों से सीधे उत्पादन होता है।"),
            ("तृतीयक क्षेत्र का एक उदाहरण दीजिए।", "बैंकिंग सेवा।")
        ])
    ],

    "अंग्रेज़ी": [
        ("A Letter to God", [
            ("Why did Lencho write a letter to God?", "He asked God for money after his crop was destroyed by hail."),
            ("What destroyed Lencho's crop?", "A hailstorm destroyed his crop.")
        ]),
        ("Nelson Mandela: Long Walk to Freedom", [
            ("What does courage mean to Mandela?", "Courage is the triumph over fear."),
            ("When did Mandela become President?", "He became President of South Africa in 1994.")
        ]),
        ("Two Stories about Flying", [
            ("Why was the young seagull afraid to fly?", "He feared that his wings would not support him."),
            ("Who helped the young seagull to fly?", "His mother encouraged him.")
        ]),
        ("From the Diary of Anne Frank", [
            ("Why did Anne write a diary?", "She wanted a true friend to share her thoughts with."),
            ("What name did Anne give her diary?", "She named it Kitty.")
        ]),
        ("The Hundred Dresses", [
            ("Who was Wanda Petronski?", "A Polish girl who studied with Peggy and Maddie."),
            ("Why did Wanda's classmates feel sorry?", "They realised that their teasing had hurt Wanda.")
        ]),
        ("A Triumph of Surgery", [
            ("Why was Tricki ill?", "He was overfed and did not get enough exercise."),
            ("Who was Tricki's doctor?", "Dr Herriot.")
        ]),
        ("The Thief's Story", [
            ("Who was Hari Singh?", "A young thief."),
            ("Why did Hari return to Anil?", "Anil's kindness and trust made him want to change.")
        ]),
        ("The Necklace", [
            ("Why was Matilda unhappy?", "She desired a life of luxury."),
            ("What did Matilda borrow?", "A necklace from her friend.")
        ]),
        ("Bholi", [
            ("How did education change Bholi?", "It gave her confidence and self-respect."),
            ("Why did Bholi refuse to marry Bishamber?", "She refused to accept a marriage based on dowry.")
        ])
    ],

    "हिंदी A": [
        ("गद्य खंड", [
            ("गद्य पाठ का केंद्रीय विचार कैसे लिखें?", "पाठ की मुख्य घटना, लेखक का उद्देश्य और सीख संक्षेप में लिखें।"),
            ("लेखक का उद्देश्य क्या होता है?", "लेखक जिस विचार या संदेश को पाठ के माध्यम से व्यक्त करना चाहता है।")
        ]),
        ("पद्य खंड", [
            ("कविता का केंद्रीय भाव क्या होता है?", "कविता में व्यक्त मुख्य विचार या संदेश।"),
            ("कविता में रस का क्या महत्व है?", "रस कविता को भावपूर्ण और प्रभावशाली बनाता है।")
        ]),
        ("व्याकरण", [
            ("समास किसे कहते हैं?", "दो या अधिक शब्दों के मेल से बना संक्षिप्त शब्द समास कहलाता है।"),
            ("उपसर्ग किसे कहते हैं?", "शब्द के पहले जुड़कर अर्थ बदलने वाला शब्दांश उपसर्ग कहलाता है।")
        ]),
        ("लेखन कौशल", [
            ("औपचारिक पत्र के मुख्य भाग लिखिए।", "पता, दिनांक, संबोधन, विषय, मुख्य भाग और समापन।"),
            ("अनुच्छेद लेखन में किन बातों का ध्यान रखना चाहिए?", "विषय की एकता, सरल भाषा और विचारों का क्रम।")
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
.tag{color:#dce8ff}
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
<img src="/founder.jpg" alt="Founder photo"
onerror="this.style.display='none'"
style="width:130px;height:130px;border-radius:50%;object-fit:cover;border:4px solid #28558e">
<h1 style="color:#244f89">EDUSUTRA</h1>
<h3>ज्ञान से सफलता की ओर।</h3>
<p>Learn • Practice • Achieve</p>
<h2>Class 10 Learning Hub</h2>
<p>अपना विषय चुनें और अध्याय के प्रश्न-उत्तर पढ़ें।</p>
<div class="grid" id="subjects"></div>
</section>

<section id="questions" class="panel hidden">
<h1>Chapter-wise Short Questions</h1>
<label>विषय चुनें:</label>
<select id="subjectSelect" onchange="fillChapters()"></select>
<label>अध्याय चुनें:</label>
<select id="chapterSelect" onchange="showQuestions()"></select>
<br>
<input id="searchBox" type="search" placeholder="प्रश्न खोजें..." oninput="showQuestions()">
<p id="chapterInfo" class="count"></p>
<div id="chapterNotes" class="panel"></div>
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
        `<button class="subject" onclick="openSubject(${JSON.stringify(s)})">${s}</button>`
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

    document.getElementById("chapterNotes").innerHTML =
        `<h2>Chapter Quick Notes</h2>` +
        chapter[1].map((q,j) =>
            `<div class="note"><b>मुख्य बिंदु ${j+1}:</b> ${q[1]}</div>`
        ).join("");

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
            page = HTML.replace(
                "__DATA__",
                json.dumps(DATA, ensure_ascii=False)
            )
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
    HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
