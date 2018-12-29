enum Image_type {COLOR, GRAYSCALE};

/* Information about a pixel */
typedef struct {
	unsigned char r, g, b;
} pixel;

/* representation of an image */
typedef struct {
  int width;
  int height;
  int maxval;
  enum Image_type type;
  pixel **matrix;
} image;