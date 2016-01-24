package prog;

public class Data {

	private Object ra;
	private Object dec;
	private Object id;
	private Object main_id;
	private Object coo_bibcode;
	private Object sp_type;
	private Object nbref;
	
	public Object getRa() {
		return ra;
	}
	public void setRa(Object ra) {
		this.ra = ra;
	}
	public Object getDec() {
		return dec;
	}
	public void setDec(Object dec) {
		this.dec = dec;
	}
	public Object getId() {
		return id;
	}
	public void setId(Object id) {
		this.id = id;
	}
	public Object getMain_id() {
		return main_id;
	}
	public void setMain_id(Object main_id) {
		this.main_id = main_id;
	}
	public Object getCoo_bibcode() {
		return coo_bibcode;
	}
	public void setCoo_bibcode(Object coo_bibcode) {
		this.coo_bibcode = coo_bibcode;
	}
	public Object getSp_type() {
		return sp_type;
	}
	public void setSp_type(Object sp_type) {
		this.sp_type = sp_type;
	}
	public Object getNbref() {
		return nbref;
	}
	public void setNbref(Object nbref) {
		this.nbref = nbref;
	}
		
	@Override 
	public String toString()
	{
		String csv = "";
		
		try
		{
			csv += ((Long)ra).toString() + ";";
		}
		catch (Exception e)
		{
			csv += ((Double)ra).toString() + ";";
		}
		try
		{
			csv += ((Long)dec).toString() + ";";
		}
		catch (Exception e)
		{
			csv += ((Double)dec).toString() + ";";
		}
		csv += (String)id + ";" + (String)main_id + ";" + (String)coo_bibcode + ";" + (String)sp_type + ";" + ((Long)nbref).toString() + "\n";
		return csv;
	}
}
