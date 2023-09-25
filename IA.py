import spacy
from spacy.matcher import Matcher

nlp = spacy.load("es_dep_news_trf") #Versión más pesada y precisa del modelo de NLR

matcher = Matcher(nlp.vocab)

directions = {  "arriba" : [4, 135], 
                "abajo" : [4, 45],
                "izquierda" : [1, 135],
                "derecha" : [1, 45],
                "frente" : [3, 135],
                "atrás" : [3, 45],
                } #Direcciones, servos y grados
mov_vars = ["mover", "muévete", "movetar"] #Variaciones del verbo mover, por nuestro hacento

patterns = [] #Se carga un diccionario con las variaciones de mover y las direcciones para crear la o las oraciones que tiene que reconocer
for mov in mov_vars:
    for direction in directions:
        pattern = [{"LEMMA": mov},{"POS": "ADP", "OP": "?"}, {"POS": "DET", "OP": "?"}, {"POS": "NOUN", "OP": "?"}, {"POS": "ADP", "OP": "?"}, {"LEMMA": direction}]
        patterns.append(pattern)
matcher.add("mover", patterns) #Se añade la rule al modelo

pattern = [{"LEMMA": "hola"}] #Otra rule para el saludo
matcher.add("saludo", [pattern])


def DocTypeRec(STT): #Fucnión de "inicio" que agarra el texto y decide qué rule se disparó y eligiendo la función para esa rule
    doc = nlp(STT)
    matches = matcher(doc)
    for match_id, start, end in matches:
        string_id = nlp.vocab.strings[match_id] 
        break
    if string_id == "mover":
        return defined_mov(doc) 
    if string_id == "saludo":
        return Hola() 

def defined_mov(doc): #Función de movimiento predefinido
    matches = matcher(doc) #Trata de reconocer la oración
    servo, grados = 0, 0
    for match_id, start, end in matches:
        matched_span = doc[start:end]
        print(matched_span)
        for token in matched_span: #Si reconoció la rule, recorre las palabras de la oración
            text = token.text
            if token.pos_ == "ADV" or token.pos_ == "NOUN": #Si reconoce un advervio(arriba o abajo) o un pronombre(derecha o izquierda)
                if text in directions: #Recorre el diccionario de direcciones y devuelve el servo y los grados
                    servo = directions[text][0]
                    grados = directions[text][1]
                    #print(f"{text}. Servo nro {servo}, grados: {grados}")            
                    return servo, grados
                
def Hola(): #La función mueve el servo 3(frente y atrás), luego abre y cierra la garra 2 veces
    saludo = [[3,60],[2,180],[2,10],[2,180],[2,10]]
    return saludo
                
def DescomponeOracion(doc): #Función de debugueo, sirve para descomponer una oración y ver cada uno de sus componentes
    doc = nlp(doc)
    matches = matcher(doc)
    for token in doc:
        print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)
    for match_id, start, end in matches:
        matched_span = doc[start:end]

#DescomponeOracion("mover a la izquierda")