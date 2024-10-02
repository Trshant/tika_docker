## About
This is a software that will allow you to run a tika server and a script in python to read multiple filetypes and get text and all possible metadata from it.  

## TODO
a place to list what i want before i use a task board or project management software.  

1. Look into including Tesseract. 
2. Look into getting metadata from the file itself (apart from the data collected by Tika.)
3. see if i can give more metadata derived from the text.

## Change Tracker
### 2nd OCT 2024
docker directive reference
https://docs.docker.com/reference/dockerfile/

#### Some commands which i will get rid of ASAP

docker --debug build -t tikka_learn . --no-cache
docker run -p 9998:9998 -d tikka_learn /bin/bash -c "sleep infinity"

```mermaid
graph TD;
    A-->B;
    A-->C;
    B-->D;
    C-->D;
```