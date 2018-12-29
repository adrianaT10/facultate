

import java.util.HashMap;

public class Alphabet {
	HashMap<Character, Integer> symbols;
	
	public Alphabet() {
		this.symbols = new HashMap<Character, Integer>();
	}
	
	public void addSymbol(char c) {
		this.symbols.put(c, 1);
	}
	
	public boolean contains(char c) {
		return this.symbols.containsKey(c);
	}
	
	public int size() {
		return symbols.size();
	}
	
	@Override
	public String toString() {
		String result = "{";
		String delim = "";
		for(char c:this.symbols.keySet()){
			result += delim + c;
			delim = ",";
		}
		result += "}";
		return result;
	}
}
