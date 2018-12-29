import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.UnsupportedEncodingException;
import java.util.Comparator;
import java.util.TreeSet;
import java.util.concurrent.CyclicBarrier;


/**
 * Clasa care apeleaza algoritmul mapReduce
 */
public class MapReduce {
	
	// workpool pentru task-urile map
	public static WorkPool mapWP;
	// workpool pentru task-urile reduce
	public static WorkPoolReduce reduceWP;
	// bariera
	public static CyclicBarrier barrier;
	// sirul fibonacci
	public static long[] fibo;
	// numele fisierelor in ordinea in care au fost citite
	public static String[] fileOrder;
	// rezultatele ordonate dupa rang
	public static TreeSet<Result> result = new TreeSet<Result>(new ResultComparator());
	
	/**
	 * Adauga un rezultat dupa reduce
	 * @param file - numele fisierului
	 * @param rank - rangul lui
	 * @param maxLen - dimensiunea maxima a cuvintelor
	 * @param countMax - numarul de cuvinte maximale
	 */
	public static synchronized void addResult(String file, double rank, int maxLen, int countMax) {
		result.add(new Result(file, rank, maxLen, countMax));
	}
	
	/**
	 * Genereaza sirul fibonacci
	 */
	public static void generateFibo() {
		fibo = new long[90];
		fibo[0] = 0;
		fibo[1] = 1;
		for(int i = 2; i < 90; i++) {
			fibo[i] = fibo[i-1] + fibo[i-2];
		}
	}

	public static void main(String[] args) throws IOException, InterruptedException {
		
		int nThreads = Integer.valueOf(args[0]);
		String fileIn = args[1];
		String fileOut = args[2];
		int D, nrFiles;
		
		mapWP = new WorkPool(nThreads);
		reduceWP = new WorkPoolReduce(nThreads);
		barrier = new CyclicBarrier(nThreads);
		
		generateFibo();
		
		BufferedReader reader = new BufferedReader(new FileReader(fileIn));
		D = Integer.valueOf(reader.readLine());
		nrFiles = Integer.valueOf(reader.readLine());
		fileOrder = new String[nrFiles];
		
		// citeste fisierul de intrare
		for(int i = 0; i < nrFiles; i++) {
			String file = reader.readLine();
			fileOrder[i] = file;
			File f = new File(file);
			// dimensiune fisierului
			long numBytes = f.length();
			//genereaza task-uri mappentru fragmente de dimensiune D
			int count = 0;
			while(count < numBytes) {
				int dimension = (int)Math.min(D, numBytes - count);
				mapWP.putWork(new MapTask(file, count, dimension));
				count += D;
			}
		}
		
		reader.close();
		
		// creeaza si porneste thread-urile
		Worker[] threads = new Worker[nThreads];
		for(int i = 0 ; i < nThreads; i++) {
			threads[i] = new Worker();
			threads[i].start();
		}
		
		for(int i = 0 ; i < nThreads; i++) {
			threads[i].join();
		}
		
		writeResults(fileOut);
	}
	
	/**
	 * Scrie rezultatele in fisierul de output
	 * @param file
	 */
	public static void writeResults(String file) {
		
		try {
			PrintWriter writer = new PrintWriter(file, "UTF-8");
			for(Result r : result) {
				writer.print(r.document+";");
				writer.printf("%.2f", r.rank);
				writer.print(";["+r.maxLength+","+r.countMaxLength+"]\n");
			}
			writer.close();
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (UnsupportedEncodingException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	/**
	 * Clasa ce retine rezultatul final pentru un fisier
	 */
	private static class Result {
		String document;
		double rank;
		int maxLength;
		int countMaxLength;
		
		public Result(String document, double rank, int maxLength,
				int countMaxLength) {
			this.document = document;
			this.rank = rank;
			this.maxLength = maxLength;
			this.countMaxLength = countMaxLength;
		}
		
	}
	
	/**
	 * Comparator pentru a ordona rezultatele dupa ordinea rang-ului
	 * documentelor si dupa ordinea citirii din fisierul de intrare
	 */
	private static class ResultComparator implements Comparator<Result>{

		@Override
		public int compare(Result o1, Result o2) {
			if(o1.rank > o2.rank) {
				return -1;
			}
			if(o1.rank < o2.rank) {
				return 1;
			}
			//compara aparitiile in fisierul de intrare
			for(String file : fileOrder) {
				if(file.equals(o1.document)) {
					return -1;
				}
				if(file.equals(o2.document)) {
					return 1;
				}
			}
			return 0;
		}
		
	}

}
