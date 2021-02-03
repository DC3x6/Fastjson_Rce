import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;

public class exp{
    public exp() throws Exception {
        Process p = Runtime.getRuntime().exec(new String[]{"bash", "-c", "ping dnslog"});
        InputStream is = p.getInputStream();
        BufferedReader reader = new BufferedReader(new InputStreamReader(is));

        String line;
        while((line = reader.readLine()) != null) {
            System.out.println(line);
        }

        p.waitFor();
        is.close();
        reader.close();
        p.destroy();
    }

    public static void main(String[] args) throws Exception {
    }
}
