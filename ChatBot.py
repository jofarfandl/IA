#Tarea 1 IA 
#Esparza Duran Kenia Jaqueline
#Farfan de Leon Jose Osvaldo
#Salcedo Arellano Alexa
import re
import random
minombre = ' '


def get_response(texo_usuario):
    split_message = re.split(r'\s|[,:;.?!-_]\s*', texo_usuario.lower())#quitaremos todos los signos que no nos sirven y aplicaremos minusculas a todo
    response = check_all_messages(split_message) #revisamos todas las posibles respuestas
    return response#regresamos la respuestas posibles

def message_probability(mensaje_usuario, palabras_reconocidas, single_response=False, palabras_requeridas=[]):
    message_certainty = 0
    palabras_validas = True

    for word in mensaje_usuario:
        if word in palabras_reconocidas:
            message_certainty +=1

    percentage = float(message_certainty) / float (len(palabras_reconocidas))#porcentaje de exactitud de que el mensaje sea el mas adecuado a responder

    for word in palabras_requeridas:
        if word not in mensaje_usuario:
            palabras_validas = False
            break
    if palabras_validas or single_response:
        return int(percentage * 100)
    else:
        return 0

def check_all_messages(message):
        highest_prob = {}
        def response(bot_response, list_of_words, single_response = False, required_words = []):
            nonlocal highest_prob
            highest_prob[bot_response] = message_probability(message, list_of_words, single_response, required_words)

        response('Hola', ['hola', 'hello', 'Saludos', 'Buenas tardes','Buenos dias', 'Buenas noches'], single_response = True)
        response('Estoy bien y tu?', ['como', 'estas', 'va', 'vas', 'sientes'], required_words=['estas'])
        response('Me alegra mucho',['estoy, muy, bien, gracias'], required_words=['estoy'])
        response('Mi nombre es Robert Pattinson, tienes un lindo nombre por cierto',['Cual','es','tu','nombre','como','llamas'], required_words=['llamas'])
        response('Actualmente vivo en mi mansion en Hollywood, y tu?', ['donde', 'ubicacion','vives'], single_response=True)
        response('Que interesante',['vivo','en'],required_words=['vivo'])
        response('Espero poder hacerlo pronto',['si','deberias','venir'], required_words=['deberias'])
        response('Soy actor',['en','que','trabajas'], required_words=['trabajas'])
        response('Las hamburguesas de la cadena In and Out',['cual','es','tu','comidad','favorita'], required_words=['comida','favorita'])
        response('El piano',['tocas','algun','instrumento'], required_words=['tocas','instrumento'])
        response('Tengo 36 años, y tu?',['cuantos', 'años', 'tienes'], required_words=['cuantos'])
        response('No se te nota la edad',['tengo', 'años'],required_words=['tengo'])
        response(grateful(),['gracias', 'te lo agradezco', 'thanks'], required_words=['gracias'])
        response('Naci en Reino Unido y tu?',['donde','naciste'], required_words=['donde'])
        response('Es un gran pais, quisiera visitarlo algun dia',['naci','en','yo'], required_words=['naci', 'en'])
        response('13 de Mayo de 1986',['cuando','naciste'], required_words=['cuando'])
        response('Mi pelicula favorita es Prenom Carmen y la tuya?',['cual', 'es', 'tu','pelicula','favorita'], required_words=['cual','pelicula'])
        response('Es una gran pelicula, tienes buenos gustos',['mi', 'mia', 'es','mi','pelicula', 'favorita','me', 'gusta'], required_words=['mi','pelicula','favorita'])
        response('Me gusta mucho el color negro y a ti?',['cual','es','tu','color','favorito','preferido'], required_words=['tu','color'])
        response('Es un color muy bonito',['mi','color','favorito','es','me','gusta','el'], required_words=['mi','color','me','gusta'])
        response('Tambien yo, hey! Ya tenemos algo en comun',['estoy','muy','feliz','cansada','cansado','triste'], required_words=['estoy','muy'])
        response('Adios, fue un gusto conocerte!!',['tengo', 'que','irme', 'ya','me','voy','adios'], required_words= ['adios'])
        best_match = max(highest_prob, key=highest_prob.get)#verifica cual es la mejor opcion a responder
        return unknown() if highest_prob[best_match] < 1 else best_match #en caso de no encontrar nada en comun va a funcion unknown
        

def unknown():#solo muestra una opcion random que no entiende lo que escribio
    response = ['Lo siento, no puedo entenderte', 'No estoy seguro de lo quieres', 'Intenta decirlo de otra manera'][random.randrange(3)]
    return response

def grateful():#solo muestra una opcion random que no entiende lo que escribio
    response = ['Por nada', 'No hay de que', 'No es nada'][random.randrange(3)]
    return response

minombre = input('Dime cual es tu nombre para poder conocerte mejor...\n')
while True:  #Funcion que siempre estara preguntando al usuario
    print("Bot: " + get_response(input(minombre+":")))#recibira un parametro de parte del usuario