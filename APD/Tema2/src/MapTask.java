/**
 * Clasa pentru task-ul de tip Map
 */
public class MapTask {
	// numele documentului
	private String document;
	// pozitia de la care se citeste din document
	private int startPos;
	// dimensiunea fragmentului de citit
	private int dimension;

	/**
	 * Constructor
	 * @param document
	 * @param start
	 * @param dimension
	 */
	public MapTask(String document, int start, int dimension) {
		this.document = document;
		this.startPos = start;
		this.dimension = dimension;
	}

	public String getDocument() {
		return document;
	}

	public int getStartPos() {
		return startPos;
	}

	public int getDimension() {
		return dimension;
	}

	@Override
	public String toString() {
		return "MapTask [document=" + document + ", startPos=" + startPos
				+ ", dimension=" + dimension + "]";
	}

	
}
