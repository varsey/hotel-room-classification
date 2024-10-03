def get_view(query):
    if 'view' in query:
        words = [x for x in (''.join(query.split('view')[0]) + ' view').split(' ') if len(x) > 1]
        res = ' '.join([words[words.index("view") - 1], words[words.index("view")]])
        res = res.replace('harbor', 'harbour').replace('urban', 'city')
        if 'partial' in words:
            res = f'partial-{res}'
        return res
    elif 'front' in query:
        words = [x for x in (''.join(query.split('front')[0]) + ' front').split(' ') if len(x) > 1]
        res = ' '.join([words[words.index("front") - 1], words[words.index("front")]])
        return res
    return 'undefined'

def get_capacity(query):
    if 'triple' in query or '3' in query:
        return 'triple'
    elif 'quadruple' in query or '2 queen bed' in query or '2 double bed' in query or 'two queen bed' in query or 'two double bed' in query:
        return 'quadruple'
    elif '6'  in query or 'sextuple' in query:
        return 'sextuple'
    elif '5' in query or 'quintuple' in query:
        return 'quintuple'
    elif query.count('single') == 1 or query.count('sgl') == 1 or query.count('s g l') == 1:
        return 'single'
    elif query.count('double') == 1 or query.count('dbl') == 1 or query.count('d b l') == 1 or query.count('twin') == 1 or '1 king bed' in query:
        return 'double'
    return 'undefined'

