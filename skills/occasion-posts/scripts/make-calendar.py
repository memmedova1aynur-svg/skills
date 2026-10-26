#!/usr/bin/env python3
"""Source of truth for assets/calendar.json. Edit here, then run: python3 scripts/make-calendar.py

Fixed dates are "MM-DD". Movable days (Novruz, the çərşənbələr, Ramazan and Qurban bayramı,
Mother's/Father's Day, Black Friday) carry "date": null plus a rule and an approximate month;
their exact dates are announced or computed each year and must be checked, never guessed.
"""
import json, os

def d(id, az, en, date, tone, groups, motifs, angles, avoid=(), niches=(), approx=None, rule=None,
      palette=None, prompt=None, verify=False, note=None):
    e = {'id': id, 'name': {'az': az, 'en': en}, 'date': date, 'tone': tone, 'groups': list(groups),
         'motifs': list(motifs), 'angles': list(angles)}
    if avoid: e['avoid'] = list(avoid)
    if niches: e['niches'] = list(niches)
    if approx: e['approx_month'] = approx
    if rule: e['rule'] = rule
    if palette: e['palette'] = palette
    if prompt: e['ai_prompt'] = prompt
    if verify or date is None: e['verify'] = True
    if note: e['note'] = note
    return e

AZ, KID, INT = 'az-national', 'child-development', 'international'
NO_SALES = ['endirim, satış, reklam', 'yumor, meme, emoji', 'parlaq rənglər, konfetti', '"yadda saxla" CTA-sı',
            'faciənin realist AI şəkli, qurbanların təsviri']

PALETTES = {
    'novruz':   {'bg': '#F6F3EA', 'surface': '#FFFFFF', 'text': '#1D2B1F', 'muted': '#56614F', 'accent': '#2F8A3E'},
    'national': {'bg': '#F5F7FA', 'surface': '#FFFFFF', 'text': '#13202B', 'muted': '#566270', 'accent': '#00A0C8'},
    'yeni-il':  {'bg': '#0F2A22', 'surface': '#163A2F', 'text': '#F4EFE3', 'muted': '#BFC8BC', 'accent': '#E3B04B'},
    'children': {'bg': '#FFF8EC', 'surface': '#FFFFFF', 'text': '#1F2240', 'muted': '#5A5E7A', 'accent': '#F25C54'},
    'autism':   {'bg': '#F3F6FB', 'surface': '#FFFFFF', 'text': '#1B2340', 'muted': '#57607A', 'accent': '#7A4FD1'},
    'spring':   {'bg': '#FFF4F6', 'surface': '#FFFFFF', 'text': '#2A1820', 'muted': '#6E5560', 'accent': '#D6336C'},
    'religious':{'bg': '#F4F1E8', 'surface': '#FFFFFF', 'text': '#1C2A24', 'muted': '#5A6560', 'accent': '#1F6F54'},
    'knowledge':{'bg': '#F3F6FF', 'surface': '#FFFFFF', 'text': '#141C33', 'muted': '#56607A', 'accent': '#2F6BFF'},
}

CAL = [
    # ---------------- Azərbaycan: bayramlar ----------------
    d('yeni-il', 'Yeni il', "New Year's Day", '01-01', 'celebration', [AZ, INT], ['yolka', 'qar', 'konfetti'],
      ['ilin xülasəsi: 5 ən yaxşı an', 'gələn il üçün 3 məqsəd', 'müştərilərə təşəkkür'], palette='yeni-il',
      prompt='festive New Year still life, decorated fir branch, warm string lights, gold and deep green, soft bokeh, no text'),
    d('qadinlar-gunu', 'Beynəlxalq Qadınlar Günü', "International Women's Day", '03-08', 'celebration', [AZ, INT],
      ['lale', 'qerenfil'], ['komandadakı və ya müştərilərdəki qadınların hekayəsi', 'qadın sahibkarlara təşəkkür'],
      avoid=['"qadın = mətbəx/gözəllik" stereotipləri', 'yalnız endirim postu'], palette='spring',
      prompt='bouquet of red tulips on a soft pink background, natural light, minimal, no text'),
    d('novruz', 'Novruz bayramı', 'Novruz', None, 'celebration', [AZ, INT], ['semeni', 'sekerbura', 'tonqal', 'nar'],
      ['xonçanın mənası: səməni, şəkərbura, paxlava, qoğal', 'uşaqla Novruz: səməni əkmək', 'bayram təbriki'],
      approx='03', rule='Yaz bərabərliyi, adətən 20-21 mart; rəsmi bayram günləri hər il Nazirlər Kabineti tərəfindən elan olunur.',
      avoid=['İran "heft-sin" süfrəsi (7 "s" əşyası) Azərbaycan xonçası kimi', 'Qərb Pasxa estetikası (dovşan, pastel yumurta səbəti)'],
      palette='novruz',
      prompt='Azerbaijani Novruz khoncha: copper tray with green semeni tied with a red ribbon, shekerbura, pakhlava, gogal, '
             'dyed eggs, candles, warm daylight, top-down, no text. NOT Persian haft-sin, no goldfish bowl'),
    d('su-cersenbe', 'Su çərşənbəsi', 'Water Tuesday', None, 'celebration', [AZ], ['semeni'],
      ['çərşənbələrin ardıcıllığı: Su, Od, Yel, Torpaq', 'suyun təmizlik simvolu'], approx='02-03',
      rule='Novruzdan əvvəlki dörd çərşənbə axşamının birincisi.', palette='novruz'),
    d('od-cersenbe', 'Od çərşənbəsi', 'Fire Tuesday', None, 'celebration', [AZ], ['tonqal'],
      ['tonqal üstündən tullanma ənənəsi və təhlükəsizlik'], approx='03', rule='Novruzdan əvvəlki ikinci çərşənbə axşamı.', palette='novruz'),
    d('yel-cersenbe', 'Yel çərşənbəsi', 'Wind Tuesday', None, 'celebration', [AZ], ['semeni'],
      ['təbiətin oyanışı'], approx='03', rule='Novruzdan əvvəlki üçüncü çərşənbə axşamı.', palette='novruz'),
    d('torpaq-cersenbe', 'Torpaq çərşənbəsi', 'Earth Tuesday', None, 'celebration', [AZ], ['semeni', 'nar'],
      ['torpağın oyanması, bayrama son hazırlıq'], approx='03', rule='Novruzdan əvvəlki son çərşənbə axşamı.', palette='novruz'),
    d('ramazan-bayrami', 'Ramazan bayramı', 'Eid al-Fitr', None, 'religious', [AZ], ['hilal'],
      ['sakit, səmimi təbrik', 'ailə və paylaşma'], approx='hicri təqvim', palette='religious',
      rule='Hicri təqvimlə hər il ~11 gün tez gəlir; tarixi Qafqaz Müsəlmanları İdarəsi elan edir.',
      avoid=['satış kampaniyası təbriki əvəz etməsin', 'yumor', 'dini simvolların dekorativ istifadəsi']),
    d('qurban-bayrami', 'Qurban bayramı', 'Eid al-Adha', None, 'religious', [AZ], ['hilal'],
      ['sakit, səmimi təbrik', 'paylaşma və mərhəmət'], approx='hicri təqvim', palette='religious',
      rule='Hicri təqvimlə hər il ~11 gün tez gəlir; tarixi Qafqaz Müsəlmanları İdarəsi elan edir.',
      avoid=['heyvan kəsimi şəkilləri', 'satış', 'yumor']),
    d('qelebe-gunu', 'Faşizm üzərində qələbə günü', 'Victory over Fascism Day', '05-09', 'celebration', [AZ], ['qerenfil', 'ulduz'],
      ['ehtiram, nəsillərin yaddaşı'], avoid=['satış']),
    d('musteqillik-gunu', 'Müstəqillik günü', 'Independence Day', '05-28', 'celebration', [AZ], ['bayraq', 'ulduz'],
      ['1918 Xalq Cümhuriyyəti', 'təbrik'], palette='national'),
    d('qurtulus-gunu', 'Milli Qurtuluş günü', 'National Salvation Day', '06-15', 'celebration', [AZ], ['bayraq'], ['təbrik'], palette='national'),
    d('silahli-quvveler-gunu', 'Silahlı Qüvvələr günü', 'Armed Forces Day', '06-26', 'celebration', [AZ], ['bayraq', 'ulduz'],
      ['əsgərlərə təşəkkür'], palette='national'),
    d('musteqilliyin-berpasi', 'Müstəqilliyin Bərpası günü', 'Independence Restoration Day', '10-18', 'celebration', [AZ],
      ['bayraq'], ['təbrik'], palette='national'),
    d('zefer-gunu', 'Zəfər günü', 'Victory Day', '11-08', 'celebration', [AZ], ['bayraq', 'ulduz'],
      ['qürur və təşəkkür', 'şəhidləri anmaq'], palette='national', avoid=['endirim kodu "ZEFER"', 'yumor']),
    d('bayraq-gunu', 'Dövlət Bayrağı günü', 'National Flag Day', '11-09', 'celebration', [AZ], ['bayraq'],
      ['bayrağın rənglərinin mənası: mavi, qırmızı, yaşıl'], palette='national',
      avoid=['bayrağın təhrif olunmuş, yanlış nisbətli və ya üstündə loqo olan təsviri']),
    d('konstitusiya-gunu', 'Konstitusiya günü', 'Constitution Day', '11-12', 'celebration', [AZ], ['bayraq', 'kitab'], ['təbrik'], palette='national'),
    d('dircelis-gunu', 'Milli Dirçəliş günü', 'National Revival Day', '11-17', 'celebration', [AZ], ['bayraq'], ['təbrik'], palette='national'),
    d('hemreylik-gunu', 'Dünya azərbaycanlılarının həmrəyliyi günü', 'World Azerbaijanis Solidarity Day', '12-31', 'celebration', [AZ],
      ['bayraq', 'konfetti'], ['dünyadakı azərbaycanlılara təbrik', 'Yeni il ilə birgə təbrik'], palette='national'),
    d('bilik-gunu', 'Bilik günü', 'Knowledge Day (first school day)', '09-15', 'celebration', [AZ, KID], ['kitab', 'kublar'],
      ['məktəbə hazırlıq siyahısı', 'birinci sinfə adaptasiya', 'valideyn üçün 5 məsləhət'], palette='knowledge',
      niches=['education', 'child-development'], prompt='school backpack, notebooks and colored pencils on a light desk, morning light, no text, no faces'),

    # ---------------- Azərbaycan: anma günləri ----------------
    d('20-yanvar', 'Ümumxalq Hüzn Günü (20 Yanvar)', 'National Day of Mourning (Black January)', '01-20', 'remembrance', [AZ],
      ['qerenfil', 'sam'], ['şəhidlərin xatirəsinə ehtiram', 'yalnız anma mətni'], avoid=NO_SALES,
      note='Gün ərzində planlaşdırılmış reklam və əyləncəli postları dayandır.'),
    d('xocali', 'Xocalı soyqırımı günü', 'Khojaly genocide remembrance', '02-26', 'remembrance', [AZ],
      ['qerenfil', 'sam'], ['qurbanların xatirəsi', 'yalnız anma mətni'], avoid=NO_SALES,
      note='Rəqəm və tarixi faktları yalnız rəsmi mənbədən götür.'),
    d('31-mart', 'Azərbaycanlıların soyqırımı günü', 'Day of the Genocide of Azerbaijanis', '03-31', 'remembrance', [AZ],
      ['qerenfil', 'sam'], ['anma mətni'], avoid=NO_SALES,
      ),
    d('anim-gunu', 'Anım günü', 'Remembrance Day', '09-27', 'remembrance', [AZ],
      ['qerenfil', 'sam', 'bayraq'], ['şəhidlərin xatirəsi', 'yalnız anma mətni'], avoid=NO_SALES,
      note='27 sentyabr həm də Ümumdünya Turizm Günüdür; Azərbaycanda turizm postlarını bu günə qoyma.'),

    # ---------------- Uşaq inkişafı və sağlamlıq ----------------
    d('braille-gunu', 'Ümumdünya Brayl günü', 'World Braille Day', '01-04', 'awareness', [KID, INT], ['kitab'],
      ['görmə məhdudiyyətli uşaqlar üçün oxu'], niches=['education', 'inclusion']),
    d('usaq-xercengi', 'Beynəlxalq Uşaq Xərçəngi Günü', 'International Childhood Cancer Day', '02-15', 'awareness', [KID, INT], ['urek'],
      ['ailələrə dəstək yolları'], avoid=['xəstə uşaqların icazəsiz fotosu', 'qorxu mesajı']),
    d('ana-dili-gunu', 'Beynəlxalq Ana Dili Günü', 'International Mother Language Day', '02-21', 'awareness', [KID, INT], ['kitab', 'kublar'],
      ['uşaqla ana dilində oxumaq', 'ikidilli uşaqlar: mif vs fakt'], niches=['education', 'child-development', 'speech']),
    d('esitme-gunu', 'Ümumdünya Eşitmə Günü', 'World Hearing Day', '03-03', 'awareness', [KID, INT], ['urek'],
      ['uşaqda eşitmə problemini necə tanımaq'], niches=['child-development', 'speech', 'health']),
    d('logopediya-gunu', 'Avropa Loqopediya Günü', 'European Day of Speech and Language Therapy', '03-06', 'awareness', [KID, INT],
      ['kublar', 'kitab'], ['loqoped nə edir', 'nitq gecikməsi: nə vaxt narahat olmaq'], niches=['speech', 'child-development'],
      verify=True, note='CPLOL tərəfindən qeyd olunur; mövzunu hər il yoxla.'),
    d('daun-sindromu-gunu', 'Ümumdünya Daun Sindromu Günü', 'World Down Syndrome Day', '03-21', 'awareness', [KID, INT],
      ['urek', 'kublar'], ['fərqli corablar (#LotsOfSocks) kampaniyası', 'inklüziv bağça və məktəb'],
      avoid=['"xəstəlik" dili', 'yazıq/qəhrəman çərçivəsi'], niches=['child-development', 'inclusion'],
      note='Novruzla eyni günə düşə bilər; ikisini ayrı postlarda ver.'),
    d('autizm-gunu', 'Ümumdünya Autizm Məlumatlandırma Günü', 'World Autism Awareness Day', '04-02', 'awareness', [KID, INT],
      ['sonsuzluq', 'urek'], ['autizm haqqında 5 mif', 'sensor həssaslıq: evdə nə etmək', 'qəbul, "müalicə" yox'],
      avoid=['pazl (puzzle) simvolu: autist icmanın çoxu onu qəbul etmir', '"autizmdən əziyyət çəkir" dili',
             '"sağalmaq", "müalicə" vədi', 'yalnız mavi rəng ("Light It Up Blue" mübahisəlidir)'],
      palette='autism', niches=['child-development', 'inclusion', 'speech', 'psychology'],
      prompt='child and parent hands building with colorful wooden blocks on a calm light table, soft natural light, '
             'gentle rainbow accents, no puzzle pieces, no text, faces not shown',
      note='Aprel həm də Autizm Qəbulu Ayıdır: ay boyu seriya etmək olar.'),
    d('usaq-kitab-gunu', 'Beynəlxalq Uşaq Kitabı Günü', "International Children's Book Day", '04-02', 'awareness', [KID, INT], ['kitab'],
      ['yaşa görə 5 kitab', 'uşağa necə oxumaq'], niches=['education', 'child-development']),
    d('saglamliq-gunu', 'Ümumdünya Sağlamlıq Günü', 'World Health Day', '04-07', 'awareness', [INT], ['urek'],
      ['ilin ÜST mövzusu'], niches=['health', 'fitness', 'dental'], verify=True, note='Mövzu hər il ÜST tərəfindən elan olunur.'),
    d('kitab-gunu', 'Ümumdünya Kitab və Müəllif Hüquqları Günü', 'World Book Day', '04-23', 'awareness', [KID, INT], ['kitab'],
      ['oxu vərdişi', 'tövsiyə siyahısı'], niches=['education']),
    d('aile-gunu', 'Beynəlxalq Ailə Günü', 'International Day of Families', '05-15', 'awareness', [KID, INT], ['urek', 'gunes'],
      ['ailə ilə 10 dəqiqəlik oyunlar', 'ekran vaxtı vs ailə vaxtı'], niches=['child-development', 'psychology']),
    d('usaqlar-gunu', 'Uşaqların Beynəlxalq Müdafiəsi Günü', "International Children's Day", '06-01', 'celebration', [AZ, KID, INT],
      ['sarlar', 'kublar', 'gunes', 'konfetti'], ['uşaq hüquqları sadə dillə', 'evdə inkişaf oyunları', 'uşaqlara təbrik'],
      palette='children', niches=['child-development', 'education'],
      prompt='joyful flat illustration of colorful balloons, kites and building blocks in a sunny park, bright and soft, no text, no faces',
      avoid=['uşaq fotolarını valideyn icazəsi olmadan istifadə']),
    d('ana-suddu-hefte', 'Ümumdünya Ana Südü Həftəsi', 'World Breastfeeding Week', '08-01', 'awareness', [KID, INT], ['urek'],
      ['mütəxəssis məsləhəti', 'mif vs fakt'], niches=['health', 'child-development'], note='1-7 avqust.',
      avoid=['süni qidalandıran anaları utandırmaq']),
    d('isare-dili-gunu', 'Beynəlxalq İşarə Dilləri Günü', 'International Day of Sign Languages', '09-23', 'awareness', [KID, INT], ['urek'],
      ['5 sadə jest uşaqla ünsiyyət üçün'], niches=['inclusion', 'speech']),
    d('sdi-gunu', 'Ümumdünya Serebral İflic Günü', 'World Cerebral Palsy Day', '10-06', 'awareness', [KID, INT], ['urek'],
      ['inklüzivlik', 'ailələrə dəstək'], niches=['child-development', 'inclusion', 'health']),
    d('psixi-saglamliq-gunu', 'Ümumdünya Psixi Sağlamlıq Günü', 'World Mental Health Day', '10-10', 'awareness', [KID, INT], ['urek'],
      ['valideyn tükənməsi', 'uşaqda narahatlıq əlamətləri'], niches=['psychology', 'health', 'child-development']),
    d('kekeleme-gunu', 'Beynəlxalq Kəkələmə Məlumatlandırma Günü', 'International Stuttering Awareness Day', '10-22', 'awareness', [KID, INT],
      ['kublar'], ['kəkələyən uşaqla necə danışmaq'], niches=['speech', 'child-development'],
      avoid=['kəkələməni lağa qoyan meme']),
    d('xeyirxahliq-gunu', 'Ümumdünya Xeyirxahlıq Günü', 'World Kindness Day', '11-13', 'awareness', [KID, INT], ['urek'],
      ['uşaqlara empatiyanı öyrətmək'], niches=['child-development', 'education']),
    d('vaxtindan-evvel-gunu', 'Ümumdünya Vaxtından Əvvəl Doğulmuş Körpələr Günü', 'World Prematurity Day', '11-17', 'awareness', [KID, INT],
      ['urek'], ['erkən doğulmuş körpənin inkişaf qrafiki'], niches=['health', 'child-development'], palette='autism'),
    d('dunya-usaq-gunu', 'Ümumdünya Uşaq Günü', "World Children's Day", '11-20', 'awareness', [KID, INT], ['kublar', 'gunes'],
      ['BMT Uşaq Hüquqları Konvensiyası'], niches=['child-development', 'education']),
    d('elillik-gunu', 'Beynəlxalq Əlilliyi olan Şəxslər Günü', 'International Day of Persons with Disabilities', '12-03', 'awareness', [KID, INT],
      ['urek'], ['əlçatanlıq', 'inklüziv dil'], avoid=['"şikəst", "xəstə" dili', 'yazıq çərçivəsi'], niches=['inclusion']),

    # ---------------- Ümumi beynəlxalq ----------------
    d('sevgililer-gunu', 'Sevgililər günü', "Valentine's Day", '02-14', 'celebration', [INT], ['urek'],
      ['özünə qayğı', 'cütlüklər üçün təklif'], palette='spring'),
    d('xosbextlik-gunu', 'Beynəlxalq Xoşbəxtlik Günü', 'International Day of Happiness', '03-20', 'awareness', [INT], ['gunes'],
      ['kiçik xoşbəxtliklər siyahısı']),
    d('yer-kuresi-gunu', 'Yer Kürəsi Günü', 'Earth Day', '04-22', 'awareness', [INT], ['gunes', 'semeni'],
      ['uşaqla ekoloji vərdişlər'], avoid=['real addım olmadan "yaşıl" iddia (greenwashing)']),
    d('emek-gunu', 'Beynəlxalq Əmək Günü', "International Workers' Day", '05-01', 'celebration', [INT], ['ulduz'], ['komandaya təşəkkür']),
    d('analar-gunu', 'Analar günü', "Mother's Day", None, 'celebration', [INT], ['lale', 'urek'],
      ['analara təşəkkür'], approx='05', rule='Bir çox ölkədə mayın ikinci bazarı. Azərbaycanda ənənəvi olaraq 8 Mart daha güclüdür.',
      palette='spring', avoid=['övladını itirmiş və ya ana olmaq istəyən auditoriyanı unutmaq']),
    d('atalar-gunu', 'Atalar günü', "Father's Day", None, 'celebration', [INT], ['urek'], ['ata-uşaq oyunları'], approx='06',
      rule='Bir çox ölkədə iyunun üçüncü bazarı.'),
    d('muellimler-gunu', 'Müəllimlər günü', "Teachers' Day", '10-05', 'celebration', [INT, KID], ['kitab', 'lale'],
      ['sevimli müəllim hekayəsi', 'müəllimlərə təşəkkür'], niches=['education'], verify=True,
      note='5 oktyabr Ümumdünya Müəllimlər Günüdür; yerli qeyd tarixini yoxla.'),
    d('qara-cume', 'Qara Cümə', 'Black Friday', None, 'celebration', [INT], ['konfetti'], ['aydın endirim posteri'],
      approx='11', rule='Noyabrın dördüncü cüməsi.'),

    # ---------------- Niş günləri ----------------
    d('stomatoloq-gunu', 'Beynəlxalq Stomatoloq Günü', "International Dentist's Day", '03-06', 'celebration', [INT], ['urek'],
      ['həkimlərə təşəkkür'], niches=['dental'], verify=True),
    d('agiz-saglamligi-gunu', 'Ümumdünya Ağız Sağlamlığı Günü', 'World Oral Health Day', '03-20', 'awareness', [INT], ['gunes'],
      ['uşaqlarda diş təmizliyi'], niches=['dental']),
    d('sokolad-gunu', 'Ümumdünya Şokolad Günü', 'World Chocolate Day', '07-07', 'celebration', [INT], ['urek'], ['menyu təklifi'], niches=['cafe']),
    d('qehve-gunu', 'Beynəlxalq Qəhvə Günü', 'International Coffee Day', '10-01', 'celebration', [INT], ['urek'],
      ['günün qəhvəsi', 'qonağa pulsuz qəhvə'], niches=['cafe']),
    d('qida-gunu', 'Ümumdünya Qida Günü', 'World Food Day', '10-16', 'awareness', [INT], ['nar'], ['israfı azaltmaq'], niches=['cafe', 'health']),
    d('turizm-gunu', 'Ümumdünya Turizm Günü', 'World Tourism Day', '09-27', 'celebration', [INT], ['gunes'], ['səyahət təklifi'],
      niches=['travel'], note='Azərbaycanda Anım günü ilə üst-üstə düşür: bu gün turizm postu paylaşma, bir gün sonraya keçir.'),
    d('idman-gunu', 'Beynəlxalq İdman Günü', 'International Day of Sport for Development and Peace', '04-06', 'awareness', [INT], ['gunes'],
      ['uşaq üçün hərəkət oyunları'], niches=['fitness', 'child-development']),
]

# Who declares each day, and whether it is official. The authority is named; the exact link is
# checked by a person before first use (source_verified stays false until then).
AUTH = {
    'autizm-gunu': ('BMT (A/RES/62/139)', 'official'), 'daun-sindromu-gunu': ('BMT (A/RES/66/149)', 'official'),
    'dunya-usaq-gunu': ('BMT', 'official'), 'aile-gunu': ('BMT', 'official'), 'elillik-gunu': ('BMT', 'official'),
    'braille-gunu': ('BMT', 'official'), 'isare-dili-gunu': ('BMT', 'official'), 'xosbextlik-gunu': ('BMT', 'official'),
    'saglamliq-gunu': ('ÜST', 'official'), 'esitme-gunu': ('ÜST', 'official'), 'psixi-saglamliq-gunu': ('ÜPSF / ÜST', 'official'),
    'ana-dili-gunu': ('UNESCO', 'official'), 'kitab-gunu': ('UNESCO', 'official'), 'muellimler-gunu': ('UNESCO', 'official'),
    'qida-gunu': ('FAO', 'official'), 'turizm-gunu': ('BMT Turizm', 'official'), 'qehve-gunu': ('Beynəlxalq Qəhvə Təşkilatı', 'official'),
    'usaqlar-gunu': ('Beynəlxalq; Azərbaycanda qeyd olunur', 'official'),
    'ana-suddu-hefte': ('WABA / ÜST', 'official'), 'idman-gunu': ('BMT', 'official'),
    'agiz-saglamligi-gunu': ('FDI Dünya Stomatoloji Federasiyası', 'official'),
    'logopediya-gunu': ('CPLOL', 'unofficial'), 'kekeleme-gunu': ('Beynəlxalq Kəkələmə Assosiasiyası', 'unofficial'),
    'sdi-gunu': ('World CP Day təşəbbüsü', 'unofficial'), 'vaxtindan-evvel-gunu': ('EFCNI', 'unofficial'),
    'usaq-xercengi': ('Childhood Cancer International', 'unofficial'), 'usaq-kitab-gunu': ('IBBY', 'unofficial'),
    'xeyirxahliq-gunu': ('World Kindness Movement', 'unofficial'), 'yer-kuresi-gunu': ('Earth Day Network', 'unofficial'),
}
FORMATS = {
    'celebration': ['təbrik postu', 'karusel (praktik bucaq)', 'story'],
    'awareness': ['karusel (izah / mif–reallıq)', 'story (sual, resurs)'],
    'religious': ['təbrik postu', 'sakit story'],
    'remembrance': ['anma postu', 'sakit story (satış yox)'],
}
for e in CAL:
    g = e['groups']
    e['scope'] = 'Azərbaycan' if g == [AZ] else 'Azərbaycan + beynəlxalq' if AZ in g else 'beynəlxalq'
    if e['id'] in AUTH:
        e['source'], e['status'] = AUTH[e['id']]
    elif AZ in g and e['tone'] != 'religious':
        e['source'], e['status'] = 'AR qanunvericiliyi (Əmək Məcəlləsi, md. 105 və müvafiq fərmanlar)', 'official'
    elif e['tone'] == 'religious':
        e['source'], e['status'] = 'Qafqaz Müsəlmanları İdarəsi (tarix hər il elan olunur)', 'official'
    else:
        e['source'], e['status'] = 'qeyri-rəsmi / kommersiya günü', 'unofficial'
    e['source_verified'] = False
    e['formats'] = FORMATS[e['tone']]

out = {'palettes': PALETTES, 'occasions': CAL}
p = os.path.join(os.path.dirname(__file__), '..', 'assets', 'calendar.json')
json.dump(out, open(p, 'w'), indent=1, ensure_ascii=False)
print(f'{len(CAL)} occasions, {len(PALETTES)} palettes -> {os.path.relpath(p)}')
