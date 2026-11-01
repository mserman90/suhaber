"""
app/legal_data.py
Yasal Sorumluluk Reddi Beyanı (Legal Disclaimer), 6698 Sayılı KVKK ve Gizlilik Politikası,
ve Künye / Telif Politikası veri ve şablon motoru.
"""

from typing import Dict, Any

LEGAL_DISCLAIMER_TR = """
<div class="legal-section">
    <h4>1. Genel Bilgilendirme ve Hizmet Niteliği</h4>
    <p>
        Bu dijital yayın platformu (<strong>Su Gündemi</strong>, <strong>Tarım Gündemi</strong> ve <strong>Hayvancılık Gündemi</strong>);
        Türkiye ve dünyadaki su kaynakları, hidroloji, tarımsal üretim, bitki sağlığı, hayvancılık, yem sanayii ve kırsal kalkınma alanlarındaki
        gelişmeleri takip etmek isteyen araştırmacılar, çiftçiler, üreticiler ve kamuoyu için hazırlanmış
        <strong>bağımsız ve kâr amacı gütmeyen bir dijital gazete ve açık veri portalıdır</strong>.
    </p>
    <p>
        Portalda yer alan tüm haberler, basın bültenleri, editoryal özetler, harita koordinatları, hidrolojik doluluk göstergeleri,
        uluslararası toplantı takvimleri ve emtia fiyat pariteleri yalnızca <strong>genel kamuoyu bilgilendirmesi, akademik izleme ve farkındalık</strong>
        amacıyla yayımlanmaktadır.
    </p>
</div>

<div class="legal-section">
    <h4>2. Yatırım, Finans ve Ticari Karar Tavsiyesi Değildir</h4>
    <div class="legal-alert-box">
        <strong>⚠️ Önemli Uyarı:</strong> Bu sitede sunulan hiçbir piyasa verisi, emtia fiyatı veya analiz bir yatırım tavsiyesi değildir.
    </div>
    <p>
        Portalda paylaşılan tarımsal ve hayvansal ürün fiyatları (ekmeklik ve makarnalık buğday, mısır, ayçiçeği, pamuk, çiğ süt, karkas dana/kuzu eti,
        karma yem, gübre, mazot vb.), uluslararası borsa pariteleri (AB Euronext, ABD CBOT/USDA, Dünya FOB) ve döviz dönüşümleri;
        açık kaynaklı piyasa göstergelerinden ve resmi bültenlerden derlenmiş <em>tahmini ve gösterge niteliğinde</em> bilgilerdir.
    </p>
    <p>
        Bu veriler; <strong>6362 sayılı Sermaye Piyasası Kanunu</strong> veya ilgili finansal/ticari mevzuat kapsamında kesinlikle
        <strong>yatırım danışmanlığı, alım-satım tavsiyesi, portföy yöneticiliği veya resmi borsa teyidi niteliği taşımamaktadır</strong>.
        Kullanıcıların bu portalda yer alan fiyat, parite veya haber verilerine dayanarak gerçekleştirecekleri her türlü ticari sözleşme,
        alım-satım, ekim/dikim, besicilik veya yatırım kararından doğabilecek doğrudan veya dolaylı maddi/manevi zararlardan,
        kâr mahrumiyetinden veya idari yaptırımlardan portal yöneticileri ve teknik geliştiriciler sorumlu tutulamaz.
        Gerçek ticari işlemlerde ilgili kurumların (TMO, ESK, USK, Ticaret Borsaları, TOBB vb.) resmi ilan ve tescil bültenleri bağlayıcıdır.
    </p>
</div>

<div class="legal-section">
    <h4>3. Veri Kaynakları ve Üçüncü Taraf Bağlantıları (Dış Linkler)</h4>
    <p>
        Portalımızdaki haber akışları; ulusal ve yerel basın kuruluşları, kamu kurumları (Tarım ve Orman Bakanlığı, DSİ, Meteoroloji Genel Müdürlüğü, İSKİ vb.),
        uluslararası örgütler (BM, FAO, Dünya Su Konseyi, WRI, OECD vb.) ve hakemli akademik dergi açık arşivlerinden (Crossref, PubMed, arXiv)
        otomatik tarayıcılar (RSS / Scraper) ve editoryal süzgeçlerle derlenmektedir.
    </p>
    <p>
        Haber kartlarında veya modal pencerelerde yer alan harici bağlantılar (dış linkler) üçüncü taraf sitelere yönlendirme sağlar.
        Bağlantı verilen internet sitelerinin içeriği, güncelliği, güvenliği veya gizlilik standartları üzerinde portalımızın herhangi bir denetim veya
        müdahale yetkisi bulunmamakta olup, üçüncü taraf kaynakların eylem veya yayınlarından dolayı portalımıza hiçbir hukuki veya cezai sorumluluk yüklenemez.
    </p>
</div>

<div class="legal-section">
    <h4>4. Harita ve Jeo-Uzamsal (GIS) Konumlandırma Doğruluğu</h4>
    <p>
        İnteraktif haritada haberlerin konumlandırılması; haber metinleri içerisinde geçen il, ilçe, nehir havzası, baraj veya sulama tesisi adlarının
        çok katmanlı semantik coğrafi kodlayıcı (geocoder) algoritmalarıyla analiz edilmesi suretiyle gerçekleştirilir.
        Haritada gösterilen konum iğneleri (marker) ve ısı haritaları yönlendirici ve tematik mahiyette olup; hiçbir şekilde kadastral, mülki,
        idari veya resmî sınır/tesis tayini teşkil etmez; bu amaçlarla delil olarak kullanılamaz.
    </p>
</div>

<div class="legal-section">
    <h4>5. Hizmet Sürekliliği ve Değişiklik Hakkı</h4>
    <p>
        Portal içeriğinin kesintisiz, anlık veya hatasız sunulacağına dair zımni veya açık hiçbir garanti verilmemektedir.
        Portal yönetimi; sistem mimarisini, sunulan kanalları, veri kaynaklarını veya işbu yasal şartları önceden bildirimde bulunmaksızın
        dilediği zaman güncelleme, askıya alma veya sonlandırma hakkını saklı tutar.
    </p>
</div>
"""

LEGAL_DISCLAIMER_EN = """
<div class="legal-section">
    <h4>1. General Information & Scope of Service</h4>
    <p>
        This digital portal (comprising <strong>Water Agenda</strong>, <strong>Agriculture Agenda</strong>, and <strong>Livestock Agenda</strong>)
        is an <strong>independent, open-source, non-profit digital newspaper and open GIS intelligence portal</strong> dedicated to monitoring
        water resources, hydrology, agricultural commodity markets, smart farming, and livestock economics in Turkey and globally.
    </p>
    <p>
        All articles, market trackers, GIS coordinates, conference schedules, and parity indices are published strictly for
        <strong>general public awareness, academic research, and informational monitoring</strong>.
    </p>
</div>

<div class="legal-section">
    <h4>2. No Financial, Investment or Commercial Advice</h4>
    <div class="legal-alert-box">
        <strong>⚠️ Notice:</strong> No market quote, commodity pricing, or editorial analysis on this portal constitutes financial or commercial advice.
    </div>
    <p>
        Agricultural and livestock commodity prices (milling/durum wheat, corn, sunflower, raw milk, carcass beef/lamb, feed ratios, fertilizer, diesel)
        and global parities (EU Euronext, US CBOT/USDA, World FOB parity) are aggregated from open public sources and indicative trade bulletins.
    </p>
    <p>
        These figures do not represent licensed financial advice, solicitation, trading instructions, or formal exchange quotations under
        Turkish Capital Market Law No. 6362 or international securities regulations. Neither the portal nor its developers shall be held liable
        for any commercial, trading, agricultural, or investment decisions made based on this information. Official trade contracts must always be
        verified against certified bulletins issued by accredited mercantile exchanges and regulatory boards (e.g., TMO, ESK, USK).
    </p>
</div>

<div class="legal-section">
    <h4>3. External Links & Third-Party Content</h4>
    <p>
        News items are aggregated from credible national news media, governmental agencies (Ministry of Agriculture and Forestry, DSI, WRI, FAO, UN Water),
        and open-access academic repositories. We bear no control or liability over third-party external websites linked from our articles.
    </p>
</div>

<div class="legal-section">
    <h4>4. GIS Spatial Coordinates Disclaimer</h4>
    <p>
        Geospatial pins on the interactive Leaflet map are placed via algorithmic multi-tier geocoding matching topographic landmarks, river basins,
        and municipal districts. They are purely thematic visual references and cannot be used for cadastral or legal demarcation.
    </p>
</div>
"""

LEGAL_KVKK_TR = """
<div class="legal-section">
    <h4>1. 6698 Sayılı KVKK Kapsamında Aydınlatma Metni</h4>
    <p>
        Bu aydınlatma metni, <strong>6698 sayılı Kişisel Verilerin Korunması Kanunu ("KVKK")</strong> ve ilgili mevzuat uyarınca;
        ziyaretçilerimizin temel hak ve özgürlüklerini korumak, veri güvenliğini sağlamak ve kişisel veri işleme süreçlerine ilişkin şeffaflığı
        temin etmek amacıyla hazırlanmıştır.
    </p>
</div>

<div class="legal-section">
    <h4>2. Veri Sorumlusu Sıfatı</h4>
    <p>
        İşbu portal, tamamen <strong>statik (static website)</strong> mimaride barındırılan, kâr amacı gütmeyen açık kaynaklı bir kamusal bilgilendirme
        aracıdır. Tüzel kişilik veya ticari şirket niteliğinde olmayıp, açık kaynak topluluk ilkeleri çerçevesinde sürdürülmektedir.
    </p>
</div>

<div class="legal-section">
    <h4>3. Kişisel Verilerin İşlenmemesi ve Toplanmaması</h4>
    <div class="legal-badge-pill">🔒 Sıfır Kişisel Veri Toplama Prensibi</div>
    <p>
        Portalımız üzerinde;
    </p>
    <ul class="legal-list">
        <li>Kullanıcı kaydı, hesap oluşturma veya üyelik sistemi <strong>yoktur</strong>.</li>
        <li>İsim, soyisim, T.C. kimlik numarası, telefon numarası veya posta adresi talep eden formlar <strong>bulunmamaktadır</strong>.</li>
        <li>E-bülten veya e-posta aboneliği için e-posta toplama veritabanı <strong>işletilmemektedir</strong>.</li>
        <li>Yorum yapma, kullanıcı girişi veya dosya yükleme modülü <strong>yer almamaktadır</strong>.</li>
        <li>Kredi kartı, banka bilgisi veya finansal veri işleme <strong>kesinlikle söz konusu değildir</strong>.</li>
    </ul>
    <p>
        Dolayısıyla ziyaretçilerimizin kimliğini doğrudan veya dolaylı olarak belirleyen <strong>hiçbir kişisel veri toplanmamakta, kaydedilmemekte,
        işlenmemekte ve sunucularımızda saklanmamaktadır</strong>.
    </p>
</div>

<div class="legal-section">
    <h4>4. Çerezler (Cookies) ve Yerel Tarayıcı Depolaması (LocalStorage)</h4>
    <p>
        Sitemizde reklam ağları, Google Analytics benzeri davranışsal izleyiciler veya üçüncü taraf profilleme çerezleri (cookies)
        <strong>kullanılmamaktadır</strong>.
    </p>
    <p>
        Sayfanın yalnızca sizin belirlediğiniz görsel ve dilsel tercihlerle görüntülenebilmesi amacıyla tarayıcınızın kendi dahili depolama alanında
        (<code>localStorage</code>) iki adet teknik parametre saklanmaktadır:
    </p>
    <ul class="legal-list">
        <li><code>su_portal_theme</code>: Tercih ettiğiniz koyu (dark) veya açık (light) renk teması.</li>
        <li><code>portal_language</code>: Tercih ettiğiniz Türkçe (tr) veya İngilizce (en) dil seçimi.</li>
    </ul>
    <p>
        Bu veriler yalnızca sizin kendi cihazınızda yerel olarak tutulur; hiçbir harici sunucuya veya üçüncü tarafa iletilmez.
        Dilediğiniz an tarayıcı ayarlarınızdan site verilerini ve yerel depolamayı temizleyebilirsiniz.
    </p>
</div>

<div class="legal-section">
    <h4>5. Sunucu Günlükleri ve CDN Güvenliği</h4>
    <p>
        Portal sayfaları GitHub Pages (GitHub Inc.) altyapısı üzerinde statik olarak barındırılmaktadır.
        İnternet protokollerinin zorunlu teknik bir gereği olarak, web sayfalarının ve harita kütüphanelerinin (Leaflet, OpenStreetMap, CartoDB, Google Fonts)
        cihazınıza ulaştırılması esnasında IP adresiniz ve tarayıcı başlık bilginiz (User-Agent) ilgili altyapı sağlayıcıları tarafından
        siber güvenlik, DDoS koruması ve içerik dağıtım ağı (CDN) önbelleklemesi amacıyla standart sunucu günlüklerinde geçici olarak işlenebilir.
    </p>
</div>

<div class="legal-section">
    <h4>6. İlgili Kişinin Hakları (KVKK Madde 11) ve Başvuru</h4>
    <p>
        6698 sayılı Kanun’un 11. maddesi uyarınca veri sahipleri; kişisel verilerinin işlenip işlenmediğini öğrenme, işlenmişse buna ilişkin bilgi talep etme
        ve silinmesini isteme haklarına sahiptir. Sitemizde hiçbir kişisel veri tutulmamakla birlikte, telif hakkı ihlali iddiaları veya içerik kaldırma
        başvuruları için resmi proje depomuz üzerinden (<a href="https://github.com/mserman90/suhaber/issues" target="_blank" rel="noopener noreferrer">GitHub Issues</a>)
        doğrudan iletişime geçebilirsiniz.
    </p>
</div>
"""

LEGAL_KVKK_EN = """
<div class="legal-section">
    <h4>1. Data Protection & Privacy Notice (KVKK & GDPR Compliance)</h4>
    <p>
        This privacy notice explains the data processing practices for this portal in strict accordance with the
        <strong>Turkish Personal Data Protection Law No. 6698 (KVKK)</strong> and international privacy standards (GDPR).
    </p>
</div>

<div class="legal-section">
    <h4>2. Static Architecture & Zero Personal Data Policy</h4>
    <p>
        This website is a completely static, open-source informative portal. We adhere to a strict <strong>Zero Personal Data Collection Policy</strong>:
    </p>
    <ul class="legal-list">
        <li>No user accounts, registrations, or profile systems exist.</li>
        <li>No contact forms, personal identification, or newsletter sign-ups are collected.</li>
        <li>No financial, payment, or transactional data is handled.</li>
    </ul>
</div>

<div class="legal-section">
    <h4>3. Cookies & Client-Side Local Storage</h4>
    <p>
        We do <strong>not</strong> employ commercial advertising, tracking beacons, or behavioural analytics cookies.
    </p>
    <p>
        The portal uses your browser's local client storage (<code>localStorage</code>) exclusively to store your personal interface preferences:
    </p>
    <ul class="legal-list">
        <li><code>su_portal_theme</code>: Dark or light color mode selection.</li>
        <li><code>portal_language</code>: Turkish (tr) or English (en) localization preference.</li>
    </ul>
    <p>
        These values reside strictly on your personal device and are never transmitted to external servers. You can clear them at any time via your browser settings.
    </p>
</div>

<div class="legal-section">
    <h4>4. Hosting Infrastructure & CDN Logs</h4>
    <p>
        The static assets are served through GitHub Pages infrastructure with open CDNs (Google Fonts, Leaflet, OpenStreetMap tiles).
        Standard, automated technical server request headers (IP address, user-agent) may be processed transiently by these cloud networks solely
        for cybersecurity and bandwidth caching purposes.
    </p>
</div>

<div class="legal-section">
    <h4>5. Inquiries and Rights (Article 11)</h4>
    <p>
        To submit inquiries or content attribution notices, please open a ticket on our official
        <a href="https://github.com/mserman90/suhaber/issues" target="_blank" rel="noopener noreferrer">GitHub Issues</a> tracker.
    </p>
</div>
"""

LEGAL_IMPRINT_TR = """
<div class="legal-section">
    <h4>1. Künye ve Yayın Sahibi</h4>
    <table class="legal-table">
        <tbody>
            <tr>
                <td><strong>Yayın Adı:</strong></td>
                <td>Su, Tarım ve Hayvancılık Dijital Gazete Portalı (Su Gündemi &bull; Tarım Gündemi &bull; Hayvancılık Gündemi)</td>
            </tr>
            <tr>
                <td><strong>Yayın Türü:</strong></td>
                <td>Süreli Dijital Gazete, Bilimsel Bülten & Açık Veri Portalı (Statik Web Yayını)</td>
            </tr>
            <tr>
                <td><strong>Proje Sahibi & Geliştirici:</strong></td>
                <td>@mserman90 &bull; Bağımsız Açık Kaynak Geliştirici</td>
            </tr>
            <tr>
                <td><strong>Kaynak Depo (Repository):</strong></td>
                <td><a href="https://github.com/mserman90/suhaber" target="_blank" rel="noopener noreferrer">github.com/mserman90/suhaber</a></td>
            </tr>
            <tr>
                <td><strong>Barındırma (Hosting):</strong></td>
                <td>GitHub Pages (GitHub Inc., 88 Colin P Kelly Jr St, San Francisco, CA 94107, USA)</td>
            </tr>
            <tr>
                <td><strong>Derleme Otomasyonu:</strong></td>
                <td>GitHub Actions CI/CD (Python 3 &bull; Günlük Otomatik Besleme & Senkronizasyon)</td>
            </tr>
        </tbody>
    </table>
</div>

<div class="legal-section">
    <h4>2. Telif Hakları, Atıf ve 5846 Sayılı FSEK İlkeleri</h4>
    <p>
        Portalda yer verilen haberler, fotoğraflar ve makale özetleri; <strong>5846 sayılı Fikir ve Sanat Eserleri Kanunu ("FSEK")</strong> ve basın mevzuatı
        kapsamında adil kullanım (fair use) ve kamuoyunun haber alma hürriyeti çerçevesinde kaynak gösterilerek alıntılanmaktadır.
    </p>
    <ul class="legal-list">
        <li>Her haber kartında ve modal detayında haberin asıl kaynağı (ajans, gazete, resmi kurum veya dergi adı) ile orijinal haber linki açıkça belirtilmiştir.</li>
        <li>Haberlerin fikri mülkiyeti ve telif hakları ilgili orijinal kaynak ve yayıncı kuruluşa aittir.</li>
        <li>Haber görselleri lisanslı açık fotoğraf kütüphanelerinden (Unsplash API) veya ilgili yayının kamuya açık basın bültenlerinden temin edilmektedir.</li>
        <li>Telif hakkı sahibi olduğunu kanıtlayan kişi veya kurumların haklı içerik kaldırma (take-down notice) talepleri en geç 24 saat içerisinde incelenerek işleme alınır.</li>
    </ul>
</div>
"""

LEGAL_IMPRINT_EN = """
<div class="legal-section">
    <h4>1. Imprint & Platform Ownership</h4>
    <table class="legal-table">
        <tbody>
            <tr>
                <td><strong>Publication:</strong></td>
                <td>Water, Agriculture & Livestock Digital Newspaper (Water Agenda &bull; Agriculture Agenda &bull; Livestock Agenda)</td>
            </tr>
            <tr>
                <td><strong>Nature:</strong></td>
                <td>Open-access, non-profit digital newspaper and GIS data portal</td>
            </tr>
            <tr>
                <td><strong>Repository:</strong></td>
                <td><a href="https://github.com/mserman90/suhaber" target="_blank" rel="noopener noreferrer">github.com/mserman90/suhaber</a></td>
            </tr>
            <tr>
                <td><strong>Hosting:</strong></td>
                <td>GitHub Pages (GitHub Inc., San Francisco, CA)</td>
            </tr>
            <tr>
                <td><strong>Automation:</strong></td>
                <td>GitHub Actions CI/CD Pipeline (Scheduled Python scraping & static publishing)</td>
            </tr>
        </tbody>
    </table>
</div>

<div class="legal-section">
    <h4>2. Copyright & Intellectual Property Attribution</h4>
    <p>
        News articles, research papers, and media excerpts are curated under fair use journalistic doctrines. Full attribution with direct canonical hyperlinks
        is provided for every story. Original intellectual property rights remain strictly with the respective content owners and news agencies.
    </p>
</div>
"""

def render_footer_legal_bar_html() -> str:
    """
    Gazete altbilgisinde yer alan şık yasal bağlantılar çubuğu.
    """
    return """
            <!-- Legal & KVKK Links Bar -->
            <div class="footer-legal-bar" role="navigation" aria-label="Yasal Bildirimler">
                <button type="button" class="footer-legal-btn" onclick="openLegalModal('disclaimer')" title="Yasal Sorumluluk Reddi Beyanını Oku">
                    <span class="legal-icon">⚖️</span>
                    <span data-i18n="legal_disclaimer_btn">Yasal Sorumluluk Reddi</span>
                </button>
                <span class="footer-sep">&bull;</span>
                <button type="button" class="footer-legal-btn" onclick="openLegalModal('kvkk')" title="6698 Sayılı KVKK ve Gizlilik Politikası">
                    <span class="legal-icon">🔒</span>
                    <span data-i18n="legal_kvkk_btn">KVKK &amp; Gizlilik Beyanı</span>
                </button>
                <span class="footer-sep">&bull;</span>
                <button type="button" class="footer-legal-btn" onclick="openLegalModal('imprint')" title="Künye, Telif Hakları ve İletişim">
                    <span class="legal-icon">ℹ️</span>
                    <span data-i18n="legal_imprint_btn">Künye &amp; Atıf Politikası</span>
                </button>
                <span class="footer-sep">&bull;</span>
                <a href="yasal.html" target="_blank" rel="noopener noreferrer" class="footer-legal-link" title="Yasal Beyanları Ayrı Sayfada Aç">
                    <span class="legal-icon">📄</span>
                    <span data-i18n="legal_standalone_link">Tam Metin (Ayrı Sayfa)</span>
                    <span class="ext-icon">↗</span>
                </a>
            </div>

            <div class="footer-disclaimer-preview">
                <p class="footer-micro-disclaimer" id="footerMicroDisclaimer">
                    <strong>⚖️ Yasal Uyarı:</strong> Bu portalda yer alan haber, emtia ve borsa verileri açık kaynaklardan derlenmiş olup, yatırım veya ticari danışmanlık niteliği taşımaz. 6698 sayılı KVKK kapsamında ziyaretçilerden kişisel veri toplanmamaktadır.
                </p>
            </div>
    """

def render_legal_modal_html() -> str:
    """
    Portala gömülecek zengin, sekmeli ve çift dilli yasal modal penceresi.
    """
    return f"""
    <!-- Legal & KVKK Modal -->
    <div class="modal-backdrop" id="legalModal" onclick="closeLegalModal(event)" role="dialog" aria-labelledby="legalModalTitle" aria-modal="true">
        <div class="modal-window legal-modal-window" onclick="event.stopPropagation()">
            <div class="modal-header legal-modal-header">
                <div class="legal-header-titles">
                    <span class="legal-badge" id="legalModalBadge">HUKUKİ BİLGİLENDİRME &amp; ŞEFFAFLIK BEYANI</span>
                    <h3 class="legal-modal-title" id="legalModalTitle">Yasal Sorumluluk Reddi ve KVKK Bildirimi</h3>
                </div>
                <button type="button" class="btn-close-modal" onclick="closeLegalModal()" title="Pencereyi Kapat">&times;</button>
            </div>
            
            <!-- Modal Tabs Bar -->
            <div class="legal-modal-tabs">
                <button type="button" class="legal-tab-btn active" id="btnLegalTab_disclaimer" onclick="switchLegalTab('disclaimer')">
                    <span class="tab-icon">⚖️</span>
                    <span data-i18n="legal_tab_disclaimer">Yasal Sorumluluk Reddi</span>
                </button>
                <button type="button" class="legal-tab-btn" id="btnLegalTab_kvkk" onclick="switchLegalTab('kvkk')">
                    <span class="tab-icon">🔒</span>
                    <span data-i18n="legal_tab_kvkk">KVKK &amp; Gizlilik Beyanı</span>
                </button>
                <button type="button" class="legal-tab-btn" id="btnLegalTab_imprint" onclick="switchLegalTab('imprint')">
                    <span class="tab-icon">ℹ️</span>
                    <span data-i18n="legal_tab_imprint">Künye &amp; Atıf Politikası</span>
                </button>
            </div>

            <!-- Modal Content Area -->
            <div class="modal-body legal-modal-body" id="legalModalBody">
                <!-- Tab 1: Yasal Sorumluluk Reddi -->
                <div class="legal-tab-pane active" id="legalPane_disclaimer">
                    <div class="legal-lang-tr">
                        {LEGAL_DISCLAIMER_TR}
                    </div>
                    <div class="legal-lang-en" style="display:none;">
                        {LEGAL_DISCLAIMER_EN}
                    </div>
                </div>

                <!-- Tab 2: KVKK & Gizlilik -->
                <div class="legal-tab-pane" id="legalPane_kvkk" style="display:none;">
                    <div class="legal-lang-tr">
                        {LEGAL_KVKK_TR}
                    </div>
                    <div class="legal-lang-en" style="display:none;">
                        {LEGAL_KVKK_EN}
                    </div>
                </div>

                <!-- Tab 3: Künye & Atıf -->
                <div class="legal-tab-pane" id="legalPane_imprint" style="display:none;">
                    <div class="legal-lang-tr">
                        {LEGAL_IMPRINT_TR}
                    </div>
                    <div class="legal-lang-en" style="display:none;">
                        {LEGAL_IMPRINT_EN}
                    </div>
                </div>
            </div>

            <!-- Modal Action Footer -->
            <div class="legal-modal-footer">
                <div class="legal-footer-left">
                    <a href="yasal.html" target="_blank" rel="noopener noreferrer" class="btn-legal-standalone">
                        <span>📄 Ayrı Sayfada Aç</span>
                        <span class="ext-icon">↗</span>
                    </a>
                </div>
                <div class="legal-footer-right">
                    <button type="button" class="btn-legal-close" onclick="closeLegalModal()">
                        <span data-i18n="legal_close_btn">Anladım ve Kapat</span>
                    </button>
                </div>
            </div>
        </div>
    </div>
    """

def generate_standalone_legal_html(last_updated: str) -> str:
    """
    Ayrı bir URL olarak sunulacak müstakil 'yasal.html' sayfası üreticisi.
    """
    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Yasal Sorumluluk Reddi ve KVKK Beyanı | Su, Tarım ve Hayvancılık Portalı</title>
    
    <meta name="description" content="Su, Tarım ve Hayvancılık Dijital Gazete Portalı Yasal Sorumluluk Reddi, 6698 Sayılı KVKK ve Gizlilik Politikası ile Künye ve Telif Hakları Şeffaflık Metni.">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://mserman90.github.io/suhaber/yasal.html">
    <meta name="theme-color" content="#0a192f">

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800;900&family=Merriweather:ital,wght@0,300;0,400;0,700;1,300;1,400&family=Public+Sans:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,600;0,800;0,900;1,400;1,700&display=swap" rel="stylesheet">

    <style>
        :root {{
            --bg-body: #f8fafc;
            --surface-card: #ffffff;
            --text-main: #1e293b;
            --text-muted: #64748b;
            --border-line: #e2e8f0;
            --primary-blue: #0284c7;
            --primary-hover: #0369a1;
            --badge-bg: #e0f2fe;
            --badge-text: #0369a1;
            --alert-bg: #fffbeb;
            --alert-border: #fde68a;
            --alert-text: #92400e;
        }}
        [data-theme="dark"] {{
            --bg-body: #0b1526;
            --surface-card: #132238;
            --text-main: #f1f5f9;
            --text-muted: #94a3b8;
            --border-line: #1e3a5f;
            --primary-blue: #38bdf8;
            --primary-hover: #7dd3fc;
            --badge-bg: #0c2d48;
            --badge-text: #7dd3fc;
            --alert-bg: #2d2412;
            --alert-border: #5a420b;
            --alert-text: #fef08a;
        }}

        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: 'Public Sans', system-ui, sans-serif;
            background: var(--bg-body);
            color: var(--text-main);
            line-height: 1.65;
            padding-bottom: 60px;
        }}

        .legal-page-header {{
            background: var(--surface-card);
            border-bottom: 2px solid var(--border-line);
            padding: 24px 20px;
            position: sticky;
            top: 0;
            z-index: 100;
        }}
        .header-container {{
            max-width: 960px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 16px;
        }}
        .logo-title {{
            font-family: 'Playfair Display', serif;
            font-size: 1.4rem;
            font-weight: 800;
            color: var(--text-main);
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .nav-actions {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .btn-nav {{
            padding: 8px 14px;
            font-size: 13px;
            font-weight: 600;
            border-radius: 6px;
            text-decoration: none;
            border: 1px solid var(--border-line);
            background: var(--surface-card);
            color: var(--text-main);
            cursor: pointer;
            transition: all 0.2s;
        }}
        .btn-nav:hover {{
            border-color: var(--primary-blue);
            color: var(--primary-blue);
        }}
        .btn-nav.primary {{
            background: var(--primary-blue);
            color: #ffffff;
            border-color: var(--primary-blue);
        }}
        .btn-nav.primary:hover {{
            background: var(--primary-hover);
        }}

        .legal-page-main {{
            max-width: 960px;
            margin: 40px auto;
            padding: 0 20px;
        }}
        .legal-card {{
            background: var(--surface-card);
            border: 1px solid var(--border-line);
            border-radius: 12px;
            padding: 40px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.06);
            margin-bottom: 30px;
        }}
        @media (max-width: 640px) {{
            .legal-card {{ padding: 24px 18px; }}
        }}

        .main-legal-title {{
            font-family: 'Playfair Display', serif;
            font-size: 2.2rem;
            font-weight: 800;
            margin-bottom: 12px;
            letter-spacing: -0.5px;
        }}
        .main-legal-subtitle {{
            color: var(--text-muted);
            font-size: 1rem;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 1px solid var(--border-line);
        }}

        .legal-section {{
            margin-bottom: 32px;
        }}
        .legal-section h4 {{
            font-family: 'Playfair Display', serif;
            font-size: 1.25rem;
            font-weight: 700;
            margin-bottom: 12px;
            color: var(--text-main);
        }}
        .legal-section p {{
            margin-bottom: 14px;
            font-size: 14.5px;
            color: var(--text-main);
        }}

        .legal-alert-box {{
            background: var(--alert-bg);
            border: 1px solid var(--alert-border);
            color: var(--alert-text);
            padding: 14px 18px;
            border-radius: 8px;
            font-size: 14px;
            margin-bottom: 16px;
        }}
        .legal-badge-pill {{
            display: inline-block;
            background: var(--badge-bg);
            color: var(--badge-text);
            font-size: 12px;
            font-weight: 700;
            padding: 4px 10px;
            border-radius: 20px;
            margin-bottom: 14px;
        }}
        .legal-list {{
            margin-left: 20px;
            margin-bottom: 16px;
            font-size: 14px;
        }}
        .legal-list li {{
            margin-bottom: 8px;
        }}
        .legal-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13.5px;
            margin-top: 10px;
        }}
        .legal-table td {{
            padding: 10px 14px;
            border-bottom: 1px solid var(--border-line);
        }}
        .legal-table td:first-child {{
            width: 30%;
            white-space: nowrap;
        }}

        .legal-page-footer {{
            max-width: 960px;
            margin: 0 auto;
            text-align: center;
            font-size: 13px;
            color: var(--text-muted);
            padding: 20px;
        }}
    </style>
</head>
<body>
    <header class="legal-page-header">
        <div class="header-container">
            <a href="index.html" class="logo-title">
                <span>🌊</span>
                <span>Su, Tarım ve Hayvancılık Portalı</span>
            </a>
            <div class="nav-actions">
                <a href="index.html" class="btn-nav">💧 Su</a>
                <a href="tarim.html" class="btn-nav">🌾 Tarım</a>
                <a href="hayvancilik.html" class="btn-nav">🐄 Hayvancılık</a>
                <button type="button" class="btn-nav primary" onclick="toggleTheme()" id="themeBtn">🌓 Tema</button>
            </div>
        </div>
    </header>

    <main class="legal-page-main">
        <div class="legal-card">
            <h1 class="main-legal-title">Hukuki Bildirimler, Yasal Sorumluluk Reddi ve KVKK Beyanı</h1>
            <p class="main-legal-subtitle">
                Yürürlük Tarihi: 01.11.2026 &bull; Son Güncelleme: {last_updated} &bull; Şeffaflık ve Veri Güvenliği İlkesi
            </p>

            <article id="disclaimer">
                <h2 style="font-family:'Playfair Display', serif; font-size:1.6rem; margin-bottom:20px; color:var(--primary-blue);">
                    ⚖️ Yasal Sorumluluk Reddi Beyanı (Legal Disclaimer)
                </h2>
                {LEGAL_DISCLAIMER_TR}
                <hr style="border:none; border-top:1px dashed var(--border-line); margin:40px 0;">
                <h3 style="font-family:'Playfair Display', serif; font-size:1.3rem; margin-bottom:16px;">English Summary</h3>
                {LEGAL_DISCLAIMER_EN}
            </article>

            <hr style="border:none; border-top:2px solid var(--border-line); margin:50px 0;">

            <article id="kvkk">
                <h2 style="font-family:'Playfair Display', serif; font-size:1.6rem; margin-bottom:20px; color:var(--primary-blue);">
                    🔒 6698 Sayılı KVKK ve Gizlilik Politikası
                </h2>
                {LEGAL_KVKK_TR}
                <hr style="border:none; border-top:1px dashed var(--border-line); margin:40px 0;">
                <h3 style="font-family:'Playfair Display', serif; font-size:1.3rem; margin-bottom:16px;">Privacy Summary (GDPR / KVKK)</h3>
                {LEGAL_KVKK_EN}
            </article>

            <hr style="border:none; border-top:2px solid var(--border-line); margin:50px 0;">

            <article id="imprint">
                <h2 style="font-family:'Playfair Display', serif; font-size:1.6rem; margin-bottom:20px; color:var(--primary-blue);">
                    ℹ️ Künye, Telif Hakları ve İletişim
                </h2>
                {LEGAL_IMPRINT_TR}
            </article>
        </div>
    </main>

    <footer class="legal-page-footer">
        <p>© 2026 Su, Tarım & Hayvancılık Dijital Gazete Portalı. Tüm hakları saklıdır.</p>
        <p style="margin-top:6px;">Açık Kaynak Kod Deposu: <a href="https://github.com/mserman90/suhaber" target="_blank" rel="noopener noreferrer" style="color:var(--primary-blue);">mserman90/suhaber</a></p>
    </footer>

    <script>
        function toggleTheme() {{
            const cur = document.documentElement.getAttribute('data-theme') || 'light';
            const next = cur === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', next);
            localStorage.setItem('su_portal_theme', next);
        }}
        (function() {{
            const saved = localStorage.getItem('su_portal_theme');
            const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
            if (saved === 'dark' || (!saved && prefersDark)) {{
                document.documentElement.setAttribute('data-theme', 'dark');
            }}
        }})();
    </script>
</body>
</html>
"""
