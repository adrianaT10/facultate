import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;


public class Main {

	public static void main(String[] args) {
		BufferedReader br;
		try {
			br = new BufferedReader(new FileReader("input"));
			Flexer scanner = new Flexer(br);
			scanner.yylex();
			
			// daca sunt erori de orice fel, afiseaza eroarea si termina
			scanner.graph.checkForSemanticErrors();
			if(scanner.graph.hasSyntaxError()) {
				System.out.println("Syntax error");
				return;
			}
			if(scanner.graph.hasSemanticError()) {
				System.out.println("Semantic error");
				return;
			}
			
			//incepe parsarea input-ului
			br = new BufferedReader(new FileReader("text"));
			scanner.yyreset(br);
			scanner.yybegin(scanner.WORD);
			scanner.yylex();
			
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

}
