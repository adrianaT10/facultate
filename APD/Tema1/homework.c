#include "homework.h"
#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

int num_threads;
int resize_factor;

void readInput(const char * fileName, image *img) {
  FILE *file;
  unsigned char buffer[8];
  int i, j;

  file = fopen(fileName, "rb");

  if(!file) {
  	printf("Fisierul nu exista\n");
  	return;
  }

  /* read and set the type of the image */
  fscanf(file, "%s\n", buffer);
  
  if (buffer[1] == '6') {
  	img->type = COLOR;
  } else {
  	img->type = GRAYSCALE;
  }

  /* get information about the photo */
  fscanf(file, "%d %d\n", &img->width, &img->height);
  fscanf(file, "%d\n", &img->maxval);

  omp_set_num_threads(num_threads);

  /* initialize the matrix of pixels */
  img->matrix = (pixel **)malloc(img->height * sizeof(pixel *));

  /* read all the pixels in a buffer depending on the image type 
     and then put the information in the matrix */
  if(img->type == COLOR) {
  	unsigned char data[img->height * img->width * 3];
  	fread(data, 1, sizeof(data), file);
  	#pragma omp parallel for shared(img, data) private(j)
    for(i = 0; i < img->height; i++) {
  	  img->matrix[i] = (pixel *)malloc(img->width * sizeof(pixel));
  	  for(j = 0; j < img->width; j++) {
        img->matrix[i][j].r = data[(img->width*i*3)+j*3];
        img->matrix[i][j].g = data[(img->width*i*3)+j*3+1];
        img->matrix[i][j].b = data[(img->width*i*3)+j*3+2];
  	   }
     }
  } else {
  	unsigned char data[img->height * img->width];
  	fread(data, 1, sizeof(data), file);
  	#pragma omp parallel for shared(img,data) private(j)
  	for(i = 0; i < img->height; i++) {
  	  img->matrix[i] = (pixel *)malloc(img->width * sizeof(pixel));
  	  for(j = 0; j < img->width; j++) {
        img->matrix[i][j].b = data[i * img->width + j];
  	  }
    }
  }

  fclose(file);
}

void writeData(const char * fileName, image *img) {
  FILE *fout = fopen(fileName, "wb");
  int i, j;

  omp_set_num_threads(num_threads);

  if (img->type == COLOR) {
  	fprintf(fout, "P6\n");
  } else {
  	fprintf(fout, "P5\n");
  }

  fprintf(fout, "%d %d\n%d\n", img->width, img->height, img->maxval);
  
  /* put the information back in a buffer and then write it in the file */
  if(img->type == COLOR) {
  	unsigned char buffer[3 * img->height * img->width];
  	#pragma omp parallel for shared(buffer, img) collapse(2)
    for(i = 0; i < img->height; i++) {
  	  for(j = 0; j < img->width; j++) {
        buffer[(i*img->width + j)*3] = img->matrix[i][j].r;
  		  buffer[(i*img->width + j)*3 + 1] = img->matrix[i][j].g;
  		  buffer[(i*img->width + j)*3 + 2] = img->matrix[i][j].b;
  	  }
    }
    fwrite(buffer, sizeof(buffer), 1, fout);
  } else {
  	unsigned char buffer[img->height * img->width];
  	#pragma omp parallel for shared(buffer, img) collapse(2)
  	for(i = 0; i < img->height; i++) {
  		for(j = 0; j < img->width; j++) {
  			buffer[i*img->width + j] = img->matrix[i][j].b;
  		}
  	}
  	fwrite(buffer, sizeof(buffer), 1, fout);
  }

  fclose(fout);
  free(img->matrix);
}


/* 
  Calculate the value of a resized area with the Gaussian Kernel
  l, c -> coordinates of the pixel in the resized picture
  m -> the matrix of pixels from the original image
*/
pixel calculate(int l, int c, pixel ** m, enum Image_type type) {
  int kernel[3][3] = {{1, 2, 1}, {2, 4, 2}, {1, 2, 1}};
  int i, j, sumr = 0, sumg = 0, sumb = 0;
  pixel sum;
  
  /* multiply the resized area of 3X3 pixels with the Gaussian Kernel */
  if(type == COLOR) {
    for(i = 0; i < 3; i++) {
  	  for(j = 0; j < 3; j++) {
  	    sumr += m[i + l][j + c].r * kernel[i][j];
  	    sumg += m[i + l][j + c].g * kernel[i][j];
  	    sumb += m[i + l][j + c].b * kernel[i][j];
  	  }
    }
  } else {
  	for(i = 0; i < 3; i++) {
  	  for(j = 0; j < 3; j++) {
  	    sumb += m[i + l][j + c].b * kernel[i][j];
  	  }
    }
  }

  /* the resulting pixel */
  sum.r = sumr / 16;
  sum.g = sumg / 16;
  sum.b = sumb / 16;

  return sum;
}

/* Resizing algorithm when the resizing factor is 3 */
void resize_kernel(image *in, image *out) {
    int i, j;

    /* initialize the resulting image */
    out->width = in->width / 3;
    out->height = in->height / 3;
    out->maxval = in->maxval;
    out->type = in->type;
    out->matrix = (pixel **)malloc(out->height * sizeof(pixel *));

    #pragma omp parallel for shared(out)
    for(i = 0; i < out->height; i++) {
    	out->matrix[i] = (pixel *)malloc(out->width * sizeof(pixel));
    }

    /* Compute the new values for the pixels with the Gaussian Kernel 
       Every area of 3X3 pixels will become one pixel.
       Any lines left on bottom-right side that do not fit a 3X3 area
       will be ignored. */
    #pragma omp parallel for shared(out, in) private(j)
    for(i = 0; i < in->height - 3; i = i + 3) {
    	for(j = 0; j < in->width - 3; j = j + 3) {
    		out->matrix[i/3][j/3] = calculate(i, j, in->matrix, in->type);
    	}
    }
}


/* The resizing algorithm when the resize factor is even */
void resize_with_average(image *in, image *out) {
  int i, j, k, t;
  int nr = resize_factor * resize_factor;
  int sumr = 0, sumg = 0, sumb = 0;

  /* initialize the resulting image */
  out->width = in->width / resize_factor;
  out->height = in->height / resize_factor;
  out->maxval = in->maxval;
  out->type = in->type;
  out->matrix = (pixel **)malloc(out->height * sizeof(pixel *));
  
  #pragma omp parallel for shared(out)
  for(i = 0; i < out->height; i++) {
  	out->matrix[i] = (pixel *)malloc(out->width * sizeof(pixel));
  }

  /* make the average of the RGB/BW pixels for areas of 
     resize_factor *resize_factor */
  if(out->type == COLOR) {
  	#pragma omp parallel for collapse(2) \
     shared(out, nr) private(k, t, sumr, sumg, sumb)
    for(i = 0; i < out->height; i++) {
  	  for(j = 0; j < out->width; j++) {
        /* take evry position in the new matrix and compute the average */
  	    sumr = 0; sumg = 0; sumb = 0;
        for(k = i * resize_factor; k < (i+1) * resize_factor; k++) {
      	  for(t = j * resize_factor; t < (j+1) * resize_factor; t++) {
      		  sumr += in->matrix[k][t].r ;
      		  sumg += in->matrix[k][t].g ;
      		  sumb += in->matrix[k][t].b ;
      	  }
        }
        out->matrix[i][j].r =  (unsigned char)(sumr / nr);
        out->matrix[i][j].g =  (unsigned char)(sumg / nr);
        out->matrix[i][j].b =  (unsigned char)(sumb / nr);
  	  }
    }
  } else { /* do the same for the BW images */
  	#pragma omp parallel for shared(out, nr) private(k, t, sumb) collapse(2)
  	for(i = 0; i < out->height; i++) {
  	  for(j = 0; j < out->width; j++) {
  	    sumb = 0;
        for(k = i * resize_factor; k <  (i+1) * resize_factor; k++) {
      	  for(t = j * resize_factor; t < (j+1) * resize_factor; t++) {
      		sumb += in->matrix[k][t].b ;
      	  }
        }
        out->matrix[i][j].b =  (unsigned char)(sumb / nr);
  	  }
    }
  }
}

void resize(image *in, image * out) { 
  
  omp_set_num_threads(num_threads);

  if (resize_factor % 2 == 0) {
  	resize_with_average(in, out);
  } else {
  	resize_kernel(in, out);
  }  
}