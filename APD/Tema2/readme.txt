//Tufa Adriana 333 CA
// Tema 2 APD

    Pentru implementarea temei am pornit de la scheletul de cod de la laboratorul
ReplicatedWorkers si am folosit doua threadpool-uri diferite pentru cele doua tipuri
de task-uri. 
    La inceput citesc din fisier si impart fisierele de input in fragmente de dimensiune
D, creand task-uri pe care le pun in workpool-ul pentru Map. Dupa impartire creez
thread-urile si le pornesc, fiecare luand task-uri din pool. 
    Accesul la lista de task-uri este sincronizat. Fiecare thread ia cate un task
din pool si il proceseaza. Pentru procesarea task-urilor map am procedat astfel:
citesc intr-un buffer mai mult decat dimensiunea fixa data si folosesc doi indici
pentru a determina startul si inceputul fragmentului ramas la final din tot buffer-ul.
Pentru a vedea daca fragmentul incepe cu un cuvant, citesc din fisier cu un octet
inaintea pozitiei de start. Daca acesta este separator, inseamna ca fragmentul 
incepe cu un cuvant intreg. Daca nu, mut indicele de start la inceputul urmatorului
cuvant. Asemanator pentru finalul fragmentului, daca indicele de final este in mijlocul
unui cuvant, il avansez pana ce intalnesc un separator. Textul din buffer intre indicele
de start si cel de final il impart in cuvinte dupa care le parcurg. Intr-un hashMap
adaug intrari de forma (lungime_k, nr_aparitii_cuvinte_lung_k) iar intr-un set retin
cuvintele maximale (pentru a nu fi duplicate). Rezultatul procesarii il adaug in 
workpool-ul pentru task-uri de tip reduce.
    In acest workpool am cate un task pentru fiecare fisier. Un task contine o lista
de rezultate partiale dupa map. Atunci cand adaug un rezultat map, verifica daca exista
deja un task pentru fisierul respectiv si adaug acolo datele, sau creez un task nou in 
caz contrar. Pentru a incepe procesarea task-urilor reduce dupa ce toate task-urile map
s-au terminat, folosesc o bariera. In procesarea unui task reduce, intai combin toate
rezultatele partiale, dupa care calculez rang-ul dupa formula data si numar cuvintele
maximale per intreg documentul. Rezulatul il adaug intr-un treeSet global care la adaugare
si ordoneaza rezultatele dupa rang sau dupa ordinea in fisierul de intrare pentru ranguri
egale.

Rezultatele rularii testelor initiale pe fep:

Nr threads  |   Test    |    Timp
-----------------------------------
   1             1          4.326
   2                        3.124  
   4                        1.820
-----------------------------------
   1             2         22.945
   2                       14.638
   4                        7.436
-----------------------------------
   1             3         2.940
   2                       1.685
   4                       1.003
------------------------------------
   1             4         1m4.216
   2                        35.016
   4                        18.018
------------------------------------

Se observa ca paralelizarea ofera scalabilitate. 
Pentru testul 1 diferenta e notabila intre 2 si 4 thread-uri.
La testul 2 speedup-ul este aproape liniar cu cresterea numarului de thread-uri.
La testul 3 diferenta se simte doar intre 1 si 2 thread-uri.
Pentru ultimul test, care are si fisierele cele mai mari, timpul este considerabil
mai bun pentru varianta paralela.