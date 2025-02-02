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
