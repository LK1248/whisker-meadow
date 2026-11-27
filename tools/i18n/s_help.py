# Help paragraphs, in the order they appear in openHelp(): (he, fr, ru, it, ko, ja). Whole <li>/<p> inner HTML.
H = [
# 0 goal
("אתם מנהלים מקלט חתולים. חתולי הצלה ביישנים מגיעים; אתם זוכים באהבתם, שומרים עליהם בריאים ושמחים, ועוזרים להם למצוא בית אוהב. אי אפשר להפסיד: לחתולים אף פעם לא קורה שום דבר רע, הם רק מתעצבנים כשמתעלמים מהם.",
 "Tu tiens un refuge pour chats. Des chats timides arrivent ; tu gagnes leur amour, tu les gardes en bonne santé et heureux, et tu les aides à trouver un foyer aimant. On ne peut pas perdre : les chats ne sont jamais blessés, ils boudent juste quand on les ignore.",
 "Вы управляете приютом для кошек. Приходят робкие найдёныши; вы завоёвываете их любовь, заботитесь об их здоровье и счастье и помогаете им найти любящий дом. Проиграть нельзя: кошкам ничего не грозит, они просто ворчат, если на них не обращают внимания.",
 "Gestisci un rifugio per gatti. Arrivano gatti timidi da salvare; conquisti il loro affetto, li tieni sani e felici e li aiuti a trovare una casa piena d'amore. Non si perde mai: i gatti non si fanno mai male, si offendono solo se li ignori.",
 "고양이 보호소를 운영해요. 수줍은 구조 고양이들이 찾아오면 사랑을 얻고, 건강하고 행복하게 돌보고, 사랑받는 집을 찾아 주세요. 지는 일은 없어요: 고양이는 절대 다치지 않고, 관심을 못 받으면 조금 삐칠 뿐이에요.",
 "あなたは猫の保護施設を営んでいます。シャイな保護猫がやってきます。なかよくなって、元気で幸せに暮らせるようにお世話し、やさしい家族を見つけてあげましょう。負けはありません。猫がけがをすることはなく、かまわないとすねるだけです。"),
# 1 love
("<b>אהבה</b> (לב): ליטוף עדין בקצב, משחק, האכלה, מצמוץ בחזרה, טפיחות בישבן (לחתולים שאוהבים אותן), מזון פרימיום. יורדת כשמגרדים במקום הלא נכון, מלטפים מהר מדי, או מחזיקים חתול לחוץ יותר מדי זמן. גורים מתחממים מהר יותר.",
 "<b>Amour</b> (cœur) : caresses douces en rythme, jeux, repas, clignements rendus, tapotis sur les fesses (pour les chats qui aiment), nourriture premium. Il baisse si tu gratouilles au mauvais endroit, caresses trop vite ou portes trop longtemps un chat nerveux. Les chatons s'attachent plus vite.",
 "<b>Любовь</b> (сердце): нежные поглаживания в такт, игры, кормление, моргание в ответ, похлопывания по попе (для тех, кто их любит), премиум-корм. Падает, если чесать не там, гладить слишком быстро или долго держать нервную кошку на руках. Котята привыкают быстрее.",
 "<b>Amore</b> (cuore): carezze delicate a tempo, gioco, cibo, occhiolini ricambiati, colpetti sul sedere (per i gatti a cui piacciono), cibo premium. Scende se gratti nel punto sbagliato, accarezzi troppo in fretta o tieni in braccio troppo a lungo un gatto nervoso. I gattini si affezionano prima.",
 "<b>애정</b> (하트): 박자에 맞춘 부드러운 쓰다듬기, 놀이, 밥 주기, 눈인사 답하기, 엉덩이 팡팡 (좋아하는 고양이만), 프리미엄 사료. 엉뚱한 곳을 긁거나, 너무 빨리 쓰다듬거나, 겁 많은 고양이를 너무 오래 안고 있으면 내려가요. 아기 고양이는 더 빨리 친해져요.",
 "<b>なかよし</b>（ハート）：リズムにあわせたやさしいなでなで、遊び、ごはん、まばたき返し、おしりトントン（好きな猫だけ）、プレミアムフード。ちがう場所をかいたり、なでるのが速すぎたり、こわがりな猫を長くだっこしすぎると下がります。子猫は早くなつきます。"),
# 2 groom
("<b>טיפוח</b> (מברשת): פרווה נקייה ומבריקה. הוא דועך לאט; הברישו כדי להחזיר אותו. לשופטי התערוכה זה חשוב מאוד, למשפחות קצת. חתול מוזנח מאוד נדבק ב<b>פרעושים</b> (נקודות שחורות קטנות, הרבה גירודים ורטינות): הבריש אותם החוצה.",
 "<b>Toilettage</b> (brosse) : un pelage propre et brillant. Il baisse lentement ; brosse pour le faire remonter. Les juges des concours y tiennent beaucoup, les familles un peu. Un chat très négligé attrape des <b>puces</b> (petits points noirs, beaucoup de grattage et de grognements) : brosse-les.",
 "<b>Шерсть</b> (щётка): чистая блестящая шубка. Со временем тускнеет; расчёсывайте, чтобы вернуть блеск. Судьям на выставках это очень важно, семьям — немного. Очень неухоженная кошка подхватывает <b>блох</b> (крошечные чёрные точки, много чесания и ворчания): вычешите их.",
 "<b>Pelo</b> (spazzola): un mantello pulito e lucido. Cala piano; spazzola per farlo risalire. Ai giudici delle mostre importa molto, alle famiglie un po'. Un gatto molto trasandato prende le <b>pulci</b> (puntini neri, tanto grattarsi e brontolare): toglile con la spazzola.",
 "<b>털 손질</b> (빗): 깨끗하고 윤기 나는 털. 천천히 떨어지니 빗질로 되돌려요. 대회 심사위원은 아주 중요하게 보고, 가족들은 조금 봐요. 아주 지저분한 고양이에게는 <b>벼룩</b>이 생겨요 (작은 검은 점, 계속 긁고 투덜거려요): 빗질로 없애 주세요.",
 "<b>毛並み</b>（ブラシ）：きれいでつやつやの毛。ゆっくり下がるので、ブラシで戻しましょう。コンテストの審査員はとても重視し、家族も少し気にします。ひどくぼさぼさの猫には<b>ノミ</b>がつきます（小さな黒い点、たくさんかいてぶつぶつ言う）：ブラシで取ってあげて。"),
# 3 health
("<b>בריאות</b> (עלה): בטן מלאה, כיף, פרווה מטופחת וארגז חול נקי. תנומות על כריות ומזרקת המים עוזרות.",
 "<b>Santé</b> (feuille) : ventre plein, jeux, pelage soigné et litière propre. Les siestes sur coussin et la fontaine à eau aident.",
 "<b>Здоровье</b> (листик): полный животик, веселье, ухоженная шерсть и чистый лоток. Помогают сон на подушках и фонтанчик.",
 "<b>Salute</b> (foglia): pancia piena, divertimento, pelo curato e lettiera pulita. Aiutano i pisolini sui cuscini e la fontanella.",
 "<b>건강</b> (잎): 부른 배, 즐거움, 손질된 털, 깨끗한 화장실. 방석 낮잠과 급수기가 도움이 돼요.",
 "<b>けんこう</b>（葉っぱ）：満腹、楽しさ、ととのった毛並み、きれいなトイレ。クッションでのお昼寝や給水器も効きます。"),
# 4
("הקישו על חתול כדי לראות את המדדים שלו מעל ראשו.", "Touche un chat pour voir ses jauges au-dessus de sa tête.", "Нажмите на кошку, чтобы увидеть её показатели над головой.", "Tocca un gatto per vedere le sue statistiche sopra la testa.", "고양이를 누르면 머리 위에 수치가 보여요.", "猫をタップすると頭の上にステータスが出ます。"),
# 5
("גררו על החתול: ליטוף חלק אחד, ואז <b>חכו</b>.", "Glisse sur le chat : une longue caresse, puis <b>attends</b>.", "Проведите по кошке: одно плавное поглаживание, потом <b>подождите</b>.", "Trascina sul gatto: una carezza lunga, poi <b>aspetta</b>.", "고양이 위로 끌어요: 부드럽게 한 번 쓰다듬고, <b>기다려요</b>.", "猫の上をなぞって、なめらかに一回なでたら<b>待ちます</b>。"),
# 6
("המשיכו ללטף לאט: הטבעת ליד היד מתמלאת כשהיד זזה על החתול, וכל טבעת מלאה היא גרגור שמח. החזקה במקום לא ממלאת אותה, ואחרי כמה שניות בלי תנועה החתול משתעמם והולך.",
 "Continue lentement : l'anneau près de ta main se remplit quand ta main bouge sur le chat, et chaque anneau plein donne un ronron. Rester immobile ne le remplit pas, et après quelques secondes sans bouger le chat s'ennuie et s'en va.",
 "Продолжайте гладить медленно: кольцо у руки заполняется, пока рука движется по кошке, и каждое полное кольцо — это довольное мурчание. Если держать руку неподвижно, оно не заполняется, а через несколько секунд кошке становится скучно и она уходит.",
 "Continua piano: l'anello vicino alla mano si riempie mentre la mano si muove sul gatto, e ogni anello pieno è una fusa felice. Restare fermi non lo riempie, e dopo qualche secondo di immobilità il gatto si annoia e se ne va.",
 "천천히 계속 쓰다듬어요: 손이 고양이 위를 움직이는 동안 손 옆의 고리가 차오르고, 고리가 다 차면 행복한 그르릉이에요. 가만히 있으면 차지 않고, 몇 초 동안 멈춰 있으면 고양이가 심심해서 가 버려요.",
 "ゆっくりなでつづけて。手が猫の上を動いているあいだ、手のそばの輪がたまり、輪がいっぱいになるたびに幸せなゴロゴロ。止まっているとたまらず、数秒じっとしていると猫はあきて行ってしまいます。"),
# 7
("שעון חול = להאט (שעון חול רועד = הרבה יותר מדי מהר; יותר מדי מזה והחתול כבר לא רוצה).",
 "Un sablier = ralentis (un sablier qui tremble = beaucoup trop vite ; trop de ça et le chat en a assez).",
 "Песочные часы = помедленнее (дрожащие часы = слишком быстро; если продолжать, кошке надоест).",
 "Una clessidra = rallenta (una clessidra che trema = troppo veloce; se esageri il gatto ne ha abbastanza).",
 "모래시계 = 천천히 (흔들리는 모래시계 = 너무 빨라요; 계속되면 고양이가 질려 버려요).",
 "砂時計＝ゆっくり（ふるえる砂時計＝速すぎ。つづけると猫はもういやになります）。"),
# 8
("יותר מדי ליטופים מהירים מגרים את החתול יותר מדי: שימו לב לזנב מתעוות ולאוזניים לצדדים. אז הוא הולך, או, אם הוא עוד לא אוהב אתכם, שורט (פלסטר!).",
 "Trop de caresses rapides surexcitent un chat : surveille la queue qui fouette et les oreilles de côté. Alors il s'en va, ou, s'il ne t'aime pas encore, il griffe (pansement !).",
 "Слишком много быстрых поглаживаний перевозбуждают кошку: следите за дёргающимся хвостом и прижатыми в стороны ушами. Тогда она уходит или, если ещё не привязалась к вам, царапается (пластырь!).",
 "Troppe carezze veloci agitano il gatto: guarda la coda che frusta e le orecchie di lato. Allora se ne va o, se non ti vuole ancora bene, graffia (cerotto!).",
 "빠른 쓰다듬기가 너무 많으면 고양이가 예민해져요: 씰룩이는 꼬리와 옆으로 젖힌 귀를 잘 봐요. 그러면 가 버리거나, 아직 안 친하면 할퀴어요 (반창고!).",
 "速いなでなでが多すぎると猫は興奮しすぎます。ぴくぴくするしっぽと横に倒れた耳に注意。そうなると行ってしまうか、まだなついていなければひっかきます（ばんそうこう！）。"),
# 9
("<b>ראש, לחיים, סנטר</b>: האהובים.", "<b>Tête, joues, menton</b> : les préférés.", "<b>Голова, щёки, подбородок</b>: любимые места.", "<b>Testa, guance, mento</b>: i preferiti.", "<b>머리, 볼, 턱</b>: 제일 좋아해요.", "<b>頭・ほっぺ・あご</b>：大好き。"),
# 10
("<b>גב</b>: בסדר. <b>זנב</b>: לא!", "<b>Dos</b> : ça va. <b>Queue</b> : non !", "<b>Спина</b>: можно. <b>Хвост</b>: нет!", "<b>Schiena</b>: va bene. <b>Coda</b>: no!", "<b>등</b>: 괜찮아요. <b>꼬리</b>: 안 돼요!", "<b>背中</b>：ふつう。<b>しっぽ</b>：だめ！"),
# 11
("<b>בטן</b>: רק כשחתול מתגלגל על הגב ויש לו אהבה 75+. אחרת זו מלכודת.", "<b>Ventre</b> : seulement quand un chat se roule sur le dos et a 75+ d'Amour. Sinon c'est un piège.", "<b>Животик</b>: только когда кошка переворачивается на спину и её Любовь 75+. Иначе это ловушка.", "<b>Pancia</b>: solo quando un gatto si rotola sulla schiena e ha Amore 75+. Altrimenti è una trappola.", "<b>배</b>: 고양이가 벌러덩 누웠고 애정이 75 이상일 때만. 아니면 함정이에요.", "<b>おなか</b>：猫がごろんと転がって、なかよしが75以上のときだけ。それ以外はワナです。"),
# 12
("<b>טפיחות בישבן</b>: הקישו פעם אחת על האחוריים. יש חתולים שאוהבים, יש שלא: גלו!", "<b>Tapotis sur les fesses</b> : touche une fois l'arrière-train. Certains chats adorent, d'autres non : à toi de voir !", "<b>Похлопывания по попе</b>: нажмите один раз на заднюю часть. Одни кошки обожают, другие нет: проверьте!", "<b>Colpetti sul sedere</b>: tocca una volta il posteriore. Ad alcuni gatti piace, ad altri no: scoprilo!", "<b>엉덩이 팡팡</b>: 엉덩이를 한 번 톡 눌러요. 좋아하는 고양이도, 싫어하는 고양이도 있어요: 알아봐요!", "<b>おしりトントン</b>：おしりを一回タップ。大好きな猫も、いやがる猫もいます。ためしてみて！"),
# 13
("חתולים שמחים נותנים מכת ראש ליד, לשים, נשענים ומצמצים לאט. כשחתול מרים את הראש וממצמץ אליכם לאט, <b>הקישו עליו כדי למצמץ בחזרה</b>.",
 "Les chats heureux donnent des coups de tête, pétrissent, se blottissent et clignent lentement des yeux. Quand un chat lève la tête et cligne lentement vers toi, <b>touche-le pour lui rendre son clignement</b>.",
 "Счастливые кошки бодают руку, топчутся лапками, прижимаются и медленно моргают. Когда кошка поднимает взгляд и медленно моргает вам, <b>нажмите на неё, чтобы моргнуть в ответ</b>.",
 "I gatti felici danno testate alla mano, impastano, si appoggiano e fanno l'occhiolino lento. Quando un gatto alza lo sguardo e ti fa l'occhiolino lento, <b>toccalo per ricambiare</b>.",
 "행복한 고양이는 손에 머리를 비비고, 꾹꾹이를 하고, 기대고, 천천히 눈을 깜빡여요. 고양이가 올려다보며 천천히 눈을 깜빡이면 <b>눌러서 눈인사에 답해요</b>.",
 "幸せな猫は手に頭をすりつけ、ふみふみして、よりかかり、ゆっくりまばたきします。猫が見上げてゆっくりまばたきしたら、<b>タップしてまばたきを返して</b>。"),
# 14 pet tool
("<b>ליטוף</b>: מלטפים; לחיצה ארוכה על חתול מרימה אותו (חתולים רגועים נרפים, לחוצים מתפתלים החוצה). הניחו אותו ליד חתול אחר כדי להכיר ביניהם.",
 "<b>Caresser</b> : caresse ; appuie longuement sur un chat pour le porter (les chats détendus se laissent aller, les nerveux se tortillent). Pose-le près d'un autre chat pour les présenter.",
 "<b>Гладить</b>: поглаживания; нажмите и удерживайте кошку, чтобы взять её на руки (спокойные расслабляются, нервные вырываются). Опустите рядом с другой кошкой, чтобы познакомить их.",
 "<b>Coccole</b>: accarezza; tieni premuto su un gatto per prenderlo in braccio (i gatti rilassati si abbandonano, quelli nervosi si divincolano). Posalo vicino a un altro gatto per presentarli.",
 "<b>쓰다듬기</b>: 쓰다듬어요; 고양이를 길게 누르면 안아 올려요 (편한 고양이는 축 늘어지고, 겁 많은 고양이는 버둥대며 빠져나가요). 다른 고양이 옆에 내려놓으면 서로 소개해요.",
 "<b>なでる</b>：なでなで。猫を長押しするとだっこ（リラックスした猫はだらん、こわがりな猫はじたばたして逃げます）。ほかの猫のそばにおろすと紹介できます。"),
# 15 brush tool
("<b>מברשת</b>: הבריש קדימה ואחורה, בעדינות, כדי לנקות את הפרווה. מהר מדי והחתול רוטן, ואז הולך או שורט. חתולים שעוד לא אוהבים אתכם סובלים רק הברשה איטית מאוד, אז קודם ללטף חתול חדש. חתול מוזנח (טיפוח מתחת ל־35) נראה עמום ומאובק, עם שיער פרוע, גרביים בוציות ושאריות עלים וזרדים בפרווה; הברשה מנקה אותו, ופרווה נקייה באמת נוצצת. אהבה באה מליטוף; הברשה מעלה טיפוח (זה עוזר לבריאות, מנצח בתערוכות ומסלק פרעושים). חתולים גם מטפחים את עצמם קצת כשהם שמחים ושבעים.",
 "<b>Brosse</b> : frotte d'avant en arrière, doucement, pour nettoyer le pelage. Trop vite et le chat grogne, puis part ou griffe. Les chats qui ne t'aiment pas encore ne tolèrent qu'un brossage très lent : caresse d'abord un nouveau venu. Un chat négligé (Toilettage sous 35) a l'air terne et poussiéreux, avec des poils en bataille, des chaussettes boueuses et des bouts de feuilles et de brindilles dans la fourrure ; le brossage le nettoie, et un pelage vraiment propre brille. L'amour vient des caresses ; le brossage augmente le Toilettage (bon pour la santé, les concours et contre les puces). Les chats se toilettent aussi un peu tout seuls quand ils sont heureux et nourris.",
 "<b>Щётка</b>: водите вперёд-назад, мягко, чтобы почистить шерсть. Слишком быстро — и кошка ворчит, потом уходит или царапается. Кошки, которые вас ещё не любят, терпят только очень медленное расчёсывание, так что сначала погладьте новенького. Неухоженная кошка (Шерсть ниже 35) выглядит тусклой и пыльной: взъерошенная, с грязными лапками, листиками и веточками в шерсти; расчёсывание приводит её в порядок, а по-настоящему чистая шубка сияет. Любовь даёт поглаживание; щётка повышает Шерсть (это полезно для здоровья, помогает на выставках и избавляет от блох). Довольные и сытые кошки и сами немного умываются.",
 "<b>Spazzola</b>: strofina avanti e indietro, con delicatezza, per pulire il pelo. Troppo veloce e il gatto brontola, poi se ne va o graffia. I gatti che non ti vogliono ancora bene sopportano solo una spazzolata lentissima, quindi coccola prima un nuovo arrivato. Un gatto trasandato (Pelo sotto 35) sembra spento e impolverato, arruffato, con le zampe infangate e pezzetti di foglie e rametti nel pelo; la spazzola lo sistema, e un mantello davvero pulito brilla. L'amore nasce dalle carezze; spazzolare alza il Pelo (aiuta la salute, vince le mostre e toglie le pulci). I gatti si puliscono anche un po' da soli quando sono felici e sazi.",
 "<b>빗질</b>: 앞뒤로 살살 빗어 털을 깨끗하게 해요. 너무 빠르면 고양이가 투덜대다가 가 버리거나 할퀴어요. 아직 안 친한 고양이는 아주 느린 빗질만 참으니, 새로 온 고양이는 먼저 쓰다듬어 주세요. 지저분한 고양이 (털 손질 35 미만)는 칙칙하고 먼지투성이에, 머리는 부스스하고 발은 진흙투성이고, 털에 나뭇잎과 잔가지가 붙어 있어요; 빗질하면 깨끗해지고, 정말 깨끗한 털은 반짝여요. 애정은 쓰다듬기로 오르고, 빗질은 털 손질을 올려요 (건강에도 좋고, 대회에서 이기고, 벼룩도 없애요). 고양이도 행복하고 배부르면 스스로 조금 그루밍해요.",
 "<b>ブラシ</b>：やさしく前後にこすって毛をきれいに。速すぎると猫はぶつぶつ言って、行ってしまうかひっかきます。まだなついていない猫はとてもゆっくりのブラシしかがまんできないので、新入りはまずなでてあげて。ぼさぼさの猫（毛並み35未満）はくすんでほこりっぽく、寝ぐせ、どろだらけの足、毛に葉っぱや小枝がついています。ブラシできれいになり、本当にきれいな毛はかがやきます。なかよしはなでて上がり、ブラシは毛並みを上げます（けんこうにも良く、コンテストに勝てて、ノミも取れます）。猫も幸せでおなかいっぱいなら少し自分で毛づくろいします。"),
# 16 laser
("<b>לייזר</b> (חנות): גררו את הנקודה והחתולים רצים וזונקים. אחרי שדרוג, הוא נגמר בחטיף.", "<b>Laser</b> (boutique) : fais glisser le point et les chats foncent et bondissent. Amélioré, il finit sur une friandise.", "<b>Лазер</b> (магазин): водите точку, и кошки носятся и прыгают. После улучшения в конце их ждёт вкусняшка.", "<b>Laser</b> (negozio): trascina il puntino e i gatti corrono e balzano. Migliorato, finisce con un premio.", "<b>레이저</b> (상점): 점을 끌면 고양이들이 달려가 덮쳐요. 업그레이드하면 마지막에 간식이 나와요.", "<b>レーザー</b>（ショップ）：点を動かすと猫がダッシュして飛びつきます。アップグレードすると最後におやつ。"),
# 17
("אפשר להקיש על קערות וארגזי חול עם כל כלי.", "On peut toucher les gamelles et les litières avec n'importe quel outil.", "На миски и лотки можно нажимать любым инструментом.", "Ciotole e lettiere si possono toccare con qualsiasi strumento.", "밥그릇과 화장실은 어떤 도구로도 누를 수 있어요.", "お皿とトイレはどの道具でもタップできます。"),
# 18
("הקישו על קערה כדי למלא אותה (קודם מזון פרימיום, ואז כופתיות).", "Touche une gamelle pour la remplir (nourriture premium d'abord, puis croquettes).", "Нажмите на миску, чтобы наполнить её (сначала премиум-корм, потом сухой).", "Tocca una ciotola per riempirla (prima cibo premium, poi crocchette).", "밥그릇을 누르면 채워져요 (프리미엄 사료 먼저, 그다음 일반 사료).", "お皿をタップしてごはんを入れます（プレミアムフードが先、次にカリカリ）。"),
# 19
("הקישו על ארגז החול כדי לנקות אותו; ארגזים מלוכלכים גורמים לאחו להסריח.", "Touche la litière pour la nettoyer ; les litières sales font sentir mauvais la prairie.", "Нажмите на лоток, чтобы почистить его; от грязных лотков на лугу плохо пахнет.", "Tocca la lettiera per pulirla; le lettiere sporche fanno puzzare il prato.", "화장실을 누르면 치워요; 더러운 화장실은 초원에 냄새가 나게 해요.", "トイレをタップしてそうじ。よごれたトイレは草原がくさくなります。"),
# 20
("גג לגשם שומר על החתולים יבשים במקלחות. חתולים שנשארים בגשם נעשים קצת מוזנחים.", "Un abri de pluie garde les chats au sec pendant les averses. Les chats restés sous la pluie deviennent un peu ébouriffés.", "Навес от дождя спасает кошек от ливня. Кошки, оставшиеся под дождём, становятся немного растрёпанными.", "Una tettoia tiene i gatti all'asciutto quando piove. I gatti rimasti sotto la pioggia diventano un po' arruffati.", "비 가림막이 있으면 소나기에도 고양이가 젖지 않아요. 비를 맞은 고양이는 조금 지저분해져요.", "雨よけ屋根があればにわか雨でもぬれません。雨にぬれた猫は少しぼさぼさになります。"),
# 21
("עוזרים ממלאים קערות, מנקים ומלטפים חתולים, תמורת ‎$6 לדקה. עוזרים שלא מקבלים שכר נחים.", "Les aides remplissent les gamelles, nettoient et caressent les chats, pour 6 $ la minute. Sans salaire, ils se reposent.", "Помощники наполняют миски, убирают и гладят кошек за $6 в минуту. Без зарплаты они отдыхают.", "Gli aiutanti riempiono le ciotole, puliscono e coccolano i gatti, per $6 al minuto. Se non pagati, riposano.", "도우미는 밥그릇을 채우고, 청소하고, 고양이를 쓰다듬어요. 분당 $6이에요. 월급을 못 받으면 쉬어요.", "お手伝いさんはお皿をみたし、そうじして、猫をなでます。1分 $6。お給料がないと休みます。"),
# 22
("קופת התרומות ליד השער אוספת כסף כשהחתולים שלכם שמחים.", "La tirelire à dons près du portail récolte de l'argent quand tes chats sont heureux.", "Копилка для пожертвований у ворот собирает деньги, когда ваши кошки счастливы.", "Il barattolo delle offerte vicino al cancello raccoglie soldi quando i tuoi gatti sono felici.", "문 옆의 기부함은 고양이들이 행복할 때 돈이 모여요.", "門のそばの募金箱は、猫たちが幸せだとお金がたまります。"),
# 23 fair
("חתול בוגר עם <b>אהבה 55+, טיפוח 50+ ובריאות 60+</b> מקבל כפתור <b>לתערוכה!</b> בתג שלו. ככל שהוא מטופח יותר, הוא מגיע למקום גבוה יותר והפרס גדול יותר. כל חתול זוכה בקטגוריה (הגרגור הטוב ביותר, הפרווה הרכה ביותר, ההתקדמות הגדולה, ההצלה האמיצה, הלבוש הטוב ביותר...) ובכסף. ניצחונות מקדמים אתכם לתערוכות גדולות יותר.",
 "Un chat adulte avec <b>Amour 55+, Toilettage 50+ et Santé 60+</b> a un bouton <b>Concours !</b> sur sa fiche. Mieux il est toiletté, mieux il se classe et plus le prix est gros. Chaque chat gagne une catégorie (Meilleur ronron, Pelage le plus doux, Plus beaux progrès, Sauvetage le plus courageux, Le plus élégant...) et de l'argent. Gagner te fait passer à de plus grands concours.",
 "Взрослая кошка с <b>Любовью 55+, Шерстью 50+ и Здоровьем 60+</b> получает кнопку <b>Выставка!</b> на карточке. Чем ухоженнее, тем выше место и больше приз. Каждая кошка побеждает в какой-нибудь номинации (Лучшее мурчание, Самая пушистая шерсть, Лучший прогресс, Самый смелый найдёныш, Самый нарядный...) и получает деньги. Победы открывают выставки побольше.",
 "Un gatto adulto con <b>Amore 55+, Pelo 50+ e Salute 60+</b> ha il pulsante <b>Mostra!</b> sul cartellino. Più è curato, più si piazza in alto e più grande è il premio. Ogni gatto vince una categoria (Fusa migliori, Pelo più soffice, Più migliorato, Salvataggio più coraggioso, Il più elegante...) e un premio in denaro. Vincere ti porta a mostre più grandi.",
 "<b>애정 55+, 털 손질 50+, 건강 60+</b>인 다 큰 고양이는 정보창에 <b>대회!</b> 버튼이 생겨요. 털이 좋을수록 순위가 높고 상금도 커요. 모든 고양이가 부문 하나씩 수상하고 (최고의 그르릉, 최고의 복슬털, 최고의 성장, 용감한 구조 고양이, 베스트 드레서...) 상금을 받아요. 이기면 더 큰 대회로 올라가요.",
 "<b>なかよし55以上、毛並み50以上、けんこう60以上</b>のおとなの猫には、名札に<b>コンテスト！</b>ボタンが出ます。毛並みが良いほど順位が上がり、賞金も大きくなります。どの猫も何かの部門で受賞し（ベストゴロゴロ賞、ふわふわ毛並み賞、がんばった賞、勇気ある保護猫賞、おしゃれ賞…）、賞金がもらえます。勝つとより大きなコンテストへ進めます。"),
# 24
("מצילים מגיעים ומביאים חתולי רחוב, לפעמים אמא עם גורים.", "Des sauveteurs arrivent en voiture et déposent des chats errants, parfois une maman avec ses chatons.", "Спасатели привозят бездомных кошек, иногда маму с котятами.", "I soccorritori arrivano e lasciano gatti randagi, a volte una mamma con i gattini.", "구조대가 차를 타고 와서 길고양이를 맡겨요. 가끔은 아기들과 함께 엄마 고양이도 와요.", "保護ボランティアが車で野良猫を連れてきます。ときどき子猫づれのお母さん猫も。"),
# 25
("חברים קרובים נוגעים באף ומלקקים זה את זה. זוג שמח, קשור ולא קרוב משפחה עשוי ללדת המלטה <b>אחת</b>, ואז שניהם מקבלים ביקור אצל הווטרינר.",
 "Les amis proches se touchent le nez et se lèchent. Un couple heureux, lié et sans lien de parenté peut avoir <b>une</b> portée, puis tous deux vont chez le vétérinaire.",
 "Близкие друзья трутся носами и вылизывают друг друга. Счастливая, привязанная друг к другу и не родственная пара может принести <b>один</b> помёт, после чего оба идут к ветеринару.",
 "Gli amici stretti si toccano il naso e si leccano a vicenda. Una coppia felice, affiatata e non imparentata può avere <b>una</b> cucciolata, poi entrambi vanno dal veterinario.",
 "친한 친구끼리는 코를 맞대고 서로 핥아 줘요. 행복하고 친하며 가족이 아닌 한 쌍은 새끼를 <b>한 번</b> 낳을 수 있고, 그다음 둘 다 동물병원에 가요.",
 "なかよしの猫どうしは鼻をくっつけて、なめあいます。幸せで仲が深く、血のつながらないペアは<b>一度だけ</b>子猫を産むことがあり、そのあと二匹とも動物病院へ。"),
# 26
("גורים נשארים ליד אמא עד שהם גדלים (בערך 3 דקות).", "Les chatons restent près de leur maman jusqu'à ce qu'ils grandissent (environ 3 minutes).", "Котята держатся рядом с мамой, пока не подрастут (около 3 минут).", "I gattini stanno vicino alla mamma finché non crescono (circa 3 minuti).", "아기 고양이는 다 클 때까지 엄마 곁에 있어요 (약 3분).", "子猫は大きくなるまでお母さんのそばにいます（約3分）。"),
# 27
("חתול <b>מוכן לבית</b> אחרי שהוא מתאקלם (בערך 2½ דקות) עם אהבה 50+ ובריאות 55+. סרטים לא משנים, אבל משפחה תסרב לחתול מוזנח מאוד (טיפוח מתחת ל־30) אלא אם הוא מעריץ אנשים (אהבה 90+).",
 "Un chat est <b>prêt pour un foyer</b> après s'être installé (environ 2½ minutes) avec Amour 50+ et Santé 55+. Les rubans ne comptent pas, mais une famille refuse un chat très négligé (Toilettage sous 30) sauf s'il adore les gens (Amour 90+).",
 "Кошка <b>готова к новому дому</b>, когда освоится (около 2½ минут) и у неё Любовь 50+ и Здоровье 55+. Ленты не важны, но семья откажется от очень неухоженной кошки (Шерсть ниже 30), если только она не обожает людей (Любовь 90+).",
 "Un gatto è <b>pronto per una casa</b> dopo essersi ambientato (circa 2½ minuti) con Amore 50+ e Salute 55+. Le coccarde non contano, ma una famiglia rifiuta un gatto molto trasandato (Pelo sotto 30) a meno che non adori le persone (Amore 90+).",
 "고양이는 적응한 뒤 (약 2분 30초) 애정 50+, 건강 55+이면 <b>입양 준비 완료</b>예요. 리본은 상관없지만, 아주 지저분한 고양이 (털 손질 30 미만)는 사람을 무척 좋아하지 않는 한 (애정 90+) 가족이 거절해요.",
 "猫は慣れたあと（約2分半）、なかよし50以上・けんこう55以上で<b>里親募集中</b>になります。リボンは関係ありませんが、ひどくぼさぼさの猫（毛並み30未満）は、人が大好き（なかよし90以上）でないかぎり断られます。"),
# 28
("משפחות מגיעות ואומרות מה הן היו רוצות (חתול רגוע, חתול שובב...). הקישו על <b>בחרו חתול</b>, ואז על חתול עם בית קטן. התאמה טובה באופי הולכת הביתה; חברים הכי טובים הולכים יחד.",
 "Des familles arrivent et disent ce qu'elles aimeraient (un chat calme, un chat joueur...). Touche <b>Choisir un chat</b>, puis un chat avec une petite maison. Un bon accord de caractère part avec eux ; les meilleurs amis partent ensemble.",
 "Приезжают семьи и говорят, кого хотят (спокойного кота, игривого кота...). Нажмите <b>Выбрать кошку</b>, затем кошку с домиком. Подходящий характер — и кошка едет домой; лучшие друзья уезжают вместе.",
 "Arrivano le famiglie e dicono cosa vorrebbero (un gatto tranquillo, un gatto giocherellone...). Tocca <b>Scegli un gatto</b>, poi un gatto con la casetta. Se il carattere va bene, va a casa; i migliori amici vanno insieme.",
 "가족이 차를 타고 와서 원하는 고양이를 말해요 (차분한 고양이, 장난꾸러기 고양이...). <b>고양이 고르기</b>를 누르고, 작은 집 표시가 있는 고양이를 눌러요. 성격이 잘 맞으면 입양 가고, 단짝은 함께 가요.",
 "家族が車でやってきて、どんな猫がいいか言います（おっとりした猫、あそび好きな猫…）。<b>猫をえらぶ</b>をタップして、小さな家のマークの猫をタップ。性格が合えば新しい家へ。親友どうしはいっしょに行きます。"),
# 29
("אין כאן כסף בתמורה. גלויות מגיעות אחר כך ונתלות על לוח הגלויות ליד הבית: הקישו עליו כדי לראות את כולן. הן גם בתגים ← סופים טובים.",
 "Aucun argent n'est échangé. Des cartes postales arrivent plus tard et sont épinglées sur le panneau près de la maison : touche-le pour toutes les voir. Elles sont aussi dans Badges → Belles histoires.",
 "Деньги не переходят из рук в руки. Позже приходят открытки и прикрепляются к доске у дома: нажмите на неё, чтобы увидеть все. Они есть и в разделе Значки → Счастливые хвосты.",
 "Non girano soldi. Le cartoline arrivano dopo e vengono appese alla bacheca vicino alla casa: toccala per vederle tutte. Sono anche in Medaglie → Code felici.",
 "돈은 오가지 않아요. 나중에 엽서가 도착해서 집 옆 게시판에 붙어요: 눌러서 모두 볼 수 있어요. 배지 → 행복한 꼬리에도 있어요.",
 "お金のやりとりはありません。あとからはがきが届き、家のそばの掲示板に貼られます。タップすると全部見られます。バッジ → しあわせのしっぽにもあります。"),
# 30
("הקישו על <b>להשאיר</b> בחתול כדי שיישאר לתמיד. הקישו על × כדי לשלוח משפחה.", "Touche <b>Garder</b> sur un chat pour le garder pour toujours. Touche × pour raccompagner une famille.", "Нажмите <b>Оставить</b> на кошке, чтобы она осталась навсегда. Нажмите ×, чтобы проводить семью.", "Tocca <b>Tieni</b> su un gatto per tenerlo per sempre. Tocca × per congedare una famiglia.", "고양이의 <b>키우기</b>를 누르면 평생 함께해요. ×를 누르면 가족을 돌려보내요.", "猫の<b>飼う</b>をタップすると、ずっといっしょ。×をタップすると家族を見送ります。"),
# 31 runaways
("חתול עם אהבה נמוכה מאוד עלול לחמוק מהשער. תפסו אותו לפני הודעת ה״נעלם״ בשביל התג <b>כפות זריזות</b>, או לחצו <b>לחפש</b>, עקבו אחרי עקבות הכפות והקשיבו: היללות מתחזקות ככל שמתקרבים. הקישו עליו כדי להחזיר אותו הביתה (האהבה עולה).",
 "Un chat avec très peu d'amour peut se faufiler par le portail. Rattrape-le avant l'avis de disparition pour le badge <b>Pattes rapides</b>, ou appuie sur <b>Chercher</b>, suis les traces de pattes et écoute : les miaulements sont plus forts quand tu te rapproches. Touche-le pour le ramener (l'amour augmente).",
 "Кошка с очень низкой Любовью может ускользнуть за ворота. Поймайте её до объявления о пропаже, чтобы получить значок <b>Быстрые лапы</b>, или нажмите <b>Искать</b>, идите по следам и слушайте: мяуканье громче, когда вы ближе. Нажмите на неё, чтобы вернуть домой (Любовь растёт).",
 "Un gatto con pochissimo amore può sgattaiolare fuori dal cancello. Prendilo prima dell'avviso di scomparsa per la medaglia <b>Zampe veloci</b>, oppure premi <b>Cerca</b>, segui le impronte e ascolta: i miagolii si sentono più forti man mano che ti avvicini. Toccalo per riportarlo a casa (l'amore sale).",
 "애정이 아주 낮은 고양이는 문 밖으로 빠져나갈 수 있어요. '사라졌어요' 알림 전에 잡으면 <b>재빠른 발</b> 배지를 받고, 아니면 <b>찾으러 가기</b>를 눌러 발자국을 따라가며 들어 봐요: 가까워질수록 야옹 소리가 커져요. 눌러서 집으로 데려와요 (애정이 올라요).",
 "なかよしがとても低い猫は門から出ていくことがあります。「いない！」のお知らせの前につかまえると<b>すばやい足</b>バッジ。または<b>さがす</b>を押して足あとをたどり、耳をすませて。近づくほどニャーの声が大きくなります。タップして連れて帰りましょう（なかよしが上がります）。"),
# 32
("כוכבי המקלט (1-5) באים מבתים שנמצאו, הצלות, סרטים ושמחה. כוכבים פותחים אחו גדול יותר ושדרוגי פריטים (טירת חתולים, מזרקה, חדר שמש...).",
 "Les étoiles du refuge (1 à 5) viennent des adoptions, des sauvetages, des rubans et du bonheur. Elles débloquent des prairies plus grandes et des améliorations (château à chat, fontaine, véranda...).",
 "Звёзды приюта (1–5) дают найденные дома, спасения, ленты и счастье. Звёзды открывают луга побольше и улучшения предметов (кошачий замок, фонтанчик, зимний сад...).",
 "Le stelle del rifugio (1-5) arrivano da case trovate, salvataggi, coccarde e felicità. Le stelle sbloccano prati più grandi e miglioramenti (castello per gatti, fontanella, veranda...).",
 "보호소 별 (1~5)은 입양, 구조, 리본, 행복에서 와요. 별이 있으면 더 넓은 초원과 아이템 업그레이드 (고양이 성, 급수기, 선룸...)가 열려요.",
 "保護施設の星（1〜5）は、里親決定・保護・リボン・幸せで増えます。星で広い草原やアイテムのアップグレード（ねこのお城、給水器、サンルーム…）が解放されます。"),
# 33
("ב־5 כוכבים המקלט ממשיך לגדול: אגפים חדשים עם בריכות נפתחים ככל שמוצאים בתים ליותר חתולים (3, 6, 10, 16 בתים).",
 "À 5 étoiles, le refuge continue de grandir : de nouvelles ailes avec des étangs s'ouvrent à mesure que tu trouves des foyers (3, 6, 10, 16 adoptions).",
 "На 5 звёздах приют продолжает расти: новые крылья с прудами открываются по мере того, как вы находите кошкам дома (3, 6, 10, 16 домов).",
 "A 5 stelle il rifugio continua a crescere: nuove ali con laghetti si aprono man mano che trovi casa a più gatti (3, 6, 10, 16 adozioni).",
 "별 5개가 되면 보호소가 계속 커져요: 입양을 더 보낼수록 연못이 있는 새 별관이 열려요 (입양 3, 6, 10, 16번).",
 "星5つになると施設はさらに広がります。里親が見つかるほど、池のある新しい区画が開きます（里親3、6、10、16件）。"),
# 34
("לתגים יש ארד, כסף וזהב, והם משלמים ‎$10 / ‎$25 / ‎$60. תגי זהב פותחים קולרים מיוחדים (קשת, כוכבים, פריחה). שלושה יעדים קטנים בכל ביקור משלמים ‎$15 כל אחד (תגים ← יעדים).",
 "Les badges ont trois niveaux, bronze, argent et or, et rapportent 10 $ / 25 $ / 60 $. Les badges d'or débloquent des colliers spéciaux (arc-en-ciel, étoilé, fleuri). Trois petits objectifs par visite rapportent 15 $ chacun (Badges → Objectifs).",
 "У значков есть бронза, серебро и золото, они приносят $10 / $25 / $60. Золотые значки открывают особые ошейники (радужный, звёздный, цветочный). Три маленькие цели за визит приносят по $15 (Значки → Цели).",
 "Le medaglie hanno bronzo, argento e oro, e pagano $10 / $25 / $60. Le medaglie d'oro sbloccano collari speciali (arcobaleno, stellato, fiorito). Tre piccoli obiettivi per visita pagano $15 l'uno (Medaglie → Obiettivi).",
 "배지는 동, 은, 금이 있고 $10 / $25 / $60을 줘요. 금 배지로 특별한 목걸이 (무지개, 별빛, 꽃)가 열려요. 방문마다 작은 목표 세 개가 각각 $15를 줘요 (배지 → 목표).",
 "バッジには銅・銀・金があり、$10 / $25 / $60 もらえます。金バッジで特別な首輪（にじ、星空、花）が解放されます。毎回3つの小さな目標がそれぞれ $15（バッジ → 目標）。"),
# 35
("קולרים ומזון פרימיום נמצאים בחנות.", "Les colliers et la nourriture premium sont à la boutique.", "Ошейники и премиум-корм есть в магазине.", "Collari e cibo premium sono nel negozio.", "목걸이와 프리미엄 사료는 상점에 있어요.", "首輪とプレミアムフードはショップにあります。"),
# 36
("ההתקדמות נשמרת אוטומטית במכשיר הזה.", "La progression est sauvegardée automatiquement sur cet appareil.", "Прогресс сохраняется автоматически на этом устройстве.", "I progressi si salvano da soli su questo dispositivo.", "진행 상황은 이 기기에 자동으로 저장돼요.", "進みぐあいはこの端末に自動で保存されます。"),
# 37
("גררו את הדשא כדי לזוז; צביטה או גלגלת העכבר לזום; גרירה בכפתור ימני לסיבוב (מחשב).", "Fais glisser l'herbe pour te déplacer ; pince ou molette pour zoomer ; clic droit glissé pour tourner (ordinateur).", "Тяните траву, чтобы перемещаться; щипок или колесо мыши — масштаб; правая кнопка и перетаскивание — поворот (компьютер).", "Trascina l'erba per muoverti; pizzica o usa la rotellina per lo zoom; trascina col tasto destro per ruotare (computer).", "잔디를 끌어서 이동해요; 두 손가락이나 마우스 휠로 확대; 오른쪽 버튼으로 끌어서 회전 (PC).", "草をドラッグして移動。ピンチかマウスホイールでズーム。右ドラッグで回転（パソコン）。"),
# 38
("הקישו על מונה החתולים (למעלה בצד) כדי לקפוץ בין חתולים.", "Touche le compteur de chats (en haut à gauche) pour passer d'un chat à l'autre.", "Нажмите на счётчик кошек (вверху слева), чтобы переходить между ними.", "Tocca il contatore dei gatti (in alto a sinistra) per passare da un gatto all'altro.", "고양이 수 (왼쪽 위)를 누르면 고양이 사이를 오가요.", "猫の数（左上）をタップすると猫から猫へ移動します。"),
# 39
("במחשב, המקשים 1-4 בוחרים כלים.", "Les touches 1 à 4 choisissent les outils sur ordinateur.", "Клавиши 1–4 выбирают инструменты на компьютере.", "I tasti 1-4 scelgono gli strumenti sul computer.", "PC에서는 1~4 키로 도구를 골라요.", "パソコンでは1〜4キーで道具をえらべます。"),
# 40
("כפתור הירח מדליק או מכבה את מחזור היום והלילה. בלילה החתולים מנומנמים וגחליליות יוצאות.", "Le bouton lune active ou coupe le cycle jour et nuit. La nuit, les chats ont sommeil et les lucioles sortent.", "Кнопка с луной включает и выключает смену дня и ночи. Ночью кошки сонные и появляются светлячки.", "Il pulsante della luna attiva o spegne il ciclo giorno e notte. Di notte i gatti hanno sonno ed escono le lucciole.", "달 버튼으로 낮과 밤 순환을 켜고 꺼요. 밤에는 고양이들이 졸려 하고 반딧불이가 나와요.", "月のボタンで昼と夜の切りかえをオン・オフ。夜は猫が眠くなり、ホタルが出てきます。"),
]
