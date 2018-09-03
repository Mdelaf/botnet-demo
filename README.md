## Botnets: Cracking Distruibidos y DoS Distribuido

Proyecto demostrativo para presentación del curso IIC2523 (Sistemas Distribuidos).


### Estándar de comunicación

#### Autenticación

- Endpoint: `POST /auth`
- Content: `{"uid": <session-uid>, "os": <os>, "user": <username>}`
- Expected code: `204`
- Other codes: `400`


#### Solicitud de tareas

- Endpoint: `GET /tasks`
- Header: `Authorization: Token <uuid>`
- Response: `{"task_id": <task-id>, "command": <command>}` o `{}`
- Expected code: `200`
- Other codes: `401`


#### Entrega de respuestas

- Endpoint: `POST /delivery`
- Header: `Authorization: Token <uuid>`
- Content: `{"task_id": <task-id>, "answer": <answer>}`
- Expected code: `204`
- Other codes: `400`, `401`, `403`



### Comandos

#### Cracking por fuerza bruta

`bruteforce -u [HASHES URL] -a [HASHING ALGORITHM] -s [CHAR SET] -l [LENGTH] -p [PARTITION]`

##### Descripción

Genera todos los _strings_ posibles desde largo 1 hasta el largo dado. Para cada _string_ computa su _hash_ usando la
función indicada y lo compara con el _hash_ entregado. Si coinciden envía el _string_ al servidor.

Para distribuir el cómputo se usa la opción `-p` que indica qué partición del conjunto de _strings_
posibles debe probar.

##### Opciones:

|OPTION|DESCRIPTION|EXAMPLES|
|------|-----------|--------|
|HASHES URL|Url de un archivo de texto que contiene los hashes que se quieren crackear|`http://domain.com/hashlist.txt`|
|HASHING ALGORITHM|Algoritmo de hashing que se quiere usar|`md5`, `sha1`|
|CHAR SET|Conjunto de caracteres para la fuerza bruta. Letras minúsculas (`l`), letras mayúsculas (`L`), dígitos (`d`) y símbolos (`s`)|`lLd`, `ld`, `lds`|
|LENGTH|Largo máximo de _string_|`5`, `8`, `10`|
|PARTITION|Partición de los _strings_ totales que se van a generar|`1/10`, `2/10`, `3/5`, `5/5`|
