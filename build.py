#!/usr/bin/env python3
"""Static site generator for luzyak.github.io/last-orbit.

Every page exists in English (root) and Turkish (/tr/). Content lives in this file so a
single run rebuilds the whole site; nothing is hand-edited in the output folders.
Run: python3 build.py
"""
import json, os, shutil, datetime, html

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = "https://luzyak.github.io/last-orbit"
APPSTORE = "https://apps.apple.com/app/last-orbit-space-defense/id6830081160"
PLAY_PKG = "com.yigitbayram.lastorbit.game"
SUPPORT = "https://luzyak.github.io/lastorbit-support/"
PRIVACY = SUPPORT + "privacy.html"
TERMS = SUPPORT + "terms.html"
CONTACT = "bayramelmaios@gmail.com"
TODAY = datetime.date.today().isoformat()
VERSION = "1.0.2"

# ----------------------------------------------------------------------------------------------
# Game data (mirrors the game's code and data files)
# ----------------------------------------------------------------------------------------------
FACTIONS = [
    # id, waves, EN name, TR name, EN sub, TR sub, leader EN, leader TR, admiral EN, admiral TR, flagship EN, flagship TR
    dict(id="veyra", waves=(1, 20), en="Veyra", tr="Veyra", sub_en="The Glass Choir", sub_tr="Cam Korosu",
         leader_en="Vael, Choir Regent", leader_tr="Vael, Koro Naibi", boss_en="Choir Crown", boss_tr="Koro Tacı",
         flag_en="Crown", flag_tr="Taç",
         strength_en="Strong shields", strength_tr="Güçlü kalkanlar",
         weak_en="Thin hulls", weak_tr="İnce gövdeler",
         tactic_en="Kill their shields with EMP; then mines tear the thin hulls.",
         tactic_tr="Kalkanları EMP ile söndürün, sonra mayınlar gövdeyi kolayca deler.",
         lore_en="The Veyra sing their shields into being. Their ships are vessels of layered glass and light, "
                 "and the Choir that steers them is the first civilisation to reach the last orbit. They are the "
                 "tutorial enemy: their fleets teach the mine lesson, the first admiral and the first meteor belt.",
         lore_tr="Veyra kalkanlarını şarkıyla örer. Gemileri katmanlı cam ve ışıktan; onları yöneten Koro, son "
                 "yörüngeye ulaşan ilk uygarlıktır. İlk düşman onlardır: filoları mayın dersini, ilk amirali ve ilk "
                 "meteor kuşağını öğretir.",
         ships_en="Bastion, Prism, Weaver, Needle, Lens", ships_tr="Hisar, Prizma, Dokuyucu, İğne, Mercek"),
    dict(id="nul", waves=(21, 40), en="Nul", tr="Nul", sub_en="The Zero Consensus", sub_tr="Sıfır Mutabakatı",
         leader_en="AX-01, Decision Core", leader_tr="AX-01, Karar Çekirdeği", boss_en="Prime Axiom", boss_tr="Ana Aksiyom",
         flag_en="Axiom", flag_tr="Aksiyom",
         strength_en="Long-range weapons (+20% range)", strength_tr="Uzun menzilli silahlar (+%20 menzil)",
         weak_en="No edge up close", weak_tr="Yakın dövüşte üstünlükleri kalmaz",
         tactic_en="Draw them in close: mine the way in, do not duel them at range.",
         tactic_tr="Onları yakına çekin: giriş yoluna mayın dizin, uzaktan düello etmeyin.",
         lore_en="The Nul are a machine consensus: no crews, only nodes that vote on every shot. Their weapons "
                 "outrange yours, so every fight against them is a fight about distance. The first black-hole "
                 "anomaly opens during their block, on wave 22.",
         lore_tr="Nul bir makine mutabakatıdır: mürettebat yok, her atışa oy veren düğümler var. Silahları "
                 "sizinkinden uzağa ulaşır; onlarla her çarpışma mesafe üzerine kuruludur. İlk kara delik anomalisi "
                 "onların bloğunda, 22. dalgada açılır.",
         ships_en="Wall, Ring, Patch-0, Vector, Zero", ships_tr="Duvar, Halka, Yama-0, Vektör, Sıfır"),
    dict(id="nivara", waves=(41, 60), en="Nivara", tr="Nivara", sub_en="The Phase Walkers", sub_tr="Faz Gezginleri",
         leader_en="Ilara, Threshold Regent", leader_tr="Ilara, Eşik Naibi", boss_en="Parallax", boss_tr="Paralaks",
         flag_en="Threshold", flag_tr="Eşik",
         strength_en="Very fast (+30%) with strong shields", strength_tr="Çok hızlı (+%30) ve güçlü kalkanlar",
         weak_en="Thin hulls", weak_tr="İnce gövdeler",
         tactic_en="They come fast: lay your mines further out, right on their path.",
         tactic_tr="Hızla gelirler: mayınları daha ileriye, yollarının üstüne dizin.",
         lore_en="The Nivara slip between phases of space and arrive before you expect them. Their shields are "
                 "strong and their hulls thin, like the Veyra, but at their speed a late mine is a wasted mine. "
                 "The space-time rift first tears open by itself during their block, on wave 54.",
         lore_tr="Nivara uzayın fazları arasından kayar, beklediğinizden önce varır. Kalkanları güçlü, gövdeleri "
                 "ince; Veyra gibi. Ama bu hızda geç kalan mayın boşa gider. Uzay-zaman yarığı ilk kez onların "
                 "bloğunda, 54. dalgada kendiliğinden açılır.",
         ships_en="Crescent, Halo, Loop, Focus, Orbit", ships_tr="Yarımay, Hale, İlmek, Odak, Yörünge"),
    dict(id="thalor", waves=(61, 80), en="Thalor", tr="Thalor", sub_en="The Deep Current", sub_tr="Derin Akıntı",
         leader_en="Oruun, Current Guide", leader_tr="Oruun, Akıntı Rehberi", boss_en="Leviathan", boss_tr="Leviathan",
         flag_en="Mother Current", flag_tr="Ana Akıntı",
         strength_en="Very thick hulls", strength_tr="Çok kalın gövdeler",
         weak_en="Weak shields", weak_tr="Zayıf kalkanlar",
         tactic_en="No need for EMP; use shrapnel and contact mines that wear the hull.",
         tactic_tr="EMP'ye gerek yok; gövdeyi eriten şarapnel ve temas mayınları kullanın.",
         lore_en="The Thalor rise from an ocean world; their ships are grown, not built, and their hulls are the "
                 "thickest you have met so far. Shields barely matter to them. From wave 61 the admirals of beaten "
                 "civilisations begin to fight alongside the current ruler, so the fleets grow mixed.",
         lore_tr="Thalor bir okyanus dünyasından yükselir; gemileri inşa edilmez, yetiştirilir ve gövdeleri o ana "
                 "dek gördüğünüz en kalın gövdelerdir. Kalkan onlar için önemsizdir. 61. dalgadan itibaren yenilen "
                 "uygarlıkların amiralleri mevcut hükümdarın yanında savaşmaya başlar; filolar karışır.",
         ships_en="Reef, Mantle, Coral, Harpoon, Maelstrom", ships_tr="Resif, Manto, Mercan, Zıpkın, Girdap"),
    dict(id="khar", waves=(81, 100), en="Khar", tr="Khar", sub_en="The Iron Brood", sub_tr="Demir Kuluçka",
         leader_en="Ghor, Brood Chief", leader_tr="Ghor, Kuluçka Reisi", boss_en="Brood World", boss_tr="Kuluçka Dünyası",
         flag_en="Broodmother", flag_tr="Anaç",
         strength_en="Rapid fire (+20% fire rate)", strength_tr="Seri ateş (+%20 atış hızı)",
         weak_en="Almost no shields", weak_tr="Kalkanları neredeyse yok",
         tactic_en="Do not stand in the open; meet them with mines and meteor cover.",
         tactic_tr="Ateş hattına açıkta girmeyin; mayınlar ve meteor siperleriyle karşılayın.",
         lore_en="The Khar are a brood, not a nation: iron shells bred for war and thrown at the enemy in numbers. "
                 "They carry almost no shields and make up for it with rate of fire. Standing in their line of fire "
                 "is the mistake that ends most runs in this block.",
         lore_tr="Khar bir ulus değil, bir kuluçkadır: savaş için üretilmiş demir kabuklar, düşmanın üstüne "
                 "kalabalıkla atılır. Kalkanları yok denecek kadar azdır, açığı atış hızıyla kapatırlar. Bu blokta "
                 "çoğu oyunu bitiren hata, ateş hattında açıkta durmaktır.",
         ships_en="Carapace, Furnace, Stitcher, Fang, Maw", ships_tr="Kabuk, Fırın, Dikişçi, Diş, Ağız"),
    dict(id="auralis", waves=(101, 120), en="Auralis", tr="Auralis", sub_en="The Sun Dynasty", sub_tr="Güneş Hanedanı",
         leader_en="Auren, Sun Regent", leader_tr="Auren, Güneş Naibi", boss_en="Heliarch", boss_tr="Heliarch",
         flag_en="Sun Throne", flag_tr="Sol Tahtı",
         strength_en="The hardest-hitting beams (+20% damage)", strength_tr="En sert vuran ışınlar (+%20 hasar)",
         weak_en="Their hulls give way quickly", weak_tr="Gövdeleri çabuk çöker",
         tactic_en="Bring down their gunners first; put armour in front to draw the fire.",
         tactic_tr="Önce topçularını düşürün; zırhlı gemileri öne koyup ateşi onlara çekin.",
         lore_en="The Auralis are a court of the sun: golden hulls, beam weapons that hit harder than anything "
                 "before them, and a dynasty that has never lost a war. Their block begins past wave 100, where the "
                 "fleet ceiling rises to 24 ships and every tenth wave brings more admirals.",
         lore_tr="Auralis güneşin sarayıdır: altın gövdeler, o ana dek görülmemiş sertlikte vuran ışın silahları ve "
                 "hiç savaş kaybetmemiş bir hanedan. Blokları 100. dalganın ötesinde başlar; filo tavanı 24 gemiye "
                 "çıkar ve her onuncu dalga daha çok amiral getirir.",
         ships_en="Keep, Dawn, Vesta, Sunspear, Eclipse", ships_tr="Kale, Şafak, Vesta, Gün Mızrağı, Tutulma"),
    dict(id="korvath", waves=(121, 140), en="Korvath", tr="Korvath", sub_en="The Basalt Union", sub_tr="Bazalt Birliği",
         leader_en="Durgan, Hearth Lord", leader_tr="Durgan, Ocak Efendisi", boss_en="Core Keep", boss_tr="Çekirdek Kalesi",
         flag_en="Hearth", flag_tr="Ocak",
         strength_en="Massive hulls, the toughest of all", strength_tr="Devasa gövdeler, en dayanıklı ırk",
         weak_en="Very slow (−30%), weak shields", weak_tr="Çok yavaş (−%30), zayıf kalkanlar",
         tactic_en="Use their slowness: strike from afar with Lances, lengthen their way with meteors.",
         tactic_tr="Yavaşlıklarından yararlanın: Kargı ile uzaktan vurun, yollarını meteorla uzatın.",
         lore_en="The Korvath forge their ships from the crust of a dead world. They are the slowest and the "
                 "toughest civilisation in the game, and the last of the seven. Beat their block and the war changes "
                 "hands: the Heirs arrive on wave 141.",
         lore_tr="Korvath gemilerini ölü bir dünyanın kabuğundan döver. Oyundaki en yavaş ve en dayanıklı "
                 "uygarlıktır, yedinin sonuncusudur. Bloklarını geçince savaş el değiştirir: 141. dalgada Vârisler gelir.",
         ships_en="Basalt, Ember Veil, Cast, Cinder, Collapse", ships_tr="Bazalt, Kor Perdesi, Döküm, Köz, Çöküş"),
    dict(id="heirs", waves=(141, None), en="The Heirs", tr="Vârisler", sub_en="From beyond time", sub_tr="Zamanın ötesinden",
         leader_en="Unknown", leader_tr="Bilinmiyor", boss_en="Captured admirals of every civilisation",
         boss_tr="Her uygarlığın esir alınmış amiralleri", flag_en="None of their own", flag_tr="Kendilerine ait yok",
         strength_en="Every civilisation's strength at once, larger fleets, admirals",
         strength_tr="Her ırkın gücü bir arada, kalabalık filolar ve amiraller",
         weak_en="No one aboard; steered thralls", weak_tr="Gemilerde kimse yok; yönetilen esirler",
         tactic_en="Every civilisation's tactic still holds: read each ship, focus the admirals.",
         tactic_tr="Her ırkın taktiği hâlâ geçerli: önce gelen gemiye bakın, amirallere odaklanın.",
         lore_en="The Heirs are not of our time. They are humans from a far future who have conquered every "
                 "civilisation, the Nul included, and now steer their empty ships against you. Their crimson glow "
                 "is on every hull. From wave 141 the fleet ceiling rises to 26 and the admiral count keeps growing.",
         lore_tr="Vârisler bizim zamanımızdan değil. Çok uzak bir gelecekten gelen, Nul dahil her uygarlığı "
                 "fethetmiş insanlar; şimdi o boş gemileri size karşı yönetiyorlar. Kızıl ışıkları her gövdede. "
                 "141. dalgadan itibaren filo tavanı 26 olur ve amiral sayısı artmaya devam eder.",
         ships_en="Every ship of the seven civilisations, as thralls", ships_tr="Yedi uygarlığın bütün gemileri, esir olarak"),
]

SHIPS = [
    dict(id="human_flagship", en="Command Ship", tr="Komutan Gemisi", wave=1, role_en="Flagship", role_tr="Amiral gemisi",
         pilot_en="You, the Commander", pilot_tr="Sen, Komutan",
         en_desc="Your only ship at the start and the one you must keep alive. Lose it and the run ends.",
         tr_desc="Başlangıçtaki tek gemin ve hayatta tutman gereken gemi. Düşerse oyun biter."),
    dict(id="human_fighter", en="Hunter", tr="Avcı", wave=6, role_en="Fighter", role_tr="Avcı",
         pilot_en="Captain Ece Yalın", pilot_tr="Yüzbaşı Ece Yalın",
         en_desc="Fast escort that chases targets down. Your first recruit; best used to charge what the mines have already weakened.",
         tr_desc="Hedefi kovalayan hızlı eskort. İlk gemin; mayınların yıprattığı hedefe hücumda en iyisi."),
    dict(id="human_bulwark", en="Bulwark", tr="Siper", wave=16, role_en="Armour", role_tr="Zırh",
         pilot_en="Bora Demir", pilot_tr="Bora Demir",
         en_desc="Thick hull built to stand in front and draw fire away from the Command Ship.",
         tr_desc="Öne durup ateşi Komutan Gemisi'nden uzağa çekmek için yapılmış kalın gövde."),
    dict(id="human_shield", en="Halo", tr="Hale", wave=28, role_en="Shield projector", role_tr="Kalkan yansıtıcı",
         pilot_en="İdil Aras", pilot_tr="İdil Aras",
         en_desc="Projects a shield over nearby ships. Pairs with the Bulwark to hold a line under heavy beams.",
         tr_desc="Yakındaki gemilerin üstüne kalkan yansıtır. Ağır ışın ateşi altında hattı tutmak için Siper ile eşleşir."),
    dict(id="human_artillery", en="Lance", tr="Kargı", wave=38, role_en="Artillery", role_tr="Topçu",
         pilot_en="Mira Sarp", pilot_tr="Mira Sarp",
         en_desc="Long-range, high-damage, fragile. The answer to slow heavy hulls like the Korvath.",
         tr_desc="Uzun menzil, yüksek hasar, kırılgan. Korvath gibi yavaş ağır gövdelerin cevabı."),
    dict(id="human_repair", en="Patch", tr="Yama", wave=58, role_en="Repair", role_tr="Onarım",
         pilot_en="Dr. Deniz Eren", pilot_tr="Dr. Deniz Eren",
         en_desc="Repairs hulls mid-fight. Keeps a damaged front line alive through long mixed-fleet waves.",
         tr_desc="Çarpışma sırasında gövde onarır. Uzun karışık filo dalgalarında yıpranan ön hattı ayakta tutar."),
    dict(id="human_gravity", en="Well", tr="Kuyu", wave=64, role_en="Gravity", role_tr="Kütle",
         pilot_en="Prof. Ozan Kutlu", pilot_tr="Prof. Ozan Kutlu",
         en_desc="Bends enemy paths with a gravity field. Pulls fleets onto your mines or away from your ships.",
         tr_desc="Kütle alanıyla düşman rotasını büker. Filoları mayınlarının üstüne çeker ya da gemilerinden uzaklaştırır."),
]

MINES = [
    dict(id="mine_contact", en="Contact", tr="Temas", wave=1, cost=25,
         en_desc="The basic mine. Invisible to the enemy and to their radar; detonates on touch for heavy hull damage.",
         tr_desc="Temel mayın. Düşmana ve radarına görünmez; temasta patlar, gövdeye ağır hasar verir."),
    dict(id="mine_meteor", en="Meteor", tr="Meteor", wave=4, cost=40,
         en_desc="Not a bomb but a rock: blocks the enemy's path and their line of fire. Your only cover from meteor belts.",
         tr_desc="Bomba değil kaya: düşmanın yolunu ve ateş hattını keser. Meteor kuşaklarına karşı tek siperin."),
    dict(id="mine_emp", en="EMP", tr="EMP", wave=19, cost=40,
         en_desc="Burns shields off every ship in range. Turns shield-heavy fleets (Veyra, Nivara) into thin hulls.",
         tr_desc="Menzildeki her geminin kalkanını söndürür. Kalkanı güçlü filoları (Veyra, Nivara) ince gövdeye çevirir."),
    dict(id="mine_shrapnel", en="Shrapnel", tr="Şarapnel", wave=34, cost=70,
         en_desc="Area damage that wears hulls across a formation. The tool for thick-hulled, weak-shield fleets.",
         tr_desc="Formasyon boyunca gövdeleri yıpratan alan hasarı. Kalın gövdeli, zayıf kalkanlı filoların aracı."),
    dict(id="mine_gravity", en="Mass", tr="Kütle", wave=44, cost=95,
         en_desc="Pulls the pack in, then implodes. Groups a spread formation onto one point for your other mines.",
         tr_desc="Sürüyü içine çeker, sonra çöker. Dağınık formasyonu diğer mayınların için tek noktaya toplar."),
]

POWERS = [
    dict(en="Second Shield", tr="İkinci Kalkan", wave_en="From the start", wave_tr="Baştan itibaren",
         en_desc="Raises a second shield layer over the Command Ship for one wave.",
         tr_desc="Komutan Gemisi'nin üstünde bir dalga boyunca ikinci bir kalkan katmanı açar."),
    dict(en="Meteor Rain", tr="Meteor Yağmuru", wave_en="Wave 13", wave_tr="13. dalga",
         en_desc="Calls down the belt you first survived on wave 8, onto the enemy.",
         tr_desc="8. dalgada ilk kez atlattığın kuşağı düşmanın üstüne indirir."),
    dict(en="Black Hole", tr="Kara Delik", wave_en="Wave 24", wave_tr="24. dalga",
         en_desc="Opens the anomaly you met on wave 22, where you choose.",
         tr_desc="22. dalgada karşılaştığın anomaliyi istediğin yerde açar."),
    dict(en="Rift", tr="Yarık", wave_en="Wave 55", wave_tr="55. dalga",
         en_desc="Tears space-time open. The rarest and costliest power, first seen on wave 54.",
         tr_desc="Uzay-zamanı yırtar. En nadir ve en pahalı güç; ilk kez 54. dalgada görülür."),
]

def hazard_waves(first, every, upto=160):
    return [w for w in range(first, upto + 1, every) if (w - first) % every == 0]

CHANGELOG = [
    dict(ver="1.0.2", date="2026-11-11", status_en="In testing", status_tr="Testte",
         en=["New Journey screen in the hangar: the route travelled, civilisations met, weapons used, the current wave and what lies ahead, with a shortcut to the ranking.",
             "One short metallic sound for every purchase: ships, mines, cargo and store products.",
             "The wave counter at the top now shows the wave just fought while the wreckage is being collected.",
             "Share your journey from the Journey screen through the phone's own share sheet; each share pays salvage into the run, 500 for the first and less each time (400, 300, 200, 100, 50, 25, 20).",
             "After wave 15 the game asks once whether you would like to rate it. Nothing hangs on the answer."],
         tr=["Hangarda yeni Yolculuk ekranı: katedilen rota, tanışılan uygarlıklar, kullanılan silahlar, mevcut dalga ve ilerisi; sıralamaya kısayol.",
             "Her alımda tek kısa metalik ses: gemi, mayın, kargo ve mağaza ürünleri.",
             "Üstteki dalga sayacı, enkaz toplanırken az önce savaşılan dalgayı gösteriyor.",
             "Yolculuk ekranından telefonun kendi paylaşım sayfasıyla yolculuğunu paylaş; her paylaşım oyuna ganimet verir: ilki 500, sonrakiler giderek azalır (400, 300, 200, 100, 50, 25, 20).",
             "15. dalgadan sonra oyun bir kez puan vermek isteyip istemediğini sorar. Cevaba hiçbir şey bağlı değil."]),
    dict(ver="1.0.1", date="2026-11-10", status_en="Released on the App Store", status_tr="App Store'da yayında",
         en=["Store page links and metadata fixes.", "Retry when the store cannot be reached."],
         tr=["Mağaza sayfası bağlantıları ve meta veri düzeltmeleri.", "Mağazaya ulaşılamadığında yeniden deneme."]),
    dict(ver="1.0", date="2026-11-09", status_en="First release on the App Store", status_tr="App Store'da ilk sürüm",
         en=["Endless waves across seven civilisations and the Heirs.", "Five mine types, seven ship classes, four powers.",
             "World ranking by the furthest wave reached.", "Turkish and English."],
         tr=["Yedi uygarlık ve Vârisler boyunca sonsuz dalga.", "Beş mayın türü, yedi gemi sınıfı, dört güç.",
             "Ulaşılan en uzak dalgaya göre dünya sıralaması.", "Türkçe ve İngilizce."]),
]

# ----------------------------------------------------------------------------------------------
# Page frame
# ----------------------------------------------------------------------------------------------
CSS = """
:root{color-scheme:dark;--bg:#070b14;--panel:#0f1626;--line:#223049;--text:#e6eaf2;--muted:#9aa5b8;--accent:#ffb547;--cyan:#6fd3ff;--green:#7ce0a3;--red:#ff7a7a}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--text);font:17px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:var(--cyan)}img{max-width:100%;height:auto;display:block}
header.top{border-bottom:1px solid var(--line);background:rgba(7,11,20,.92);position:sticky;top:0;backdrop-filter:blur(8px);z-index:5}
.wrap{max-width:980px;margin:0 auto;padding:0 20px}
nav.main{display:flex;align-items:center;gap:18px;height:60px;flex-wrap:wrap}
nav.main .brand{display:flex;align-items:center;gap:10px;color:var(--text);text-decoration:none;font-weight:700;margin-right:auto}
nav.main .brand img{width:30px;height:30px;border-radius:7px}
nav.main a.l{color:var(--muted);text-decoration:none;font-size:15px}nav.main a.l:hover{color:var(--text)}
nav.main a.lang{border:1px solid var(--line);border-radius:6px;padding:3px 9px;font-size:13px;color:var(--muted);text-decoration:none}
main{padding:36px 0 64px}
h1{font-size:40px;line-height:1.1;margin:0 0 10px;letter-spacing:-.5px}
h2{font-size:26px;margin:44px 0 12px;color:var(--accent)}h3{font-size:19px;margin:24px 0 6px}
p{margin:0 0 12px}.muted{color:var(--muted)}.kicker{color:var(--accent);letter-spacing:3px;font-size:13px;text-transform:uppercase;margin-bottom:8px}
.lead{font-size:21px;color:#c9d2e3}
.hero{display:grid;grid-template-columns:1.2fr .8fr;gap:36px;align-items:center}
.hero .shot{border-radius:22px;border:1px solid var(--line);overflow:hidden;max-width:300px;margin:0 auto;box-shadow:0 20px 60px rgba(0,0,0,.6)}
.cta{display:flex;gap:12px;flex-wrap:wrap;margin:22px 0}
.btn{display:inline-block;padding:12px 20px;border-radius:10px;text-decoration:none;font-weight:600;border:1px solid var(--line);color:var(--text);background:var(--panel)}
.btn.primary{background:var(--accent);color:#1a1200;border-color:var(--accent)}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:18px 20px}
.card h3{margin-top:0}.card .pic{border-radius:10px;overflow:hidden;background:#000;margin-bottom:12px}
.facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;margin:20px 0}
.fact{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:14px 16px}
.fact b{display:block;font-size:22px;color:var(--accent)}.fact span{color:var(--muted);font-size:14px}
table{border-collapse:collapse;width:100%;margin:12px 0 20px;font-size:15px}
th,td{text-align:left;padding:9px 10px;border-bottom:1px solid var(--line);vertical-align:top}th{color:var(--muted);font-weight:600}
.tag{display:inline-block;background:#182238;border:1px solid var(--line);border-radius:999px;padding:2px 10px;font-size:13px;color:var(--muted);margin:2px 4px 2px 0}
.pos{color:var(--green)}.neg{color:var(--red)}
.shots{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px}
.shots img{border-radius:14px;border:1px solid var(--line)}
.crumbs{font-size:14px;color:var(--muted);margin-bottom:14px}.crumbs a{color:var(--muted)}
.faq h3{color:var(--text)}
footer{border-top:1px solid var(--line);padding:28px 0 40px;color:var(--muted);font-size:14px}
footer a{color:var(--muted)}footer .cols{display:flex;gap:28px;flex-wrap:wrap}
.timeline li{margin-bottom:8px}
@media(max-width:760px){.hero{grid-template-columns:1fr}h1{font-size:32px}nav.main{height:auto;padding:10px 0}}
"""

NAV = dict(
    en=[("Factions", "factions/"), ("Fleet", "fleet.html"), ("Mines & Powers", "mines.html"), ("Wave Guide", "waves.html"),
        ("FAQ", "faq.html"), ("Updates", "changelog.html"), ("Press", "press.html")],
    tr=[("Uygarlıklar", "factions/"), ("Filo", "fleet.html"), ("Mayınlar ve Güçler", "mines.html"), ("Dalga Rehberi", "waves.html"),
        ("SSS", "faq.html"), ("Güncellemeler", "changelog.html"), ("Basın", "press.html")],
)

PAGES = []  # (path, lang, lastmod) for sitemap


def t(lang, en, tr):
    return en if lang == "en" else tr


def page(path, lang, title, desc, body, jsonld=None, image=None, alt_path=None, kind="website"):
    """Write one page. path is relative to the language root ('' for home)."""
    prefix = "" if lang == "en" else "tr/"
    depth = path.count("/")
    rel = "../" * (depth + (1 if lang == "tr" else 0))
    if lang == "tr" and depth == 0:
        rel = "../"
    url = f"{BASE}/{prefix}{path}"
    alt = alt_path if alt_path is not None else path
    other = f"{BASE}/{alt}" if lang == "tr" else f"{BASE}/tr/{alt}"
    og = f"{BASE}/{image}" if image else f"{BASE}/assets/og.png"
    nav = "".join(f'<a class="l" href="{rel}{prefix}{href}">{html.escape(label)}</a>' for label, href in NAV[lang])
    ld = ""
    if jsonld:
        ld = "\n".join(f'<script type="application/ld+json">{json.dumps(j, ensure_ascii=False)}</script>' for j in jsonld)
    full_title = title if "Last Orbit" in title else f"{title} · Last Orbit: Space Defense"
    doc = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(full_title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="en" href="{BASE}/{alt}">
<link rel="alternate" hreflang="tr" href="{BASE}/tr/{alt}">
<link rel="alternate" hreflang="x-default" href="{BASE}/{alt}">
<link rel="icon" href="{rel}assets/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="{rel}assets/apple-touch-icon.png">
<meta property="og:type" content="{kind}">
<meta property="og:site_name" content="Last Orbit: Space Defense">
<meta property="og:title" content="{html.escape(full_title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og}">
<meta property="og:locale" content="{'en_US' if lang == 'en' else 'tr_TR'}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(full_title)}">
<meta name="twitter:description" content="{html.escape(desc)}">
<meta name="twitter:image" content="{og}">
<meta name="apple-itunes-app" content="app-id=6830081160">
<meta name="robots" content="index,follow,max-image-preview:large">
{ld}
<style>{CSS}</style>
</head>
<body>
<header class="top"><div class="wrap"><nav class="main">
<a class="brand" href="{rel}{prefix}"><img src="{rel}assets/icon-192.png" alt="" width="30" height="30">Last Orbit</a>
{nav}
<a class="lang" href="{other}" hreflang="{'en' if lang == 'tr' else 'tr'}">{'English' if lang == 'tr' else 'Türkçe'}</a>
</nav></div></header>
<main><div class="wrap">
{body}
</div></main>
<footer><div class="wrap"><div class="cols">
<span>© 2026 Yigit Bayram · Last Orbit: Space Defense</span>
<a href="{APPSTORE}">App Store</a>
<a href="{SUPPORT}">{t(lang, 'Support', 'Destek')}</a>
<a href="{PRIVACY}">{t(lang, 'Privacy', 'Gizlilik')}</a>
<a href="{TERMS}">{t(lang, 'Terms', 'Hizmet Şartları')}</a>
<a href="mailto:{CONTACT}">{CONTACT}</a>
<a href="{rel}llms.txt">llms.txt</a>
</div></div></footer>
</body>
</html>
"""
    out = os.path.join(ROOT, prefix, path)
    if path == "" or path.endswith("/"):
        out = os.path.join(out, "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(doc)
    PAGES.append((url, alt, lang))
    return rel


def stores(lang, rel):
    return f"""<div class="cta">
<a class="btn primary" href="{APPSTORE}">{t(lang, 'Download on the App Store', "App Store'dan indir")}</a>
<a class="btn" href="{rel}{'' if lang == 'en' else 'tr/'}faq.html#android">{t(lang, 'Android: closed beta', 'Android: kapalı beta')}</a>
</div>"""


GAME_LD = {
    "@context": "https://schema.org",
    "@type": ["VideoGame", "MobileApplication"],
    "name": "Last Orbit: Space Defense",
    "alternateName": "Last Orbit",
    "url": BASE + "/",
    "image": BASE + "/assets/og.png",
    "description": "Free tower-defense strategy game for iPhone and Android: lay invisible mines, command a small fleet in real time and hold the last orbit against endless waves of seven alien civilisations.",
    "applicationCategory": "GameApplication",
    "applicationSubCategory": "Strategy",
    "operatingSystem": "iOS 15.0 or later, Android",
    "genre": ["Tower defense", "Strategy", "Science fiction"],
    "gamePlatform": ["iOS", "Android"],
    "playMode": "SinglePlayer",
    "numberOfPlayers": {"@type": "QuantitativeValue", "minValue": 1, "maxValue": 1},
    "inLanguage": ["en", "tr"],
    "contentRating": "Apple 12+",
    "datePublished": "2026-11-09",
    "softwareVersion": VERSION,
    "author": {"@type": "Person", "name": "Yigit Bayram"},
    "publisher": {"@type": "Person", "name": "Yigit Bayram"},
    "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD", "availability": "https://schema.org/InStock",
               "url": APPSTORE},
    "installUrl": APPSTORE,
    "sameAs": [APPSTORE, SUPPORT],
}


def breadcrumbs(lang, items):
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}
    crumbs = " › ".join(f'<a href="{u}">{html.escape(n)}</a>' if i < len(items) - 1 else html.escape(n)
                        for i, (n, u) in enumerate(items))
    return ld, f'<div class="crumbs">{crumbs}</div>'


def shots_html(lang, rel, nums):
    return '<div class="shots">' + "".join(
        f'<img src="{rel}assets/shots/{n:02d}_{lang}.png" alt="{html.escape(SHOT_ALT[lang][n])}" width="600" height="1304" loading="lazy">'
        for n in nums) + "</div>"


SHOT_ALT = {
    "en": {1: "Last Orbit powers panel on wave 23", 2: "The space-time rift opens on wave 33", 3: "Mixed fleet combat on wave 61",
           4: "Early combat on wave 10", 5: "Wave intel screen before wave 23", 6: "A full hangar on wave 61",
           7: "Ship card in the hangar", 8: "Last Orbit title screen", 9: "The Veyra enter the war", 10: "Mine placement before wave 23"},
    "tr": {1: "23. dalgada Last Orbit güç paneli", 2: "33. dalgada uzay-zaman yarığı", 3: "61. dalgada karışık filo çatışması",
           4: "10. dalgada erken çatışma", 5: "23. dalga öncesi istihbarat ekranı", 6: "61. dalgada dolu hangar",
           7: "Hangarda gemi kartı", 8: "Last Orbit açılış ekranı", 9: "Veyra savaşa giriyor", 10: "23. dalga öncesi mayın yerleştirme"},
}


# ----------------------------------------------------------------------------------------------
# Pages
# ----------------------------------------------------------------------------------------------
def build_home(lang):
    rel = "" if lang == "en" else "../"
    rel = page_rel(lang, "")
    if lang == "en":
        h1 = "Last Orbit: Space Defense"
        lead = ("A free tower-defense strategy game for iPhone and Android. The enemy cannot see your mines. "
                "Neither can their radar. That is your only advantage.")
        pitch = ("You have one Command Ship, a field of invisible mines and an endless enemy advancing through the dark. "
                 "Every wave is a puzzle you set up before it arrives: read the formation, predict the path, lay the trap, "
                 "then command your escorts in real time while it springs.")
        why_h = "Why it plays differently"
        why = [
            ("Every wave is planned first, fought second", "You see the incoming fleet, its formation and its arrival zone before it jumps in. The mines you place in that quiet minute decide the fight."),
            ("Five mines, seven ships, four powers, one answer per enemy", "EMP strips Veyra shields; shrapnel wears Thalor hulls; meteors stall the Khar; Lances punish the slow Korvath. Each civilisation needs a different plan."),
            ("Real-time command on top of the plan", "Guard, charge or focus fire. When the plan fails, your pilots can still make the final sacrifice."),
            ("Hazards that become weapons", "Survive a meteor belt, then call one down. Meet a black hole, then open one. Watch the rift tear, then tear it yourself."),
            ("Seven civilisations, then the Heirs", "Veyra, Nul, Nivara, Thalor, Khar, Auralis and Korvath each hold twenty waves with their own ships and admirals. From wave 141 the Heirs steer them all."),
            ("A world ranking", "Every commander is placed by the furthest wave they reached. No lives to buy; only the plan counts."),
        ]
        facts = [("Free", "with optional ads and purchases"), ("Endless", "waves; the Heirs rule from 141"), ("7+1", "civilisations"),
                 ("5 / 7 / 4", "mines / ships / powers"), ("12+", "age rating"), ("TR · EN", "languages")]
        shots_h = "Screenshots"
        more_h = "Go deeper"
        more = [("Factions", "factions/", "Each civilisation's strength, weakness and the tactic that beats it."),
                ("Fleet", "fleet.html", "The seven human ship classes and when they unlock."),
                ("Mines & powers", "mines.html", "What every mine does and which fleet it is for."),
                ("Wave guide", "waves.html", "Blocks, admirals, hazards and unlock waves at a glance."),
                ("FAQ", "faq.html", "Price, platforms, offline play, purchases, ranking."),
                ("Press kit", "press.html", "Facts, descriptions, icon and screenshots.")]
    else:
        h1 = "Last Orbit: Space Defense"
        lead = ("iPhone ve Android için ücretsiz kule savunma strateji oyunu. Düşman mayınlarını göremez. "
                "Radarı da. Tek üstünlüğün bu.")
        pitch = ("Elinde tek bir Komutan Gemisi, görünmez mayınlardan bir alan ve karanlıktan durmadan gelen bir düşman var. "
                 "Her dalga, gelmeden önce kurduğun bir bulmaca: formasyonu oku, rotayı tahmin et, tuzağı kur, "
                 "sonra tuzak kapanırken eskortlarını anlık yönet.")
        why_h = "Neden farklı oynanır"
        why = [
            ("Her dalga önce planlanır, sonra savaşılır", "Gelen filoyu, formasyonunu ve varış bölgesini sıçramadan önce görürsün. O sessiz dakikada dizdiğin mayınlar çarpışmayı belirler."),
            ("Beş mayın, yedi gemi, dört güç; her düşmana ayrı cevap", "EMP Veyra kalkanını söker; şarapnel Thalor gövdesini yıpratır; meteor Khar'ı durdurur; Kargı yavaş Korvath'ı cezalandırır. Her uygarlık farklı plan ister."),
            ("Planın üstüne anlık komuta", "Koru, hücum et ya da ateşi topla. Plan çökerse pilotların son fedakârlığı yapabilir."),
            ("Silaha dönüşen tehlikeler", "Meteor kuşağından sağ çık, sonra bir tanesini düşmanın üstüne indir. Kara deliği gör, sonra bir tane aç. Yarığın yırtılmasını izle, sonra kendin yırt."),
            ("Yedi uygarlık, sonra Vârisler", "Veyra, Nul, Nivara, Thalor, Khar, Auralis ve Korvath yirmişer dalga boyunca kendi gemileri ve amiralleriyle gelir. 141. dalgadan sonra hepsini Vârisler yönetir."),
            ("Dünya sıralaması", "Her komutan ulaştığı en uzak dalgaya göre sıralanır. Satın alınacak can yok; yalnız plan sayılır."),
        ]
        facts = [("Ücretsiz", "isteğe bağlı reklam ve satın alma"), ("Sonsuz", "dalga; 141'den sonra Vârisler"), ("7+1", "uygarlık"),
                 ("5 / 7 / 4", "mayın / gemi / güç"), ("12+", "yaş derecesi"), ("TR · EN", "dil")]
        shots_h = "Ekran görüntüleri"
        more_h = "Derine in"
        more = [("Uygarlıklar", "factions/", "Her uygarlığın gücü, zayıflığı ve onu yenen taktik."),
                ("Filo", "fleet.html", "Yedi insan gemisi sınıfı ve açıldıkları dalgalar."),
                ("Mayınlar ve güçler", "mines.html", "Her mayın ne yapar, hangi filo için."),
                ("Dalga rehberi", "waves.html", "Bloklar, amiraller, tehlikeler ve açılış dalgaları tek bakışta."),
                ("SSS", "faq.html", "Fiyat, platform, çevrimdışı oynama, satın alma, sıralama."),
                ("Basın kiti", "press.html", "Bilgiler, açıklamalar, simge ve ekran görüntüleri.")]
    pre = "" if lang == "en" else "tr/"
    body = f"""
<section class="hero">
<div>
<div class="kicker">{t(lang, 'Free · iPhone · Android (beta)', 'Ücretsiz · iPhone · Android (beta)')}</div>
<h1>{h1}</h1>
<p class="lead">{lead}</p>
<p>{pitch}</p>
{stores(lang, rel)}
</div>
<div class="shot"><img src="{rel}assets/shots/10_{lang}.png" alt="{html.escape(SHOT_ALT[lang][10])}" width="600" height="1304"></div>
</section>
<div class="facts">{''.join(f'<div class="fact"><b>{html.escape(a)}</b><span>{html.escape(b)}</span></div>' for a, b in facts)}</div>
<h2>{why_h}</h2>
<div class="grid">{''.join(f'<div class="card"><h3>{html.escape(a)}</h3><p>{html.escape(b)}</p></div>' for a, b in why)}</div>
<h2>{shots_h}</h2>
{shots_html(lang, rel, [10, 4, 3, 2, 1, 6])}
<h2>{more_h}</h2>
<div class="grid">{''.join(f'<div class="card"><h3><a href="{rel}{pre}{h}">{html.escape(a)}</a></h3><p>{html.escape(b)}</p></div>' for a, h, b in more)}</div>
"""
    page("", lang, "Last Orbit: Space Defense – " + t(lang, "Free tower defense game for iPhone & Android", "iPhone ve Android için ücretsiz kule savunma oyunu"),
         t(lang, "Lay invisible mines, command your fleet in real time and hold the last orbit against endless waves of seven alien civilisations. Free on the App Store.",
           "Görünmez mayınlar diz, filonu anlık yönet ve yedi uzaylı uygarlığın bitmeyen dalgalarına karşı son yörüngeyi tut. App Store'da ücretsiz."),
         body, jsonld=[GAME_LD])


def page_rel(lang, path):
    depth = path.count("/")
    return "../" * (depth + (1 if lang == "tr" else 0))


def build_factions(lang):
    pre = "" if lang == "en" else "tr/"
    rel = page_rel(lang, "factions/")
    home = f"{BASE}/{pre}"
    ld, crumbs = breadcrumbs(lang, [("Last Orbit", home), (t(lang, "Factions", "Uygarlıklar"), f"{home}factions/")])
    cards = ""
    for f in FACTIONS:
        w = f["waves"]
        wtxt = t(lang, f"Waves {w[0]}–{w[1]}", f"{w[0]}–{w[1]}. dalgalar") if w[1] else t(lang, f"Wave {w[0]} onward", f"{w[0]}. dalgadan itibaren")
        pic = f'<div class="pic"><img src="{rel}assets/cards/{f["id"]}_boss.png" alt="{html.escape(f[lang])} {html.escape(f["boss_" + lang])}" width="480" height="313" loading="lazy"></div>' if f["id"] != "heirs" else ""
        cards += f"""<div class="card">{pic}<h3><a href="{f['id']}.html">{html.escape(f[lang])}</a> <span class="muted">· {html.escape(f['sub_' + lang])}</span></h3>
<p class="muted">{wtxt}</p>
<p><span class="pos">▲ {html.escape(f['strength_' + lang])}</span><br><span class="neg">▼ {html.escape(f['weak_' + lang])}</span></p></div>"""
    intro = t(lang,
              "Last Orbit's enemy comes in blocks of twenty waves. Each block belongs to one civilisation with its own ships, admiral and leader, and each needs a different answer from your mines and fleet. After the seventh block the Heirs take over every fleet.",
              "Last Orbit'te düşman yirmişer dalgalık bloklar halinde gelir. Her blok kendi gemileri, amirali ve lideri olan bir uygarlığındır; her biri mayınlarından ve filondan farklı bir cevap ister. Yedinci bloktan sonra bütün filoları Vârisler devralır.")
    body = f"""{crumbs}<h1>{t(lang, 'The civilisations of Last Orbit', "Last Orbit'in uygarlıkları")}</h1>
<p class="lead">{intro}</p><div class="grid">{cards}</div>"""
    page("factions/", lang, t(lang, "Factions: the seven civilisations and the Heirs", "Uygarlıklar: yedi ırk ve Vârisler"),
         t(lang, "Every enemy civilisation in Last Orbit: Veyra, Nul, Nivara, Thalor, Khar, Auralis, Korvath and the Heirs, with their waves, strengths, weaknesses and the tactic that beats each one.",
           "Last Orbit'teki her düşman uygarlık: Veyra, Nul, Nivara, Thalor, Khar, Auralis, Korvath ve Vârisler; dalgaları, güçleri, zayıflıkları ve her birini yenen taktik."),
         body, jsonld=[ld])
    for f in FACTIONS:
        build_faction(lang, f)


def build_faction(lang, f):
    pre = "" if lang == "en" else "tr/"
    rel = page_rel(lang, "factions/x")
    home = f"{BASE}/{pre}"
    name = f[lang]
    ld, crumbs = breadcrumbs(lang, [("Last Orbit", home), (t(lang, "Factions", "Uygarlıklar"), f"{home}factions/"), (name, f"{home}factions/{f['id']}.html")])
    w = f["waves"]
    wtxt = t(lang, f"Waves {w[0]}–{w[1]}", f"{w[0]}–{w[1]}. dalgalar") if w[1] else t(lang, f"Wave {w[0]} and every wave after", f"{w[0]}. dalga ve sonrası")
    heirs = f["id"] == "heirs"
    pics = ""
    if not heirs:
        pics = f"""<div class="grid">
<div class="card"><div class="pic"><img src="{rel}assets/cards/{f['id']}_boss.png" alt="{html.escape(f['boss_' + lang])}" width="480" height="313"></div><h3>{html.escape(f['boss_' + lang])}</h3><p class="muted">{t(lang, 'Admiral ship. Comes on waves', 'Amiral gemisi. Geldiği dalgalar:')} {w[0] + 9} {t(lang, 'and', 've')} {w[1]}; {t(lang, 'two on the second.', 'ikincisinde iki tane.')}</p></div>
<div class="card"><div class="pic"><img src="{rel}assets/cards/{f['id']}_flagship.png" alt="{html.escape(f['flag_' + lang])}" width="480" height="313"></div><h3>{html.escape(f['flag_' + lang])}</h3><p class="muted">{t(lang, 'Flagship. Leads the mid-block wave', 'Sancak gemisi. Blok ortası dalgasına önderlik eder:')} {w[0] + 14}.</p></div>
</div>"""
    faq = [
        (t(lang, f"When do the {name} appear in Last Orbit?", f"{name} Last Orbit'te ne zaman gelir?"),
         t(lang, f"The {name} hold {wtxt.lower()}.", f"{name} {wtxt.lower()} boyunca saldırır.") if not heirs else
         t(lang, "The Heirs take over on wave 141, after all seven civilisations have been beaten.", "Vârisler yedi uygarlık yenildikten sonra, 141. dalgada devralır.")),
        (t(lang, f"How do you beat the {name}?", f"{name} nasıl yenilir?"), f["tactic_" + lang]),
        (t(lang, f"What are the {name} weak against?", f"{name} neye karşı zayıf?"), f["weak_" + lang]),
    ]
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
    body = f"""{crumbs}
<div class="kicker">{wtxt}</div>
<h1>{html.escape(name)} <span class="muted" style="font-weight:400">· {html.escape(f['sub_' + lang])}</span></h1>
<p class="lead">{html.escape(f['lore_' + lang])}</p>
<div class="facts">
<div class="fact"><b>{html.escape(f['leader_' + lang].split(',')[0])}</b><span>{html.escape(f['leader_' + lang].split(',')[-1].strip()) if ',' in f['leader_' + lang] else t(lang, 'leader', 'lider')}</span></div>
<div class="fact"><b>{html.escape(f['boss_' + lang]) if not heirs else '—'}</b><span>{t(lang, 'admiral ship', 'amiral gemisi')}</span></div>
<div class="fact"><b>{html.escape(f['flag_' + lang]) if not heirs else '—'}</b><span>{t(lang, 'flagship', 'sancak gemisi')}</span></div>
</div>
<h2>{t(lang, 'Strength, weakness, tactic', 'Güç, zayıflık, taktik')}</h2>
<p><span class="pos">▲ {html.escape(f['strength_' + lang])}</span></p>
<p><span class="neg">▼ {html.escape(f['weak_' + lang])}</span></p>
<p><b style="color:var(--accent)">{t(lang, 'Tactic', 'Taktik')}:</b> {html.escape(f['tactic_' + lang])}</p>
<h2>{t(lang, 'Ships', 'Gemiler')}</h2>
<p>{html.escape(f['ships_' + lang])}.</p>
{pics}
<h2 class="faq">{t(lang, 'Questions', 'Sorular')}</h2>
<div class="faq">{''.join(f'<h3>{html.escape(q)}</h3><p>{html.escape(a)}</p>' for q, a in faq)}</div>
<p><a href="{rel}{pre}factions/">{t(lang, '← All civilisations', '← Bütün uygarlıklar')}</a> · <a href="{rel}{pre}waves.html">{t(lang, 'Wave guide', 'Dalga rehberi')}</a></p>
"""
    page(f"factions/{f['id']}.html", lang, f"{name} ({f['sub_' + lang]}) – " + t(lang, "how to beat them", "nasıl yenilir"),
         t(lang, f"The {name} in Last Orbit: Space Defense. {wtxt}. Strength: {f['strength_en']}. Weakness: {f['weak_en']}. Tactic: {f['tactic_en']}",
           f"Last Orbit'te {name}. {wtxt}. Güç: {f['strength_tr']}. Zayıflık: {f['weak_tr']}. Taktik: {f['tactic_tr']}"),
         body, jsonld=[ld, faq_ld], image=f"assets/cards/{f['id']}_boss.png" if not heirs else None, kind="article")


def build_fleet(lang):
    pre = "" if lang == "en" else "tr/"
    rel = page_rel(lang, "fleet.html")
    home = f"{BASE}/{pre}"
    ld, crumbs = breadcrumbs(lang, [("Last Orbit", home), (t(lang, "Fleet", "Filo"), f"{home}fleet.html")])
    cards = ""
    for s in SHIPS:
        cards += f"""<div class="card"><div class="pic"><img src="{rel}assets/cards/{s['id']}.png" alt="{html.escape(s[lang])}" width="480" height="313" loading="lazy"></div>
<h3>{html.escape(s[lang])} <span class="muted">· {html.escape(s['role_' + lang])}</span></h3>
<p class="muted">{t(lang, 'Pilot', 'Pilot')}: {html.escape(s['pilot_' + lang])} · {t(lang, 'unlocks on wave', 'açılış:')} {s['wave']}{'' if lang == 'en' else '. dalga'}</p>
<p>{html.escape(s[lang + '_desc'])}</p></div>"""
    intro = t(lang,
              "You start alone with the Command Ship and earn the rest by surviving. Ships cost salvage recovered from enemy wrecks, can be repaired and upgraded in the hangar, and answer to three orders in battle: guard, charge, focus fire.",
              "Yalnız Komutan Gemisi ile başlarsın, gerisini hayatta kalarak kazanırsın. Gemiler düşman enkazından toplanan malzemeyle alınır, hangarda onarılıp yükseltilir ve savaşta üç emre uyar: koru, hücum et, ateşi topla.")
    body = f"""{crumbs}<h1>{t(lang, 'The fleet', 'Filo')}</h1><p class="lead">{intro}</p><div class="grid">{cards}</div>
<h2>{t(lang, 'Unlock order', 'Açılış sırası')}</h2>
<table><tr><th>{t(lang, 'Wave', 'Dalga')}</th><th>{t(lang, 'Ship', 'Gemi')}</th><th>{t(lang, 'Role', 'Görev')}</th></tr>
{''.join(f"<tr><td>{s['wave']}</td><td>{html.escape(s[lang])}</td><td>{html.escape(s['role_' + lang])}</td></tr>" for s in SHIPS)}</table>"""
    page("fleet.html", lang, t(lang, "Fleet: the seven ship classes", "Filo: yedi gemi sınıfı"),
         t(lang, "Every human ship in Last Orbit: Command Ship, Hunter, Bulwark, Halo, Lance, Patch and Well, with roles, pilots and unlock waves.",
           "Last Orbit'teki her insan gemisi: Komutan Gemisi, Avcı, Siper, Hale, Kargı, Yama ve Kuyu; görevleri, pilotları ve açılış dalgaları."),
         body, jsonld=[ld])


def build_mines(lang):
    pre = "" if lang == "en" else "tr/"
    rel = page_rel(lang, "mines.html")
    home = f"{BASE}/{pre}"
    ld, crumbs = breadcrumbs(lang, [("Last Orbit", home), (t(lang, "Mines & Powers", "Mayınlar ve Güçler"), f"{home}mines.html")])
    cards = ""
    for m in MINES:
        cards += f"""<div class="card"><div class="pic"><img src="{rel}assets/cards/{m['id']}.png" alt="{html.escape(m[lang])}" width="480" height="313" loading="lazy"></div>
<h3>{html.escape(m[lang])}</h3><p class="muted">{t(lang, 'unlocks on wave', 'açılış:')} {m['wave']}{'' if lang == 'en' else '. dalga'} · {m['cost']} {t(lang, 'salvage', 'malzeme')}</p>
<p>{html.escape(m[lang + '_desc'])}</p></div>"""
    powers = "".join(f"<tr><td>{html.escape(p[lang])}</td><td>{html.escape(p['wave_' + lang])}</td><td>{html.escape(p[lang + '_desc'])}</td></tr>" for p in POWERS)
    intro = t(lang,
              "Mines are the heart of Last Orbit. The enemy cannot see them and their radar cannot find them, so the quiet minute before each wave is where the fight is won. Powers come later: each hazard you survive becomes a weapon you can call down yourself, paid for with dark matter that persists between runs.",
              "Mayınlar Last Orbit'in kalbidir. Düşman onları göremez, radarı bulamaz; bu yüzden her dalgadan önceki sessiz dakika savaşın kazanıldığı yerdir. Güçler sonra gelir: atlattığın her tehlike, oyunlar arasında kalıcı olan karanlık maddeyle kendin çağırabileceğin bir silaha dönüşür.")
    body = f"""{crumbs}<h1>{t(lang, 'Mines and powers', 'Mayınlar ve güçler')}</h1><p class="lead">{intro}</p>
<h2>{t(lang, 'The five mines', 'Beş mayın')}</h2><div class="grid">{cards}</div>
<h2>{t(lang, 'Which mine for which fleet', 'Hangi filoya hangi mayın')}</h2>
<table><tr><th>{t(lang, 'Enemy', 'Düşman')}</th><th>{t(lang, 'Use', 'Kullan')}</th></tr>
<tr><td>Veyra, Nivara ({t(lang, 'strong shields, thin hulls', 'güçlü kalkan, ince gövde')})</td><td>EMP → {t(lang, 'Contact', 'Temas')}</td></tr>
<tr><td>Thalor, Korvath ({t(lang, 'thick hulls, weak shields', 'kalın gövde, zayıf kalkan')})</td><td>{t(lang, 'Shrapnel, Contact; Meteor to lengthen the path', 'Şarapnel, Temas; yolu uzatmak için Meteor')}</td></tr>
<tr><td>Khar ({t(lang, 'rapid fire', 'seri ateş')})</td><td>{t(lang, 'Meteor cover, mines on the approach', 'Meteor siperi, yaklaşma yoluna mayın')}</td></tr>
<tr><td>Nul ({t(lang, 'long range', 'uzun menzil')})</td><td>{t(lang, 'Mass to pull them in, then everything else', 'İçeri çekmek için Kütle, sonra gerisi')}</td></tr>
<tr><td>Auralis ({t(lang, 'hard-hitting beams', 'sert ışınlar')})</td><td>{t(lang, 'Mines on the gunners first; Bulwark up front', 'Önce topçulara mayın; Siper öne')}</td></tr></table>
<h2>{t(lang, 'The four powers', 'Dört güç')}</h2>
<table><tr><th>{t(lang, 'Power', 'Güç')}</th><th>{t(lang, 'Available', 'Açılış')}</th><th></th></tr>{powers}</table>"""
    page("mines.html", lang, t(lang, "Mines & powers: Contact, Meteor, EMP, Shrapnel, Mass", "Mayınlar ve güçler: Temas, Meteor, EMP, Şarapnel, Kütle"),
         t(lang, "What every mine in Last Orbit does, when it unlocks, what it costs and which enemy fleet it is for; plus the four powers: Second Shield, Meteor Rain, Black Hole and Rift.",
           "Last Orbit'teki her mayın ne yapar, ne zaman açılır, kaça mal olur ve hangi düşman filosu için; ayrıca dört güç: İkinci Kalkan, Meteor Yağmuru, Kara Delik ve Yarık."),
         body, jsonld=[ld])


def build_waves(lang):
    pre = "" if lang == "en" else "tr/"
    rel = page_rel(lang, "waves.html")
    home = f"{BASE}/{pre}"
    ld, crumbs = breadcrumbs(lang, [("Last Orbit", home), (t(lang, "Wave guide", "Dalga rehberi"), f"{home}waves.html")])
    blocks = "".join(
        f"<tr><td>{f['waves'][0]}–{f['waves'][1] or '∞'}</td><td><a href=\"{rel}{pre}factions/{f['id']}.html\">{html.escape(f[lang])}</a> · {html.escape(f['sub_' + lang])}</td><td>{html.escape(f['tactic_' + lang])}</td></tr>"
        for f in FACTIONS)
    meteors = ", ".join(str(w) for w in hazard_waves(8, 9, 120))
    holes = ", ".join(str(w) for w in hazard_waves(22, 6, 120))
    unlocks = sorted([(s["wave"], s[lang], t(lang, "ship", "gemi")) for s in SHIPS if s["wave"] > 1] +
                     [(m["wave"], m[lang], t(lang, "mine", "mayın")) for m in MINES if m["wave"] > 1] +
                     [(13, POWERS[1][lang], t(lang, "power", "güç")), (24, POWERS[2][lang], t(lang, "power", "güç")), (55, POWERS[3][lang], t(lang, "power", "güç"))])
    body = f"""{crumbs}<h1>{t(lang, 'Wave guide', 'Dalga rehberi')}</h1>
<p class="lead">{t(lang, 'Last Orbit is endless, but it is not random: every wave is derived from its number, so the same wave is the same fight for every commander in the world. This is the structure.', 'Last Orbit sonsuzdur ama rastgele değildir: her dalga numarasından türetilir, yani aynı dalga dünyadaki her komutan için aynı çarpışmadır. Yapı şöyle.')}</p>
<h2>{t(lang, 'Blocks of twenty', 'Yirmilik bloklar')}</h2>
<table><tr><th>{t(lang, 'Waves', 'Dalgalar')}</th><th>{t(lang, 'Civilisation', 'Uygarlık')}</th><th>{t(lang, 'Tactic', 'Taktik')}</th></tr>{blocks}</table>
<h2>{t(lang, 'Rhythm inside a block', 'Blok içi ritim')}</h2>
<ul class="timeline">
<li><b>{t(lang, 'Waves 1–3', '1–3. dalgalar')}</b>: {t(lang, 'the tutorial; the arrival zone is exact and wave 1 is the mine lesson.', 'öğretici; varış bölgesi kesindir ve 1. dalga mayın dersidir.')}</li>
<li><b>{t(lang, 'Waves 2–9', '2–9. dalgalar')}</b>: {t(lang, 'a bigger crowd of lighter ships, so the opening fights are busy but forgiving.', 'daha kalabalık ama hafif gemiler; açılış çarpışmaları yoğun fakat affedicidir.')}</li>
<li><b>{t(lang, 'Every 10th wave', 'Her 10. dalga')}</b>: {t(lang, 'an admiral ship (1×2, the block\'s boss). Every 20th wave brings two.', 'bir amiral gemisi (1×2, bloğun patronu). Her 20. dalga iki tane getirir.')}</li>
<li><b>{t(lang, 'Waves 15, 25, 35 …', '15, 25, 35 … dalgalar')}</b>: {t(lang, 'the civilisation\'s flagship leads the fleet.', 'uygarlığın sancak gemisi filoya önderlik eder.')}</li>
<li><b>{t(lang, 'From wave 61', '61. dalgadan itibaren')}</b>: {t(lang, 'admirals of beaten civilisations fight for the current ruler: every third wave, then every second, then every wave, then two at a time from 121.', 'yenilen uygarlıkların amiralleri mevcut hükümdar için savaşır: önce her üçüncü dalga, sonra her ikinci, sonra her dalga, 121\'den sonra ikişer.')}</li>
<li><b>{t(lang, 'From wave 141', '141. dalgadan itibaren')}</b>: {t(lang, 'the Heirs. Fleet ceiling 26, two admirals and one more every 25 waves.', 'Vârisler. Filo tavanı 26, iki amiral ve her 25 dalgada bir tane daha.')}</li>
</ul>
<h2>{t(lang, 'Hazards', 'Tehlikeler')}</h2>
<p><b>{t(lang, 'Meteor belt', 'Meteor kuşağı')}</b>: {t(lang, 'from wave 8, every ninth wave', '8. dalgadan itibaren her dokuzuncu dalga')} ({meteors} …). {t(lang, 'Meteor mines are your only cover.', 'Tek siperin Meteor mayınları.')}</p>
<p><b>{t(lang, 'Black-hole anomaly', 'Kara delik anomalisi')}</b>: {t(lang, 'from wave 22, every sixth wave', '22. dalgadan itibaren her altıncı dalga')} ({holes} …).</p>
<p><b>{t(lang, 'Space-time rift', 'Uzay-zaman yarığı')}</b>: {t(lang, 'first tears open by itself on wave 54.', 'ilk kez 54. dalgada kendiliğinden açılır.')}</p>
<h2>{t(lang, 'Unlocks by wave', 'Dalgaya göre açılışlar')}</h2>
<table><tr><th>{t(lang, 'Wave', 'Dalga')}</th><th></th><th></th></tr>{''.join(f'<tr><td>{w}</td><td>{html.escape(n)}</td><td class="muted">{k}</td></tr>' for w, n, k in unlocks)}</table>
<p class="muted">{t(lang, 'Enemy firepower and hulls scale gently with the wave number; the fleet ceiling is 22 ships, 24 from wave 101 and 26 under the Heirs.', 'Düşman ateş gücü ve gövdeleri dalga numarasıyla yumuşak artar; filo tavanı 22 gemi, 101. dalgadan sonra 24, Vârisler altında 26.')}</p>"""
    page("waves.html", lang, t(lang, "Wave guide: blocks, admirals, hazards, unlocks", "Dalga rehberi: bloklar, amiraller, tehlikeler, açılışlar"),
         t(lang, "How Last Orbit's endless waves are structured: twenty-wave civilisation blocks, admiral waves, meteor belts, black holes, the rift and every unlock wave.",
           "Last Orbit'in sonsuz dalgaları nasıl kurulu: yirmi dalgalık uygarlık blokları, amiral dalgaları, meteor kuşakları, kara delikler, yarık ve bütün açılış dalgaları."),
         body, jsonld=[ld])


def build_faq(lang):
    pre = "" if lang == "en" else "tr/"
    home = f"{BASE}/{pre}"
    ld, crumbs = breadcrumbs(lang, [("Last Orbit", home), (t(lang, "FAQ", "SSS"), f"{home}faq.html")])
    if lang == "en":
        qa = [
            ("what", "What is Last Orbit: Space Defense?", "Last Orbit is a free mobile tower-defense strategy game by Yigit Bayram. You command a single Command Ship and a field of invisible mines against endless waves of alien fleets, placing mines before each wave and commanding your escorts in real time during it."),
            ("free", "Is Last Orbit free?", "Yes. The game is free to download and play. It contains optional ads and optional in-app purchases (removing ads and cargo packs of salvage and dark matter). Nothing in the ranking can be bought."),
            ("platforms", "Which platforms is it on?", f"iPhone and iPad (iOS 15.0 or later) on the App Store. An Android version is in closed beta and will follow on Google Play."),
            ("android", "When is the Android version coming?", "The Android build is complete and in Google Play's closed-testing phase. It will be published on Google Play once that phase ends. The package name is " + PLAY_PKG + "."),
            ("offline", "Can I play offline?", "No. Last Orbit requires an internet connection for the world ranking and the store."),
            ("mines", "How do mines work?", "You place mines on the battlefield before each wave. The enemy cannot see them and their radar cannot detect them. There are five kinds: Contact, Meteor (a rock that blocks paths and fire), EMP (strips shields), Shrapnel (area hull damage) and Mass (pulls ships in, then implodes)."),
            ("waves", "How many waves are there?", "There is no last wave. Seven civilisations hold twenty waves each (1–140), then the Heirs rule from wave 141 onward with ever larger fleets."),
            ("ranking", "How does the ranking work?", "Every commander in the world is placed by the furthest wave they have reached. You pick a callsign; no account or login is needed."),
            ("languages", "Which languages does it support?", "English and Turkish."),
            ("age", "What is the age rating?", "12+ on the App Store (fantasy sci-fi violence against spaceships, no blood)."),
            ("purchases", "How do I restore purchases?", "Open the Store in the game and tap Restore Purchases, using the same Apple Account you bought them with."),
            ("developer", "Who made Last Orbit?", "Last Orbit is made by Yigit Bayram, an independent developer. Contact: " + CONTACT + "."),
            ("data", "What data does the game collect?", "An anonymous player ID and callsign for the ranking, and the advertising identifier used by AdMob for optional ads. See the privacy policy for details."),
        ]
    else:
        qa = [
            ("what", "Last Orbit: Space Defense nedir?", "Last Orbit, Yiğit Bayram'ın yaptığı ücretsiz bir mobil kule savunma strateji oyunudur. Tek bir Komutan Gemisi ve görünmez mayınlardan oluşan bir alanla uzaylı filolarının bitmeyen dalgalarına karşı savaşırsın: her dalgadan önce mayın dizer, dalga sırasında eskortlarını anlık yönetirsin."),
            ("free", "Last Orbit ücretsiz mi?", "Evet. İndirmesi ve oynaması ücretsizdir. İsteğe bağlı reklam ve isteğe bağlı uygulama içi satın alma (reklam kaldırma, malzeme ve karanlık madde kargoları) içerir. Sıralamada hiçbir şey satın alınamaz."),
            ("platforms", "Hangi platformlarda var?", "App Store'da iPhone ve iPad (iOS 15.0 ve üstü). Android sürümü kapalı betada, Google Play'de yayınlanacak."),
            ("android", "Android sürümü ne zaman gelecek?", "Android derlemesi hazır ve Google Play'in kapalı test aşamasında. Bu aşama bitince Google Play'de yayınlanacak. Paket adı: " + PLAY_PKG + "."),
            ("offline", "Çevrimdışı oynayabilir miyim?", "Hayır. Last Orbit dünya sıralaması ve mağaza için internet bağlantısı ister."),
            ("mines", "Mayınlar nasıl çalışır?", "Her dalgadan önce mayınları savaş alanına yerleştirirsin. Düşman onları göremez, radarı bulamaz. Beş tür var: Temas, Meteor (yolu ve ateşi kesen kaya), EMP (kalkan söker), Şarapnel (alan gövde hasarı) ve Kütle (gemileri çeker, sonra çöker)."),
            ("waves", "Kaç dalga var?", "Son dalga yok. Yedi uygarlık yirmişer dalga tutar (1–140), sonra 141. dalgadan itibaren giderek büyüyen filolarla Vârisler yönetir."),
            ("ranking", "Sıralama nasıl çalışır?", "Dünyadaki her komutan ulaştığı en uzak dalgaya göre sıralanır. Bir çağrı adı seçersin; hesap ya da giriş gerekmez."),
            ("languages", "Hangi dilleri destekliyor?", "Türkçe ve İngilizce."),
            ("age", "Yaş derecesi nedir?", "App Store'da 12+ (uzay gemilerine karşı hayali bilim kurgu şiddeti, kan yok)."),
            ("purchases", "Satın almalarımı nasıl geri yüklerim?", "Oyundaki Mağaza'yı açıp Satın Almaları Geri Yükle'ye dokun; satın aldığın Apple Hesabı ile."),
            ("developer", "Last Orbit'i kim yaptı?", "Last Orbit'i bağımsız geliştirici Yiğit Bayram yaptı. İletişim: " + CONTACT + "."),
            ("data", "Oyun hangi verileri topluyor?", "Sıralama için anonim oyuncu kimliği ve çağrı adı, isteğe bağlı reklamlar için AdMob'un kullandığı reklam kimliği. Ayrıntılar gizlilik politikasında."),
        ]
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for _, q, a in qa]}
    body = f"""{crumbs}<h1>{t(lang, 'Frequently asked questions', 'Sık sorulan sorular')}</h1><div class="faq">
{''.join(f'<h3 id="{i}">{html.escape(q)}</h3><p>{html.escape(a)}</p>' for i, q, a in qa)}</div>
<p><a href="{SUPPORT}">{t(lang, 'Support page', 'Destek sayfası')}</a> · <a href="{PRIVACY}">{t(lang, 'Privacy policy', 'Gizlilik politikası')}</a></p>"""
    page("faq.html", lang, t(lang, "FAQ", "SSS"),
         t(lang, "Answers about Last Orbit: Space Defense: price, platforms, Android release, offline play, mines, waves, ranking, languages, age rating and purchases.",
           "Last Orbit: Space Defense hakkında cevaplar: fiyat, platformlar, Android çıkışı, çevrimdışı oynama, mayınlar, dalgalar, sıralama, diller, yaş derecesi ve satın almalar."),
         body, jsonld=[ld, faq_ld])


def build_changelog(lang):
    pre = "" if lang == "en" else "tr/"
    home = f"{BASE}/{pre}"
    ld, crumbs = breadcrumbs(lang, [("Last Orbit", home), (t(lang, "Updates", "Güncellemeler"), f"{home}changelog.html")])
    items = ""
    for c in CHANGELOG:
        items += f"<h2>{c['ver']} <span class=\"muted\" style=\"font-size:15px\">· {c['date']} · {html.escape(c['status_' + lang])}</span></h2><ul>{''.join(f'<li>{html.escape(x)}</li>' for x in c[lang])}</ul>"
    body = f"""{crumbs}<h1>{t(lang, 'Updates', 'Güncellemeler')}</h1><p class="lead">{t(lang, 'What changed in each version of Last Orbit.', "Last Orbit'in her sürümünde ne değişti.")}</p>{items}"""
    page("changelog.html", lang, t(lang, "Updates and release notes", "Güncellemeler ve sürüm notları"),
         t(lang, "Release notes for every version of Last Orbit: Space Defense.", "Last Orbit: Space Defense'in her sürümünün notları."), body, jsonld=[ld])


def build_press(lang):
    pre = "" if lang == "en" else "tr/"
    rel = page_rel(lang, "press.html")
    home = f"{BASE}/{pre}"
    ld, crumbs = breadcrumbs(lang, [("Last Orbit", home), (t(lang, "Press kit", "Basın kiti"), f"{home}press.html")])
    facts = [
        (t(lang, "Title", "Ad"), "Last Orbit: Space Defense"),
        (t(lang, "Developer", "Geliştirici"), "Yigit Bayram (independent, Türkiye)"),
        (t(lang, "Release", "Çıkış"), t(lang, "9 November 2026 (App Store); Android in closed beta", "9 Kasım 2026 (App Store); Android kapalı betada")),
        (t(lang, "Platforms", "Platformlar"), "iOS 15+, Android"),
        (t(lang, "Price", "Fiyat"), t(lang, "Free, optional ads and in-app purchases", "Ücretsiz, isteğe bağlı reklam ve satın alma")),
        (t(lang, "Genre", "Tür"), t(lang, "Tower defense / real-time strategy, sci-fi", "Kule savunma / gerçek zamanlı strateji, bilim kurgu")),
        (t(lang, "Languages", "Diller"), "English, Türkçe"),
        (t(lang, "Engine", "Motor"), "Unity"),
        (t(lang, "Contact", "İletişim"), CONTACT),
        ("App Store", APPSTORE),
    ]
    one = t(lang, "Lay invisible mines, command your fleet, hold the last orbit. Endless waves.", "Görünmez mayınlar diz, filonu yönet, son yörüngeyi tut. Dalgalar bitmez.")
    short = t(lang, "Last Orbit is a free mobile tower-defense game where the enemy cannot see your mines. Plan each wave before it arrives, then command a small fleet in real time against seven alien civilisations and the Heirs who follow them.",
              "Last Orbit, düşmanın mayınlarını göremediği ücretsiz bir mobil kule savunma oyunu. Her dalgayı gelmeden planla, sonra yedi uzaylı uygarlığa ve ardından gelen Vârisler'e karşı küçük bir filoyu anlık yönet.")
    shots = "".join(f'<a href="{rel}assets/press/screenshot_{n:02d}_en.png"><img src="{rel}assets/shots/{n:02d}_{lang}.png" alt="{html.escape(SHOT_ALT[lang][n])}" width="600" height="1304" loading="lazy"></a>' for n in range(1, 11))
    body = f"""{crumbs}<h1>{t(lang, 'Press kit', 'Basın kiti')}</h1>
<p class="lead">{t(lang, 'Everything here may be used freely in coverage of the game.', 'Buradaki her şey oyunla ilgili haberlerde serbestçe kullanılabilir.')}</p>
<h2>{t(lang, 'Facts', 'Bilgiler')}</h2><table>{''.join(f'<tr><th>{html.escape(k)}</th><td>{html.escape(v)}</td></tr>' for k, v in facts)}</table>
<h2>{t(lang, 'Descriptions', 'Açıklamalar')}</h2>
<p><b>{t(lang, 'One line', 'Tek satır')}:</b> {one}</p>
<p><b>{t(lang, 'Short', 'Kısa')}:</b> {short}</p>
<h2>{t(lang, 'Icon', 'Simge')}</h2><p><a href="{rel}assets/press/icon_1024.png"><img src="{rel}assets/icon-192.png" alt="Last Orbit icon" width="96" height="96" style="border-radius:20px"></a> <a href="{rel}assets/press/icon_1024.png">1024×1024 PNG</a></p>
<h2>{t(lang, 'Screenshots (1320×2868, click for full size)', 'Ekran görüntüleri (1320×2868, tam boyut için tıkla)')}</h2><div class="shots">{shots}</div>
<h2>{t(lang, 'Feature image', 'Öne çıkan görsel')}</h2><p><a href="{rel}assets/og.png"><img src="{rel}assets/og.png" alt="Last Orbit feature image" width="1024" height="500"></a></p>"""
    page("press.html", lang, t(lang, "Press kit", "Basın kiti"),
         t(lang, "Press kit for Last Orbit: Space Defense: facts, descriptions, icon, screenshots and contact.",
           "Last Orbit: Space Defense basın kiti: bilgiler, açıklamalar, simge, ekran görüntüleri ve iletişim."), body, jsonld=[ld])


def build_extras():
    with open(os.path.join(ROOT, "robots.txt"), "w") as f:
        f.write("User-agent: *\nAllow: /\n\n")
        for bot in ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "Claude-User", "PerplexityBot", "Perplexity-User",
                    "Google-Extended", "Googlebot", "Bingbot", "Applebot", "Applebot-Extended", "DuckAssistBot", "Amazonbot", "meta-externalagent", "YouBot"]:
            f.write(f"User-agent: {bot}\nAllow: /\n\n")
        f.write(f"Sitemap: {BASE}/sitemap.xml\n")
    with open(os.path.join(ROOT, "sitemap.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n')
        for url, alt, lang in PAGES:
            en, tr = f"{BASE}/{alt}", f"{BASE}/tr/{alt}"
            f.write(f'  <url><loc>{url}</loc><lastmod>{TODAY}</lastmod>'
                    f'<xhtml:link rel="alternate" hreflang="en" href="{en}"/><xhtml:link rel="alternate" hreflang="tr" href="{tr}"/></url>\n')
        f.write("</urlset>\n")
    lines = ["# Last Orbit: Space Defense", "",
             "> Free mobile tower-defense strategy game (iOS, Android beta) by independent developer Yigit Bayram. "
             "The player commands one Command Ship and a field of mines the enemy cannot see, against endless waves of seven alien civilisations and the Heirs. "
             "Released 9 November 2026. Languages: English, Turkish.", "",
             f"- App Store: {APPSTORE}", f"- Support and privacy: {SUPPORT}", f"- Contact: {CONTACT}", "",
             "## Pages", ""]
    for url, alt, lang in PAGES:
        if lang == "en":
            lines.append(f"- {url}")
    lines += ["", "## Key facts", "",
              "- Genre: tower defense / real-time strategy, science fiction; single player; endless waves.",
              "- Core loop: place invisible mines before each wave, then command escorts (guard, charge, focus fire) in real time.",
              "- Mines: Contact (wave 1), Meteor (4), EMP (19), Shrapnel (34), Mass (44).",
              "- Ships: Command Ship, Hunter (6), Bulwark (16), Halo (28), Lance (38), Patch (58), Well (64).",
              "- Powers: Second Shield, Meteor Rain (13), Black Hole (24), Rift (55).",
              "- Civilisations in twenty-wave blocks: Veyra 1–20, Nul 21–40, Nivara 41–60, Thalor 61–80, Khar 81–100, Auralis 101–120, Korvath 121–140; the Heirs from 141.",
              "- Admiral ship every 10th wave, two every 20th; flagship leads waves 15, 25, 35 …",
              "- Hazards: meteor belt from wave 8 every 9 waves; black hole from wave 22 every 6; rift first on wave 54.",
              "- World ranking by furthest wave reached; callsign only, no account.",
              "- Monetisation: optional ads, Remove Ads, cargo packs. Nothing competitive is sold.",
              "- Age rating 12+. Internet connection required."]
    with open(os.path.join(ROOT, "llms.txt"), "w") as f:
        f.write("\n".join(lines) + "\n")
    with open(os.path.join(ROOT, ".nojekyll"), "w") as f:
        f.write("")
    with open(os.path.join(ROOT, "404.html"), "w") as f:
        f.write(f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0; url={BASE}/"><title>Last Orbit</title></head><body><a href="{BASE}/">Last Orbit: Space Defense</a></body></html>')


def main():
    for lang in ("en", "tr"):
        build_home(lang)
        build_factions(lang)
        build_fleet(lang)
        build_mines(lang)
        build_waves(lang)
        build_faq(lang)
        build_changelog(lang)
        build_press(lang)
    build_extras()
    print(f"{len(PAGES)} pages written")


if __name__ == "__main__":
    main()
