#define MAXVAL 255
#define ORIG_SCALE 100 /* the dimension to which we have to 
                          relate when computing the distance */

/* Struct to define an image */
typedef struct {
  int width;
  int height;
  int maxval;
  unsigned char **matrix; /* pixel matrix */
} image;