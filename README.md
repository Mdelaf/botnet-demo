## Botnets: Cracking Distruibidos y DoS Distribuido

Proyecto demostrativo para presentación del curso IIC2523 (Sistemas Distribuidos).


### Estándar de comunicación

#### Autenticación

- Endpoint: `POST /auth`
- Content: `{"uid": <session-uid>}`
- Expected code: `204`


#### Solicitud de tareas

- Endpoint: `GET /tasks/{uid}`
- Response: `{"task_id": <task-id>, "command": <command>}` o `{}`
- Expected code: `200`


#### Entrega de respuestas

- Endpoint: `POST /delivery`
- Content: `{"task_id": <task-id>, "uid": <session-uid>, "answer": <answer>}`
- Expected code: `204`
- Other codes: `403` 



### Comandos

#### Cracking por fuerza bruta

`bruteforce -h [HASH] -a [HASHING ALGORITHM] -s [CHAR SET] -l [LENGTH] -p [PARTITION]`

##### Descripción

Genera todos los _strings_ posibles desde largo 1 hasta el largo dado. Para cada _string_ computa su _hash_ usando la
función indicada y lo compara con el _hash_ entregado. Si coinciden envía el _string_ al servidor.

Para distribuir el cómputo se usa la opción `-p` que indica qué partición del conjunto de _strings_
posibles debe probar.

##### Opciones:

|OPTION|DESCRIPTION|EXAMPLES|
|------|-----------|--------|
|HASH|Hash que se quiere crackear|`925d7518fc597af0e43f5606f9a51512`|
|HASHING ALGORITHM|Algoritmo de hashing que se quiere usar|`md5`, `sha1`|
|CHAR SET|Conjunto de caracteres para la fuerza bruta. Letras minúsculas (`l`), letras mayúsculas (`L`), dígitos (`d`) y símbolos (`s`)|`lLd`, `ld`, `lds`|
|LENGTH|Largo máximo de _string_|`5`, `8`, `10`|
|PARTITION|Partición de los _strings_ totales que se van a generar|`1/10`, `2/10`, `3/5`, `5/5`|



#### Ataques de Denegación de Servicios