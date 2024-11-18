import math
import random
import matplotlib.pyplot as plt


class City:
    def __init__(self, x, y):
        # Coordenadas de cada ciudad
        self.x = x
        self.y = y

    #Calcular distancias entre ciudades
    def distance(self, city):
        return math.hypot(self.x - city.x, self.y - city.y)

    def __repr__(self):
        return f"({self.x}, {self.y})"


def read_cities(size, file_path ="data/cities_150.data"):
    """
    Lee las ciudades de un archivo de texto
    :param size (float): cantidad de ciudades
    :return (list): lista de ciudades (Coleccion de Objetos)

    El archivo de texto debe tener el siguiente formato:
    x1 y1
    x2 y2
    ...
    xn yn
    """
    cities = []
    with open(file_path, 'r') as handle:
        for i, line in enumerate(handle, start=1):

            x, y = map(float, line.split())
            cities.append(City(x, y))
            if i == size:
                break
    return cities


'''def write_cities_and_return_them(size):
    cities = generate_cities(size)
    with open(f'data/cities_{size}.data', 'w+') as handle:
        for city in cities:
            handle.write(f'{city.x} {city.y}\n')
    return cities


def generate_cities(size):
    return [City(x=int(random.random() * 1000), y=int(random.random() * 1000)) for _ in range(size)]
'''

def path_cost(route):
    """
    route: lista de ciudades de la ruta
    return: distancia total de la ruta

    Para cada ciudad, calcula la distancia con la ciudad anterior y la suma
    """
    return sum([city.distance(route[index - 1]) for index, city in enumerate(route)])

class Particle:
    def __init__(self, route, cost=None):
        self.route = route #Lista de ciudades
        self.pbest = route #Inicializa ruta por defecto para cada particula
        self.current_cost = cost if cost else self.path_cost()
        self.pbest_cost = cost if cost else self.path_cost()
        self.velocity = []

    def clear_velocity(self):
        self.velocity.clear()

    def update_costs_and_pbest(self):
        self.current_cost = self.path_cost()
        if self.current_cost < self.pbest_cost:
            self.pbest = self.route
            self.pbest_cost = self.current_cost

    def path_cost(self):
        return path_cost(self.route)


class PSO:

    def __init__(self, iterations, population_size, pbest_probability=1.0, gbest_probability=1.0, cities=None):
        self.cities = cities
        self.gbest = None
        self.gcost_iter = []
        self.iterations = iterations
        self.population_size = population_size #Cantidad de particulas definidas manualmente
        self.particles = []
        self.gbest_probability = gbest_probability
        self.pbest_probability = pbest_probability

        solutions = self.initial_population()
        self.particles = [Particle(route=solution) for solution in solutions]

    # def random_route(self):
    #     """
    #     Retorna una ruta aleatoria. 
    #     En esta versión no se especifica una ciudad de origen
    #     """    
    #     return random.sample(self.cities, len(self.cities))
    def random_route(self, start_index):
        """
        Retorna una ruta aleatoria.
        Ciudad de origen especificada
        """
        original = random.sample(self.cities, len(self.cities))
        for i,cit in enumerate(original):
            if cit == self.cities[start_index]:
                #Establece ciudad de origen en primera posición
                original[start_index], original[i] = original[i], original[start_index]
                #¿Agregar la ciudad de origen al final de la lista?
                #original.append(original[start_index])
                return original

    def initial_population(self):
        #Recordar establecer ciudad de origen
        random_population = [self.random_route(0) for _ in range(self.population_size - 1)]
        greedy_population = [self.greedy_route(0)]
        return [*random_population, *greedy_population]
        #return [*random_population]

    def greedy_route(self, start_index):
        """
        Retorna la ruta entre las ciudades más cercanas.
        """
        unvisited = self.cities[:]
        del unvisited[start_index]
        route = [self.cities[start_index]]
        while len(unvisited):
            index, nearest_city = min(enumerate(unvisited), key=lambda item: item[1].distance(route[-1]))
            route.append(nearest_city)
            del unvisited[index]
        #route.append(self.cities[start_index])
        return route

    def run(self):
        self.gbest = min(self.particles, key=lambda p: p.pbest_cost)
        print(f"initial cost is {self.gbest.pbest_cost}")
        plt.ion()
        plt.draw()
        prob_c0 = 1 - (self.gbest_probability + self.pbest_probability)
        for t in range(self.iterations):
            #Actualizar la mejor solución global
            self.gbest = min(self.particles, key=lambda p: p.pbest_cost)

            #Mostrar gráfico en pantalla
            # if t % 20 == 0:
            #     plt.figure(0)
            #     plt.plot(pso.gcost_iter, 'g')
            #     plt.ylabel('Distancia')
            #     plt.xlabel('Iteración')
            #     fig = plt.figure(0)
            #     fig.suptitle(f'Loss Function. Iteration: {t}')
                
            #     x_list, y_list = [], []
            #     for city in self.gbest.pbest:
            #         x_list.append(city.x)
            #         y_list.append(city.y)
            #     x_list.append(pso.gbest.pbest[0].x)
            #     y_list.append(pso.gbest.pbest[0].y)
            #     fig = plt.figure(1)
            #     fig.clear()
            #     fig.suptitle(f'PSO - TSP cities. Iteration {t}')

            #     plt.plot(y_list, x_list, 'ro')
            #     plt.plot(y_list, x_list, 'g')
            #     plt.draw()
            #     plt.pause(.001)
            self.gcost_iter.append(self.gbest.pbest_cost)

            for particle in self.particles:
                particle.clear_velocity()
                temp_velocity = []
                gbest = self.gbest.pbest[:]
                new_route = particle.route[:]

                #Operador Path Relinking
                for i in range(len(self.cities)):
                    if new_route[i] != particle.pbest[i]:
                        # swap es una tupla (i, j, probabilidad)
                        # Es el operador de intercambio, y representa la 
                        # velocidad con su respectiva probabilidad
                        swap = (i, particle.pbest.index(new_route[i]), self.pbest_probability)
                        """
                        i => indice de la ciudad en la ruta actual
                        particle.pbest.index(new_route[i]) => indice de la ciudad en la mejor ruta
                        self.pbest_probability => probabilidad de intercambio (puede cambiar por iteración)
                        """
                        temp_velocity.append(swap)
                        new_route[swap[0]], new_route[swap[1]] = \
                            new_route[swap[1]], new_route[swap[0]]
                # Path Relinking para gbest
                for i in range(len(self.cities)):
                    if new_route[i] != gbest[i]:
                        swap = (i, gbest.index(new_route[i]), self.gbest_probability)
                        temp_velocity.append(swap)
                        gbest[swap[0]], gbest[swap[1]] = gbest[swap[1]], gbest[swap[0]]

                particle.velocity = temp_velocity

                for swap in temp_velocity:
                    """Revisa cada operador de intercambio (velocidad) y
                     aplica el cambio de acuerdo a su probabildiad"""
                    if random.random() <= swap[2]: #En swap[2] recordar que es probabilidad
                        # Accede a cada ciudad, el índice es dado por swap[0] y swap[1]
                        new_route[swap[0]], new_route[swap[1]] = \
                            new_route[swap[1]], new_route[swap[0]]

                particle.route = new_route #Actualiza ruta
                particle.update_costs_and_pbest() #Actualiza costos y mejor ruta de particula
            #Actualizar probabilidad de intercambio
            self.pbest_probability = self.pbest_probability * 1.00001
            self.gbest_probability = self.gbest_probability * 1.00001

import folium


def plot_map(x_list, y_list,name='map.html'):
    """
    x_list: lista de coordenadas x
    y_list: lista de coordenadas y
    name: nombre del archivo html

    Muestra las ciudades en el mapa, y guarda el archivo en la carpeta output_map
    """
    map = folium.Map(location=[40,-95], zoom_start = 4)
    points = []
    for i in range(len(x_list)):
        points.append([x_list[i], y_list[i]])
    points.append([x_list[0], y_list[0]])
    folium.PolyLine(points, color="red", weight=2.5, opacity=1).add_to(map)
    map.save(f'output_map/{name}')
    map

if __name__ == "__main__":
    # num_cities = 50 #Establecer cantidad de ciudades
    # file_path = 'data/cities_150.data'  # Archivo de texto con las ciudades

    # cities = read_cities(num_cities, file_path) # Lista de objetos City
    # pso = PSO(iterations= 2000, population_size=5000, pbest_probability=0.04, gbest_probability=0.02, cities=cities)
    # pso.run()
    # print(f'cost: {pso.gbest.pbest_cost}\t| gbest: ⁄n{pso.gbest.pbest}')

    # x_list, y_list = [], []
    # for city in pso.gbest.pbest:
    #     x_list.append(city.x)
    #     y_list.append(city.y)
    # x_list.append(pso.gbest.pbest[0].x)
    # y_list.append(pso.gbest.pbest[0].y)
    # # Save map
    # plot_map(x_list, y_list, 'map.html')

    # fig = plt.figure(1)
    # fig.suptitle('PSO for TSP')

    # plt.plot(y_list, x_list, 'ro')
    # plt.plot(y_list, x_list)
    # plt.show(block=True)

    lista_ciudades = [10, 15, 20, 50, 70, 100, 150]
    for i in lista_ciudades:
        file_path = 'data/cities_150.data'  # Archivo de texto con las ciudades
        cities = read_cities(i, file_path)
        pso = PSO(iterations= 500, population_size=1000, pbest_probability=0.5, gbest_probability=0.5, cities=cities)
        pso.run()
        print(f'cost: {pso.gbest.pbest_cost}\t| gbest: {pso.gbest.pbest}')
        
        plt.figure(0)
        plt.plot(pso.gcost_iter, 'g')
        plt.ylabel('Distancia')
        plt.xlabel('Iteración')
        fig = plt.figure(0)
        fig.suptitle(f'Loss Function. Cities: {i}')
        x_list, y_list = [], []
        for city in pso.gbest.pbest:
            x_list.append(city.x)
            y_list.append(city.y)
        x_list.append(pso.gbest.pbest[0].x)
        y_list.append(pso.gbest.pbest[0].y)
        # Save map
        plot_map(x_list, y_list, f'map_{i}.html')

        fig = plt.figure(1)
        fig.suptitle('PSO for TSP. Cities: '+str(i))

        plt.plot(y_list, x_list, 'ro')
        plt.plot(y_list, x_list)
        plt.show(block=True)

    