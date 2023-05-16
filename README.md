<h1 class="code-line" data-line-start=0 data-line-end=1>fastapi_sgre</h1>
<h2 class="code-line" data-line-start=1 data-line-end=2 ><a id=""></a><em>Sistema de control de configuración equipos de red activos gestionable</em></h2>
<p class="has-line-data" data-line-start="3" data-line-end="4"><a href="https://fastapi.tiangolo.com/"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="N|Solid"></a></p>

<h2 class="code-line" data-line-start=5 data-line-end=6 ><a id="Caractersticas_5"></a>Características</h2>
<ul>
<li class="has-line-data" data-line-start="7" data-line-end="8">Registro de usuarios</li>
<li class="has-line-data" data-line-start="8" data-line-end="9">Asigna rol de administrativo o personal asociado a la organización</li>
<li class="has-line-data" data-line-start="10" data-line-end="11">Asignar permisos al rol personal (r,rw,rwx,drwx) para ejecutar ciertas acciones</li>
<li class="has-line-data" data-line-start="10" data-line-end="11">Registros de equipos activos de red, enlace SSH, router, switch u otros equipos</li>
<li class="has-line-data" data-line-start="10" data-line-end="11">Registro y gestión de configuraciones en texto plano</li>
<li class="has-line-data" data-line-start="9" data-line-end="10">Verificación y envió de configuraciones a equipos </li>
<li class="has-line-data" data-line-start="9" data-line-end="10">BackgrondTask registrando configuraciones al sistema </li>
<li class="has-line-data" data-line-start="9" data-line-end="10">Sistema de autenticación y autorización implementando Oauth2 y JWT</li>
<li class="has-line-data" data-line-start="11" data-line-end="12">Documentación enpoint con open api</li>
</ul>

<h2 class="code-line" data-line-start=5 data-line-end=6 ><a id="Caractersticas_5"></a>Construcción</h2>
<ul>
<li class="has-line-data" data-line-start="7" data-line-end="8">Integrar nuevas funcionalidades</li>
<li class="has-line-data" data-line-start="8" data-line-end="9">Integrar MongoDB a funcionalidad seguimiento</li>
<li class="has-line-data" data-line-start="8" data-line-end="9">Integrar gestión de equipos por telnet: túnel SSH</li>
<li class="has-line-data" data-line-start="8" data-line-end="9"> Agregar funcionalidad ubicación para identificar el equipo</li>
</ul>


<h2 class="code-line" data-line-start=13 data-line-end=14 ><a id="Estructura_13"></a>Diagrama clases ORM</h2>
  <img src="https://github.com/ccobando66/fastapi_sgre/assets/115023210/fa28f8c9-bf86-4699-bf29-afe515e495c8"/>



<h2 class="code-line" data-line-start=13 data-line-end=14 ><a id="Estructura_13"></a>Tecnologías</h2>
<pre><code class="has-line-data" data-line-start="16" data-line-end="67" class="language-s">
├── FastApi   -> Framework web Backend
├── SqlAlchemy  -> ORM Database Mapping
├── Pytest -> Unit Testing
├── AIOFiles -> write in server asyncio applications
├── Os -> Custom packages
├── PostgreSql -> Databasee 
└── netmiko -> Network automation
</code></pre>

<h2 class="code-line" data-line-start=126 data-line-end=127 ><a id="instalacin_126"></a>Documentación</h2>

<p class="has-line-data" data-line-start="129" data-line-end="130">Open Api</p>
<pre><code class="has-line-data" data-line-start="131" data-line-end="135" class="language-sh"> https://su_dominio:su_puerto/docs 
--> recomendado
</code></pre>

<p class="has-line-data" data-line-start="129" data-line-end="130">Redocs</p>
<pre><code class="has-line-data" data-line-start="131" data-line-end="135" class="language-sh"> https://su_dominio:su_puerto/redoc
</code></pre>

<h2 class="code-line" data-line-start=13 data-line-end=14 ><a id="Estructura_13"></a>Estructura</h2>
<pre><code class="has-line-data" data-line-start="16" data-line-end="67" class="language-s">
├── auth   -> Sistema de autenticación y autorización
├── config  -> Configuración enlace a base de datos 
├── dependencies.py -> Módulos de uso general 
├── files -> Guarda archivos de configuración .txt
├── __init__.py -> módulo paquete
├── main.py -> Punto de entrada 
├── models -> ORM
├── requeriment.txt -> Módulos requeridos para funcionamiento 
├── routers -> HTTP REST endpoint
├── schema -> Validador de datos
├── services -> Lógica de negocio
└── tests -> Pruebas unitarias 
</code></pre>

<h2 class="code-line" data-line-start=126 data-line-end=127 ><a id="instalacin_126"></a>Instalación</h2>
<p class="has-line-data" data-line-start="127" data-line-end="128">Versión usada en este proyecto <a href="https://www.python.org/">Python 3.10</a>  o superior</p>
<p class="has-line-data" data-line-start="129" data-line-end="130">Clonar repositorio.</p>
<pre><code class="has-line-data" data-line-start="131" data-line-end="135" class="language-sh">git <span class="hljs-built_in">clone</span> https://github.com/ccobando66/fastapi_sgre.git
<span class="hljs-built_in">cd</span> fastapi_sgre --&gt; linux
dir fastapi_sgre --&gt; windows
</code></pre>

<p class="has-line-data" data-line-start="136" data-line-end="137">Crear entono virtual venv…</p>
<pre><code class="has-line-data" data-line-start="139" data-line-end="143" class="language-sh">python<span class="hljs-number"></span> -m venv venv
<span class="hljs-built_in">source</span> venv/bin/activate --&gt; linux
venv\Scripts\activate.bat --&gt; windows
</code></pre>

<p class="has-line-data" data-line-start="144" data-line-end="145">Instalar dependencias en el entorno virtual…</p>
<pre><code class="has-line-data" data-line-start="147" data-line-end="149" class="language-sh">pip<span class="hljs-number"></span> install -r requirements.txt
</code></pre>

<p class="has-line-data" data-line-start="127" data-line-end="128">variables de entorno</p>
<p class="has-line-data" data-line-start="129" data-line-end="130">nano .env</p>
<pre><code class="has-line-data" data-line-start="131" data-line-end="135" class="language-sh">
# JWT_ENVIROMENT
JWT_SECRET="value"
JWT_ALGORITH="value"
JWT_EXPIRATE="value"
# DATABASE CONNECTIONS STRING ENVIROMENT
DB_USER="value"
DB_PASSWD="value"
DB_HOST="value"
DB_NAME="value"

</code></pre>

<p class="has-line-data" data-line-start="149" data-line-end="150">Iniciar servidor uvicorn…</p>
<pre><code class="has-line-data" data-line-start="152" data-line-end="154" class="language-sh">
cd ..
uvicorn fastapi_sgre.main:app --host <span class="hljs-number">0.0</span>.<span class="hljs-number">0.0</span> --port <span class="hljs-number">8080</span> --reload 
</code></pre>


