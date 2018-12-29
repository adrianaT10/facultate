import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;
import java.util.StringTokenizer;
import java.util.concurrent.BrokenBarrierException;

public class Worker extends Thread {
	public static String separator = ";:/?~\\.,><~`[]{}()!@#$%^&-_+'=*\"| \t\n";

	@Override
	public void run() {
		System.out.println("Thread-ul worker " + this.getName()
				+ " a pornit...");
		while (true) {
			//ia un task Map
			MapTask task = MapReduce.mapWP.getWork();
			if (task == null)
				break;
           
			processMapTask(task);
		}
		try {
			// asteapta ca toate task-urile map sa se termine
			MapReduce.barrier.await();
			// proceseaza task-urile reduce
			while (true) {
				ReduceTask task = MapReduce.reduceWP.getWork();
				if (task == null)
					break;

				processReduceTask(task);
			}

		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (BrokenBarrierException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

		System.out.println("Thread-ul worker " + this.getName()
				+ " s-a terminat...");
	}

	
	public void processReduceTask(ReduceTask task) {
		// hash-ul final de intrari (lungime_k, nr_cuvinte_lungime_k)
		HashMap<Integer, Integer> finalHash = new HashMap<Integer, Integer>();
		LengthComparator comp = new LengthComparator();
		// lista de cuvinte maximale
		ArrayList<String> maxWordsList = new ArrayList<String>();
		int maxLength = 0, nrMaxWords = 0;
		int totalWords = 0;
		double rank = 0;

		// combina rezultatele partiale ale hash-urilor
		for (HashMap<Integer, Integer> hash : task.getHashList()) {
			for (Map.Entry<Integer, Integer> entry : hash.entrySet()) {
				if (finalHash.containsKey(entry.getKey())) {
					int val = finalHash.get(entry.getKey());
					finalHash.put(entry.getKey(), val + entry.getValue());
				} else {
					finalHash.put(entry.getKey(), entry.getValue());
				}
			}
		}

		// calculeaza rang-ul documentului
		for (Map.Entry<Integer, Integer> entry : finalHash.entrySet()) {
			rank += MapReduce.fibo[entry.getKey() + 1] * entry.getValue();
			totalWords += entry.getValue();
		}

		rank = rank / totalWords;
		rank = Math.floor(rank * 100.0) / 100.00; //truncheaza la 2 zecimale
		
        // adauga in maxWordsList toate cuvintele maximale
		for (Set<String> set : task.getLocalMaxWords()) {
			for(String ss : set) {
				maxWordsList.add(ss);
			}
		}
		// sorteaza cuvintele dupa lungime
		Collections.sort(maxWordsList, comp);
		
		// ia lungimea maxima
	    maxLength = maxWordsList.get(0).length();
	    //pune cuvintele de lungime maxima intr-un set pentru a elimina duplicatele
	    HashSet<String> resMax = new HashSet<String>();
	    for(String s : maxWordsList) {
	    	if(s.length() == maxLength) {
	    		resMax.add(s);
	    	}
	    }
	    // numarul de cuvinte maximale
	    nrMaxWords = resMax.size();
	    
	    // adauga rezultatul procesarii in lista globala
		MapReduce.addResult(task.document, rank, maxLength, nrMaxWords);
	}

	public void processMapTask(MapTask task) {
		String file = task.getDocument();
		int start = task.getStartPos();
		int dimension = task.getDimension();

		try {
			BufferedReader reader = new BufferedReader(
				      new InputStreamReader(
				            new FileInputStream(new File(file)), "UTF-8"));
			// citeste mai mult decat dimensiunea data 
			char[] buff = new char[dimension + 80];
			// indici pentru a sti de unde pana unde se parseaza din buff
			int startBuff = 0, endBuff = dimension;
			int bytesRead;
			
			// afla daca fragmentul incepe in mijlocul unui cuvant
			if (start > 0) {
				// citeste cu un octet inaintea pozitiei de start
				reader.skip(start);
				bytesRead = reader.read(buff);
				//daca primul octet nu e separator, inseamna ca se incepe din mijlocul
				// unui cuvant si trebuie sa sarim peste acesta
				while (startBuff < endBuff
						&& !separator.contains(String.valueOf(buff[startBuff]))) {
					startBuff++;
				}
			} else { // daca e inceputul documentului
				bytesRead = reader.read(buff);
			}
			reader.close();

			endBuff = Math.min(bytesRead, dimension);
		
			// daca fragmentul se termina in mijlocul unui cuvant, muta endBuff
		    // la sfarsitul cuvantului
			while (endBuff < bytesRead
					&& !separator.contains(String.valueOf(buff[endBuff]))) {
				endBuff++;
			}
			
			// daca fragmentul e nul
			if(endBuff <= startBuff) {
				return;
			}
			
			// proceseaza textul intre startBuff si endBuff
			String text = String.copyValueOf(buff, startBuff, endBuff
					- startBuff);
			StringTokenizer s = new StringTokenizer(text, 
					"\r ;:/?~\\.,><~`[]{}()!@#$%^&-_+\'=*\"|\t\n");
	
			String[] words = new String[s.countTokens()];
			for(int i = 0; i < words.length; i++) {
				words[i] = s.nextToken();
			}

			// hash cu intrari (lungime_cuvant, nr_aparitii_cuvant)
			HashMap<Integer, Integer> hash = new HashMap<Integer, Integer>();
			// set pentru cuvintele maximale din fragment
			HashSet<String> maxWords = new HashSet<String>();
			int maxLen = 0;
			int len;
			
			for (String word : words) {
				len = word.length();
				word = word.toLowerCase();
				
				// actualizeaza hash
				if (hash.containsKey(len)) {
					int existingCount = hash.get(len);
					hash.put(len, existingCount + 1);
				} else {
					hash.put(len, 1);
				}
				
				// cuvinte maximale
				if (len > maxLen) { //daca s-a gasit o noua lungime maxima
					maxWords.clear();
					maxWords.add(word);
					maxLen = len;
				} else if (len == maxLen) {
					maxWords.add(word);
				}
			}
            
			//pune rezultatul in workpool-ul pentru reduce
			MapReduce.reduceWP.putWork(file, hash, maxWords);

		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	/** Comparator dupa lungimea cuvintelor in ordine descrescatoare */
	private class LengthComparator implements Comparator<String> {

		@Override
		public int compare(String arg0, String arg1) {
			return Integer.compare(arg1.length(), arg0.length());
		}

	}
}
