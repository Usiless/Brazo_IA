import spacy
from spacy.matcher import Matcher

nlp = spacy.load("es_dep_news_trf")

matcher = Matcher(nlp.vocab)

directions = {  "arriba" : [4, 135], 
                "abajo" : [4, 45],
                "izquierda" : [1, 135],
                "derecha" : [1, 45],
                "frente" : [3, 135],
                "atrás" : [3, 45],
                }
mov_vars = ["mover", "muévete", "movetar"]

patterns = []
for mov in mov_vars:
    for direction in directions:
        pattern = [{"LEMMA": mov},{"POS": "ADP", "OP": "?"}, {"POS": "DET", "OP": "?"}, {"POS": "NOUN", "OP": "?"}, {"POS": "ADP", "OP": "?"}, {"LEMMA": direction}]
        patterns.append(pattern)
matcher.add("mover", patterns)

pattern = [{"LEMMA": "hola"}]
matcher.add("saludo", [pattern])


def DocTypeRec(STT):
    doc = nlp(STT)
    matches = matcher(doc)
    for match_id, start, end in matches:
        string_id = nlp.vocab.strings[match_id] 
        break
    if string_id == "mover":
        return defined_mov(doc) 
    if string_id == "saludo":
        return Hola() 

def defined_mov(doc):
    matches = matcher(doc)
    servo, grados = 0, 0
    for match_id, start, end in matches:
        matched_span = doc[start:end]
        print(matched_span)
        for token in matched_span:
            text = token.text
            if token.pos_ == "ADV" or token.pos_ == "NOUN":
                if text in directions:
                    servo = directions[text][0]
                    grados = directions[text][1]
                    #print(f"{text}. Servo nro {servo}, grados: {grados}")            
                    return servo, grados
                
def Hola():
    saludo = [[3,60],[2,180],[2,10],[2,180],[2,10]]
    return saludo
                
def DescomponeOracion(doc):
    doc = nlp(doc)
    matches = matcher(doc)
    for token in doc:
        print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)
    for match_id, start, end in matches:
        matched_span = doc[start:end]

DescomponeOracion("mover a la izquierda")