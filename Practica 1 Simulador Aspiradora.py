#Practica 1- Simulador Aspiradora
#Materia: Inteligencia Artificial
#Esparza Kenia
#Salcedo Alexa
#Farfan de Leon Jose Osvaldo

def main():
    habitaciones = [] #lista que contrendra las habitaciones
    numerohabitaciones = int(input("Ingrese el numero de habitaciones: "))#definimos el numero de habitaciones

    for i in range(numerohabitaciones):
        habitacion = []#lista que contendra los estatus de numero de habitacion, basura,estatus de donde esta la aspiradora
        habitacion.append(i) #Identificador de la habitacion
        habitacion.append(int(input(f"Ingrese el estado de la habitacion {i}(0 = limpia, 1 = sucia): ")))# 0 limpia, 1 sucia
        habitacion.append(0)#aspiradora no esta aqui
        habitaciones.append(habitacion)#agregamos la lista pequeña a la lista de habitaciones
    
    aspiradora = int(input("Ingrese la habitacion en la que esta la aspiradora: "))#preguntamos en donde esta la aspiradora
    habitaciones[aspiradora][2] = 1 #definimos en nuestra lista donde esta la aspiradora

    print(habitaciones)#mostramos las habitaciones y los estatus de cada
    
main()