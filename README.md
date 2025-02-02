# M2: Construccion de la fase inicial de un compilador con Lex y Yacc

## 1. **_Levantar imagen y contenedor_**

- Dirigirse a la carpeta lab-lex

```bash
cd lab-lex
```

- Primero ejecutar este comando para crear la imagen:

```bash
docker build --rm . -t lab1-image
```

- Luego ejecutar **uno** de los siguientes comandos para el contenedor:

```bash
docker run --rm -ti lab1-image
```

```bash
docker run --rm -ti -v "${PWD}:/home" lab1-image
```

```bash
docker run --rm -ti -v "${(path hacia la carpeta)} lab1-image
```

## 2. **_Compilar gramatica_**

```bash
flex ./files/simple_language.l
yacc -dtv ./files/simple_language.y
g++ -c lex.yy.c
g++ -c y.tab.c
g++ -o calc y.tab.o lex.yy.o
```

```bash
./calc
```


## 3. **_Expresiones mas complejas_**
- ingresar una expresion y luego presionar enter
```bash
10+5:
8+6/2:
(5*5)/(2+3):
((8+6)/2)+((5-3)*2):
8*5+(3/(4+9/(1+3/2)))):
(-3+(2*(4/(1-9)))): 

```
## 4. **_Asignacion de variables_**

```bash


```
