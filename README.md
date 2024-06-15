# Webir 2024

### Variables de Ambiente

Duplicar el archivo `.env.example`.

```python
MONGODB_URI="mongodb://localhost:27017/"
OPENFING_URL="https://open.fing.edu.uy"
DATABASE_NAME="webir"

CACHE_PATH="models" # Folder to persist models and avoid downloading every time, e.g., embeddings.
VDB_PATH="store/vector_database" # Folder where the vector database will be persisted.
DATA_PATH="store/transcriptions" # Folder containing transcribed and segmented lessons outputted by Whisper.

HUGGINGFACEHUB_API_TOKEN="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" # Access token of Hugging Face Hub, for the llm
LANGCHAIN_API_KEY="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" # Api key for LangSmith
```

### Requerimientos

Ver el archivo `requirments.txt`.

-   Para **instalar** los requerimientos ejecutar:

```
pip install -r requirements.txt
```

-   Para **actualizar** el archivo de `requirments.txt` hacer:

```
pip freeze > requirements.txt
```

## Store

### Data

En este modulo se gestiona los datos de las materias (`subjects`) y sus clases (`lessons`) que son almacenados en una base de datos no relacional de **Mongo DB**.

#### Ejecutando MongoDB

Para ejecutar **Mongo DB** localmente, simplemente se debe:

1. Instalar Mongo DB ([Manual](https://www.mongodb.com/docs/manual/installation/)).
2. (Opcional) Instalar la interfaz de usuario [MongoDB Compass](https://www.mongodb.com/try/download/compass).
3. Setear la variable de ambiente `MONGODB_URI` con el link de conexión correspondiente. Por defecto es `mongodb://localhost:27017/`.

Para ejecutar **Mongo DB** en el servidor, se debe:

1. Ir a [Atlas MongoDB](https://www.mongodb.com/atlas).
2. Ingresar con su cuenta.
3. Ingresar al proyecto **Webir** (se envio una invitación al proyecto). En este proyecto ya se creo un cluster que corre en AWS que se llama WebirDatabase.
4. Conectar al cluster WebirDatabase usando Python Drivers, lo cual ya esta configurado. Simplemente se tiene que modificar la variable de ambiente `MONGODB_URI` con el connection string correspondiente.
5. Agregar la IP local actual para que permita la conexión satisfactoriamente.
   ![alt text](image.png)
   Ver [Network Access](https://cloud.mongodb.com/v2/664a4897fbf0be7fcc03e6c6#/security/network/accessList) para otros tipos de conexiones (Por ejemplo para conectarse desde el colab).

#### Modelos de Subjects y Lessons

Dentro del modulo **data** hay un submodulo **models** en los cuales se tiene dos modelos: `SubjectModel` y `LessonModel`.

Estos modelos cuentan con metodos para crear, actualizar, obtener por el id, obtener un item por el valor de algun atributo y obtener todos los items de la colección correspondiente.

Ejemplo:

```python
from store.data.models.subjects import SubjectModel
from store.data.models.lessons import LessonModel

model = SubjectModel()

id = model.create("AGPI", "fklgdflgnlkdngkdfnglkdfngkdlfnxg")
print(f"ID {id}\n")

s = model.get(id)
print(f"Retrieved subject: {s}\n")

all = model.getAll()
print(f"All subjects: {all}\n")


lessons = LessonModel()
id1 = lessons.create(id, "Clase 1","url1", "videourl1")
id2 = lessons.create(id, "Clase 2","url2", "videourl2")

allS = lessons.getAll()
print(f"All lessons: {allS}\n")

s1 = lessons.get(id1)
print(f"Retrieved Lesson: {s1}\n")

lessons.update(id1, {"transcribed": True})

sTranscribed = lessons.getBy({"transcribed": False})
print(f"Retrieved Lesson Not Transcribed: {sTranscribed}\n")


sWithLessons = model.get(id, True)
print(f"Retrieved subject with lessons: {sWithLessons}\n")
```

### Embedding

## Transcriptor
Este  modulo se encarga de transcribir las clases de las materias almacenadas en la base de datos de MongoDB. Actualmente se transcriben solo las clases de las materias definidas dentro del arreglo subjects en el archivo `transcriptor/transcriptor.py`. Para ejecutar el transcriptor, se debe correr el siguiente comando:

```bash
python main.py transcriptor
```

Verificar MONGODB_URI para saber de donde está obteniendo la info (localhost o en el servidor de atlas).

## Scrapper

Para ejecurar el scrapper se debe correr el siguiente comando:

```
python main.py scrapping
```

Verificar `MONGODB_URI` para saber donde se esta guardando la info (localhost o en el servidor de atlas).

## Loader

Se puede ejecutar el loader, desde la raiz del proyecto de las siguientes maneras:

-   Llamando al script loader usando main.py

```python
python main.py loader (--seed [path to folder with seeding data] | --drop)
```

-   Ejecutando el script loader.py directamente como un modulo de python

```python
python -m loader.loader (--seed [path to folder with seeding data] | --drop)
```

> Note: se asume que el path_to_folder es relativo a donde se esta ejecutando el script.

> Note: acordarse de agregar tu ip publica a la whitelist de ips en el cluster de mongo atlas (Ver Ejecutando MongoDB) al usar la funcionalidad seed dado que se conecta al mismo para recuperar los id de las clases transcritas.

## Backend

Para ejecutar el backend, se debe correr el siguiente comando:

```bash
fastapi (run | dev) backend/api.py
```

> Note: [See FastAPI CLI docs](https://fastapi.tiangolo.com/fastapi-cli/)

## Chat

### Deploy

Para hacer el deploy del Chat en vercel, seguir los siguientes pasos:

1. Instalar (globalmente) Vercel CLI:

```
npm install -g vercel
```

2. Iniciar sesión con vercel

```
vercel login
```

Usar el email `webirgrupo3@gmail.com`. Luego entrar a gmail con ese correo y contraseña `WEBIRwebir` para verificar (si pide un codigo se los mando porque asocie mi telefono).

Todo esto porque no permitia crear team en la version gratis.

3. Ir al directorio del chat

```
cd chat
```

4. Ejecutar el script para el deploy

```
npm run deploy
```

![alt text](image-1.png)
