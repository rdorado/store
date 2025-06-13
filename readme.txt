cluster.py [image] [clusters] [output dir/file]
preprocess.py [image] [output dir/file]


paintside2.py

--Run in compose:

pwd (current directory of this file)
docker compose up

 Linux: install vnenv sudo apt install python3-venv

--Install backend deps and reqs:
 -Go to source dir:
   backend\src

 -Install dependencies:
    pip install fastapi[standard] sqlalchemy python-multipart


 -Install python virtual environment:
    python -m venv .venv


--Run backend as local dev (no blender)
 -Go to source dir:
   backend/src
   
 -Activate python virtual environment:
   win:
     .venv\Scripts\activate
   linux:
     . .venv/bin/activate
     source .venv/bin/activate

 -Run the server:
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload


--Run frontend as local dev

 -Go to source dir:
   cd frontend

 -Install app
   npm install
   
 -Run app
   ng serve 
