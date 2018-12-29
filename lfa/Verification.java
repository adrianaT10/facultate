public class Verification {

	public static void verify(Graph g, String word) {
		if(!g.hasFinalState()) {
			return;
		}
		
		Node initial = null;

		// gaseste starea initiala
		for (Node n : g.getNodes()) {
			if (n.isInitialState()) {
				initial = n;
				break;
			}
		}
		if (initial != null) {
			//taie spatiile libere de la sfarsit
			String correctWord = word.trim();
			// porneste verificarea pe automat de pe fiecare pozitie
			// din correctWord
			while (correctWord.length() > 0) {
				match(initial, correctWord, 0);
				correctWord = correctWord.substring(1);
			}
		} 

	}
	
    /**
     * crt -> nodul curent din automat
     * word -> cuvantul pe care se face match
     * index -> se verifica substring-ul de la 0 la index din word
     */
	private static void match(Node crt, String word, int index) {
		// daca s-a terminat cuvantul 
		if (index == word.length()) {
			if (crt.isFinalState()) {
				System.out.println(word);
			} 
			return;
		}
		
		// daca substring-ul pana la index este acceptat de automat
		if(index != 0 && crt.isFinalState()) {
			System.out.println(word.substring(0, index));
		}
		
		// verifica pentru urmatorul substring
		Node next = crt.getNextNode(word.charAt(index));
		if (next != null) {
			match(next, word, index+1);
		}
	}
}
