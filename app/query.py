import re

"""
Запись для корпусных запросов
Токен: [lex:...][gr:...][add:...], где
    указаны лексические, грамматические и дополнительные параметры
    
Расстояние: {n}; {_, a}; {_, b}; {a, b} ,
    аналогично формату НКРЯ
"""


class CorpusQuery:
    def __init__(self, query):
        self.parser = re.compile(r'''
        (?P<class> \[|{) # token or a distance pattern?
        (?P<content>
            (?P<type>lex|add|gr):(?P<properties>[^\]]+)\] # if it's a token, then lex/add/gr?
            | (?P<limits>[\d,_]+)\} # if it's a d pattern, what are the limits?
        )''', re.X)
        self.class_token = "["
        self.class_distance = "{"
        self.query = query

    def decode(self):
        result = [{"class": "token"}]
        for item in self.parser.finditer(self.query):
            if item.group("class") == self.class_token:
                result[-1][item.group("type")] = item.group("properties").split(",")
            elif item.group("class") == self.class_distance:
                result.append({
                    "class": "distance",
                    "limits": item.group("limits").split(",")
                })
                result.append({"class": "token"})
        return result

    def to_markup(self):

        def item_to_markup(item):
            if item["class"] == "distance":
                if len(item["limits"]) == 1:
                    if item["limits"][0] == "_":
                        return "<br>на любом расстоянии от "
                    else:
                        return f"<br> на расстоянии {item['limits'][0]} от "
                else:
                    if item["limits"][0] == "_":
                        if int(item["limits"][1]) >= 0:
                            return f"<br> на расстоянии (от начала предложения до {item['limits'][1]}) от "
                        else:
                            return f"<br> на расстоянии (от {item['limits'][1]-1} до {item['limits'][1]}) от "
                    elif item["limits"][1] == "_":
                        if int(item["limits"][0]) < 0:
                            return f"<br> на расстоянии (от {item['limits'][1]} до конца предложения) от "
                        else:
                            return f"<br> на расстоянии (от {item['limits'][1]} до {item['limits'][1]+1}) от "
                    else:
                        return f"<br> на расстоянии (от {item['limits'][0]} до {item['limits'][1]}) от "
            elif item["class"] == "token":
                r = []
                if "lex" in item:
                    r.append(f"<b>{item['lex'][0]}</b>")
                if "gr" in item:
                    r.append(" ".join([f"<small>{x}</small>" for x in item["gr"]]))
                if "add" in item:
                    r.append(" ".join([f"<small>{x}</small>" for x in item["add"]]))
                return " ".join(r)

        return "\n".join(item_to_markup(item) for item in self.decode())
