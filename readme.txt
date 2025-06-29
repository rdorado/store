cluster.py [image] [clusters] [output dir/file]
preprocess.py [image] [output dir/file]


paintside2.py

--Run in compose:

pwd (current directory of this file)
docker compose up

Install python version compatible with bpy:
 sudo install python3.11 python3.11-venv
 then use python3.11 to install the virtual environment

 Linux: install vnenv sudo apt install python3-venv

--Install backend deps and reqs:
 -Go to source dir:
   backend\src

 -Install dependencies:
    pip install fastapi[standard] sqlalchemy python-multipart bpy


 -Install python virtual environment:
    python -m venv .venv


--Run backend as local dev (no blender)

 -Activate python virtual environment:
   win:
     .venv\Scripts\activate
   linux:
     . .venv/bin/activate
     source .venv/bin/activate

 -Go to source dir:
   backend/src

 -Run the server:
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload


--Run frontend as local dev

 -Go to source dir:
   cd frontend

 -Install app
   npm install
   
 -Run app
   ng serve 
