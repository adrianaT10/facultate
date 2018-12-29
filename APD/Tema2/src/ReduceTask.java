import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Set;


/**
 * Task pentru workpool-ul reduce
 */
public class ReduceTask {
	// Numele documentului
	String document;
	// Liste de rezultate partiale dupa operatiile de map
	private List<HashMap<Integer,Integer>> hashList;
	private List<Set<String>> localMaxWords;
	
	
	/**
	 * Constructor
	 * @param document - numele fisierului
	 */
	public ReduceTask(String document) {
		this.document = document;
		hashList = new ArrayList<HashMap<Integer, Integer>>();
		localMaxWords = new ArrayList<Set<String>>();
	}
	
	/**
	 * Adauga un rezultat partial
	 * @param hash
	 * @param words
	 */
	public void addMapResult(HashMap<Integer, Integer> hash, Set<String> words) {
		hashList.add(hash);
		localMaxWords.add(words);
	}

	public List<HashMap<Integer, Integer>> getHashList() {
		return hashList;
	}

	public List<Set<String>> getLocalMaxWords() {
		return localMaxWords;
	}

	@Override
	public String toString() {
		return "ReduceTask [document=" + document + "]";
	}
	
}
