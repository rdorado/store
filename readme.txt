cluster.py [image] [clusters] [output dir/file]
preprocess.py [image] [output dir/file]


paintside2.py

--Run in compose:

pwd (current directory of this file)
docker compose up

--Install banckend deps and reqs:
 -Go to source dir:
   src\backend\src

 -Install python virtual environment: 
    python -m venv .venv

 -Activate python virtual environment:
   .venv\Scripts\activate
   
 -Install dependencies:
    pip install fastapi[standard] sqlalchemy python-multipart


--Run backend as local dev (no blender)
 -Go to source dir:
   src\backend\src
   
 -Run the server:
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload


--Run frontend as local dev

 -Install app
   npm install
   
 -Run app
   ng serve 