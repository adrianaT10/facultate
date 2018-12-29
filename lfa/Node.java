import java.util.ArrayList;
import java.util.HashMap;

public class Node {
	public String stateName;
	private boolean isInitialState;
	private boolean isFinalState;
	private boolean hasSemanticError;
	//tranzitii de forma (simbol, nextState)
	private HashMap<String, Node> transitions = new HashMap<String, Node>();

	public Node(String state_name) {
		this.stateName = state_name;
	}
	
	public void addTransition(char input, Node nextState) {
		String symbol = String.valueOf(input);
		
		// daca tranzitia exista deja
		if(transitions.put(symbol, nextState) != null) {
			hasSemanticError = true;
		}
	}
	
	public void markInitial() {
		isInitialState = true;
	}
	
	public void markFinal() {
		isFinalState = true;
	}
	
	public boolean isInitialState() {
		return isInitialState;
	}

	public boolean isFinalState() {
		return isFinalState;
	}

    /** Returneaza stare urmatoare pentru tranzitia ce are
        ca simbol input */
	public Node getNextNode(char input) {
		String s = String.valueOf(input);
		return transitions.get(s);
	}
	
	public boolean hasSemanticError() {
		return hasSemanticError;
	}
	
	/** Verifica daca nodul are toate tranzitiile posibile */
	public boolean checkNoTransitions(int goodNr) {
		return transitions.size() == goodNr;
	}
	
	@Override
	/** Folositor cand se adauga noduri in Graph (pentru Set) */
	public boolean equals(Object obj) {
		if(!(obj instanceof Node)) return false;
		
		if(((Node)obj).stateName.equals(stateName)) return true;
		return false;
	}
	
}


