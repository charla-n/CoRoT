package prog;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Vizier {

	private static String FILE = "corot-vizier.txt";
	
	public void Process(List<Data> list) throws IOException
	{		
		 List<String> splitted = Arrays.asList(new String(Files.readAllBytes(Paths.get(FILE)), StandardCharsets.UTF_8).split("\n|\t"));
		 List<Data> toDelete = new ArrayList<Data>();
		 
		 for (Data currentData : list) 
		 {
			if (currentData.getSp_type() == null)
			{
				String Id = (String)currentData.getId();
				
				if (Id.contains(" "))
					Id = Id.split(" ")[1];
				int index = splitted.indexOf(Id);
				
				if (index == -1)
					toDelete.add(currentData);	
				
				currentData.setSp_type(splitted.get(index + 3).substring(0, 3));
			}
		}
		list.removeAll(toDelete);
	}
	
}
