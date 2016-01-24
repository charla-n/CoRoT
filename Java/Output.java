package prog;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;

public class Output {
	
	private static String FILE = "corot-resultat.csv";
	
	public void Save(List<Data> list) throws IOException
	{				
		StringBuilder builder = new StringBuilder();
		
		for (Data data : list) 
		{
			builder.append(data.toString());
		}
		Files.write(Paths.get(FILE), builder.toString().getBytes());		
	}
}
