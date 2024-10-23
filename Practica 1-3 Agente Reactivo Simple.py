#Practica 1- Simulador Aspiradora (Parte 2 y 3)
#Alexa Salcedo Arellano
#Esparza Duran Kenia Jaqueline
#Farfan de Leon Jose Osvaldo

def left(habitaciones,aspiradora,min):
    posicion = aspiradora
    aux = posicion
    movimientos = 0
    posicion_aux = posicion
    #Izquierda
    print(f'aux{min}')
    for i in range(min,posicion+1):
        print(f'Aspiradora en habitacion {posicion_aux}')
        if (habitaciones[posicion_aux] == 1):
            habitaciones[posicion_aux] = 0
            movimientos += 1
        movimientos += 1
        posicion_aux -= 1
    movimientos -= 1 
    posicion = min
    print(f'posicion actual: {posicion}')
    #Derecha
    print("\nderecha")
    for i in range(posicion,len(habitaciones)):
        if(habitaciones[i] == 1):
            print(f'La habitacion {i} esta sucia')
            min = i
        else:
            print(f'habitacion {i} limpia')
    for i in range(posicion,min+1):
        print(f'Aspiradora en habitacion {i}')
        if(habitaciones[i] == 1):
            habitaciones[i] = 0
            movimientos += 1
        movimientos += 1 
    movimientos -= 1       
    print(f'El total de movimientos fue {movimientos}')
    return movimientos


def right(habitaciones,aspiradora):
    posicion = aspiradora
    aux = posicion
    movimientos = 0
    posicion_aux = posicion
    for i in range(posicion,len(habitaciones)):
        if(habitaciones[i] == 1):
            print(f'La habitacion {i} esta sucia')
            aux = i
        else:
            print(f'habitacion {i} limpia')
    for i in range(posicion,aux+1):
        print(f'Aspiradora en habitacion {i}')
        if(habitaciones[i] == 1):
            habitaciones[i] = 0
            movimientos += 1
        movimientos += 1
    movimientos -= 1  
    posicion = aux+1
    print(f'posicion actual: {posicion}')
    posicion_aux = posicion-1
    #Izquierda
    print("\nIzquierda")
    for i in range(0,posicion):#recorremos a izquierda
        if (habitaciones[(posicion-1)-i] == 1):#verificamos si esta limpia o sucia
            print(f'La habitacion {(posicion-1)-i} esta sucia')
            aux = (posicion-1)-i#ubica la habitacion sucia mas a la izquierda
    print(f'aux{aux}')
    for i in range(aux,posicion):
        print(f'Aspiradora en habitacion {posicion_aux}')
        
        if (habitaciones[posicion_aux] == 1):
            habitaciones[posicion_aux] = 0
            movimientos += 1
        movimientos += 1
        posicion_aux -= 1   
    movimientos -= 1     
    print(f'El total de movimientos fue {movimientos}')
    return movimientos


def main():
    habitaciones = [] #numero y estatus 
    max = 0
    min = 99999
    numerohabitaciones = int(input("Ingrese el numero de habitaciones: "))#numero de habitaciones
    
    for i in range(numerohabitaciones):#recorremos para insertar la suciedad
        x = int(input(f"Ingrese el estado de la habitacion {i}(Limpia = 0, Sucia = 1): "))#preguntamos si esta sucia
        if(x == 1):
            habitaciones.append(1)# agregamos 
            if i < min: min = i
            if i > max: max = i
        else:
            habitaciones.append(0)
        
    habitaciones2 = habitaciones.copy()
    aspiradora = int(input("Ingrese la habitacion en la que esta la aspiradora: "))

    derecha = right(habitaciones,aspiradora)#vamos a la funcion que recorrera a la izquierda
    print("\n\n\n-----------------------------------------------------------------------------------------------\n\n\n")
    izquierda = left(habitaciones2,aspiradora,min)#vamos a la funcion que recorrera a la izquierda
    promedio = (derecha + izquierda) / 2
    print(f'Configuracion media global = {promedio}')
    bateria =20 
    if (derecha < izquierda):
        bateria -= derecha
        print(f'Queda {bateria}% de bateria')
    else:
        bateria -= izquierda
        print(f'Queda {bateria}% de bateria')
main()