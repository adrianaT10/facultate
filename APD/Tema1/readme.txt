//Tufa Adriana 333CA
//Tema 1 APD

PARTEA 1
  Pentru reprezentarea unui pixel am folosit o structura cu 3 char-uri, R, G,
respectiv B. Imaginile alb negru vor folosi doar B. O imagine contine campuri
pentru latime, inaltime, valoarea maxima si matricea de pixeli.
  Citirea din fisier o fac printr-un singur apel de sistem intr-un buffer, pentru
a minimiza timpul in defavoarea memoriei. Din buffer trec apoi informatiile in
matricea de pixeli pentru un acces mai usor la date si mai lizibil. La scriere
fac aceleasi operatii dar in ordine inversa.
  Pentru resize factor multiplu de 2, fiecare pixel din imaginea rezultata va fi
o medie aritmetica a unei matrici de resize_factor * resize_factor pixeli din 
imaginea data ca input. Desi pentru acest calcul implementarea contine 4 for-uri
imbricate, le-am paralelizat doar pe primele doua prin collapse. Paralelizarea
celorlalte 2 for-uri ar fi crescut doar timpul total din cauza formarii thread-urilor,
dar numarul acestora nu ar fi crescut, nefiind eficient.
  Daca resize factor este 3, calculez noua matrice de pixeli folosind kernelul Gaussian.
Pentru paralelizare este aceeasi observatie ca si mai sus.

Scalabilitate:
 Am testat tema pe cluster, pe coada ibm-nehalem pe o imagine PNM color cu rezolutia 
18518 x 7531.
 Timpul masurat este doar cel al functiei de resize.
 Rezultatele obtinute sunt:

 resize_factor   nr threads		time
---------------------------------------
     3              1           2.125
                    2           1.097
                    4           0.5629
                    8           0.54282
----------------------------------------
     2              1           2.033
                    2           1.057
                    4           0.5486
                    8           0.2942
----------------------------------------

 Pentru resize factor de 3 raporturile de timp sunt:
  1 : 2 = 1.93
  2 : 4 = 1.94
  4 : 8 = 1.03
  Se observa ca pana la 4 thread-uri paralelizarea aduce aproape injumatatirea
timpului, dupa care diferenta dintre 4 si 8 thread-uri nu este foarte vizibila,
deci nu mai scaleaza.

  Pentru resize factor de 2, raporturile obtinute devin:
  1 : 2 = 1.93
  2 : 4 = 1.95
  4 : 8 = 1.86
  In acest caz, scalabilitatea se pastreaza pana la 8 thread-uri, desi raportul
de timp tinde sa scada.


PARTEA 2
  Reprezentarea imaginii este asemanatoare cu cea de la prima parte cu diferenta ca,
neavand nevoie de 3 char-uri pentru fiecare pixel, nu am mai folosit structura pixel.
Algoritmul calculeaza pentru fiecare pixel distanta dintre el si linia -x+2y = 0, 
distanta raportata la cei 100 de metri patrati pe care ii reprezinta imaginea. 
La paralelizarea randarii, desi am 2 for-uri independente am observat o usoara imbunatatire
daca doar primul for este paralelizat.

Scalabilitate:
Am testat pe fep, pe cluster, cum a fost indicat in tema. Rezultatele obtinute pentru
rezolutia 10000 sunt:

Nr threads     Timp
--------------------
   1          1.701  
   2          0.859
   4          0.441
   8          0.254
---------------------

Calculand raporturile de timp:
  1 : 2 = 1.98
  2 : 4 = 1.94
  4 : 8 = 1.73
Se observa ca timpul scade aproape liniar cu cresterea numarului de thread-uri, deci 
paralelizarea sigur scaleaza. Desi intre 4 si 8 thread-uri diferenta a mai scazut, tot
ramane una semnificativa.