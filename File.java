import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.util.stream.Collectors;
import java.util.List;

public class File {

    public static void main(String[] args) {
        try (var in = new BufferedReader(new FileReader("space.txt"))){
            List<String> list = in.lines() 
                                    //            .map(s -> s + "\n")
                                    //    .map(s -> s.replaceAll("\n", ", "))
                                    //    .map(s -> s.replaceAll("\t",", "))
                                        .collect(Collectors.toList());
           var out = new BufferedWriter(new FileWriter("space.txt"));
            for (int i = 0 ; i < list.size(); i++) {
                out.write(list.get(i) + ", ");
            }
            out.close();
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }
}