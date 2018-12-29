import java.util.HashMap;
import java.util.LinkedList;
import java.util.Set;

/**
 * Clasa ce implementeaza un "work pool" conform modelului "replicated workers".
 * Task-urile introduse in work pool sunt obiecte de tipul PartialSolution.
 *
 */
public class WorkPoolReduce {
	int nThreads; // nr total de thread-uri worker
	int nWaiting = 0; // nr de thread-uri worker care sunt blocate asteptand un task
	public boolean ready = false; // daca s-a terminat complet rezolvarea problemei 
	
	LinkedList<ReduceTask> tasks = new LinkedList<ReduceTask>();

	/**
	 * Constructor pentru clasa WorkPool.
	 * @param nThreads - numarul de thread-uri worker
	 */
	public WorkPoolReduce(int nThreads) {
		this.nThreads = nThreads;
	}

	/**
	 * Functie care incearca obtinera unui task din workpool.
	 * Daca nu sunt task-uri disponibile, functia se blocheaza pana cand 
	 * poate fi furnizat un task sau pana cand rezolvarea problemei este complet
	 * terminata
	 * @return Un task de rezolvat, sau null daca rezolvarea problemei s-a terminat 
	 */
	public synchronized ReduceTask getWork() {
		if (tasks.size() == 0) { // workpool gol
			nWaiting++;
			/* condtitie de terminare:
			 * nu mai exista nici un task in workpool si nici un worker nu e activ 
			 */
			if (nWaiting == nThreads) {
				ready = true;
				/* problema s-a terminat, anunt toti ceilalti workeri */
				notifyAll();
				return null;
			} else {
				while (!ready && tasks.size() == 0) {
					try {
						this.wait();
					} catch(Exception e) {e.printStackTrace();}
				}
				
				if (ready)
				    /* s-a terminat prelucrarea */
				    return null;

				nWaiting--;
				
			}
		}
		return tasks.remove();

	}


	/**
	 * Functie care adauga rezulatele partiale dupa o operatie de map, in
	 * task-ul specific documentului dat ca parametru
	 * @param file - numele documentului
	 * @param hash - hash dupa operatia de map
	 * @param maxWords - lista de cuvinte maximale locale
	 */
	synchronized void putWork(String file, HashMap<Integer, Integer> hash, Set<String> maxWords) {
		// daca un task pentru file exista deja, adauga rezultatele la acesta
		for(ReduceTask task : tasks) {
			if(task.document.equals(file)) {
				task.addMapResult(hash, maxWords);
				this.notify();
				return;
			}
		}
		// daca nu, creeaza un nou task
		ReduceTask task = new ReduceTask(file);
		task.addMapResult(hash, maxWords);
		tasks.add(task);
		/* anuntam unul dintre workerii care asteptau */
		this.notify();
	}


}


