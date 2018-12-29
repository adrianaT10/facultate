import java.util.HashSet;
import java.util.Set;


public class Graph {
    private Set<Node> nodes = new HashSet<Node>();
    private boolean hasFinalState;
    private boolean hasInitialState;
    private Alphabet alphabet = new Alphabet();
    private boolean hasSemanticError;
    private boolean hasSyntaxError;
    
    public void addNode(String stateName) {
        // daca nodul exista deja
    	if(!nodes.add(new Node(stateName))) {
    		hasSemanticError = true;
    	}
    }
    
    public void addTransition(String source, char input, String nextState) {
		// daca simbolul nu exista in alfabet
    	if(!alphabet.contains(input)) {
    		hasSemanticError = true;
    		return;
    	}
    	
        // gaseste nodurile sursa si destinatie si adauga tranzitia
		for(Node n : nodes) {
			if(n.stateName.equals(source)) {
				for(Node n1 : nodes) {
					if(n1.stateName.equals(nextState)) {
						n.addTransition(input, n1);
						return;
					}
				}
			}
		}
		//daca se ajunge aici inseamna ca source sau nextState nu exista
		hasSemanticError = true;
	}
    
    public void addToAlphabet(char c) {
    	alphabet.addSymbol(c);
    }
    
    /** Verifica si afiseaza substring-urile lui word care sunt
        acceptate de automat */
    public void verifyWord(String word) {
    	Verification.verify(this, word);
    }
    
    public void setInitialState(String nodeName) {
    	for(Node n : nodes) {
    		if(n.stateName.equals(nodeName)) {
    			n.markInitial();
    			hasInitialState = true;
    			return;
    		}
    	}
        // daca starea nu exista
    	hasSemanticError = true;
    }
    
    public void setFinalState(String nodeName) {
    	for(Node n : nodes) {
    		if(n.stateName.equals(nodeName)) {
    			n.markFinal();
    			hasFinalState = true;
    			return;
    		}
    	}
        // daca starea nu exista
    	hasSemanticError = true;
    }

    public void checkForSemanticErrors() {
    	if(!hasInitialState) {
    		hasSemanticError = true;
    		return;
    	}
    	for(Node n : nodes) {
    		//verific daca un nod are eroare semantica sau daca are mai putine tranzitii
    		if(n.hasSemanticError() || !n.checkNoTransitions(alphabet.size())){
    			hasSemanticError = true;
    			return;
    		}
    	}
    }
    
    public void foundSyntaxError() {
    	hasSyntaxError = true;
    }
    
    public boolean hasSemanticError() {
    	return hasSemanticError;
    }
    
    public boolean hasSyntaxError() {
    	return hasSyntaxError;
    }
     
	public Set<Node> getNodes() {
		return nodes;
	}
    
    public boolean hasFinalState() {
    	return hasFinalState;
    }
    
    public boolean hasInitialState() {
    	return hasInitialState;
    }
}
