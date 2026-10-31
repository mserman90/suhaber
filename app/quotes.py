"""
app/quotes.py
Su yönetimi, tarımsal üretim ve hayvancılık konularında iki dilli (TR/EN) günün öğüt sözleri.
"""

from datetime import datetime, timezone
from typing import Dict, Any, List

WATER_MANAGEMENT_QUOTES: List[Dict[str, str]] = [
    {
        "quote": "Tarımsal sulamada yapılacak her yüzde 10'luk verimlilik artışı, metropollerin yıllık içme suyu ihtiyacını karşılayabilecek ölçektedir. Akıllı sensörler ve damla sulama bir tercih değil, milli bir zorunluluktur.",
        "quote_en": 'Every 10 percent increase in efficiency in agricultural irrigation is sufficient to meet the annual drinking water needs of metropolises. Smart sensors and drip irrigation are not a choice, but a national necessity.',
        "author": 'Su Verimliliği ve Tarımsal Sulama Rehberi',
        "author_en": 'Water Efficiency and Agricultural Irrigation Guide',
        "category": 'Tarımsal Sulama',
        "category_en": 'Agricultural Irrigation'
    },
    {
        "quote": 'Suyu atalarımızdan miras almadık, gelecek nesillerden ödünç aldık. Havzalarımızdaki her bir damlayı yarının emaneti bilinciyle yönetmek zorundayız.',
        "quote_en": 'We did not inherit water from our ancestors, we borrowed it from future generations. We have to manage every drop in our basins with the awareness that they are the trust of tomorrow.',
        "author": 'Sürdürülebilir Havza Yönetimi İlkesi',
        "author_en": 'Sustainable Basin Management Principle',
        "category": 'Gelecek & Koruma',
        "category_en": 'Future & Protection'
    },
    {
        "quote": 'Yeraltı suları sınırsız bir kaynak değil, kuraklık yıllarının stratejik güvenlik sigortasıdır. Akiferlerimizi aşırı çekimden korumak gıda güvenliğimizin teminatıdır.',
        "quote_en": 'Groundwater is not an unlimited resource, but a strategic security insurance during drought years. Protecting our aquifers from overdraft is the guarantee of our food security.',
        "author": 'Hidrojeoloji ve Yeraltı Suları Bilinci',
        "author_en": 'Hydrogeology and Groundwater Awareness',
        "category": 'Yeraltı Suları',
        "category_en": 'Groundwater'
    },
    {
        "quote": 'Bir damla suyun yönetimi, bir milletin geleceğinin yönetimidir. Kuraklık kapıyı çalmadan önce alınan tedbirler, kriz anındaki çaresiz çabalardan bin kat daha kıymetlidir.',
        "quote_en": 'The management of a drop of water is the management of the future of a nation. The measures taken before drought knocks on the door are a thousand times more valuable than desperate efforts in times of crisis.',
        "author": 'Entegre Su Politikaları Masası',
        "author_en": 'Integrated Water Policies Desk',
        "category": 'Stratejik Yönetim',
        "category_en": 'Strategic Management'
    },
    {
        "quote": 'Vahşi sulama sadece suyu değil, toprağın en verimli organik katmanını ve mineral zenginliğini de alıp götürür. Toprağı korumak, suyu damla damla vermekten geçer.',
        "quote_en": 'Wild irrigation takes away not only water, but also the most fertile organic layer and mineral richness of the soil. Protecting the soil means providing water drop by drop.',
        "author": 'Toprak ve Su Koruma Öğüdü',
        "author_en": 'Soil and Water Conservation Advice',
        "category": 'Tarımsal Sulama',
        "category_en": 'Agricultural Irrigation'
    },
    {
        "quote": 'Arıtılmış atık suların tarımsal sulama ve sanayide yeniden kullanımı, su kıtlığı çeken havzalarda can simididir. Döngüsel su ekonomisi geleceğin anahtarıdır.',
        "quote_en": 'Reuse of treated wastewater in agricultural irrigation and industry is a lifeline in water-scarce basins. The circular water economy is the key to the future.',
        "author": 'Döngüsel Su Ekonomisi Raporu',
        "author_en": 'Circular Water Economy Report',
        "category": 'Geri Kazanım',
        "category_en": 'Recovery'
    },
    {
        "quote": 'Gökyüzünden düşen her yağmur damlasını betonla denize akıtmak yerine; yağmur hasadı, sünger şehirler ve taşkın göletleriyle toprakla buluşturmalıyız.',
        "quote_en": 'Instead of pouring every drop of rain falling from the sky into the sea with concrete; We must bring it together with the soil through rain harvesting, sponge cities and flood ponds.',
        "author": 'Kentsel Su ve İklim Direnci İlkeleri',
        "author_en": 'Urban Water and Climate Resilience Principles',
        "category": 'Yağmur Hasadı',
        "category_en": 'Rain Harvest'
    },
    {
        "quote": 'Su ayak izinizi küçültmek, musluğu kısmaktan fazlasıdır; ne tükettiğimizin, ne ektiğimizin ve nasıl ürettiğimizin farkında olmakla başlar.',
        "quote_en": 'Reducing your water footprint is more than turning down the tap; It starts with being aware of what we consume, what we plant and how we produce.',
        "author": 'Su Ayak İzi ve Tüketim Bilinci',
        "author_en": 'Water Footprint and Consumption Awareness',
        "category": 'Bilinçli Tüketim',
        "category_en": 'Conscious Consumption'
    },
    {
        "quote": 'Nehirler sadece su akıtmaz; bir havzanın can damarı, biyoçeşitliliğin yuvası ve medeniyetlerin taşıyıcısıdır. Nehir yataklarına müdahale ederken doğanın hakkını gözetmeliyiz.',
        "quote_en": "Rivers don't just flow water; It is the lifeblood of a basin, the home of biodiversity and the carrier of civilizations. We must respect the rights of nature when intervening in river beds.",
        "author": 'Ekolojik Akış ve Nehir Havzası Etiği',
        "author_en": 'Ecological Flow and River Basin Ethics',
        "category": 'Havza Koruma',
        "category_en": 'Watershed Protection'
    },
    {
        "quote": 'Kurak havzalarda çok su tüketen ürün deseni seçmek, geleceği bugünden tüketmektir. Havza bazlı doğru ürün planlaması su tasarrufunun temelidir.',
        "quote_en": 'Choosing a product pattern that consumes a lot of water in arid basins means consuming the future today. Correct basin-based product planning is the basis of water saving.',
        "author": 'Tarımsal Planlama ve Havza Dengesi',
        "author_en": 'Agricultural Planning and Basin Balance',
        "category": 'Ürün Deseni',
        "category_en": 'Product Pattern'
    },
    {
        "quote": 'Su kayıp ve kaçak oranlarını düşürmeyen bir şehir şebekesi, delik bir kovaya su doldurmaya benzer. Altyapıyı yenilemek, yeni baraj yapmaktan daha etkilidir.',
        "quote_en": 'A city network that does not reduce water loss and leakage rates is like filling a holey bucket with water. Renewing infrastructure is more effective than building new dams.',
        "author": 'Kentsel Su Altyapısı İlkeleri',
        "author_en": 'Urban Water Infrastructure Principles',
        "category": 'Şebeke Yönetimi',
        "category_en": 'Network Management'
    },
    {
        "quote": 'Suyun zenginliği debisinde değil, akılcı ve adil paylaşımındadır. Sektörler arası su tahsisinde bilimi ve adaleti rehber edinmeliyiz.',
        "quote_en": 'The richness of water is not in its flow rate, but in its rational and fair sharing. We must be guided by science and justice in intersectoral water allocation.',
        "author": 'Adil Su Tahsisi ve Yönetişim',
        "author_en": 'Fair Water Allocation and Governance',
        "category": 'Su Yönetişimi',
        "category_en": 'Water Governance'
    },
    {
        "quote": 'Barajlarımızdaki su seviyesini sadece yağışlar değil, havzada yaşayan her bir bireyin su tasarrufu kültürü belirler.',
        "quote_en": 'The water level in our dams is determined not only by rainfall, but also by the water saving culture of each individual living in the basin.',
        "author": 'Toplumsal Su Seferberliği',
        "author_en": 'Social Water Mobilization',
        "category": 'Tasarruf Kültürü',
        "category_en": 'Savings Culture'
    },
    {
        "quote": 'Toprağın nemini ölçmeden yapılan sulama, hem bitkiye hem de su bütçesine yüktür. Dijital tarım ve hassas sulama teknolojileri su israfının panzehiridir.',
        "quote_en": 'Irrigation without measuring soil moisture is a burden on both the plant and the water budget. Digital farming and precision irrigation technologies are the antidote to water waste.',
        "author": 'Akıllı Tarım ve Sensör Teknolojileri',
        "author_en": 'Smart Agriculture and Sensor Technologies',
        "category": 'Teknoloji',
        "category_en": 'Technology'
    },
    {
        "quote": 'Sulak alanları kurutmak, havzanın doğal böbreklerini ve iklim regülatörlerini yok etmektir. Göllerimizi ve bataklıklarımızı korumak iklim krizine karşı ilk kalkanımızdır.',
        "quote_en": "Draining wetlands is destroying the basin's natural kidneys and climate regulators. Protecting our lakes and marshes is our first shield against the climate crisis.",
        "author": 'Sulak Alanlar ve Ekolojik Denge',
        "author_en": 'Wetlands and Ecological Balance',
        "category": 'Sulak Alanlar',
        "category_en": 'Wetlands'
    },
    {
        "quote": 'Su krizi bir gün aniden gelmez; yıllar süren ihmallerin, plansız tüketimin ve ertelemelerin sonucu olarak sessizce kapıyı çalar. Tedbir bugündür.',
        "quote_en": 'Water crisis does not come suddenly one day; It quietly knocks on the door as a result of years of neglect, unplanned consumption and postponement. The measure is today.',
        "author": 'Kuraklık Erken Uyarı Sistemi',
        "author_en": 'Drought Early Warning System',
        "category": 'Kriz Önleme',
        "category_en": 'Crisis Prevention'
    },
    {
        "quote": 'Bir damla suyun toprağa sızması yıllar alır, ancak kontrolsüz bir kuyu onu dakikalar içinde tüketebilir. Kaçak sondajlar yer altının gizli felaketidir.',
        "quote_en": 'It takes years for a drop of water to seep into the ground, but an uncontrolled well can consume it in minutes. Illegal drilling is the hidden disaster of the underground.',
        "author": 'Yeraltı Su Kaynakları Koruma Masası',
        "author_en": 'Underground Water Resources Protection Desk',
        "category": 'Yeraltı Suları',
        "category_en": 'Groundwater'
    },
    {
        "quote": 'Sanayide her metreküp suyun kapalı devre sistemlerle defalarca kullanımı, hem sanayicinin maliyetini düşürür hem de nehirlerimizi kirlilikten korur.',
        "quote_en": 'Repeated use of every cubic meter of water in industry with closed circuit systems reduces the costs of industrialists and protects our rivers from pollution.',
        "author": 'Yeşil Sanayi ve Endüstriyel Su Verimliliği',
        "author_en": 'Green Industry and Industrial Water Efficiency',
        "category": 'Sanayi Verimliliği',
        "category_en": 'Industrial Efficiency'
    },
    {
        "quote": 'Ormanlar suyun yeryüzündeki en büyük süngeridir. Ağaçlandırma sadece erozyonu önlemez; temiz içme suyu havzalarının devamlılığını sağlar.',
        "quote_en": 'Forests are the largest sponge of water on earth. Afforestation not only prevents erosion; It ensures the continuity of clean drinking water basins.',
        "author": 'Orman ve Havza Hidrolojisi',
        "author_en": 'Forest and Basin Hydrology',
        "category": 'Havza Koruma',
        "category_en": 'Watershed Protection'
    },
    {
        "quote": 'Su bilinci okullarda çocuklukta başlamalı, tarlada çiftçiyle, fabrikada mühendisle olgunlaşmalıdır. Bilinçsiz su yönetimi hiçbir kanunla tam olarak çözülemez.',
        "quote_en": 'Water awareness should start in childhood in schools and mature with farmers in the field and engineers in the factory. Unconscious water management cannot be completely solved by any law.',
        "author": 'Su Okuryazarlığı ve Eğitim',
        "author_en": 'Water Literacy and Education',
        "category": 'Eğitim & Kültür',
        "category_en": 'Education & Culture'
    },
    {
        "quote": 'İklim değişikliği su rejimini hızla değiştiriyor; artık geçmişin yağış ortalamalarıyla geleceğin su politikaları inşa edilemez. Dinamik ve esnek yönetim şarttır.',
        "quote_en": 'Climate change is rapidly changing the water regime; Water policies of the future can no longer be built with the rainfall averages of the past. Dynamic and flexible management is essential.',
        "author": 'İklim Değişikliği ve Hidrolojik Uyum',
        "author_en": 'Climate Change and Hydrological Adaptation',
        "category": 'İklim Uyumu',
        "category_en": 'Climate Adaptation'
    },
    {
        "quote": 'Suyu kaynağında temiz tutmak, kirlettikten sonra ileri arıtma tesisleriyle temizlemeye çalışmaktan yüz kat daha ucuz ve sürdürülebilirdir.',
        "quote_en": 'Keeping water clean at the source is a hundred times cheaper and more sustainable than trying to clean it with advanced treatment plants after polluting it.',
        "author": 'Su Kirliliğini Önleme İlkesi',
        "author_en": 'Water Pollution Prevention Policy',
        "category": 'Kirlilik Önleme',
        "category_en": 'Pollution Prevention'
    },
    {
        "quote": 'Gece sulaması yapmak buharlaşma kaybını yarı yarıya azaltır. Doğanın döngüsüne uyumlu sulama takvimleri, bedelsiz ve anında su tasarrufudur.',
        "quote_en": 'Watering at night reduces evaporation loss by half. Irrigation schedules compatible with the cycle of nature provide free and instant water savings.',
        "author": 'Çiftçi Su Yönetimi Rehberi',
        "author_en": 'Farmer Water Management Guide',
        "category": 'Tarımsal Sulama',
        "category_en": 'Agricultural Irrigation'
    },
    {
        "quote": 'Su kaynaklarının korunması sadece bir çevre meselesi değil; doğrudan ulusal güvenlik, bağımsızlık ve gıda egemenliği meselesidir.',
        "quote_en": 'Protecting water resources is not just an environmental issue; It is directly a matter of national security, independence and food sovereignty.',
        "author": 'Stratejik Su Güvenliği Doktrini',
        "author_en": 'Strategic Water Security Doctrine',
        "category": 'Ulusal Güvenlik',
        "category_en": 'National Security'
    },
    {
        "quote": 'Kuraklık dönemlerinde su kısıtı uygulamak geç kalmış bir adımdır; asıl marifet bereketli yıllarda su hasadı yapıp rezervleri dolu tutmaktır.',
        "quote_en": 'Imposing water restrictions during drought periods is a step too late; The real trick is to harvest water in fertile years and keep the reserves full.',
        "author": 'Su Güvenliği ve Rezerv Yönetimi',
        "author_en": 'Water Security and Reserve Management',
        "category": 'Rezerv Yönetimi',
        "category_en": 'Reserve Management'
    },
    {
        "quote": 'Her dere yatağı milyonlarca yıldır kendi yolunu çizer. Dere yataklarını daraltmak veya kapatmak, ilk büyük yağışta felakete davetiye çıkarmaktır.',
        "quote_en": 'Each stream bed follows its own path for millions of years. Narrowing or closing the stream beds means inviting disaster at the first heavy rainfall.',
        "author": 'Taşkın ve Havza Mühendisliği',
        "author_en": 'Flood and Basin Engineering',
        "category": 'Taşkın Yönetimi',
        "category_en": 'Flood Management'
    },
    {
        "quote": 'Kırsal alanda kapalı basınçlı boru sistemlerine geçilmedikçe, açık kanallarda buharlaşan ve sızan her damla milli servetin kaybıdır.',
        "quote_en": 'Unless closed pressure pipe systems are used in rural areas, every drop that evaporates and leaks in open channels is a loss of national wealth.',
        "author": 'DSİ Modern Sulama Sistemleri Vizyonu',
        "author_en": 'DSI Modern Irrigation Systems Vision',
        "category": 'Sulama Altyapısı',
        "category_en": 'Irrigation Infrastructure'
    },
    {
        "quote": 'Su tasarrufu fedakarlık değil, yarın susuz kalmamak için bugün atılan en rasyonel ve kazançlı yatırımdır.',
        "quote_en": 'Saving water is not a sacrifice, it is the most rational and profitable investment made today to avoid being left without water tomorrow.',
        "author": 'Su Verimliliği Seferberliği',
        "author_en": 'Water Efficiency Mobilization',
        "category": 'Verimlilik',
        "category_en": 'Productivity'
    },
    {
        "quote": 'Akarsuların doğduğu kaynak noktalarından döküldüğü denizlere kadar bir bütün olarak yönetilmediği hiçbir model başarılı olamaz.',
        "quote_en": 'No model can be successful if the rivers are not managed as a whole, from their source points to the seas where they flow.',
        "author": 'Entegre Nehir Havzası Yönetim Planı (ENHYP)',
        "author_en": 'Integrated River Basin Management Plan (ENHYP)',
        "category": 'Havza Planlama',
        "category_en": 'Basin Planning'
    },
    {
        "quote": 'Toprak organik maddesi yüksek olan tarla, suyu sünger gibi tutar; organik maddesi fakir toprak ise suyu hızla kaybeder. Suyu tutmak toprağı beslemekle başlar.',
        "quote_en": 'The field with high soil organic matter retains water like a sponge; Soil with poor organic matter loses water rapidly. Holding water starts with nourishing the soil.',
        "author": 'Onarıcı Tarım ve Toprak Nemi Yönetimi',
        "author_en": 'Regenerative Agriculture and Soil Moisture Management',
        "category": 'Toprak Sağlığı',
        "category_en": 'Soil Health'
    },
    {
        "quote": 'Bir litre kullanılmış motor yağı veya kimyasal atık, bir milyon litre temiz yer altı suyunu zehirleyebilir. Suyu korumak, toprağa ne döktüğümüzü bilmektir.',
        "quote_en": 'One liter of used motor oil or chemical waste can poison one million liters of clean groundwater. Conserving water means knowing what we put into the ground.',
        "author": 'Çevre Koruma ve Akifer Güvenliği',
        "author_en": 'Environmental Protection and Aquifer Safety',
        "category": 'Akifer Güvenliği',
        "category_en": 'Aquifer Safety'
    },
    {
        "quote": 'Geleceğin şehirleri, suyu dışarıdan getiren değil; tükettiği suyu yerinde arıtıp dönüştüren ve yağmurunu depolayan akıllı şehirler olacaktır.',
        "quote_en": 'The cities of the future will not be those that bring water from outside; There will be smart cities that purify and transform the water they consume on site and store their rain.',
        "author": 'Geleceğin Akıllı Şehirleri Su Raporu',
        "author_en": 'Future Smart Cities Water Report',
        "category": 'Akıllı Şehirler',
        "category_en": 'Smart Cities'
    },
    {
        "quote": 'Su kaynaklarını yönetirken sadece insan ihtiyaçlarını değil; havzadaki börtü böceğin, balıkların ve ormanların su hakkını da teslim etmeliyiz.',
        "quote_en": 'When managing water resources, we consider not only human needs; We must also deliver the water rights of the insects, fish and forests in the basin.',
        "author": 'Ekolojik Hakkaniyet ve Can Suyu İlkesi',
        "author_en": 'Ecological Equity and the Lifeline Principle',
        "category": 'Can Suyu',
        "category_en": 'life water'
    },
    {
        "quote": 'Barajlardaki buharlaşmayı azaltan yüzer güneş enerjisi panelleri, hem temiz enerji üretir hem de suyun buharlaşarak kaybolmasını önler. İkili fayda, geleceğin mühendisliğidir.',
        "quote_en": 'Floating solar energy panels, which reduce evaporation in dams, both produce clean energy and prevent water from being lost by evaporation. The dual benefit is the engineering of the future.',
        "author": 'Yenilikçi Su ve Enerji Teknolojileri',
        "author_en": 'Innovative Water and Energy Technologies',
        "category": 'Yenilikçi Teknoloji',
        "category_en": 'Innovative Technology'
    },
    {
        "quote": 'Su yönetiminde en pahalı çözüm, hiçbir şey yapmayıp kriz anında su taşımak veya tankerlerle çare aramaktır. En ucuz çözüm ise tasarruftur.',
        "quote_en": 'The most expensive solution in water management is to do nothing and carry water or seek solutions with tankers in times of crisis. The cheapest solution is savings.',
        "author": 'Su Ekonomisi ve Kriz Maliyeti',
        "author_en": 'Water Economy and Cost of Crisis',
        "category": 'Su Ekonomisi',
        "category_en": 'Water Economy'
    },
    {
        "quote": 'Kurakçıl peyzaj (xeriscaping), şehir parklarında ve refüjlerde içme suyuyla çim sulama israfına son veren en estetik ve akılcı su yönetimidir.',
        "quote_en": 'Xeriscaping is the most aesthetic and rational water management that puts an end to the waste of lawn irrigation with drinking water in city parks and medians.',
        "author": 'Kentsel Yeşil Alan ve Kurakçıl Peyzaj',
        "author_en": 'Urban Green Space and Arid Landscape',
        "category": 'Kentsel Tasarruf',
        "category_en": 'Urban Savings'
    },
    {
        "quote": 'Bir göl kuruduğunda sadece su kaybolmaz; o bölgenin mikroiklimi, tarımı, balıkçılığı ve çocukların geleceği de kurur. Göllerimizi yaşatmak vatani görevdir.',
        "quote_en": "When a lake dries up, not only water is lost; The microclimate, agriculture, fishing and children's future of that region also dry up. It is our national duty to keep our lakes alive.",
        "author": 'Sulak Alanlar ve Doğa Koruma Çağrısı',
        "author_en": 'Call for Wetlands and Nature Conservation',
        "category": 'Göl Koruma',
        "category_en": 'Lake Protection'
    },
    {
        "quote": 'Akıllı sayaçlar ve scada sistemleri ile donatılmayan içme suyu şebekelerinde sızıntılar görünmez bir hırsız gibidir; dijitalleşme suyun koruyucusudur.',
        "quote_en": 'Leaks are like an invisible thief in drinking water networks that are not equipped with smart meters and SCADA systems; Digitalization is the guardian of water.',
        "author": 'Dijital Su Şebekeleri ve SCADA Yönetimi',
        "author_en": 'Digital Water Networks and SCADA Management',
        "category": 'Dijitalleşme',
        "category_en": 'digitalization'
    },
    {
        "quote": 'Gıda israfı, aynı zamanda o gıdayı üretmek için harcanan yüzlerce metreküp suyun çöpe atılması demektir. Tabağındaki yemeği koruyan, suyu korur.',
        "quote_en": 'Food waste also means throwing away hundreds of cubic meters of water spent to produce that food. He who preserves the food on his plate preserves the water.',
        "author": 'Gıda-Su Bağı ve Sürdürülebilirlik',
        "author_en": 'Food-Water Nexus and Sustainability',
        "category": 'Gıda-Su Bağı',
        "category_en": 'Food-Water Nexus'
    },
    {
        "quote": 'Tuzlanma ve çoraklaşma, aşırı ve yanlış sulamanın bereketli ovalara vurduğu en acı darbedir. Ölçülü su, ömür boyu bereket getirir.',
        "quote_en": 'Salinization and barrenness are the most painful blow that excessive and incorrect irrigation inflicts on the fertile plains. Water in moderation brings abundance for life.',
        "author": 'Tarımsal Drenaj ve Tuzluluk Kontrolü',
        "author_en": 'Agricultural Drainage and Salinity Control',
        "category": 'Toprak Koruma',
        "category_en": 'Soil Conservation'
    },
    {
        "quote": 'Suyu yönetmek doğayı fethetmek değil; doğanın hidrolojik döngüsünü anlayıp onunla barışık ve uyumlu bir yaşam kurabilmektir.',
        "quote_en": 'Managing water is not about conquering nature; is to understand the hydrological cycle of nature and establish a peaceful and harmonious life with it.',
        "author": 'Doğa Temelli Su Çözümleri',
        "author_en": 'Nature Based Water Solutions',
        "category": 'Doğa Temelli Çözümler',
        "category_en": 'Nature Based Solutions'
    },
    {
        "quote": 'Her bireyin evinde yapacağı 1 dakikalık duş tasarrufu veya damlatan musluğu onarması, bir yılda barajlar dolusu suyun havzada kalmasını sağlar.',
        "quote_en": 'Saving 1 minute of shower time or repairing a dripping faucet at home by each individual will ensure that dams full of water remain in the basin in a year.',
        "author": 'Bireysel Tasarruf ve Hanehalkı Su Rehberi',
        "author_en": 'Individual Savings and Household Water Guide',
        "category": 'Evsel Tasarruf',
        "category_en": 'Household Savings'
    },
]
AGRICULTURE_MANAGEMENT_QUOTES: List[Dict[str, str]] = [
    {
        "quote": 'Milli ekonominin temeli tarımdır. Üreten ve toprağını koruyan çiftçi, milletin refahının en güçlü teminatıdır.',
        "quote_en": "The basis of the national economy is agriculture. The farmer who produces and protects his land is the strongest guarantee of the nation's prosperity.",
        "author": 'Mustafa Kemal Atatürk',
        "author_en": 'Mustafa Kemal Ataturk',
        "category": 'Milli Tarım',
        "category_en": 'National Agriculture'
    },
    {
        "quote": 'Hassas tarım ve akıllı sensörler bir lüks değil; girdi maliyetlerini düşüren ve toprağı koruyan çağdaş bir zorunluluktur.',
        "quote_en": 'Precision farming and smart sensors are not a luxury; It is a contemporary necessity that reduces input costs and protects the soil.',
        "author": 'Akıllı Tarım Teknolojileri',
        "author_en": 'Smart Agriculture Technologies',
        "category": 'Tarım Teknolojileri',
        "category_en": 'Agricultural Technologies'
    },
    {
        "quote": "Yerli tohumculuk ve genetik çeşitliliğin korunması, iklim krizine karşı Türkiye'nin en dirençli gıda güvenliği kalkanıdır.",
        "quote_en": "Local seed production and preservation of genetic diversity are Türkiye's most resilient food security shield against the climate crisis.",
        "author": 'Tohum Islahı ve Biyoçeşitlilik Masası',
        "author_en": 'Seed Breeding and Biodiversity Desk',
        "category": 'Tohum Güvenliği',
        "category_en": 'Seed Safety'
    },
    {
        "quote": 'Toprak organik maddesini zenginleştirmek, tarlayı kuraklığa karşı doğal bir su deposuna ve bereket merkezine dönüştürür.',
        "quote_en": 'Enriching soil organic matter turns the field into a natural water reservoir and fertility center against drought.',
        "author": 'Onarıcı Tarım ve Toprak Sağlığı',
        "author_en": 'Regenerative Agriculture and Soil Health',
        "category": 'Toprak Sağlığı',
        "category_en": 'Soil Health'
    },
    {
        "quote": 'Dengeli ve toprak analizine dayalı gübreleme hem çiftçinin cebini korur hem de yeraltı sularının nitratla kirlenmesini önler.',
        "quote_en": "Balanced fertilization based on soil analysis protects the farmer's pocket and prevents groundwater contamination with nitrate.",
        "author": 'Bitki Besleme ve Toprak Verimliliği',
        "author_en": 'Plant Nutrition and Soil Fertility',
        "category": 'Gübreleme',
        "category_en": 'Fertilization'
    },
    {
        "quote": 'Güçlü kooperatifleşme ve lisanslı depoculuk, küçük üreticinin emeğini piyasa dalgalanmalarına karşı koruyan en sağlam sigortadır.',
        "quote_en": 'Strong cooperatives and licensed warehousing are the strongest insurance that protects the labor of small producers against market fluctuations.',
        "author": 'Tarımsal Pazarlama ve Kooperatifçilik',
        "author_en": 'Agricultural Marketing and Cooperatives',
        "category": 'Tarım Ekonomisi',
        "category_en": 'Agricultural Economics'
    },
    {
        "quote": 'Meraların korunması ve ıslahı yapılmadan, yerli ve sürdürülebilir bir hayvancılık politikası başarıya ulaşamaz.',
        "quote_en": 'A local and sustainable livestock policy cannot be successful without the protection and improvement of pastures.',
        "author": 'Mera Islahı ve Hayvancılık Vizyonu',
        "author_en": 'Pasture Improvement and Livestock Vision',
        "category": 'Hayvancılık',
        "category_en": 'livestock'
    },
    {
        "quote": 'Biyolojik mücadele ve entegre zararlı yönetimi, hem ihracatta kalıntı sorununu çözer hem de ekosistemi korur.',
        "quote_en": 'Biological control and integrated pest management both solve the residue problem in exports and protect the ecosystem.',
        "author": 'Bitki Sağlığı ve Biyolojik Mücadele',
        "author_en": 'Plant Health and Biological Control',
        "category": 'Bitki Koruma',
        "category_en": 'Plant Protection'
    },
    {
        "quote": 'Gıda güvenliği ulusal bağımsızlığın temelidir; tarlasını ekmeyen ülke geleceğini başka ülkelerin kararlarına teslim eder.',
        "quote_en": 'Food security is the foundation of national independence; A country that does not cultivate its fields surrenders its future to the decisions of other countries.',
        "author": 'Stratejik Gıda Egemenliği Doktrini',
        "author_en": 'Strategic Food Sovereignty Doctrine',
        "category": 'Gıda Güvenliği',
        "category_en": 'Food Safety'
    },
    {
        "quote": 'Jeotermal seracılık ve modern örtüaltı üretimi, yılın 12 ayı kesintisiz ve yüksek katma değerli tarımsal üretimin kapısıdır.',
        "quote_en": 'Geothermal greenhouse cultivation and modern greenhouse production are the gateway to uninterrupted and high value-added agricultural production 12 months a year.',
        "author": 'Modern Örtüaltı ve Seracılık Vizyonu',
        "author_en": 'Modern Greenhouse and Greenhouse Vision',
        "category": 'Seracılık',
        "category_en": 'greenhouse cultivation'
    },
]
LIVESTOCK_MANAGEMENT_QUOTES: List[Dict[str, str]] = [
    {
        "quote": 'Yerli damızlık ve genetik ıslah, sürdürülebilir bir hayvancılık modelinin en temel taşıdır. Dışa bağımlılığı azaltmak damızlık kalitesini yükseltmekle başlar.',
        "quote_en": 'Local breeding and genetic improvement are the cornerstone of a sustainable livestock model. Reducing foreign dependency starts with improving breeding quality.',
        "author": 'Milli Damızlık ve Islah Rehberi',
        "author_en": 'National Breeding and Breeding Guide',
        "category": 'Genetik & Damızlık',
        "category_en": 'Genetics & Breeding'
    },
    {
        "quote": 'Kaba yem açığını kapatmayan ve kaliteli silaj üretmeyen bir işletmede besi ve süt maliyetleri kontrol altına alınamaz.',
        "quote_en": 'Fattening and milk costs cannot be controlled in a business that does not close the roughage gap and does not produce quality silage.',
        "author": 'Hayvan Besleme ve Kaba Yem Masası',
        "author_en": 'Animal Nutrition and Roughage Table',
        "category": 'Yem & Besleme',
        "category_en": 'Feed & Nutrition'
    },
    {
        "quote": "Meralar sadece hayvan otlatma alanı değil, Anadolu'nun en zengin doğal ekosistemi ve biyolojik hazinesidir. Islah edilen meralar et ve sütte maliyeti yarıya düşürür.",
        "quote_en": 'Pastures are not just animal grazing areas, they are the richest natural ecosystem and biological treasure of Anatolia. Improved pastures reduce the cost of meat and milk by half.',
        "author": 'Mera Islahı ve Otlatma Yönetimi',
        "author_en": 'Pasture Improvement and Grazing Management',
        "category": 'Mera & Otlatma',
        "category_en": 'Pasture & Grazing'
    },
    {
        "quote": 'Biyogüvenlik ve koruyucu hekimlik tedbirleri, salgın hastalık ortaya çıktıktan sonraki tedavi maliyetlerinden yüz kat daha ekonomiktir.',
        "quote_en": 'Biosecurity and preventive medicine measures are a hundred times more economical than the treatment costs after the epidemic occurs.',
        "author": 'Veteriner Halk Sağlığı ve Biyogüvenlik',
        "author_en": 'Veterinary Public Health and Biosecurity',
        "category": 'Hayvan Sağlığı',
        "category_en": 'Animal Health'
    },
    {
        "quote": 'Sürü takip sensörleri, otomatik sağım robotları ve kızgınlık tespit sistemleri akıllı hayvancılıkta verimliliği zirveye taşır.',
        "quote_en": 'Herd tracking sensors, automatic milking robots and estrus detection systems bring efficiency to the top in smart livestock farming.',
        "author": 'Hassas Hayvancılık Teknolojileri',
        "author_en": 'Precision Livestock Technologies',
        "category": 'Akıllı Çiftlik',
        "category_en": 'Smart Farm'
    },
    {
        "quote": 'Kaliteli çiğ süt, soğuk zincir bozulmadan mandıraya ulaştığında hem üreticiye hak ettiği değeri hem de tüketiciye sağlığı sunar.',
        "quote_en": 'When quality raw milk reaches the dairy with the cold chain intact, it offers both the value it deserves to the producer and health to the consumer.',
        "author": 'Süt Hijyeni ve Soğuk Zincir Masası',
        "author_en": 'Milk Hygiene and Cold Chain Table',
        "category": 'Süt Endüstrisi',
        "category_en": 'Dairy Industry'
    },
    {
        "quote": 'Hayvan refahı ve konforu, doğrudan süt verimi ve et kalitesini belirleyen en kritik fizyolojik faktördür. Huzurlu sürü, bereketli üretimdir.',
        "quote_en": 'Animal welfare and comfort is the most critical physiological factor that directly determines milk yield and meat quality. Peaceful herd means abundant production.',
        "author": 'Çiftlik Yönetimi ve Hayvan Refahı',
        "author_en": 'Farm Management and Animal Welfare',
        "category": 'Hayvan Refahı',
        "category_en": 'Animal Welfare'
    },
    {
        "quote": "Küçükbaş hayvancılık Anadolu'nun kadim coğrafyasına ve kurak iklimine en uygun, suyu ve merayı en verimli değerlendiren üretim modelidir.",
        "quote_en": 'Small livestock farming is the production model that is most suitable for the ancient geography and arid climate of Anatolia and uses water and pasture most efficiently.',
        "author": 'Anadolu Küçükbaş Yetiştiriciliği Vizyonu',
        "author_en": 'Anatolian Small Cattle Breeding Vision',
        "category": 'Küçükbaş',
        "category_en": 'ovine'
    },
]

def get_daily_water_quote(dt: datetime = None) -> Dict[str, str]:
    if dt is None:
        dt = datetime.now(timezone.utc)
    day_of_year = dt.timetuple().tm_yday
    year = dt.year
    index = (day_of_year + (year * 7)) % len(WATER_MANAGEMENT_QUOTES)
    return WATER_MANAGEMENT_QUOTES[index]

def get_daily_agri_quote(dt: datetime = None) -> Dict[str, str]:
    if dt is None:
        dt = datetime.now(timezone.utc)
    day_of_year = dt.timetuple().tm_yday
    year = dt.year
    index = (day_of_year + (year * 11)) % len(AGRICULTURE_MANAGEMENT_QUOTES)
    return AGRICULTURE_MANAGEMENT_QUOTES[index]

def get_daily_livestock_quote(dt: datetime = None) -> Dict[str, str]:
    if dt is None:
        dt = datetime.now(timezone.utc)
    day_of_year = dt.timetuple().tm_yday
    year = dt.year
    index = (day_of_year + (year * 13)) % len(LIVESTOCK_MANAGEMENT_QUOTES)
    return LIVESTOCK_MANAGEMENT_QUOTES[index]


# Backward compatibility alias
get_daily_agriculture_quote = get_daily_agri_quote
