package prog;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class Program {
	
	public static void main(String[] args) {
		
		List<Data> list = new ArrayList<>();
		
		ParseJSON json = new ParseJSON();
		try {
			json.Parse(list);
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		Vizier vizier = new Vizier();
		
		try {
			vizier.Process(list);
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		Output out = new Output();
		
		try {
			out.Save(list);
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		System.exit(0);
	}

}
