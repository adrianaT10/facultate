#include "homework1.h"
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <omp.h>

int num_threads;
int resolution;

void initialize(image *im) {
  int i, j;

  im->width = resolution;
  im->height = resolution;
  im->maxval = MAXVAL;
  im->matrix = (unsigned char**)malloc(resolution * sizeof(unsigned char *));

  omp_set_num_threads(num_threads);

  /* allocate memory for the pixel matrix */
  #pragma omp parallel for shared(im)
  for(i = 0; i < im->height; i++)  {
  	im->matrix[i] = (unsigned char*)malloc(resolution * sizeof(unsigned char));
  }
}


/* Return the distance from the pixel to the line */
int compute_distance(int x, int y) {
  return abs(-1 * x + 2 * y + 0)/sqrt(1 + 4);
}


void render(image *im) {
  int i, j;
  int dist, factor;

  factor = resolution / ORIG_SCALE;

  omp_set_num_threads(num_threads);

  /* take every pixel and compute the distance to the given line */
  #pragma omp parallel for private(j, dist) shared(im, factor, resolution)
  for(i = 0; i < im->height; i++) {
  	for(j = 0; j < im->width; j++) {
  		dist = compute_distance(j / factor, i / factor);
  		/* if the distance is smaller than 3, the pixel is on the line */
  		im->matrix[i][j] = dist < 3 ? 0 : MAXVAL;
  	}
  }
}

void writeData(const char * fileName, image *img) {
  FILE *fout = fopen(fileName, "wb");
  int i, j;
  unsigned char buffer[img->height * img->width];

  fprintf(fout, "P5\n");
  fprintf(fout, "%d %d\n%d\n", img->width, img->height, img->maxval);

  omp_set_num_threads(num_threads);

  /* write the matrix of pixels in a buffer */
  #pragma omp parallel for private(j) shared(buffer, img)
  for(i = 0; i < img->height; i++) {
  	for(j = 0; j < img->width; j++) {
  		buffer[(img->height - i - 1)*img->width + j] = img->matrix[i][j];
  	}
  }
  /* write the buffer in the file */
  fwrite(buffer, sizeof(buffer), 1, fout);
}

