package prog;

import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.List;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.JSONValue;

public class ParseJSON {   
	
	private static String FILE = "corot-simbad.txt"; 
	
	public void Parse(List<Data> list) throws IOException
	{
		JSONObject obj = (JSONObject)JSONValue.parse(new FileReader(FILE));

		@SuppressWarnings("unchecked")		
		HashMap<String, Object> map = (HashMap<String, Object>)obj;
		
		JSONArray data = (JSONArray)map.get("data");
		
		for (Object object : data) {
			JSONArray cast = (JSONArray)object;
			
			Data datafinal = new Data();
			
			datafinal.setRa(cast.get(0));
			datafinal.setDec(cast.get(1));
			datafinal.setId(cast.get(2));
			datafinal.setMain_id(cast.get(3));
			datafinal.setCoo_bibcode(cast.get(4));
			datafinal.setSp_type(cast.get(5));
			datafinal.setNbref(cast.get(6));
	
			list.add(datafinal);
		}
	}
	
}
