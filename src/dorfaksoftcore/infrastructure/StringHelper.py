# coding=utf-8
import re
import traceback
from random import choice
from string import ascii_uppercase, ascii_letters, digits


class StringHelper:
    STOP_WORD_REGEX = "[, \-!?:\n،_#.]+"

    @staticmethod
    def correctionNumber(str):
        if str == "" or str is None:
            return "0"
        else:
            str = re.sub('[^0-9]', '', StringHelper.toEnglishNumber(str))
            return str

    @staticmethod
    def randomString(len):
        return ''.join(choice(ascii_uppercase) for i in range(len))

    @staticmethod
    def strs_diff(str1, str2):
        # تقسیم رشته به کلمات با استفاده از split()
        set1 = set(str1.split())
        set2 = set(str2.split())
        # محاسبه تفاوت مجموعه‌ها
        diff_set = set2.difference(set1)
        # چاپ کلماتی که در دو رشته متفاوت هستند
        return ' '.join(diff_set)

    @staticmethod
    def randomNumberString(len):
        return ''.join(choice(ascii_letters + digits) for i in range(len))

    @staticmethod
    def human_format(num, with_tag=False):
        n = float('{:.3g}'.format(num))
        magnitude = 0
        while abs(n) >= 1000:
            magnitude += 1
            n /= 1000.0
        fr = "{}<span class='format-label'>{}</span>" if with_tag else "{}{}"
        return fr.format('{:f}'.format(n).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

    @staticmethod
    def formatNumber(num):
        return "{:,}".format(num)

    @staticmethod
    def toEnglishNumber(inp):
        if inp and isinstance(inp, str):
            return inp.replace("۰", "0").replace("۱", "1").replace("۲", "2").replace("۳", "3").replace("۴", "4") \
                .replace("۵", "5").replace("۶", "6").replace("۷", "7").replace("۸", "8").replace("۹", "9") \
                .replace("٠", "0").replace("١", "1").replace("٢", "2").replace("٣", "3").replace("٤", "4") \
                .replace("٥", "5").replace("٦", "6").replace("٧", "7").replace("٨", "8").replace("٩", "9")
        return inp

    @staticmethod
    def toPersianChar(inp):
        inp = re.sub('ك', 'ک', inp)
        inp = re.sub('ګ', 'ک', inp)
        inp = re.sub('ي', 'ی', inp)
        inp = re.sub('ي', 'ی', inp)
        inp = re.sub('ۍ', 'ی', inp)
        inp = re.sub('ې', 'ی', inp)
        inp = re.sub('أ', 'ا', inp)
        inp = re.sub('إ', 'ا', inp)
        inp = re.sub('ٱ', 'ا', inp)
        inp = re.sub('ٲ', 'ا', inp)
        inp = re.sub('ٳ', 'ا', inp)
        inp = re.sub('ٵ', 'ا', inp)
        inp = re.sub('ؤ', 'و', inp)
        inp = re.sub('ٶ', 'و', inp)
        inp = re.sub('ٷ', 'و', inp)
        inp = re.sub('ٶ', 'و', inp)
        inp = re.sub(' ً', '', inp)
        return inp

    @staticmethod
    def toPersianNumber(inp):
        inp = str(inp)
        char_to_replace = {'0': '۰',
                           '1': '۱',
                           '2': '۲',
                           '3': '۳',
                           '4': '۴',
                           '5': '۵',
                           '6': '۶',
                           '7': '۷',
                           '8': '۸',
                           '9': '۹'}
        for key, value in char_to_replace.items():
            inp = inp.replace(key, value)
        return inp

    @staticmethod
    def farsi2finglish(strFarsi):
        d = {'۱': "1",
             '۲': "2",
             '۳': "3",
             '۴': "4",
             '۵': "5",
             '۶': "6",
             '۷': "7",
             '۸': "8",
             '۹': "9",
             '۰': "0",
             'آ': 'aa',
             'ا': 'a',
             'ب': 'b',
             'پ': 'p',
             'ت': 't',
             'ث': 's',
             'ج': 'j',
             'چ': 'ch',
             'ح': 'h',
             'خ': 'kh',
             'د': 'd',
             'ذ': 'z',
             'ر': 'r',
             'ز': 'z',
             'س': 's',
             'ش': 'sh',
             'ص': 's',
             'ض': 'z',
             'ط': 't',
             'ظ': 'z',
             'ع': 'aa',
             'غ': 'gh',
             'ف': 'f',
             'ق': 'gh',
             'ك': 'k',
             'ک': 'k',
             'گ': 'g',
             'ل': 'l',
             'م': 'm',
             'ن': 'n',
             'و': 'v',
             'ه': 'h',
             'ي': 'y',
             'ی': 'y'}
        for key, val in d.items():
            strFarsi = strFarsi.replace(key, val)
        return strFarsi

    @staticmethod
    def toStandardMob(mob):
        return "0" + mob[len(mob) - 10: len(mob)]

    @staticmethod
    def str2bool(v):
        if isinstance(v, bool):
            return v
        return v.lower() in ("yes", "true", "t", "1")

    @staticmethod
    def add0(num):
        return format(num, '02')

    @staticmethod
    def getStyleCount(num):
        if num < 50:
            return "<50"
        if num < 100:
            return "+50"
        if num < 500:
            return "+100"
        if num < 1000:
            return "+500"
        if num < 10000:
            return "+%s" % StringHelper.formatNumber(int(num / 1000) * 1000)
        if num < 100000:
            return "+%s" % StringHelper.formatNumber(int(num / 10000) * 10000)
        if num < 1000000:
            return "+%s" % StringHelper.formatNumber(int(num / 100000) * 100000)

        return "+%s" % StringHelper.formatNumber(int(num / 500000) * 500000)

    @staticmethod
    def similar(a, b):
        from difflib import SequenceMatcher
        return SequenceMatcher(None, a, b).ratio()

    @staticmethod
    def splitByStopWords(s):
        return re.split(StringHelper.STOP_WORD_REGEX, s)

    @staticmethod
    def similarByWord(str1, str2):
        a = set(StringHelper.splitByStopWords(str1))
        b = set(StringHelper.splitByStopWords(str2))
        c = a.intersection(b)
        return float(len(c)) / (len(a) + len(b) - len(c))

    @staticmethod
    def htmlEncode(html):
        return html.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;') \
            .replace("'", '&#39;')

    @staticmethod
    def htmlDecode(encodedHtml):
        if encodedHtml:
            htmlCodes = (
                ("'", '&#39;'),
                ('"', '&quot;'),
                ('>', '&gt;'),
                ('<', '&lt;'),
                ('&', '&amp;')
            )
            for code in htmlCodes:
                encodedHtml = encodedHtml.replace(code[1], code[0])
            return encodedHtml

    @staticmethod
    def htmlToText(html):
        from bs4 import BeautifulSoup

        try:
            soup = BeautifulSoup(html)
        except:
            print("***** err htmlToText",html,"***",str(traceback.format_exc()))
            return ""

        return soup.get_text()

    @staticmethod
    def replace_exact_word(string, target, replacement):
        import re

        pattern = r'\b{}\b'.format(target)  # الگوی به دنبال کلمه مورد نظر
        if re.search(pattern, string):  # بررسی وجود کلمه مورد نظر در رشته
            string = re.sub(pattern, replacement, string)  # جایگزینی کلمه مورد نظر با رشته جایگزین
        return string

    @staticmethod
    def removeBadStringCharachters(txt, removeCots=False):
        if txt:
            txt = txt.replace("\u200c", " ").replace("\r\n", " ").replace("\r", " ").replace('\\r\\n', "").replace(
                "\xad", "").replace("\t", " ").replace("\ud83d", " ").replace("\udc4c", " ").replace("\ud83d",
                                                                                                     " ").replace(
                "\udc4d", " ").replace("\u200d", "").replace("\\", "|")
            if removeCots:
                txt = txt.replace("\"", " ")
            return StringHelper.removeEnter(txt)
        return txt

    @staticmethod
    def strip(txt):
        return re.sub(r"^[‌ \t]+|[‌ \t]+$", "", txt)

    @staticmethod
    def removeEnter(txt):
        return txt.replace("\r\n", " ").replace("\r", " ").replace("\n", " ")

    @staticmethod
    def removeUrlFromString(text, replaceWith=""):
        pattern = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"

        return re.sub(pattern, replaceWith, text)

    @staticmethod
    def getAllLinks(text):
        pattern = "(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-&?=%.]+"
        return re.findall(pattern, text)

    @staticmethod
    def to01(text):
        text = str(text or "").lower()
        is1 = text == "1" or text == "true" or text == "active" or text == "yes"
        return 1 if is1 else 0

    @staticmethod
    def linkUrlFromString(text, replaceWith=None):
        def repl(match):
            url = match.group(0)
            return f'<a href="{url}" rel="nofollow" target="_blank">{url}</a>'

        pattern = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"

        if not replaceWith:
            replaceWith = repl
        return re.sub(pattern, replaceWith, text)
