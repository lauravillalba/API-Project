![Portada](/input/Portada.jpg)

------------------------------
                                                    # API-Project 
------------------------------

El objetivo de este proyecto es crear una API mediante la cual se puedan analizar mensajes y con esto definer el nivel de sentiment que tiene cada grupo y cada persona. Además se implantará un sistema de recomendación, con el que se indicará la persona con mayor similitud para otra del todos de usuarios de la aplicación.  


## Temática:

           "Inside Out film" --> Se analiza el sentiment de los personajes de la película de animación "Inside Out", 
           y dado un personaje el sistema de recomendación le dirá con quién tiene mayor similitud de los personajes con 
                                            los que no comparta diálogo en la película.

## Consideraciones previas:
- Los personajes serán los usuarios de esta aplicación.
- Las escenas simbolizan los chats en los que los usuarios mantienen conversaciones.
- Los diálogos son los mensajes de cada chat.
- La base de datos tiene 3 colecciones: users (personajes), escenas y diálogos.


## Input:
- JSON escenas
- JSON diálogos


## Output:
*- Métodos POST:
  * Creación nuevo personaje: se valida si el personaje ya existe antes de añadirlo a la colección.
  * Creación nueva escena: se valida si la escena y los personajes que intervienen en la misma ya existen.
  * Creación nuevo diálogo: se valida antes de añadir el mensaje a la colección que exista el usuario y que este forme parte      de la escena a la que se añade cada frase.

- Métodos GET:
  * Obtener todos los usuarios.
  * Obtener detalles de un usuario concreto.
  * Obtener todas las escenas donde sale un personaje.
  * Obtener dada una escena, los personajes que intervienen.
  * Obtener diálogos de una escena determinada.
  * Obtener todos los diálogos de la película para un un personaje.

- Cálculo Sentiment:
  * Sentiment de una escena a partir de los diálogos de los distintos personajes que intervienen
  * Sentiment de cada personaje a partir de todos las frases de la película.

- Sistema de recomendación:
  * Con una petición a la API indicando uno de los personajes, se devuelve el personaje con el que aún no ha compartido          escena que mayor similitud tiene.


## Próximos pasos:
- Incluir grupos como nueva característica de los personajes --> Hay escenas en las que aunque hablen distintos personajes, no se comunican entre ellos. Habría que agrupar: Riley, Mom y Dad.
