import re

import pymysql


class DBHelper:
    @staticmethod
    def to_fulltext_command(inp):
        fts_search_text = []
        inp=inp or ""
        # for w in re.compile('[ -()]*').split(inp.strip()):
        #-+~/\<>'":*$#@()!,.?`=%&^';
        for w in inp.strip().replace("(", " ").replace(")", " ").replace("-", " ").replace("@", " ") \
                .replace("*", " ").replace("~", " ").replace("%20", " ").replace("%", " ").replace("\"", " ") \
                .replace("\'", " ").replace("<", " ").replace(">", " ").replace("+", " ").split(" "):
            if w != "":
                if len(w) < 3:
                    w = "%s*" % w
                    fts_search_text.append("%s" % w)
                else:
                    fts_search_text.append("+%s" % w)
        return ' '.join(fts_search_text)

    def getConnection(self):
        # return  pymysql.connect(host="127.0.0.1", user="root", passwd="", db="dorfaksoft_core", charset='utf8mb4', use_unicode=True)
        return pymysql.connect(host="127.0.0.1", user="root", passwd="h3DkGx9Bs0AJ", db="dorfaksoft_core",
                               charset='utf8mb4', use_unicode=True)
        # return  pymysql.connect(host="192.168.1.130", user="dbuser", passwd="", db="dorfaksoft_core", charset='utf8mb4', use_unicode=True)
        # return pymysql.connect(host="95.216.65.179", user="dbuser", passwd="0zGNtgA4apx3", db="dorfaksoft_core", charset='utf8mb4',
        #                        use_unicode=True)
